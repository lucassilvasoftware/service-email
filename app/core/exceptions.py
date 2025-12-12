"""
Exceções customizadas para o serviço de e-mails.
"""
from fastapi import HTTPException, status


class EmailServiceException(Exception):
    """Exceção base para erros do serviço de e-mail."""
    pass


class TemplateNotFoundError(EmailServiceException):
    """Exceção lançada quando um template não é encontrado."""
    pass


class KafkaConnectionError(EmailServiceException):
    """Exceção lançada quando há erro de conexão com Kafka."""
    pass


class InvalidEmailDataError(EmailServiceException):
    """Exceção lançada quando os dados do e-mail são inválidos."""
    pass


def raise_kafka_error() -> None:
    """Lança HTTPException para erro de Kafka."""
    raise HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail="Serviço de fila Kafka indisponível. Tente novamente mais tarde."
    )


def raise_template_error() -> None:
    """Lança HTTPException para erro de template."""
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Erro ao gerar o conteúdo do e-mail. Template não encontrado ou inválido."
    )


def raise_invalid_data_error(message: str = "Dados do e-mail inválidos") -> None:
    """Lança HTTPException para dados inválidos."""
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=message
    )

