"""
Modelos Pydantic para validação de dados de e-mail.
"""
import re
from pydantic import BaseModel, Field, field_validator
from typing_extensions import Annotated
from fastapi import Form


class WiplayEmail(BaseModel):
    """
    Modelo de dados para envio de e-mail Wiplay.
    
    Attributes:
        args: Argumentos separados por vírgula para substituição no template
        destinatary: Endereço de e-mail do destinatário
        subject: Assunto do e-mail
    """
    args: Annotated[str, Form(description="Argumentos separados por vírgula para o template")]
    destinatary: Annotated[str, Form(description="Endereço de e-mail do destinatário")]
    subject: Annotated[str, Form(description="Assunto do e-mail")]

    @field_validator('destinatary')
    @classmethod
    def validate_email(cls, v: str) -> str:
        """
        Valida formato básico de e-mail.
        
        Args:
            v: Endereço de e-mail a ser validado
            
        Returns:
            str: E-mail validado
            
        Raises:
            ValueError: Se o formato do e-mail for inválido
        """
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, v.strip()):
            raise ValueError('Formato de e-mail inválido')
        return v.strip().lower()

    @field_validator('subject')
    @classmethod
    def validate_subject(cls, v: str) -> str:
        """
        Valida e sanitiza o assunto do e-mail.
        
        Args:
            v: Assunto do e-mail
            
        Returns:
            str: Assunto sanitizado
            
        Raises:
            ValueError: Se o assunto estiver vazio ou muito longo
        """
        v = v.strip()
        if not v:
            raise ValueError('Assunto do e-mail não pode estar vazio')
        if len(v) > 200:
            raise ValueError('Assunto do e-mail não pode ter mais de 200 caracteres')
        return v

    @field_validator('args')
    @classmethod
    def validate_args(cls, v: str) -> str:
        """
        Valida os argumentos do template.
        
        Args:
            v: String com argumentos separados por vírgula
            
        Returns:
            str: Argumentos validados
            
        Raises:
            ValueError: Se os argumentos estiverem vazios
        """
        if not v or not v.strip():
            raise ValueError('Argumentos não podem estar vazios')
        return v.strip()

    def get_args_list(self) -> list[str]:
        """
        Retorna lista de argumentos processados.
        
        Returns:
            list[str]: Lista de argumentos limpos
        """
        return [arg.strip() for arg in self.args.split(',') if arg.strip()]

