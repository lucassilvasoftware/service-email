"""
Validação de token de autenticação para as rotas da API.
"""
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.config import AUTH_TOKEN

security = HTTPBearer()


def verify_static_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    """
    Verifica se o token Bearer fornecido é válido.
    
    Args:
        credentials: Credenciais HTTP Bearer do header Authorization
        
    Returns:
        str: O token válido
        
    Raises:
        HTTPException: Se o token for inválido ou não fornecido
    """
    if credentials.credentials != AUTH_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")
    return credentials.credentials

