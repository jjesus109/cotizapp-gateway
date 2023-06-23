from app.db.connections import create_connection
from app.infra.repository import Repository
from app.adapters.gateway import Gateway

db_conn = create_connection()
repo = Repository(nosql_conn=db_conn)
gateway = Gateway(repo)


def get_gateway():
    return gateway
