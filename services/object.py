"""
物品相关业务逻辑。
"""

from typing import List
from uuid import UUID

from fastapi import HTTPException
from loguru import logger
from sqlmodel.ext.asyncio.session import AsyncSession

from model import Item, ItemDataResponse, Setting, User
from model.item import ItemDataUpdateRequest, ItemTypeEnum
from pkg.sender import ServerChatBot, WeChatBot
from pkg.utils import raise_bad_request, raise_internal_error, raise_not_found
from starlette.status import HTTP_204_NO_CONTENT


async def list_items(
    session: AsyncSession,
    user: User,
    item_id: int | None = None,
    key: str | None = None,
) -> List[Item]:
    """
    根据条件获取当前用户的物品列表。
    """
    if item_id is not None:
        results = await Item.get(session, (Item.id == item_id) & (Item.user_id == user.id))
        results = [results] if results else []
    elif key is not None:
        results = await Item.get(session, (Item.key == key) & (Item.user_id == user.id))
        results = [results] if results else []
    else:
        results = await Item.get(session, Item.user_id == user.id, fetch_mode="all")

    if not results:
        return []

    items: list[Item] = []
    for obj in results:
        items.append(
            Item(
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
                lost_time=obj.lost_at.isoformat() if obj.lost_at else None,
            )
        )
    return items


async def create_item(
    session: AsyncSession,
    user: User,
    request: ItemDataUpdateRequest,
) -> None:
    """
    创建新的物品信息。
    """
    try:
        request_dict = request.model_dump()
        request_dict["user"] = user
        request_dict["user_id"] = user.id
        await Item.add(session, Item.model_validate(request_dict))
    except Exception as exc:  # noqa: BLE001
        logger.error(f"Failed to add item: {exc}")
        raise HTTPException(status_code=500, detail=str(exc)) from exc


async def update_item(
    session: AsyncSession,
    user: User,
    item_id: UUID,
    request: ItemDataUpdateRequest,
) -> None:
    """
    更新物品信息。
    """
    obj = await Item.get(session, (Item.id == item_id) & (Item.user_id == user.id))
    if not obj:
        raise_not_found("Item not found or access denied")

    await obj.update(session, request, exclude_unset=True)


async def delete_item(
    session: AsyncSession,
    user: User,
    item_id: UUID,
) -> None:
    """
    删除指定物品。
    """
    obj = await Item.get(session, (Item.id == item_id) & (Item.user_id == user.id))
    if not obj:
        raise_not_found("Item not found or access denied")
    await Item.delete(session, obj)


async def retrieve_object(
    session: AsyncSession,
    item_id: UUID,
    client_host: str,
) -> ItemDataResponse:
    """
    根据物品 ID 获取物品信息并视情况更新寻找者 IP。
    """
    object_data = await Item.get(session, Item.id == item_id)

    if not object_data:
        raise_not_found("物品不存在或出现异常")

    if object_data.status == "lost":
        object_data.find_ip = client_host
        object_data = await object_data.save(session)

    return ItemDataResponse.model_validate(object_data)


async def notify_move_car(
    session: AsyncSession,
    item_id: UUID,
    phone: str | None = None,
) -> int:
    """
    向车主发送挪车通知。
    """
    item_data = await Item.get_exist_one(session=session, id=item_id)

    if item_data.type != ItemTypeEnum.car:
        raise_bad_request("Item is not car")

    server_chan_key = await Setting.get(session, Setting.name == "server_chan_key")
    wechat_bot_key = await Setting.get(session, Setting.name == "wechat_bot_key")
    if not (server_chan_key.value or wechat_bot_key.value):
        raise_internal_error("未配置Server酱，无法发送挪车通知")

    title = "挪车通知 - Findreve"
    description = (
        f"您的车辆“{item_data.name}”被请求挪车。\n"
        f"{f'请求挪车者电话：[{phone}](tel:{phone})' if phone else ''}\n"
        "请尽快联系请求者并挪车。"
    )

    mentioned_channel = (await Setting.get(session, Setting.name == "mentioned_channel")).value

    if mentioned_channel == "server_chan":
        await ServerChatBot.send_text(session=session, title=title, description=description)
    elif mentioned_channel == "wechat_bot":
        await WeChatBot.send_markdown(
            session=session,
            markdown=f"# {title}\n\n{description}",
            version="v1",
        )

    return HTTP_204_NO_CONTENT
