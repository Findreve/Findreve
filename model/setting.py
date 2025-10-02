# model/setting.py
from typing import TYPE_CHECKING, Optional
from sqlmodel import Field
from .base import TableBase

"""
原表：
CREATE TABLE IF NOT EXISTS fr_settings (
    type TEXT,
    name TEXT PRIMARY KEY,
    value TEXT
)
"""

if TYPE_CHECKING:
    pass

class Setting(TableBase, table=True):
    __tablename__ = 'fr_settings'

    type: str = Field(index=True, nullable=False, description="设置类型")
    name: str = Field(primary_key=True, nullable=False, description="设置名称")  # name 为唯一主键
    value: Optional[str] = Field(description="设置值")
