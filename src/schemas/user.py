from pydantic import BaseModel


class ResquestAuthToken(BaseModel):
    login: str
    password: str
