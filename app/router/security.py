import logging
from typing import Annotated

from app.errors import (
    EmptyDataError,
    CorruptedTokenError,
    DBError,
    UserNotFoundException,
    PasswordNotMatchedException,
)
from app.depends import get_gateway
from app.adapters.gateway_i import GatewayInterface
from app.schemas import Token

from fastapi import Depends, APIRouter, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


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
    tags=["auth"],
    responses=responses,
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/token")


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        gateway: Annotated[GatewayInterface, Depends(get_gateway)]
) -> bool:
    try:
        await gateway.validate_user_token(token)
    except (UserNotFoundException, EmptyDataError, CorruptedTokenError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except DBError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not connect to other services"
        )
    return True


@router.post("/api/v1/token", response_model=Token)
async def login_for_access_token(
    request: Request,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    gateway: Annotated[GatewayInterface, Depends(get_gateway)]
):
    try:
        user = await gateway.authenticate_user(
            form_data.username,
            form_data.password
        )
    except (UserNotFoundException, PasswordNotMatchedException):
        log.error("User not match")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return await gateway.create_acces_token(
        user
    )
