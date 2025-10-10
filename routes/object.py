from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import SessionDep
from middleware.user import get_current_user
from model import DefaultResponse, User, database
from model.item import ItemDataUpdateRequest
from services import object as object_service
from starlette.status import HTTP_204_NO_CONTENT

limiter = Limiter(key_func=get_remote_address)

Router = APIRouter(prefix='/api/object', tags=['物品 Object'])

@Router.get(
    path='/items',
    summary='获取物品信息',
    description='返回物品信息列表',
    response_model=DefaultResponse,
    response_description='物品信息列表'
)
async def get_items(
    session: Annotated[AsyncSession, Depends(database.Database.get_session)],
    token: Annotated[User, Depends(get_current_user)],
    id: int | None = Query(default=None, ge=1, description='物品ID'),
    key: str | None = Query(default=None, description='物品序列号')):
    """
    获得物品信息。

    不传参数返回所有信息,否则可传入 `id` 或 `key` 进行筛选。
    """
    items = await object_service.list_items(
        session=session,
        user=token,
        item_id=id,
        key=key,
    )
    return DefaultResponse(data=items)

@Router.post(
    path='/items',
    summary='添加物品信息',
    description='添加新的物品信息',
	status_code=HTTP_204_NO_CONTENT,
    response_description='添加物品成功'
)
async def add_items(
    session: Annotated[AsyncSession, Depends(database.Database.get_session)],
    user: Annotated[User, Depends(get_current_user)],
    request: ItemDataUpdateRequest
):
    """
    添加物品信息。
    """
    await object_service.create_item(
        session=session,
        user=user,
        request=request,
    )

@Router.patch(
    path='/items/{item_id}',
    summary='更新物品信息',
    description='更新现有物品的信息',
	status_code=HTTP_204_NO_CONTENT,
    response_description='更新物品成功'
)
async def update_items(
    session: Annotated[AsyncSession, Depends(database.Database.get_session)],
    user: Annotated[User, Depends(get_current_user)],
    item_id: UUID,
	request: ItemDataUpdateRequest,
):
    """
    更新物品信息。

    只有 `id` 是必填参数，其余参数都是可选的，在不传入任何值的时候将不做任何更改。

    - **id**: 物品的ID
    - **key**: 物品的序列号
    - **name**: 物品的名称
    - **icon**: 物品的图标
    - **status**: 物品的状态
    - **phone**: 联系电话
    - **lost_description**: 物品丢失描述
    - **find_ip**: 找到物品的IP
    - **lost_time**: 物品丢失时间
    """

    await object_service.update_item(
        session=session,
        user=user,
        item_id=item_id,
        request=request,
    )

@Router.delete(
    path='/items/{item_id}',
    summary='删除物品信息',
    description='删除指定的物品信息',
	status_code=HTTP_204_NO_CONTENT,
    response_description='删除物品成功'
)
async def delete_items(
    session: Annotated[AsyncSession, Depends(database.Database.get_session)],
    user: Annotated[User, Depends(get_current_user)],
	item_id: UUID
):
    """
    删除物品信息。
    - **id**: 物品的ID
    """
    await object_service.delete_item(
        session=session,
        user=user,
        item_id=item_id,
    )

@Router.get(
    path='/{item_id}',
    summary="获取物品信息",
    description="根据物品键获取物品信息",
    response_model=DefaultResponse,
    response_description="物品信息"
)
async def get_object(
    session: Annotated[AsyncSession, Depends(database.Database.get_session)],
	item_id: UUID,
    request: Request
) -> DefaultResponse:
    """
    获取物品信息 / Get object information
    """
    data = await object_service.retrieve_object(
        session=session,
        item_id=item_id,
        client_host=str(request.client.host),
    )
    return DefaultResponse(data=data.model_dump())

@Router.post(
    path='/{item_id}/notify_move_car',
    summary="通知车主进行挪车",
    description="向车主发送挪车通知",
	status_code=HTTP_204_NO_CONTENT,
    response_description="挪车通知结果"
)
async def notify_move_car(
    _request: Request,
    session: SessionDep,
    item_id: UUID,
    phone: str = None,
):
    """
    通知车主进行挪车 / Notify car owner to move the car

    Args:
        _request (Request): ...
        session (AsyncSession): 数据库会话 / Database session
        item_id (int): 物品ID / Item ID
        phone (str): 挪车发起者电话 / Phone number of the person initiating the move. Defaults to None.
    """
    await object_service.notify_move_car(
        session=session,
        item_id=item_id,
        phone=phone,
    )
