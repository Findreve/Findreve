"""
会话服务，负责处理登录与令牌生成逻辑。
"""

from datetime import datetime, timedelta, timezone
from typing import Any

import JWT
import jwt
from loguru import logger
from sqlmodel.ext.asyncio.session import AsyncSession

from model import Setting, User
from model.response import TokenResponse
from pkg import Password


async def create_access_token(
    session: AsyncSession,
    data: dict[str, Any],
    expires_delta: timedelta | None = None,
) -> str:
    """
    创建访问令牌。
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        jwt_exp_setting = await Setting.get(session, Setting.name == "jwt_token_exp")
        expire = datetime.now(timezone.utc) + timedelta(int(jwt_exp_setting.value))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key=await JWT.get_secret_key(), algorithm="HS256")
    return encoded_jwt


async def authenticate_user(
    session: AsyncSession,
    username: str,
    password: str,
) -> User | None:
    """
    验证用户名和密码，返回认证后的用户。
    """
    account = await User.get(session, User.email == username)

    if not account:
        logger.error("Account or password not set in settings.")
        return None

    if account.email != username or not Password.verify(account.password, password):
        logger.error("Invalid username or password.")
        return None

    return account


async def login_for_access_token(
    session: AsyncSession,
    username: str,
    password: str,
) -> TokenResponse | None:
    """
    登录并生成访问令牌。
    """
    user = await authenticate_user(session=session, username=username, password=password)
    if not user:
        return None

    access_token = await create_access_token(
        session=session,
        data={"sub": user.email},
    )
    return TokenResponse(access_token=access_token)
