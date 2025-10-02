from pydantic import BaseModel
from typing import Literal, Optional

class DefaultResponse(BaseModel):
    code: int = 0
    data: dict | list | bool | None = None
    msg: str = ""

class ObjectData(BaseModel):
    id: int
    type: Literal['normal', 'car']
    key: str
    name: str
    icon: str
    status: Literal['ok', 'lost']
    phone: str
    context: Optional[str] = None