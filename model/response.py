from pydantic import BaseModel

from model.base import SQLModelBase


class DefaultResponse(BaseModel):
    code: int = 0
    data: dict | list | bool | SQLModelBase | None = None
    msg: str = ""

# FastAPI 鉴权返回模型
class TokenResponse(BaseModel):
    access_token: str

class TokenData(BaseModel):
    username: str | None = None
