import logging

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from db.model.user import UserModel
from enums.exception_error import ExceptionError
from schemas.user import ResquestAuthToken
from utils.functions import hash_password_md5


class UserRepository:
    def __init__(self):
        self._logger = logging.getLogger(__name__)

    def get_user_by_login_password(
        self, db_session: Session, data: ResquestAuthToken
    ) -> UserModel:
        self._logger.debug("-------------repository----------")

        pass_hash = hash_password_md5(data.password)

        print(f"------pass_hash-----: {pass_hash}")

        user = (
            db_session.query(UserModel)
            .filter(
                UserModel.email == data.login,
                UserModel.password == pass_hash,
                UserModel.is_active == True
            )
            .first()
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=ExceptionError.USER_NOT_FOUND.value,
            )

        return user
