from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from middleware.admin import is_admin
from model import database
from model.response import DefaultResponse
from services import admin as admin_service

Router = APIRouter(
    prefix='/api/admin', 
    tags=['管理员 Admin'],
    dependencies=[Depends(is_admin)]
)

@Router.get(
    path='/',
    summary='验证管理员身份',
    description='返回管理员身份验证结果',
    response_model=DefaultResponse,
    response_description='当前为管理员'
)
async def verity_admin() -> DefaultResponse:
    '''
    使用 API 验证是否为管理员。
    
    - 若为管理员，返回 `True`
    - 若不是管理员，抛出 `401` 错误
    '''
    return DefaultResponse(data=True)

@Router.get(
    path='api/admin/settings',
    summary='获取设置项',
    description='获取设置项, 留空则获取所有',
    response_model=DefaultResponse,
    response_description='设置项列表'
)
async def get_settings(
    session: Annotated[AsyncSession, Depends(database.Database.get_session)],
    name: str | None = None
) -> DefaultResponse:
    data = await admin_service.fetch_settings(session=session, name=name)
    return DefaultResponse(data=data)


@Router.put(
    path='api/admin/settings',
    summary='更新设置项',
    description='更新设置项',
    response_model=DefaultResponse,
    response_description='更新结果'
)
async def update_settings(
    session: Annotated[AsyncSession, Depends(database.Database.get_session)],
    name: str,
    value: str
) -> DefaultResponse:
    result = await admin_service.update_setting_value(session=session, name=name, value=value)
    return DefaultResponse(data=result)
