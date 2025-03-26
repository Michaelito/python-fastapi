import hashlib
import base64

from fastapi import HTTPException


def hash_password_md5(password: str) -> str:

    hashed_password = hashlib.md5(password.encode('utf-8')).digest()
    return base64.b64encode(hashed_password).decode('utf-8')


def create_http_exception(self, status_code: int, detail: str) -> HTTPException:
    return HTTPException(
        status_code=status_code, detail=detail, headers={
            "WWW-Authenticate": "Bearer"}
    )
