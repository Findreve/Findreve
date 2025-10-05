from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Request, Query, HTTPException
from loguru import logger
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import SessionDep
from middleware.user import get_current_user
from model import DefaultResponse, ItemDataResponse, User, database, Setting, Item
from model.item import ItemDataUpdateRequest, ItemTypeEnum
from pkg.sender import ServerChatBot, WeChatBot
from pkg.utils import raise_not_found, raise_bad_request, raise_internal_error

from starlette.status import HTTP_204_NO_CONTENT

limiter = Limiter(key_func=get_remote_address)

from fastapi import Depends

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

    # 根据条件查询物品,只获取当前用户的物品
    if id is not None:
        results = await Item.get(session, (Item.id == id) & (Item.user_id == token.id))
        results = [results] if results else []
    elif key is not None:
        results = await Item.get(session, (Item.key == key) & (Item.user_id == token.id))
        results = [results] if results else []
    else:
        results = await Item.get(session, Item.user_id == token.id, fetch_mode="all")

    if results:
        items = []
        for obj in results:
            items.append(Item(
                id=obj.id,
                type=obj.type,
                key=obj.id,
                name=obj.name,
                icon=obj.icon or "",
                status=obj.status or "",
                phone=obj.phone if obj.phone and obj.phone.isdigit() else None,
                lost_description=obj.description,
                find_ip=obj.find_ip,
                create_time=obj.created_at.isoformat(),
                lost_time=obj.lost_at.isoformat() if obj.lost_at else None
            ))
        return DefaultResponse(data=items)
    else:
        return DefaultResponse(data=[])

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
    try:
        # 创建新物品对象,关联当前用户
        request_dict = request.model_dump()
        request_dict['user'] = user
        request_dict['user_id'] = user.id

        await Item.add(session, Item.model_validate(request_dict))
    except Exception as e:
        logger.error(f"Failed to add item: {e}")
        raise HTTPException(status_code=500, detail=str(e))

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
    # 获取现有物品,验证归属权
    obj = await Item.get(session, (Item.id == item_id) & (Item.user_id == user.id))
    if not obj:
        raise_not_found("Item not found or access denied")

    await obj.update(session, request, exclude_unset=True)

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
    # 获取现有物品,验证归属权
    obj = await Item.get(session, (Item.id == item_id) & (Item.user_id == user.id))
    if not obj:
        raise_not_found("Item not found or access denied")
    await Item.delete(session, obj)

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
    object_data = await Item.get(session, Item.id == item_id)

    if object_data:
        if object_data.status == 'lost':
            # 物品已标记为丢失，更新IP地址
            object_data.find_ip = str(request.client.host)
            object_data = await object_data.save(session)

        data = ItemDataResponse.model_validate(object_data)

        return DefaultResponse(data=data.model_dump())
    else:
        raise_not_found('物品不存在或出现异常')

@Router.post(
    path='/{item_id}/notify_move_car',
    summary="通知车主进行挪车",
    description="向车主发送挪车通知",
	status_code=HTTP_204_NO_CONTENT,
    response_description="挪车通知结果"
)
async def notify_move_car(
    request: Request,
    session: SessionDep,
    item_id: UUID,
    phone: str = None,
):
    """
    通知车主进行挪车 / Notify car owner to move the car

    Args:
        request (Request): ...
        session (AsyncSession): 数据库会话 / Database session
        item_id (int): 物品ID / Item ID
        phone (str): 挪车发起者电话 / Phone number of the person initiating the move. Defaults to None.
    """
    # 检查是否存在该物品
    item_data = await Item.get_exist_one(session=session, id=item_id)

    # 检查物品类型是否为车辆
    if item_data.type != ItemTypeEnum.car:
        raise_bad_request("Item is not car")

    # 发起挪车通知
    server_chan_key = await Setting.get(session, Setting.name == 'server_chan_key')
    wechat_bot_key = await Setting.get(session, Setting.name == 'wechat_bot_key')
    if not (server_chan_key.value or wechat_bot_key.value):
        raise_internal_error('未配置Server酱，无法发送挪车通知')

    title = "挪车通知 - Findreve"
    description = f"""您的车辆“{item_data.name}”被请求挪车。
{f"请求挪车者电话：[{phone}](tel:{phone})" if phone else ""}
请尽快联系请求者并挪车。"""

    # 获取通知的方式
    mentioned_channel = (await Setting.get(session, Setting.name == 'mentioned_channel')).value

    if mentioned_channel == 'server_chan':
        await ServerChatBot.send_text(
            session=session,
            title=title,
            description=description
        )
    elif mentioned_channel == 'wechat_bot':
        await WeChatBot.send_markdown(
            session=session,
            markdown=f"# {title}\n\n{description}",
            version='v1'
        )
