from app.config import Configuration
from app.errors import DBError

from motor.motor_asyncio import AsyncIOMotorClient
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import (
    ConfigurationError,
    ConnectionFailure,
)

conf = Configuration()


def create_connection() -> AsyncIOMotorDatabase:
    url_connection = (
        "mongodb+srv://{}:{}@{}/?retryWrites=true&w=majority".format(
            conf.db_user,
            conf.db_passwrd,
            conf.db_host
        )
    )
    database_name = conf.db_name
    try:
        client = AsyncIOMotorClient(url_connection)
    except (ConfigurationError, ConnectionFailure) as e:
        raise DBError(
            f"Could not connect to database due to: {e}"
        )
    return client[database_name]
