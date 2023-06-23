from typing import Any
from abc import ABC, abstractmethod


class GatewayInterface(ABC):

    @abstractmethod
    async def authenticate_user(self, username: str, password: str) -> Any:
        """Authenticate user

        Args:
            username (str): username to authenticate
            password (str): password to match

        Returns:
            User: User data
        """

    @abstractmethod
    async def create_acces_token(self, user_data: Any) -> str:
        """Create access token for a user

        Args:
            data_to_encode (Any): data to generate access token

        Returns:
            str: access token
        """

    @abstractmethod
    async def validate_user_token(self, user_token: str):
        """Validate token from user

        Args:
            user_token (str): user to validate

        """
