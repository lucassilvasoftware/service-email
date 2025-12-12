"""
Serviço para envio de mensagens via Kafka.
"""
import logging
from json import dumps
from typing import Optional
from datetime import datetime

from kafka import KafkaProducer
from kafka.errors import KafkaError, NoBrokersAvailable

from app.core.config import SERVER_IP

logger = logging.getLogger(__name__)

# Instância singleton global (opcional, para health checks)
_global_kafka_instance: Optional['KafkaProducerService'] = None


class KafkaProducerService:
    """
    Serviço para produção de mensagens Kafka com gerenciamento de conexão.
    """
    
    def __init__(self, bootstrap_servers: Optional[str] = None):
        """
        Inicializa o producer Kafka.
        
        Args:
            bootstrap_servers: Servidores Kafka (padrão: SERVER_IP do config)
            
        Raises:
            Exception: Se houver erro ao inicializar o producer
        """
        self._bootstrap_servers = bootstrap_servers or SERVER_IP
        self._producer: Optional[KafkaProducer] = None
        self._connection_status: str = "disconnected"
        self._last_connection_attempt: Optional[datetime] = None
        self._last_error: Optional[str] = None
        self._initialize_producer()
        
        # Registra instância global para health checks
        global _global_kafka_instance
        _global_kafka_instance = self
    
    def _initialize_producer(self) -> None:
        """
        Inicializa o producer Kafka com configurações otimizadas.
        Registra sucesso ou falha da conexão.
        """
        self._last_connection_attempt = datetime.now()
        
        try:
            logger.info(f"Tentando conectar ao Kafka em: {self._bootstrap_servers}")
            
            self._producer = KafkaProducer(
                bootstrap_servers=self._bootstrap_servers,
                value_serializer=lambda v: dumps(v).encode('utf-8'),
                retries=3,
                acks='all',
                max_in_flight_requests_per_connection=1,
                enable_idempotence=True,
                request_timeout_ms=30000,
                delivery_timeout_ms=120000
            )
            
            # Testa a conexão tentando obter metadados
            self._producer.list_topics(timeout=5)
            
            self._connection_status = "connected"
            self._last_error = None
            
            logger.info(
                f"CONEXAO KAFKA ESTABELECIDA COM SUCESSO | "
                f"Servidores: {self._bootstrap_servers} | "
                f"Timestamp: {self._last_connection_attempt.isoformat()}"
            )
            
        except NoBrokersAvailable as e:
            self._connection_status = "failed"
            self._last_error = f"Nenhum broker disponível: {str(e)}"
            logger.warning(
                f"FALHA NA CONEXAO COM KAFKA | "
                f"Servidores: {self._bootstrap_servers} | "
                f"Erro: {self._last_error} | "
                f"Timestamp: {self._last_connection_attempt.isoformat()} | "
                f"A aplicacao iniciara sem conexao. A conexao sera tentada novamente quando necessario."
            )
            # Não levanta exceção - permite que a aplicação inicie
            self._producer = None
            
        except Exception as e:
            self._connection_status = "failed"
            self._last_error = f"Erro ao inicializar: {str(e)}"
            logger.warning(
                f"ERRO AO INICIALIZAR KAFKA PRODUCER | "
                f"Servidores: {self._bootstrap_servers} | "
                f"Erro: {self._last_error} | "
                f"Timestamp: {self._last_connection_attempt.isoformat()} | "
                f"A aplicacao iniciara sem conexao. A conexao sera tentada novamente quando necessario.",
                exc_info=True
            )
            # Não levanta exceção - permite que a aplicação inicie
            self._producer = None
    
    @property
    def producer(self) -> KafkaProducer:
        """
        Retorna a instância do producer Kafka.
        
        Returns:
            KafkaProducer: Instância do producer
            
        Raises:
            RuntimeError: Se o producer não estiver inicializado
        """
        if self._producer is None:
            raise RuntimeError("Kafka Producer não está inicializado")
        return self._producer
    
    def check_connection(self) -> dict[str, str | bool]:
        """
        Verifica o status da conexão com Kafka.
        
        Returns:
            dict: Status da conexão com informações detalhadas
        """
        status_info = {
            "status": self._connection_status,
            "bootstrap_servers": self._bootstrap_servers,
            "last_connection_attempt": self._last_connection_attempt.isoformat() if self._last_connection_attempt else None,
            "last_error": self._last_error,
            "is_connected": False
        }
        
        if self._producer is None:
            status_info["status"] = "disconnected"
            status_info["is_connected"] = False
            return status_info
        
        try:
            # Tenta obter metadados para verificar conexão
            self._producer.list_topics(timeout=5)
            status_info["status"] = "connected"
            status_info["is_connected"] = True
            status_info["last_error"] = None
        except Exception as e:
            status_info["status"] = "disconnected"
            status_info["is_connected"] = False
            status_info["last_error"] = str(e)
            self._connection_status = "disconnected"
            self._last_error = str(e)
        
        return status_info
    
    def send_message(self, topic: str, message: dict) -> None:
        """
        Envia mensagem para um tópico Kafka.
        
        Args:
            topic: Nome do tópico Kafka
            message: Dicionário com os dados da mensagem
            
        Raises:
            NoBrokersAvailable: Se não houver brokers disponíveis
            KafkaError: Se houver erro ao enviar a mensagem
            RuntimeError: Se o producer não estiver inicializado
        """
        # Tenta reconectar se o producer não estiver disponível
        if self._producer is None:
            logger.info("Kafka Producer nao inicializado. Tentando conectar...")
            self._initialize_producer()
            # Verifica se a conexão foi estabelecida após a tentativa
            if self._producer is None:
                error_msg = self._last_error or "Erro desconhecido ao conectar ao Kafka"
                logger.error(f"Tentativa de envio falhou: Nao foi possivel conectar ao Kafka: {error_msg}")
                raise RuntimeError(f"Kafka Producer não está disponível: {error_msg}")
        
        try:
            future = self.producer.send(topic, value=message)
            # Aguarda confirmação do envio com timeout
            record_metadata = future.get(timeout=10)
            
            self.producer.flush()
            
            logger.info(
                f"Mensagem enviada com sucesso para o topico {topic} | "
                f"Particao: {record_metadata.partition} | "
                f"Offset: {record_metadata.offset}"
            )
            
        except NoBrokersAvailable as e:
            self._connection_status = "failed"
            self._last_error = f"Nenhum broker disponível: {str(e)}"
            logger.error(
                f"FALHA AO ENVIAR MENSAGEM | "
                f"Nenhum broker Kafka disponivel | "
                f"Topico: {topic} | "
                f"Erro: {e}"
            )
            raise
            
        except KafkaError as e:
            self._connection_status = "failed"
            self._last_error = f"Erro Kafka: {str(e)}"
            logger.error(
                f"ERRO KAFKA AO ENVIAR MENSAGEM | "
                f"Topico: {topic} | "
                f"Erro: {e}"
            )
            raise
            
        except Exception as e:
            self._connection_status = "failed"
            self._last_error = f"Erro inesperado: {str(e)}"
            logger.error(
                f"ERRO INESPERADO AO ENVIAR MENSAGEM | "
                f"Topico: {topic} | "
                f"Erro: {e}",
                exc_info=True
            )
            raise
    
    def close(self) -> None:
        """Fecha a conexão com o Kafka de forma segura."""
        if self._producer:
            try:
                self._producer.flush(timeout=5)
                self._producer.close(timeout=5)
                self._connection_status = "disconnected"
                logger.info(
                    f"Conexao Kafka fechada com sucesso | "
                    f"Servidores: {self._bootstrap_servers}"
                )
            except Exception as e:
                logger.error(
                    f"Erro ao fechar conexao Kafka | "
                    f"Servidores: {self._bootstrap_servers} | "
                    f"Erro: {e}"
                )
            finally:
                self._producer = None
                self._connection_status = "disconnected"
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - fecha conexão automaticamente."""
        self.close()
    
    def __del__(self):
        """Destrutor - garante fechamento da conexão."""
        self.close()

