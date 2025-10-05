from enum import StrEnum
from typing import ClassVar

import sqlalchemy as sa
from pydantic import EmailStr
from sqlalchemy import event
from sqlalchemy.orm.session import Session as SessionClass
from sqlmodel import Field, Relationship

from .base import SQLModelBase, UUIDTableBase
from .item import Item


class UserTypeEnum(StrEnum):
    normal_user = 'normal_user'
    admin = 'admin'
    super_admin = 'super_admin'

class UserBase(SQLModelBase):
    pass

class User(UserBase, UUIDTableBase, table=True):
    email: EmailStr = Field(index=True, unique=True)
    """邮箱"""

    username: str = Field(index=True, unique=True)
    """用户名"""

    password: str
    """Argon2算法哈希后的密码"""

    two_factor_secret: str | None = None
    """两步验证的密钥"""

    role: UserTypeEnum = Field(default=UserTypeEnum.normal_user, index=True)
    """用户的权限等级"""

    items: list[Item] = Relationship(back_populates='user', cascade_delete=True)
    """物品关系"""

    _initializing: ClassVar[bool] = False
    """标记当前是否处于初始化阶段，初始化阶段允许创建 super_admin"""

@event.listens_for(SessionClass, "before_flush")
def check_super_admin_immutability(session, flush_context, instances):
    """
    在事务刷新到数据库前，集中检查所有关于 super_admin 的不合法操作。
    此监听器确保超级管理员的角色和存在性是不可变的。
    """
    # 检查1: 禁止创建新的 super_admin
    for obj in session.new:
        if isinstance(obj, User) and obj.role == UserTypeEnum.super_admin and not User._initializing:
            raise ValueError("业务规则：不允许创建新的超级管理员。")

    # 检查2: 禁止删除已存在的 super_admin
    for obj in session.deleted:
        if isinstance(obj, User):
            state = sa.inspect(obj)
            # 直接从对象被删除前的状态获取角色，避免不必要的 lazy load
            original_role = state.committed_state.get('role')
            if original_role == UserTypeEnum.super_admin:
                username = state.committed_state.get('username', f'(ID: {obj.id})')
                raise ValueError(f"业务规则：不允许删除超级管理员 '{username}'。")

    # 检查3: 禁止与 super_admin 相关的角色变更
    for obj in session.dirty:
        if isinstance(obj, User):
            state = sa.inspect(obj)
            # 仅在 'role' 字段确实被修改时才进行检查
            if "role" in state.committed_state:
                history = state.attrs.role.history
                original_role = history.deleted[0]
                new_role = history.added[0]

                # 场景 a: 禁止将 super_admin 降级
                if original_role == UserTypeEnum.super_admin:
                    raise ValueError(f"业务规则：不允许将超级管理员 '{obj.username}' 的角色降级。")

                # 场景 b: 禁止将任何用户提升为 super_admin
                if new_role == UserTypeEnum.super_admin:
                    raise ValueError(f"业务规则：不允许将用户 '{obj.username}' 提升为超级管理员。")
