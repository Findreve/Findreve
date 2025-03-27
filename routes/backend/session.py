from nicegui import app
from typing import Annotated
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter
import jwt, JWT

from model.token import Token
from model import database
from tool import verify_password

Router = APIRouter()

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT.SECRET_KEY, algorithm='HS256')
    return encoded_jwt

async def authenticate_user(username: str, password: str):
    # 验证账号和密码
    account = await database.Database().get_setting('account')
    stored_password = await database.Database().get_setting('password')

    if account != username or not verify_password(stored_password, password):
        return False
    
    return {'is_authenticated': True}

# FastAPI 登录路由 / FastAPI login route
@app.post("/api/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(hours=1)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")