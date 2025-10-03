from pydantic import BaseModel

# FastAPI 鉴权模型
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None