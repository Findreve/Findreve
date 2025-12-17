from typing import Annotated
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from model.user import UserTypeEnum
from .user import get_current_user
from pkg import utils
from model import User
from model import database

# 验证是否为管理员
async def is_admin(
        token: Annotated[str, Depends(get_current_user)],
        session: Annotated[AsyncSession, Depends(database.Database.get_session)],
) -> User:
    '''
    验证是否为管理员。
    
    使用方法：
    >>> APIRouter(dependencies=[Depends(is_admin)])
    '''

    user = await get_current_user(token, session)
    if user.role == UserTypeEnum.normal_user:
        utils.raise_forbidden("Admin access required")
    else:
        return user
    
async def is_super_admin(
        token: Annotated[str, Depends(is_admin)],
        session: Annotated[AsyncSession, Depends(database.Database.get_session)],
) -> User:
    '''
    验证是否为超级管理员。
    
    使用方法：
    >>> APIRouter(dependencies=[Depends(is_super_admin)])
    '''

    user = await get_current_user(token, session)
    if user.role != UserTypeEnum.super_admin:
        utils.raise_forbidden("Super admin access required")
    else:
        return user