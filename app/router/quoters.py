import logging
from typing import Annotated, Optional, List

from app.config import Configuration
from app.router.security import get_current_user
from app.domain.entities import QuoterModel, QuoterIdModel, QuoterUpdateModel

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
    tags=["quoters"],
    responses=responses,
)

conf = Configuration()
UserDeps = Annotated[bool, Depends(get_current_user)]

QUOTER_URL = conf.quoter_url


@router.get("/api/v1/quoters", response_model=List[QuoterModel])
async def search_quoter_by_content(
    user_validation: UserDeps,
    content: Optional[str] = None
):
    url = f"{QUOTER_URL}/api/v1/quoters?content={content}"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        log.error(f"Could not get data from quoters: {e}")
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


@router.get("/api/v1/quoters/{quoter_id}")
async def get_quoter(quoter_id: str, user_validation: UserDeps):
    url = f"{QUOTER_URL}/api/v1/quoters/{quoter_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        log.error(f"Could not get data from quoters: {e}")
        raise HTTPException(
            status_code=response.status_code,
            detail=response.json().get("detail")
        )
    if not response.text:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text
        )
    return response.json()


@router.post(
        "/api/v1/quoters",
        response_description="Add new quoter",
        response_model=QuoterModel)
async def insert_quoter(quoter: QuoterModel, user_validation: UserDeps):
    url = f"{QUOTER_URL}/api/v1/quoters"
    try:
        response = requests.post(url, json=jsonable_encoder(quoter))
        response.raise_for_status()
    except Exception as e:
        log.error(f"Could not post data to quoters: {e}")
        raise HTTPException(
            status_code=response.status_code,
            detail=response.json().get("detail")
        )
    if not response.text:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text
        )
    return response.json()


@router.post(
        "/api/v1/sales",
        response_description="Add new sale"
)
async def create_sell(quoter: QuoterIdModel, user_validation: UserDeps):
    url = f"{QUOTER_URL}/api/v1/sales"
    try:
        response = requests.post(url, json=jsonable_encoder(quoter))
        response.raise_for_status()
    except Exception as e:
        log.error(f"Could not post data to sales: {e}")
        raise HTTPException(
            status_code=response.status_code,
            detail=response.json().get("detail")
        )
    if not response.text:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text
        )
    return response.json()


@router.patch("/api/v1/quoters/{quoter_id}")
async def update_quoter(
    quoter_id: str,
    quoter: QuoterUpdateModel,
    user_validation: UserDeps
):
    url = f"{QUOTER_URL}/api/v1/quoters/{quoter_id}"
    try:
        response = requests.patch(url, json=jsonable_encoder(quoter))
        response.raise_for_status()
    except Exception as e:
        log.error(f"Could not patch data to quoters: {e}")
        raise HTTPException(
            status_code=response.status_code,
            detail=response.json().get("detail")
        )
    if not response.text:
        return Response(
            status_code=response.status_code
        )
    return response.json()
