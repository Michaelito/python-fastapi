import logging
import sys

from fastapi import Depends, FastAPI
from routers import auth
from services.auth import AuthService

app = FastAPI(title='ACCELERATE V8', version='1.0.0')

logging.basicConfig(stream=sys.stdout, encoding='utf-8',
                    format="%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] %(name)s: %(message)s", level=logging.DEBUG)

_logger = logging.getLogger(__name__)


@app.get("/health", tags=["Utils"], summary="Get Health")
async def get_health():
    _logger.debug("----------get_health-----------")
    return "OK"


@app.get("/protected", tags=["Protected"], summary="Protected Route")
async def protected_route(current_user: dict = Depends(AuthService().get_current_user)):
    _logger.debug("----------protected_route-----------")

    return {"message": "This is a protected route", "user": current_user}


app.include_router(auth.router)
