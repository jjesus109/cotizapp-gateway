import logging
from dataclasses import dataclass

from app.schemas import (
    User,
    Token
)
from app.errors import (
    UserNotFoundException,
    PasswordNotMatchedException,
    CorruptedTokenError,
    EmptyDataError
)
from app.adapters.gateway_i import GatewayInterface
from app.infra.repository_i import RepositoryInterface

from jose import JWTError

log = logging.getLogger(__name__)
TOKEN_TYPE = "Bearer"


@dataclass
class Gateway(GatewayInterface):

    repo: RepositoryInterface

    async def authenticate_user(self, username: str, password: str) -> User:
        user = await self.repo.get_user(username)
        if not user:
            log.error(f"User :{username} not exists")
            raise UserNotFoundException(f"User :{username} not exists")
        user_m = User(
            username=username,
            password=user.get("password")
            )
        matched = await self.repo.verify_password(
            password,
            user_m.password
        )
        if not matched:
            log.error(f"Password for user {username} not match")
            raise PasswordNotMatchedException(
                f"Password for user {username} not match"
            )
        return user_m

    async def create_acces_token(self, user_data: User) -> Token:
        token = await self.repo.create_acces_token(
            user_data.username
        )
        return Token(access_token=token, token_type=TOKEN_TYPE)

    async def validate_user_token(self, user_token: str):
        try:
            token_data = await self.repo.decode_token(user_token)
        except JWTError:
            log.error("Corrupted token data")
            raise CorruptedTokenError("Problems to decode token")
        username = token_data.get("sub")
        if username is None:
            raise EmptyDataError("Username is empty from decoded token")
        user = await self.repo.get_user(username)
        if not user:
            log.error(f"User: {username} from token not exists")
            raise UserNotFoundException(f"User :{username} not exists")
