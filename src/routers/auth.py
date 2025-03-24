import logging

from fastapi import APIRouter, HTTPException
from schemas.user import ResquestAuthToken
from services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])

logger = logging.getLogger(__name__)


@router.post("/login", summary="User Login")
def login_auth_token(data: ResquestAuthToken) -> dict:
    logger.info("-------------route----------")

    try:
        service = AuthService()
        response = service.login(data=data)

        return response

    except HTTPException as e:
        logger.error(e)
        raise e
