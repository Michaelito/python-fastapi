import logging
import sys

from fastapi import FastAPI
from routers import auth
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


app = FastAPI(title='V8 API', version='1.0.0')

logging.basicConfig(stream=sys.stdout, encoding='utf-8',
                    format="%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] %(name)s: %(message)s", level=logging.DEBUG)


@app.get("/health", tags=["Utils"], summary="Get Health")
async def get_health():
    print("------Health-------")
    return "OK"


app.include_router(auth.router)
