from typing import Annotated

import jwt
from fastapi import Depends
from jwt import InvalidTokenError
from sqlmodel.ext.asyncio.session import AsyncSession

import JWT
from model import User
from model.database import Database
from pkg import utils

async def get_current_user(
        token: Annotated[str, Depends(JWT.oauth2_scheme)],
        session: Annotated[AsyncSession, Depends(Database.get_session)],
) -> User:
    """
    验证用户身份并返回当前用户信息。
    """

    try:
        payload = jwt.decode(token, await JWT.get_secret_key(), algorithms=[JWT.ALGORITHM])
        username = payload.get("sub")
        stored_account = await User.get(session, User.email == username)
        if username is None or stored_account.email != username:
            utils.raise_unauthorized("Login required")
        return stored_account
    except InvalidTokenError:
        utils.raise_unauthorized("Login required")