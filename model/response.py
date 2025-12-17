from pydantic import BaseModel

from model.base import SQLModelBase

"""
[TODO] 弃用，改成 ResponseBase：

class ResponseBase(BaseModel):
    code: int = 0
    msg: str = ""
    request_id: UUID

再根据需要继承
"""
class DefaultResponse(BaseModel):
    code: int = 0
    data: dict | list | bool | SQLModelBase | None = None
    msg: str = ""

# FastAPI 鉴权返回模型
class TokenResponse(BaseModel):
    access_token: str

class TokenData(BaseModel):
    username: str | None = None
