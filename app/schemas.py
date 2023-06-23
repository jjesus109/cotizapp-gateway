from datetime import datetime
from typing import TypedDict

from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str


class UserDict(TypedDict):
    username: str
    password: str


class TokenToEncode(TypedDict):
    sub: str
    exp: datetime


class Token(BaseModel):
    access_token: str
    token_type: str
