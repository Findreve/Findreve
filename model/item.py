from datetime import datetime
from enum import StrEnum
from typing import TYPE_CHECKING, Self, Optional
from uuid import UUID

from sqlmodel import Field, Relationship

from .base import SQLModelBase, UUIDTableBase

if TYPE_CHECKING:
    from .user import User

class ItemTypeEnum(StrEnum):
    normal = 'normal'
    car = 'car'

class ItemStatusEnum(StrEnum):
    ok = 'ok'
    lost = 'lost'

class ItemBase(SQLModelBase):
    type: ItemTypeEnum = ItemTypeEnum.normal
    """物品的类型"""

    name: str
    """物品名称"""

    icon: str | None = None
    """物品图标"""

    status: ItemStatusEnum = ItemStatusEnum.ok
    """物品状态"""

    phone: str | None = None
    """联系电话"""

    description: str | None = None
    """物品描述"""

class Item(ItemBase, UUIDTableBase, table=True):
    expires_at: datetime | None = None
    """物品过期时间"""

    lost_at: datetime | None = None
    """物品丢失的时间"""

    find_ip: str | None = None
    """最后一次发现的IP地址"""

    user_id: UUID = Field(foreign_key='user.id', ondelete='CASCADE')
    """所属用户ID"""

    user: 'User' = Relationship(back_populates='items')

    parent_item_id: UUID | None = Field(foreign_key='item.id', ondelete='RESTRICT')
    parent_item: Optional['Item'] = Relationship(back_populates='sub_items', sa_relationship_kwargs={'remote_side': 'Item.id'})
    sub_items: list['Item'] = Relationship(back_populates='parent_item', passive_deletes='all')

class ItemDataUpdateRequest(ItemBase):
    pass

class ItemDataResponse(ItemBase):
    expires_at: datetime | None = None
    """物品过期时间"""

    lost_at: datetime | None = None
    """物品丢失的时间"""

class ItemDataResponseAdmin(ItemBase):
    expires_at: datetime | None = None
    """物品过期时间"""

    lost_at: datetime | None = None
    """物品丢失的时间"""

    user_id: UUID = Field(foreign_key='user.id')
    """所属用户ID"""
