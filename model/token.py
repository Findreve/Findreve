from pydantic import BaseModel
from passlib.context import CryptContext

# FastAPI 鉴权模型
# FastAPI authentication model
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")