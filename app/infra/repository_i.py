from typing import Any
from abc import ABC, abstractmethod


class RepositoryInterface(ABC):

    @abstractmethod
    async def get_user(self, username: str) -> Any:
        """Get user data from username

        Args:
            username (str): username go get data from

        Returns:
            Any: User data
        """

    @abstractmethod
    async def verify_password(self, form_pass: str, hashed_pass: str):
        """Verify form password matches with stores one

        Args:
            form_pass (str): passworf got from form
            hashed_pass (str): stored passworf
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
    async def decode_token(self, token: str) -> Any:
        """Decode received token

        Args:
            token (Any): token to decode

        Returns:
            Any: token decoded
        """
