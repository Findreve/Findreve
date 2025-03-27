from fastapi.security import OAuth2PasswordBearer
from model import database
import asyncio

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")

SECRET_KEY = asyncio.run(database.Database().get_setting('SECRET_KEY'))