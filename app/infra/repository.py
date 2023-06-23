import logging
from datetime import timedelta, datetime
from dataclasses import dataclass

from app.config import Configuration
from app.infra.repository_i import RepositoryInterface
from app.schemas import UserDict, TokenToEncode
from app.errors import DBError, UserNotFoundException

from jose import jwt
from passlib.context import CryptContext
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import (
    ConnectionFailure,
    ExecutionTimeout
)

conf = Configuration()
log = logging.getLogger(__name__)


@dataclass
class Repository(RepositoryInterface):

    nosql_conn: AsyncIOMotorDatabase
    pwd_context: CryptContext = CryptContext(
        schemes=["bcrypt"],
        deprecated="auto"
    )

    async def get_user(self, username: str) -> UserDict:
        try:
            user = await self.nosql_conn[conf.collection].find_one(
                {"username": username}
            )
        except (ConnectionFailure, ExecutionTimeout):
            raise DBError(
                "Quoter not found in DB"
            )
        if not user:
            raise UserNotFoundException(
                "Quoter not found in DB"
            )
        return UserDict(**user)  # type: ignore

    async def verify_password(self, form_pass: str, hashed_pass: str) -> bool:
        return self.pwd_context.verify(form_pass, hashed_pass)

    async def create_acces_token(self, user_data: str) -> str:
        expire_time = conf.expire_time
        secret_key = conf.secret_key
        algorithm = conf.algorithm
        time = datetime.utcnow() + timedelta(minutes=expire_time)
        user_encode = TokenToEncode(
            sub=user_data,
            exp=time)
        encoded_jwt = jwt.encode(user_encode, secret_key, algorithm=algorithm)
        return encoded_jwt

    async def decode_token(self, token: str) -> TokenToEncode:
        secret_key = conf.secret_key
        algorithm = conf.algorithm
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        return payload
