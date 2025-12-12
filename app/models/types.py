"""
Tipos e enums para mensagens de e-mail.
"""
from enum import Enum
from typing import Literal


class EmailType(str, Enum):
    """Tipos de e-mail disponíveis."""
    CONVITE_POR_EMAIL = "convite_por_email"
    ERRO_AO_FAZER_LOGIN = "erro_ao_fazer_login"
    RECUPERACAO_DE_SENHA = "recuperacao_de_senha"
    LOGIN_BLOQUEADO = "login_bloqueado"
    NAVEGADOR_DESCONHECIDO = "navegador_desconhecido"
    VERIFICACAO_EMAIL = "verificacao_email"
    CHANGE_PHONE = "change_phone"


# Type aliases para uso nas rotas
EmailTypeLiteral = Literal[
    "convite_por_email",
    "erro_ao_fazer_login",
    "recuperacao_de_senha",
    "login_bloqueado",
    "navegador_desconhecido",
    "verificacao_email",
    "change_phone"
]

