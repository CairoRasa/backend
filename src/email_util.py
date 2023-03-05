import os
import typing

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import EmailStr

# print(os.getenv("MAIL_USERNAME"))
# print(os.getenv("MAIL_PASSWORD"))

conf = ConnectionConfig(
    MAIL_USERNAME=str(os.getenv("MAIL_USERNAME")),  
    MAIL_PASSWORD=str(os.getenv("MAIL_PASSWORD")), 
    MAIL_FROM=EmailStr(os.getenv("MAIL_USERNAME")),  
    MAIL_PORT=465,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=False,
)


async def send_email(recipients: typing.List[EmailStr], subject: str, body: str, subtype: MessageType):
    message = MessageSchema(
        subject=subject, recipients=recipients, body=body, subtype=subtype
    )

    fm = FastMail(conf)
    return await fm.send_message(message)
