from typing import TYPE_CHECKING
from sqlmodel import Field, Column, String, Boolean, Relationship
from .base import TableBase, IdMixin

if TYPE_CHECKING:
    from .object import Object

class User(IdMixin, TableBase, table=True):

    email: str = Field(sa_column=Column(String(100), index=True, unique=True))
    username: str = Field(sa_column=Column(String(50), index=True, unique=True))
    password: str = Field(sa_column=Column(String(100)))

    is_admin: bool = Field(default=False, sa_column=Column(Boolean, default=False))
    
    objects: list["Object"] = Relationship(back_populates="user")