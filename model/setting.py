from sqlmodel import Field
from .base import TableBase

class Setting(TableBase, table=True):

    type: str = Field(index=True, nullable=False, description="设置类型")
    name: str = Field(primary_key=True, nullable=False, description="设置名称")  # name 为唯一主键
    value: str | None = Field(description="设置值")
