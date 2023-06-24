import logging
from typing import Annotated, List

from app.config import Configuration
from app.router.security import get_current_user
from app.domain.entities import (
    ServiceModel,
    ServiceUpdateModel,
    ProductModel
)

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
    tags=["products-services"],
    responses=responses,
)

conf = Configuration()
UserDeps = Annotated[bool, Depends(get_current_user)]

PRODUCT_URL = conf.service_url


@router.get("/api/v1/products", response_model=List[ProductModel])
async def search_product(product_name: str, user_validation: UserDeps):
    url = f"{PRODUCT_URL}/api/v1/products?product_name={product_name}"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        log.error(f"Could not get data from products: {e}")
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


@router.get("/api/v1/services", response_model=List[ServiceModel])
async def search_service_by_name(service_name: str, user_validation: UserDeps):
    url = f"{PRODUCT_URL}/api/v1/services?service_name={service_name}"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        log.error(f"Could not get data from services: {e}")
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


@router.get("/api/v1/services/description", response_model=List[ServiceModel])
async def search_service_by_description(
    service_description: str,
    user_validation: UserDeps
):
    url = (
        f"{PRODUCT_URL}/api/v1/services/"
        f"description?service_description={service_description}"
    )
    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        log.error(f"Could not get data from services: {e}")
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


@router.get("/api/v1/services/{service_id}", response_model=ServiceModel)
async def get_service(service_id: str, user_validation: UserDeps):
    url = f"{PRODUCT_URL}/api/v1/services/{service_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        log.error(f"Could not get data from services: {e}")
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


@router.get("/api/v1/products/{product_id}", response_model=ProductModel)
async def get_product(product_id: str, user_validation: UserDeps):
    url = f"{PRODUCT_URL}/api/v1/products/{product_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        log.error(f"Could not get data from services: {e}")
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
        "/api/v1/services",
        response_description="Add new service",
        response_model=ServiceModel)
async def create_service(service: ServiceModel, user_validation: UserDeps):
    url = f"{PRODUCT_URL}/api/v1/services"
    try:
        response = requests.patch(url, json=jsonable_encoder(service))
        response.raise_for_status()
    except Exception as e:
        log.error(f"Could not get data from services: {e}")
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
        "/api/v1/products",
        response_description="Add new service",
        response_model=ProductModel)
async def create_product(product: ProductModel, user_validation: UserDeps):
    url = f"{PRODUCT_URL}/api/v1/products"
    try:
        response = requests.patch(url, json=jsonable_encoder(product))
        response.raise_for_status()
    except Exception as e:
        log.error(f"Could not get data from services: {e}")
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


@router.patch("/api/v1/services/{service_id}")
async def modify_service(
    service_id: str,
    service: ServiceUpdateModel,
    user_validation: UserDeps
):
    url = f"{PRODUCT_URL}/api/v1/services/{service_id}"
    try:
        response = requests.patch(url, json=jsonable_encoder(service))
        response.raise_for_status()
    except Exception as e:
        log.error(f"Could not get data from services: {e}")
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text
        )
    if not response.text:
        return Response(
            status_code=response.status_code
        )
    return response.json()
