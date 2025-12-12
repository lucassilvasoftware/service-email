"""
Aplicação principal FastAPI para envio de e-mails.
"""
import asyncio
import logging
import sys
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import mail_wiplay_route
from app.api.health import health_router
from app.core.config import PORT, LOG_LEVEL

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerencia o ciclo de vida da aplicação.
    
    Args:
        app: Instância da aplicação FastAPI
    """
    # Startup
    try:
        logger.info("Inicializando aplicação...")
        
        # Verifica conexão com Kafka na inicialização
        # A conexão será estabelecida quando EmailService for criado nas rotas
        from app.services.kafka import _global_kafka_instance
        
        if _global_kafka_instance is not None:
            kafka_status = _global_kafka_instance.check_connection()
            if kafka_status["is_connected"]:
                logger.info("Kafka conectado com sucesso na inicializacao")
            else:
                logger.warning(
                    f"Kafka nao conectado na inicializacao | "
                    f"Erro: {kafka_status.get('last_error', 'Erro desconhecido')}"
                )
        else:
            logger.info("Kafka sera conectado quando o primeiro EmailService for criado")
        
        logger.info("Aplicação iniciada com sucesso")
    except Exception as e:
        logger.error(f"Erro ao inicializar aplicação: {e}", exc_info=True)
        raise
    
    yield
    
    # Shutdown
    logger.info("Encerrando aplicação...")
    logger.info("Aplicação encerrada")


app = FastAPI(
    title="Serviço de E-mails Wiplay",
    description=(
        "API para envio de e-mails transacionais através de templates HTML.\n\n"
        "Todos os endpoints requerem autenticação via Bearer Token no header Authorization."
    ),
    version="2.0.0",
    lifespan=lifespan
)

# Configuração de CORS (ajuste conforme necessário)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registra rotas
app.include_router(mail_wiplay_route, prefix='/email')
app.include_router(health_router)


async def main():
    """Função principal para executar o servidor."""
    config = uvicorn.Config(
        "app.main:app",
        host="0.0.0.0",
        port=PORT,
        log_level=LOG_LEVEL,
        workers=1
    )
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())

