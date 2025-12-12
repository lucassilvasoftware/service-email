"""
Serviço centralizado para envio de e-mails via Kafka.
"""
import logging
from datetime import datetime
from typing import Optional, Callable

from kafka.errors import NoBrokersAvailable

from app.models.email import WiplayEmail
from app.utils.templates import MessageHandler
from app.services.kafka import KafkaProducerService
from app.core.exceptions import (
    raise_kafka_error,
    raise_template_error,
    raise_invalid_data_error
)
from app.core.config import EMAIL_WIPLAY_TOPICO

logger = logging.getLogger(__name__)


class EmailService:
    """
    Serviço para processamento e envio de e-mails via Kafka.
    """
    
    def __init__(
        self,
        kafka_producer: Optional[KafkaProducerService] = None,
        message_handler: Optional[MessageHandler] = None
    ):
        """
        Inicializa o serviço de e-mail.
        
        Args:
            kafka_producer: Instância do KafkaProducerService (opcional)
            message_handler: Instância do MessageHandler (opcional)
        """
        self._kafka_producer = kafka_producer or KafkaProducerService()
        self._message_handler = message_handler or MessageHandler()
    
    def send_email(
        self,
        email_data: WiplayEmail,
        email_type: str,
        args_processor: Optional[Callable[[list[str]], list[str]]] = None
    ) -> dict[str, bool | str]:
        """
        Processa e envia e-mail via Kafka.
        
        Args:
            email_data: Dados do e-mail a ser enviado
            email_type: Tipo de e-mail/template a ser usado
            args_processor: Função opcional para processar argumentos antes da substituição
            
        Returns:
            dict: Resposta de sucesso com status e mensagem
            
        Raises:
            HTTPException: Se houver erro ao processar ou enviar o e-mail
        """
        try:
            # Processa argumentos
            args = email_data.get_args_list()
            
            if args_processor:
                args = args_processor(args)
            
            # Gera HTML do template
            html_message = self._message_handler.alter_string_information(email_type, args)
            
            if not html_message:
                logger.error(f"Template não encontrado ou inválido: {email_type}")
                raise_template_error()
            
            # Prepara mensagem para Kafka
            kafka_message = {
                'date_of_register': datetime.now().isoformat(),
                'destinatary': email_data.destinatary,
                'subject': email_data.subject,
                'type_msg': email_type,
                'html_text': html_message
            }
            
            # Envia para Kafka
            self._kafka_producer.send_message(EMAIL_WIPLAY_TOPICO, kafka_message)
            
            logger.info(
                f"E-mail {email_type} enviado com sucesso para {email_data.destinatary}"
            )
            
            return {
                "status": True,
                "message": "E-mail enviado com sucesso.",
                "email_type": email_type,
                "destinatary": email_data.destinatary
            }
            
        except ValueError as e:
            logger.error(f"Erro de validação: {e}")
            raise_invalid_data_error(str(e))
        except NoBrokersAvailable:
            logger.error("Erro na fila Kafka: serviço offline ou indisponível")
            raise_kafka_error()
        except Exception as e:
            logger.error(f"Erro inesperado ao enviar e-mail: {e}", exc_info=True)
            raise_kafka_error()

