from fastapi.security import OAuth2PasswordBearer
from model import database
import asyncio

oauth2_scheme = OAuth2PasswordBearer(
    scheme_name='获取 JWT Bearer 令牌',
    description='用于获取 JWT Bearer 令牌，需要以表单的形式提交',
    tokenUrl="/api/token"
    )

SECRET_KEY = asyncio.run(database.Database().get_setting('SECRET_KEY'))
ALGORITHM = "HS256"