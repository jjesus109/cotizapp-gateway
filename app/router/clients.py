import logging
from typing import Annotated, List

from app.config import Configuration
from app.router.security import get_current_user
from app.domain.entities import Client, ClientUpdate

import requests
from fastapi import Depends, APIRouter, HTTPException, Response
from fastapi.encoders import jsonable_encoder

log = logging.getLogger(__name__)

responses = {
    "401": {
        "description": "Unauthorized"
    },
    "500": {
        "description": "Problems with other servers"
    },
}

router = APIRouter(
    tags=["clients"],
    responses=responses,
)

conf = Configuration()
UserDeps = Annotated[bool, Depends(get_current_user)]

CLIENT_URL = conf.client_url


@router.get("/api/v1/clients", response_model=List[Client])
async def get_clients(word_to_search: str, user_validation: UserDeps):
    url = f"{CLIENT_URL}/api/v1/clients?word_to_search={word_to_search}"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        log.error(f"Could not get data from clients: {e}")
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text
        )
    if not response.text:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.json().get("detail")
        )
    return response.json()


@router.get("/api/v1/clients/{client_id}", response_model=Client)
async def get_client(client_id: str, user_validation: UserDeps):
    url = f"{CLIENT_URL}/api/v1/clients/{client_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        log.error(f"Could not get data from clients: {e}")
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text
        )
    if not response.text:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.json().get("detail")
        )
    return response.json()


@router.post(
        "/api/v1/clients",
        response_description="Add new client",
        response_model=Client)
async def create_client(client: Client, user_validation: UserDeps):
    url = f"{CLIENT_URL}/api/v1/clients"
    try:
        response = requests.post(url, json=jsonable_encoder(client))
        response.raise_for_status()
    except Exception as e:
        log.error(f"Could not get data from clients: {e}")
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text
        )
    if not response.text:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.json().get("detail")
        )
    return response.json()


@router.patch("/api/v1/clients/{client_id}")
async def modify_client(
    client_id: str,
    client: ClientUpdate,
    user_validation: UserDeps
):
    url = f"{CLIENT_URL}/api/v1/clients/{client_id}"
    try:
        response = requests.patch(url, json=jsonable_encoder(client))
        response.raise_for_status()
    except Exception as e:
        log.error(f"Could not get data from clients: {e}")
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text
        )
    if not response.text:
        return Response(
            status_code=response.status_code
        )
    return response.json()
