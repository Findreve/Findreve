from sqlmodel import Field
from .base import TableBase, SQLModelBase


class SettingBase(SQLModelBase):
    type: str = Field(index=True)
    """设置类型"""

    name: str = Field(index=True, unique=True)  # name 为唯一主键
    """设置名称"""

    value: str | None
    """设置值"""

class Setting(SettingBase, TableBase, table=True):
    pass

class SettingResponse(SettingBase):
    pass
