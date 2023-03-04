from typing import Optional
import os
from beanie import PydanticObjectId
from fastapi import Depends, Request
from fastapi_mail import MessageType
from fastapi_users import BaseUserManager, FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.db import BeanieUserDatabase, ObjectIDIDMixin
from pydantic import EmailStr

from db import User, get_user_db
from email_util import send_email

SECRET = os.getenv("JWT_SECRET_KEY")
# print(SECRET)


class UserManager(ObjectIDIDMixin, BaseUserManager[User, PydanticObjectId]): # type: ignore
    reset_password_token_secret = SECRET # type: ignore
    verification_token_secret = SECRET # type: ignore

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        await send_email(
            recipients=[EmailStr(user.email)],
            subject="Welcome! to CairoRasa!",
            body="Thanks for choosing our service\n\n"
            + "Next steps include verifying your account and start using our service",
            subtype=MessageType.plain,
        )
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")
        await send_email(recipients=[EmailStr(user.email)], subject="CairoRasa Password Recovery", body=f"Click here to reset password: {os.getenv('FRONTEND_URL')}/reset-pass?reset_token={token}", subtype=MessageType.plain)

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")
        await send_email(recipients=[EmailStr(user.email)], subject="CairoRasa account verification", body=f"Click here to verify your account: {os.getenv('FRONTEND_URL')}/verify-account?token={token}", subtype=MessageType.plain)


async def get_user_manager(user_db: BeanieUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600) # type: ignore


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, PydanticObjectId](get_user_manager, [auth_backend]) # type: ignore

current_active_user = fastapi_users.current_user(active=True)