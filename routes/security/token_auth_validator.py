from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import dotenv_values
from os import path, getcwd


config_path = path.join(getcwd(), 'env', 'credentials.cfg')
config = dotenv_values(config_path)
AUTH_TOKEN = config['AUTH_TOKEN']
security = HTTPBearer()


def verify_static_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    if credentials.credentials != f'Bearer {AUTH_TOKEN}':
        raise HTTPException(status_code=401, detail="Invalid token")
