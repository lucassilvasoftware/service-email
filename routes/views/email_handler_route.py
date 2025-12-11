from fastapi import APIRouter, HTTPException, Query, Depends
from routes.controllers.email_handler import KafkaProducerService
from datetime import datetime
from routes.helpers import MessageHandler
from routes.models.wiplay_mail import WiplayEmail
from kafka.errors import NoBrokersAvailable
from os import path, getcwd
from dotenv import dotenv_values
from routes.security.token_auth_validator import verify_static_token
from typing import Literal

"""
Mapping model:

MESSAGES_MAPPING = {'convite_por_email': CONVITE_POR_EMAIL,
                    'erro_ao_fazer_login': ERRO_AO_FAZER_LOGIN,
                    'recuperacao_de_senha': RECUPERACAO_DE_SENHA,
                    'login_bloqueado': LOGIN_BLOQUEADO,
                    'navegador_desconhecido': NAVEGADOR_DESCONHECIDO,
                    'verificacao_email': VERIFICACAO_EMAIL,
                    'change_phone': CHANGE_PHONE}"""


config_path = path.join(getcwd(), 'env', 'credentials.cfg')
config = dotenv_values(config_path)
TOPICO_WIPLAY_EMAIL = config['EMAIL_WIPLAY_TOPICO']

mail_wiplay_route = APIRouter(tags=["E-mails Wiplay"])
producer_kafka = KafkaProducerService()
handler_msg = MessageHandler()

@mail_wiplay_route.post("/wiplay/convite",
                        description="Send e-mail job to be sent to client (e-mail de convite)",
                        summary="Send greetings e-mail to client | args -> <Nome_cliente>, <código_de_ativação>")
async def send_wiplay_e_mail(email_data: WiplayEmail,
                             type_msg: Literal["convite_por_email"] = Query(
                                 "convite_por_email",
                                 title="Template HTML",
                                 description="Chave correspondente ao template HTML."
                             ),
                             authorization: str = Depends(verify_static_token)
                             ):
    try:
        args = email_data.args.split(',')
        html_message = handler_msg.alter_string_information(
            type_msg, args)

        if html_message:
            producer_kafka.send_message(TOPICO_WIPLAY_EMAIL, {'date_of_register': datetime.now().isoformat(),
                                                              'destinatary': email_data.destinatary,
                                                              'subject': email_data.subject,
                                                              'type_msg': type_msg,
                                                              'html_text': html_message})
            return {'status': True,
                    'message': 'success'}
        return HTTPException(500, detail=F"Something went wrong while generating the HTML message")
    except NoBrokersAvailable:
        return HTTPException(500, detail=F"Something went wrong with the Kafka queue! Probably offline or shm")
    except Exception as err:
        return HTTPException(500, detail=F"Something went wrong -> {err}")

@mail_wiplay_route.post("/wiplay/change_phone",
    description="Dispara e-mail referente à troca de número de celular",
    summary="Envio de e-mail para confirmação de troca de telefone | args -> <Nome_cliente>, <código_de_ativação>"
)
async def send_phone_change_email(
    email_data: WiplayEmail,
    type_msg: Literal["change_phone"] = Query(
        "change_phone",
        title="Template HTML",
        description="Chave correspondente ao template HTML para troca de celular."
    ),
    authorization: str = Depends(verify_static_token)
):
    try:
        args = email_data.args.split(',')
        args[1] = ' ' + ' '.join(args[1]) + ' '
        #
        html_message = handler_msg.alter_string_information(type_msg, args)

        if not html_message:
            raise HTTPException(
                status_code=500,
                detail="Erro ao gerar o conteúdo do e-mail (HTML)."
            )

        producer_kafka.send_message(
            TOPICO_WIPLAY_EMAIL,
            {
                'date_of_register': datetime.now().isoformat(),
                'destinatary': email_data.destinatary,
                'subject': email_data.subject,
                'type_msg': type_msg,
                'html_text': html_message
            }
        )

        return {"status": True, "message": "E-mail enviado com sucesso."}

    except NoBrokersAvailable:
        raise HTTPException(
            status_code=500,
            detail="Erro na fila Kafka. Verifique se o serviço está online."
        )
    except Exception as err:
        raise HTTPException(
            status_code=500,
            detail=f"Erro inesperado: {str(err)}"
        )

@ mail_wiplay_route.post("/wiplay/erro_login",
                         description="Send e-mail job to be sent to client (erro_login e-mail)",
                         summary="Send login error e-mail to client | args -> <nome_cliente>")
async def send_wiplay_e_mail(email_data: WiplayEmail,
                             type_msg: Literal["erro_ao_fazer_login"] = Query(
                                 "erro_ao_fazer_login",
                                 title="Template HTML",
                                 description="Chave correspondente ao template HTML."
                             ),
                             authorization: str = Depends(verify_static_token)
                             ):
    try:
        args = email_data.args.split(',')
        html_message = handler_msg.alter_string_information(
            type_msg, args)

        if html_message:
            producer_kafka.send_message(TOPICO_WIPLAY_EMAIL, {'date_of_register': datetime.now().isoformat(),
                                                              'destinatary': email_data.destinatary,
                                                              'subject': email_data.subject,
                                                              'type_msg': type_msg,
                                                              'html_text': html_message})
            return {'status': True,
                    'message': 'success'}
        return HTTPException(500, detail=F"Something went wrong while generating the HTML message")
    except NoBrokersAvailable:
        return HTTPException(500, detail=F"Something went wrong with the Kafka queue! Probably offline or shm")
    except Exception as err:
        return HTTPException(500, detail=F"Something went wrong -> {err}")


@ mail_wiplay_route.post("/wiplay/recuperar_senha",
                         description="Send e-mail job to be sent to client (password recover e-mail)",
                         summary="Send password recover e-mail to client | args -> <nome_cliente>",
                         dependencies=[Depends(verify_static_token)])
async def send_wiplay_e_mail(email_data: WiplayEmail,
                             type_msg: Literal["recuperacao_de_senha"] = Query(
                                 "recuperacao_de_senha",
                                 title="Template HTML",
                                 description="Chave correspondente ao template HTML."
                             ),
                             authorization: str = Depends(verify_static_token)
                             ):
    try:
        args = email_data.args.split(',')
        html_message = handler_msg.alter_string_information(
            type_msg, args)

        if html_message:
            producer_kafka.send_message(TOPICO_WIPLAY_EMAIL, {'date_of_register': datetime.now().isoformat(),
                                                              'destinatary': email_data.destinatary,
                                                              'subject': email_data.subject,
                                                              'type_msg': type_msg,
                                                              'html_text': html_message})
            return {'status': True,
                    'message': 'success'}
        return HTTPException(500, detail=F"Something went wrong while generating the HTML message")
    except NoBrokersAvailable:
        return HTTPException(500, detail=F"Something went wrong with the Kafka queue! Probably offline or shm")
    except Exception as err:
        return HTTPException(500, detail=F"Something went wrong -> {err}")


@ mail_wiplay_route.post("/wiplay/login_bloqueado",
                         description="Send e-mail job to be sent to client (login_bloqueado e-mail)",
                         summary="Send block login e-mail to client | args -> <nome_cliente>",
                         dependencies=[Depends(verify_static_token)])
async def send_wiplay_e_mail(email_data: WiplayEmail,
                             type_msg: Literal["login_bloqueado"] = Query(
                                 "login_bloqueado",
                                 title="Template HTML",
                                 description="Chave correspondente ao template HTML."
                             ),
                             authorization: str = Depends(verify_static_token)
                             ):
    try:
        args = email_data.args.split(',')
        html_message = handler_msg.alter_string_information(
            type_msg, args)

        if html_message:
            producer_kafka.send_message(TOPICO_WIPLAY_EMAIL, {'date_of_register': datetime.now().isoformat(),
                                                              'destinatary': email_data.destinatary,
                                                              'subject': email_data.subject,
                                                              'type_msg': type_msg,
                                                              'html_text': html_message})
            return {'status': True,
                    'message': 'success'}
        return HTTPException(500, detail=F"Something went wrong while generating the HTML message")
    except NoBrokersAvailable:
        return HTTPException(500, detail=F"Something went wrong with the Kafka queue! Probably offline or shm")
    except Exception as err:
        return HTTPException(500, detail=F"Something went wrong -> {err}")


@ mail_wiplay_route.post("/wiplay/navegador_desconhecido",
                         description="Send e-mail job to be sent to client (navegador_desconhecido e-mail)",
                         summary="Send unknown browser e-mail to client | args -> navegador, versão_do_navegador, sistema operacional, endereço IP",
                         dependencies=[Depends(verify_static_token)])
async def send_wiplay_e_mail(email_data: WiplayEmail,
                             type_msg: Literal["navegador_desconhecido"] = Query(
                                 "navegador_desconhecido",
                                 title="Template HTML",
                                 description="Chave correspondente ao template HTML."
                             ),
                             authorization: str = Depends(verify_static_token)
                             ):
    try:
        args = email_data.args.split(',')
        html_message = handler_msg.alter_string_information(
            type_msg, args)

        if html_message:
            producer_kafka.send_message(TOPICO_WIPLAY_EMAIL, {'date_of_register': datetime.now().isoformat(),
                                                              'destinatary': email_data.destinatary,
                                                              'subject': email_data.subject,
                                                              'type_msg': type_msg,
                                                              'html_text': html_message})
            return {'status': True,
                    'message': 'success'}
        return HTTPException(500, detail=F"Something went wrong while generating the HTML message")
    except NoBrokersAvailable:
        return HTTPException(500, detail=F"Something went wrong with the Kafka queue! Probably offline or shm")
    except Exception as err:
        return HTTPException(500, detail=F"Something went wrong -> {err}")


@ mail_wiplay_route.post("/wiplay/verificacao_email",
                         description="Send e-mail job to be sent to client (email verification)",
                         summary="Send email verification to client| args -> nome_cliente, código_validação",
                         dependencies=[Depends(verify_static_token)])
async def send_wiplay_e_mail(email_data: WiplayEmail,
                             type_msg: Literal["verificacao_email"] = Query(
                                 "verificacao_email",
                                 title="Template HTML",
                                 description="Chave correspondente ao template HTML."
                             ),
                             authorization: str = Depends(verify_static_token)
                             ):
    try:
        args = email_data.args.split(',')
        html_message = handler_msg.alter_string_information(
            type_msg, args)

        if html_message:
            producer_kafka.send_message(TOPICO_WIPLAY_EMAIL, {'date_of_register': datetime.now().isoformat(),
                                                              'destinatary': email_data.destinatary,
                                                              'subject': email_data.subject,
                                                              'type_msg': type_msg,
                                                              'html_text': html_message})
            return {'status': True,
                    'message': 'success'}
        return HTTPException(500, detail=F"Something went wrong while generating the HTML message")
    except NoBrokersAvailable:
        return HTTPException(500, detail=F"Something went wrong with the Kafka queue! Probably offline or shm")
    except Exception as err:
        return HTTPException(500, detail=F"Something went wrong -> {err}")

# Força recriação do esquema do OpenAPI
mail_wiplay_route.openapi_schema = None
