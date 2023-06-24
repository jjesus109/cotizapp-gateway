import logging

from app.router import quoters, security, clients, products
from app.config import Configuration, configure_logger

import uvicorn
from fastapi import FastAPI


log = logging.getLogger(__name__)


app = FastAPI(
    title="Cotizapp Gateway API",
    description="Entrypoint for all backend with cotizapp backend",
    version="0.0.1",
    openapi_url="/api/openapi.json"
)
app.include_router(security.router)
app.include_router(quoters.router)
app.include_router(clients.router)
app.include_router(products.router)

if __name__ == "__main__":
    conf = Configuration()
    configure_logger()
    config = uvicorn.Config(
        app="app.main:app",
        port=conf.port,
        host=conf.host
    )
    server = uvicorn.Server(config)
    server.run()
