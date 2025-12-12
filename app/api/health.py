"""
Rotas de health check e monitoramento.
"""
import logging
from fastapi import APIRouter
from datetime import datetime

from app.services.kafka import KafkaProducerService

logger = logging.getLogger(__name__)

health_router = APIRouter(tags=["Health Check"])


@health_router.get("/health")
async def health_check():
    """
    Endpoint de health check básico da aplicação.
    
    Returns:
        dict: Status da aplicação
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "email-service"
    }


@health_router.get("/health/kafka")
async def kafka_health_check():
    """
    Endpoint para verificar status da conexão com Kafka.
    
    Returns:
        dict: Status detalhado da conexão Kafka
    """
    try:
        # Tenta usar instância global se existir, senão cria uma nova para teste
        from app.services.kafka import _global_kafka_instance
        
        if _global_kafka_instance is not None:
            kafka_service = _global_kafka_instance
            should_close = False
        else:
            # Se não houver instância global, cria uma temporária para teste
            kafka_service = KafkaProducerService()
            should_close = True
        
        status_info = kafka_service.check_connection()
        
        # Fecha apenas se criou uma nova instância
        if should_close:
            kafka_service.close()
        
        if status_info["is_connected"]:
            return {
                "status": "healthy",
                "kafka": {
                    "connected": True,
                    "bootstrap_servers": status_info["bootstrap_servers"],
                    "last_check": datetime.now().isoformat(),
                    "last_connection_attempt": status_info["last_connection_attempt"]
                },
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "status": "unhealthy",
                "kafka": {
                    "connected": False,
                    "bootstrap_servers": status_info["bootstrap_servers"],
                    "last_check": datetime.now().isoformat(),
                    "last_error": status_info["last_error"],
                    "last_connection_attempt": status_info["last_connection_attempt"]
                },
                "timestamp": datetime.now().isoformat()
            }
            
    except Exception as e:
        logger.error(f"Erro ao verificar saúde do Kafka: {e}", exc_info=True)
        return {
            "status": "error",
            "kafka": {
                "connected": False,
                "error": str(e)
            },
            "timestamp": datetime.now().isoformat()
        }

