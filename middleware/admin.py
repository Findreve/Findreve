from typing import Annotated, Literal
from fastapi import Depends
from fastapi import HTTPException
import JWT
import jwt
from jwt import InvalidTokenError
from model import database
from sqlmodel.ext.asyncio.session import AsyncSession
from model import User
from .user import get_current_user

# 验证是否为管理员
async def is_admin(
        token: Annotated[str, Depends(get_current_user)],
        session: Annotated[AsyncSession, Depends(database.Database.get_session)],
) -> Literal[True]:
    '''
    验证是否为管理员。
    
    使用方法：
    >>> APIRouter(dependencies=[Depends(is_admin)])
    '''

    not_admin_exception = HTTPException(
        status_code=403,
        detail="Admin access required",
        headers={"WWW-Authenticate": "Bearer"},
    )

    user = await get_current_user(token, session)
    if not user.is_admin:
        raise not_admin_exception
    else:
        return True