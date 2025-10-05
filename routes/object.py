from typing import Annotated, Literal
from uuid import UUID

from fastapi import APIRouter, Request, Query, HTTPException
from fastapi.responses import JSONResponse
from loguru import logger
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.ext.asyncio import AsyncSession

from middleware.user import get_current_user
from model import DefaultResponse, ItemDataResponse, User, database, Setting, Item
from model.item import ItemDataUpdateRequest
from pkg.utils import raise_not_found, raise_bad_request, raise_internal_error, raise_service_unavailable

limiter = Limiter(key_func=get_remote_address)

from fastapi import Depends
import asyncio
import aiohttp

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
                phone=int(obj.phone) if obj.phone and obj.phone.isdigit() else 0,
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
    response_model=DefaultResponse,
    response_description='添加物品成功'
)
async def add_items(
    session: Annotated[AsyncSession, Depends(database.Database.get_session)],
    user: Annotated[User, Depends(get_current_user)],
    request: ItemDataUpdateRequest
) -> DefaultResponse:
    """
    添加物品信息。

    - **key**: 物品的关键字
    - **type**: 物品的类型
    - **name**: 物品的名称
    - **icon**: 物品的图标
    - **phone**: 联系电话
    """
    
    try:
        # 创建新物品对象,关联当前用户
        await Item.add(session, Item.model_validate(request))
    except Exception as e:
        logger.error(f"Failed to add item: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    else:
        return DefaultResponse(data=True)

@Router.patch(
    path='/items/{item_id}',
    summary='更新物品信息',
    description='更新现有物品的信息',
    response_model=DefaultResponse,
    response_description='更新物品成功'
)
async def update_items(
    session: Annotated[AsyncSession, Depends(database.Database.get_session)],
    user: Annotated[User, Depends(get_current_user)],
    item_id: UUID,
    request: ItemDataUpdateRequest
) -> DefaultResponse:
    """
    更新物品信息。

    只有 `id` 是必填参数，其余参数都是可选的，在不传入任何值的时候将不做任何更改。

    - **id**: 物品的ID
    - **key**: 物品的序列号 **不建议修改此项，这样会导致生成的物品二维码直接失效**
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

    await obj.update(session, request)

    return DefaultResponse(data=True)

@Router.delete(
    path='/items',
    summary='删除物品信息',
    description='删除指定的物品信息',
    response_model=DefaultResponse,
    response_description='删除物品成功'
)
async def delete_items(
    session: Annotated[AsyncSession, Depends(database.Database.get_session)],
    user: Annotated[User, Depends(get_current_user)],
    id: int
) -> DefaultResponse:
    """
    删除物品信息。

    - **id**: 物品的ID
    """
    # 获取现有物品,验证归属权
    obj = await Item.get(session, (Item.id == id) & (Item.user_id == user.id))
    if not obj:
        raise_not_found("Item not found or access denied")
    await Item.delete(session, obj)

    return DefaultResponse(data=True)

@Router.get(
    path='/{item_key}',
    summary="获取物品信息",
    description="根据物品键获取物品信息",
    response_model=DefaultResponse,
    response_description="物品信息"
)
async def get_object(
    session: Annotated[AsyncSession, Depends(database.Database.get_session)],
    item_key: str, 
    request: Request
) -> DefaultResponse:
    """
    获取物品信息 / Get object information
    """
    object_data = await Item.get(session, Item.key == item_key)
    
    if object_data:
        if object_data.status == 'lost':
            # 物品已标记为丢失，更新IP地址
            object_data.find_ip = str(request.client.host)
            object_data = await object_data.save(session)

        return DefaultResponse(data=ItemDataResponse.model_validate(object_data))
    else:
        raise_not_found('物品不存在或出现异常')

@Router.put(
    path='/{item_id}',
    summary="通知车主进行挪车",
    description="向车主发送挪车通知",
    response_model=DefaultResponse,
    response_description="挪车通知结果"
)
@limiter.limit(
    limit_value="1/5minute",  # 每5分钟允许1次请求
    error_message="小主已经通知过车主了，请稍安勿躁~"
)
async def notify_move_car(
    request: Request,
    session: Annotated[AsyncSession, Depends(database.Database.get_session)],
    item_id: int,
    phone: str = None,
):
    """
    通知车主进行挪车 / Notify car owner to move the car

    Args:
        item_id (int): 物品ID / Item ID
        phone (str): 挪车发起者电话 / Phone number of the person initiating the move. Defaults to None.
    """
    
    # 检查是否存在该物品
    object_data = await Item.get(session, Item.id == item_id)
    if not object_data:
        raise_not_found()
    
    # 检查物品类型是否为车辆
    if object_data.type != 'car':
        raise_bad_request("Item is not car")
    
    # 发起挪车通知（目前仅适配Server酱）
    server_chan_key = await Setting.get(session, Setting.name == 'server_chan_key')
    if not server_chan_key:
        raise_internal_error('未配置Server酱，无法发送挪车通知')
    
    title = "挪车通知 - Findreve"
    description = f"您的车辆“{object_data.name}”被请求挪车。\n\n"
    if phone:
        description += f"请求挪车者电话：[{phone}](tel:{phone})\n\n"    
    description += "请尽快联系请求者并挪车。"
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            url=f"https://sctapi.ftqq.com/{server_chan_key.value}.send",
            data={
                "title": title,
                "desp": description
            }
        ) as resp:
            if resp.status == 200:
                resp_json = await resp.json()
                if resp_json.get('code') == 0:
                    return DefaultResponse(msg='挪车通知发送成功')
                else:
                    error_msg = resp_json.get('message')
                    logger.error(
                        f"Failed to send notification via Server Chan: error_code={resp_json.get('code')}, "
                        f"error_message={error_msg}, item_id={item_id}, response={resp_json}"
                    )
                    raise_service_unavailable('Server酱出现问题，发送失败')
            else:
                response_text = await resp.text()
                logger.error(
                    f"Failed to send notification via Server Chan: http_status={resp.status}, item_id={item_id}, "
                    f"response_body={response_text}, url={resp.url}"
                )
                raise_internal_error('挪车通知发送失败')
