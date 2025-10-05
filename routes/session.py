# 导入库
from typing import Annotated
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter
import jwt, JWT
from sqlmodel.ext.asyncio.session import AsyncSession
from pkg import Password
from loguru import logger

from model.token import Token
from model import Setting, User, database

Router = APIRouter(tags=["令牌 session"])

# 创建令牌
async def create_access_token(session: AsyncSession, data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=await Setting.get(session, 'jwt_token_exp'))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key=await JWT.get_secret_key(), algorithm='HS256')
    return encoded_jwt

# 验证账号密码
async def authenticate_user(session: AsyncSession, username: str, password: str):
    # 验证账号和密码
    account = await User.get(session, User.email == username)

    if not account:
        logger.error("Account or password not set in settings.")
        return False

    if account.email != username or not Password.verify(account.password, password):
        logger.error("Invalid username or password.")
        return False
    
    return account

# FastAPI 登录路由 / FastAPI login route
@Router.post(
    path="/api/token",
    summary="获取访问令牌",
    description="使用用户名和密码获取访问令牌",
    response_model=Token,
    response_description="访问令牌"
)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[AsyncSession, Depends(database.Database.get_session)],
) -> Token:
    user = await authenticate_user(
        session=session, 
        username=form_data.username, 
        password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(hours=1)
    access_token = await create_access_token(
        session=session,
        data={"sub": form_data.username},
        expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")