# my_project/models/download.py

from typing import Literal, Optional, TYPE_CHECKING
from sqlmodel import Field, Column, SQLModel, String, DateTime
from .base import TableBase, IdMixin
from datetime import datetime

"""
原建表语句：

CREATE TABLE IF NOT EXISTS fr_objects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key TEXT NOT NULL,
    name TEXT NOT NULL,
    icon TEXT,
    status TEXT,
    phone TEXT,
    context TEXT,
    find_ip TEXT,
    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    lost_at TIMESTAMP
"""

if TYPE_CHECKING:
    pass

class Object(IdMixin, TableBase, table=True):
    __tablename__ = 'fr_objects'

    key: str = Field(index=True, nullable=False, description="物品外部ID")
    type: Literal['object', 'box'] = Field(
        default='object', 
        description="物品类型", 
        sa_column=Column(String, default='object', nullable=False)
    )
    name: str = Field(nullable=False, description="物品名称")
    icon: Optional[str] = Field(default=None, description="物品图标")
    status: Optional[str] = Field(default=None, description="物品状态")
    phone: Optional[str] = Field(default=None, description="联系电话")
    context: Optional[str] = Field(default=None, description="物品描述")
    find_ip: Optional[str] = Field(default=None, description="最后一次发现的IP地址")
    lost_at: Optional[datetime] = Field(
        default=None,
        description="物品标记为丢失的时间",
        sa_column=Column(DateTime, nullable=True)
    )