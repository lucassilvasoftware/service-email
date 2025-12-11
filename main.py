import asyncio
import uvicorn

from routes.views.email_handler_route import mail_wiplay_route
from fastapi import FastAPI, Request
from os import path, getcwd
from dotenv import dotenv_values

config_path = path.join(getcwd(), 'env', 'credentials.cfg')
config = dotenv_values(config_path)
AUTH_TOKEN = config['AUTH_TOKEN']

app = FastAPI(
    title="Envio de e-mails plataforma ME",
    description="Templates de e-mail para envio ao cliente.\n Abaixo estão as APIS com os templates diferentes, leia a documentação de cada uma.",
    version="1.0.0"
)

app.include_router(mail_wiplay_route, prefix='/email')

@ app.middleware("http")
async def verify_token_middleware(request: Request, call_next):
    """
    Verify Bearer token, just for security purposes.

    if request.url.path in ["/docs", "/redoc", "/openapi.json"]:
        return await call_next(request)
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return JSONResponse(status_code=401, content={"detail": "Token missing"})

    token = auth_header.split(" ")[1]

    if token != AUTH_TOKEN:
        return JSONResponse(status_code=401, content={"detail": "Invalid token"})"""

    response = await call_next(request)
    return response

async def main():
    #
    config = uvicorn.Config("main:app", 
                            host="0.0.0.0", port=8500, 
                            log_level="critical", workers=1)  # Define o número de workers)
    server = uvicorn.Server(config)
    await server.serve()
       
if __name__ == "__main__":
    #
    asyncio.run(main())