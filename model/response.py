from pydantic import BaseModel

class DefaultResponse(BaseModel):
    code: int = 0
    data: dict | list | None = None
    msg: str = ""