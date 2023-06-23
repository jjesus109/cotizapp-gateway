import logging

from pydantic import BaseSettings


class Configuration(BaseSettings):

    port: int = 5000
    host: str = "0.0.0.0"
    log_level: str = "INFO"
    db_host: str
    db_user: str
    db_passwrd: str
    db_name: str
    collection: str
    secret_key: str
    algorithm:  str
    expire_time: int
    quoter_url: str
    client_url: str
    service_url: str


def configure_logger():
    conf = Configuration()
    logger = logging.getLogger()
    logger.setLevel(conf.log_level)
    ch = logging.StreamHandler()
    ch.setLevel(conf.log_level)
    formatter = logging.Formatter(
        "[%(levelname)s] %(asctime)s: %(name)s: %(message)s"
    )

    ch.setFormatter(formatter)
    logger.addHandler(ch)
