"""
Rotas da API para envio de e-mails Wiplay.
"""
import logging
from fastapi import APIRouter, Query, Depends

from app.models.email import WiplayEmail
from app.models.types import EmailType, EmailTypeLiteral
from app.middleware.auth import verify_static_token
from app.services.email_service import EmailService

logger = logging.getLogger(__name__)

# Router principal
mail_wiplay_route = APIRouter(
    tags=["E-mails Wiplay"],
    prefix="/wiplay",
    dependencies=[Depends(verify_static_token)]
)

# Instância do serviço de e-mail (singleton)
_email_service = EmailService()


def _process_phone_change_args(args: list[str]) -> list[str]:
    """
    Processa argumentos para e-mail de troca de telefone.
    Adiciona espaços ao redor do código de ativação.
    
    Args:
        args: Lista de argumentos
        
    Returns:
        list[str]: Argumentos processados
    """
    if len(args) > 1:
        args[1] = f' {" ".join(args[1])} '
    return args


@mail_wiplay_route.post(
    "/convite",
    response_model=dict,
    description="Envia e-mail de convite para o cliente",
    summary="Envio de e-mail de boas-vindas | args -> <Nome_cliente>, <código_de_ativação>"
)
async def send_invite_email(
    email_data: WiplayEmail,
    type_msg: EmailTypeLiteral = Query(
        default=EmailType.CONVITE_POR_EMAIL.value,
        title="Template HTML",
        description="Chave correspondente ao template HTML."
    )
) -> dict:
    """
    Endpoint para envio de e-mail de convite/boas-vindas.
    
    Args:
        email_data: Dados do e-mail (destinatário, assunto, argumentos)
        type_msg: Tipo de template (padrão: convite_por_email)
        
    Returns:
        dict: Resposta com status e mensagem de sucesso
    """
    return _email_service.send_email(email_data, type_msg)


@mail_wiplay_route.post(
    "/change_phone",
    response_model=dict,
    description="Dispara e-mail referente à troca de número de celular",
    summary="Envio de e-mail para confirmação de troca de telefone | args -> <Nome_cliente>, <código_de_ativação>"
)
async def send_phone_change_email(
    email_data: WiplayEmail,
    type_msg: EmailTypeLiteral = Query(
        default=EmailType.CHANGE_PHONE.value,
        title="Template HTML",
        description="Chave correspondente ao template HTML para troca de celular."
    )
) -> dict:
    """
    Endpoint para envio de e-mail de troca de telefone.
    
    Args:
        email_data: Dados do e-mail (destinatário, assunto, argumentos)
        type_msg: Tipo de template (padrão: change_phone)
        
    Returns:
        dict: Resposta com status e mensagem de sucesso
    """
    return _email_service.send_email(
        email_data,
        type_msg,
        args_processor=_process_phone_change_args
    )


@mail_wiplay_route.post(
    "/erro_login",
    response_model=dict,
    description="Envia e-mail de erro de login para o cliente",
    summary="Envio de e-mail de erro de login | args -> <nome_cliente>"
)
async def send_login_error_email(
    email_data: WiplayEmail,
    type_msg: EmailTypeLiteral = Query(
        default=EmailType.ERRO_AO_FAZER_LOGIN.value,
        title="Template HTML",
        description="Chave correspondente ao template HTML."
    )
) -> dict:
    """
    Endpoint para envio de e-mail de erro de login.
    
    Args:
        email_data: Dados do e-mail (destinatário, assunto, argumentos)
        type_msg: Tipo de template (padrão: erro_ao_fazer_login)
        
    Returns:
        dict: Resposta com status e mensagem de sucesso
    """
    return _email_service.send_email(email_data, type_msg)


@mail_wiplay_route.post(
    "/recuperar_senha",
    response_model=dict,
    description="Envia e-mail de recuperação de senha para o cliente",
    summary="Envio de e-mail de recuperação de senha | args -> <nome_cliente>"
)
async def send_password_recovery_email(
    email_data: WiplayEmail,
    type_msg: EmailTypeLiteral = Query(
        default=EmailType.RECUPERACAO_DE_SENHA.value,
        title="Template HTML",
        description="Chave correspondente ao template HTML."
    )
) -> dict:
    """
    Endpoint para envio de e-mail de recuperação de senha.
    
    Args:
        email_data: Dados do e-mail (destinatário, assunto, argumentos)
        type_msg: Tipo de template (padrão: recuperacao_de_senha)
        
    Returns:
        dict: Resposta com status e mensagem de sucesso
    """
    return _email_service.send_email(email_data, type_msg)


@mail_wiplay_route.post(
    "/login_bloqueado",
    response_model=dict,
    description="Envia e-mail de login bloqueado para o cliente",
    summary="Envio de e-mail de login bloqueado | args -> <nome_cliente>"
)
async def send_blocked_login_email(
    email_data: WiplayEmail,
    type_msg: EmailTypeLiteral = Query(
        default=EmailType.LOGIN_BLOQUEADO.value,
        title="Template HTML",
        description="Chave correspondente ao template HTML."
    )
) -> dict:
    """
    Endpoint para envio de e-mail de login bloqueado.
    
    Args:
        email_data: Dados do e-mail (destinatário, assunto, argumentos)
        type_msg: Tipo de template (padrão: login_bloqueado)
        
    Returns:
        dict: Resposta com status e mensagem de sucesso
    """
    return _email_service.send_email(email_data, type_msg)


@mail_wiplay_route.post(
    "/navegador_desconhecido",
    response_model=dict,
    description="Envia e-mail de navegador desconhecido para o cliente",
    summary="Envio de e-mail de navegador desconhecido | args -> navegador, versão_do_navegador, sistema operacional, endereço IP"
)
async def send_unknown_browser_email(
    email_data: WiplayEmail,
    type_msg: EmailTypeLiteral = Query(
        default=EmailType.NAVEGADOR_DESCONHECIDO.value,
        title="Template HTML",
        description="Chave correspondente ao template HTML."
    )
) -> dict:
    """
    Endpoint para envio de e-mail de navegador desconhecido.
    
    Args:
        email_data: Dados do e-mail (destinatário, assunto, argumentos)
        type_msg: Tipo de template (padrão: navegador_desconhecido)
        
    Returns:
        dict: Resposta com status e mensagem de sucesso
    """
    return _email_service.send_email(email_data, type_msg)


@mail_wiplay_route.post(
    "/verificacao_email",
    response_model=dict,
    description="Envia e-mail de verificação de e-mail para o cliente",
    summary="Envio de e-mail de verificação | args -> nome_cliente, código_validação"
)
async def send_email_verification(
    email_data: WiplayEmail,
    type_msg: EmailTypeLiteral = Query(
        default=EmailType.VERIFICACAO_EMAIL.value,
        title="Template HTML",
        description="Chave correspondente ao template HTML."
    )
) -> dict:
    """
    Endpoint para envio de e-mail de verificação.
    
    Args:
        email_data: Dados do e-mail (destinatário, assunto, argumentos)
        type_msg: Tipo de template (padrão: verificacao_email)
        
    Returns:
        dict: Resposta com status e mensagem de sucesso
    """
    return _email_service.send_email(email_data, type_msg)

