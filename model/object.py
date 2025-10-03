# my_project/models/download.py

from typing import Literal
from sqlmodel import Field, Column, String, DateTime
from .base import TableBase, IdMixin
from datetime import datetime

class Object(IdMixin, TableBase, table=True):

    key: str = Field(index=True, nullable=False, description="物品外部ID")
    type: Literal['normal', 'car'] = Field(
        default='normal', 
        description="物品类型", 
        sa_column=Column(String, default='normal', nullable=False)
    )
    name: str = Field(nullable=False, description="物品名称")
    icon: str | None = Field(default=None, description="物品图标")
    status: Literal['ok', 'lost'] = Field(
        default='ok', 
        description="物品状态",
        sa_column=Column(String, default='ok', nullable=False)
    )
    phone: str | None = Field(default=None, description="联系电话")
    context: str | None = Field(default=None, description="物品描述")
    find_ip: str | None = Field(default=None, description="最后一次发现的IP地址")
    lost_at: datetime | None = Field(
        default=None,
        description="物品标记为丢失的时间",
        sa_column=Column(DateTime, nullable=True)
    )