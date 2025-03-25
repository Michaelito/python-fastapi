import logging
import os
import time
import jwt
import uuid

from datetime import datetime, timedelta
from fastapi import HTTPException, Request, status
from db.database import create_db_session
from db.repositories.user import UserRepository
from enums.exception_error import ExceptionError
from schemas.user import ResquestAuthToken

from dotenv import load_dotenv

load_dotenv()


class AuthService:
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._user_rep = UserRepository()
        self._jwt_algorithm = "HS256"
        self._jwt_secret = os.getenv("JWT_SECRET_KEY", "default_secret")
        self._jwt_expire_hours = int(os.getenv("JWT_EXPIRE_HOURS", "1"))

    def login(self, data: ResquestAuthToken) -> dict:
        self._logger.info(f"Login attempt: {data}")

        try:
            with create_db_session() as conn:

                user = self._user_rep.get_user_by_login_password(
                    db_session=conn, data=data)

                if not user:
                    raise self._create_http_exception(
                        status.HTTP_401_UNAUTHORIZED, ExceptionError.UNAUTHORIZED.value
                    )

                return self.generate_jwt_token(user)

        except HTTPException as http_exc:
            raise http_exc

        except Exception as e:
            self._logger.error(f"Login error: {e}")
            raise self._create_http_exception(
                status.HTTP_500_INTERNAL_SERVER_ERROR, ExceptionError.INTERNAL_ERROR.value
            )

    def generate_jwt_token(self, data) -> dict:

        self._logger.info(f"---generate_jwt_token----: {data}")

        expire_time = datetime.utcnow() + timedelta(hours=self._jwt_expire_hours)

        payload = {
            "session_id": str(uuid.uuid4()),
            "first_name": data.first_name,
            "last_name": data.last_name,
            "role": data.cd_role,
            "email": data.email,
            "exp": int(time.mktime(expire_time.timetuple())),
        }

        access_token = jwt.encode(
            payload, self._jwt_secret, algorithm=self._jwt_algorithm)

        return {"access_token": access_token, "token_type": "bearer"}

    def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, self._jwt_secret, algorithms=[self._jwt_algorithm])
        except jwt.ExpiredSignatureError:
            raise self._create_http_exception(
                status.HTTP_401_UNAUTHORIZED, ExceptionError.TOKEN_EXPIRED.value
            )
        except jwt.InvalidTokenError:
            raise self._create_http_exception(
                status.HTTP_401_UNAUTHORIZED, ExceptionError.TOKEN_INVALID.value
            )

    def get_current_user(self, request: Request) -> dict:
        token = request.headers.get("Authorization")
        if not token:
            raise self._create_http_exception(
                status.HTTP_401_UNAUTHORIZED, ExceptionError.TOKEN_INVALID.value
            )
        try:
            scheme, _, token = token.partition(" ")
            if scheme.lower() != "bearer":
                raise self._create_http_exception(
                    status.HTTP_401_UNAUTHORIZED, ExceptionError.TOKEN_INVALID.value
                )
            return self.decode_token(token)
        except HTTPException as e:
            raise e

    def _create_http_exception(self, status_code: int, detail: str) -> HTTPException:
        return HTTPException(
            status_code=status_code, detail=detail, headers={
                "WWW-Authenticate": "Bearer"}
        )
