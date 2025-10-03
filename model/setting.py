# model/setting.py
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

class Setting(TableBase, table=True):

    type: str = Field(index=True, nullable=False, description="设置类型")
    name: str = Field(primary_key=True, nullable=False, description="设置名称")  # name 为唯一主键
    value: str | None = Field(description="设置值")
