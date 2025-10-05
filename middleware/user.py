from typing import Annotated, Literal
from fastapi import Depends
from fastapi import HTTPException
import JWT
import jwt
from jwt import InvalidTokenError
from model import database
from sqlmodel.ext.asyncio.session import AsyncSession
from model import User

# 验证是否为管理员
async def get_current_user(
        token: Annotated[str, Depends(JWT.oauth2_scheme)],
        session: Annotated[AsyncSession, Depends(database.Database.get_session)],
) -> User:
    '''
    验证用户身份并返回当前用户信息。
    '''
    not_login_exception = HTTPException(
        status_code=401,
        detail="Login required",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, await JWT.get_secret_key(), algorithms=[JWT.ALGORITHM])
        username = payload.get("sub")
        stored_account = await User.get(session, User.email == username)
        if username is None or not stored_account.email == username:
            raise not_login_exception
        return stored_account
    except InvalidTokenError:
        raise not_login_exception