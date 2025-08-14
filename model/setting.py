from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, SQLModel
from .base import BaseModel

"""
原建表语句：

CREATE TABLE IF NOT EXISTS fr_settings (
    type TEXT,
    name TEXT PRIMARY KEY,
    value TEXT
"""

if TYPE_CHECKING:
    pass

class Setting(SQLModel, BaseModel, table=True):
    __tablename__ = 'fr_settings'

    type: str = Field(index=True, nullable=False, description="设置类型")
    name: str = Field(index=True, primary_key=True, nullable=False, description="设置名称")
    value: Optional[str] = Field(description="设置值")