from datetime import datetime, timezone
from typing import Optional, Type, TypeVar, Union, Literal, List

from sqlalchemy import DateTime, BinaryExpression, ClauseElement
from sqlalchemy.orm import selectinload
from sqlmodel import SQLModel, Field, select, Relationship
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql._typing import _OnClauseArgument
from sqlalchemy.ext.asyncio import AsyncAttrs

B = TypeVar('B', bound='BaseModel')
M = TypeVar('M', bound='SQLModel')

utcnow = lambda: datetime.now(tz=timezone.utc)

class BaseModel(AsyncAttrs):
    __abstract__ = True
    
    id: Optional[int] = Field(default=None, primary_key=True, description="主键ID")
    created_at: datetime = Field(
        default_factory=utcnow,
        description="创建时间",
        )
    updated_at: datetime = Field(
        sa_type=DateTime,
        description="更新时间",
        sa_column_kwargs={"default": utcnow, "onupdate": utcnow},
        default_factory=utcnow
    )
    deleted_at: Optional[datetime] = Field(
        default=None, 
        description="删除时间",
        sa_column={"nullable": True}
    )
    
    @classmethod
    async def add(
        cls: Type[B],
        session: AsyncSession,
        instances: B | List[B],
        refresh: bool = True
    ) -> B | List[B]:
        """
        新增一条记录
        
        :param session: 异步会话对象
        :param instances: 实例或实例列表
        :param refresh: 是否刷新实例
        :return: 新增的实例或实例列表
        
        Example:
        
        >>> from model.base import BaseModel
        > from model.object import Object
        > from database import Database
        > import asyncio
        > async def main():
        >     async with Database.get_session() as session:
        >         obj = Object(key="12345", name="Test Object", icon="icon.png")
        >         added_obj = await BaseModel.add(session, obj)
        >         print(added_obj)
        > asyncio.run(main())

        """
        is_list = False
        if isinstance(instances, list):
            is_list = True
            session.add_all(instances)
        else:
            session.add(instances)

        await session.commit()

        if refresh:
            if is_list:
                for instance in instances:
                    await session.refresh(instance)
            else:
                await session.refresh(instances)

        return instances
    
    async def save(
        self: B,
        session: AsyncSession,
        load: Union[Relationship, None]
    ):
        """
        保存当前实例到数据库
        
        :param session: 异步会话对象
        :param load: 需要加载的关系属性
        :return: None
        
        """
        session.add(self)
        await session.commit()
        
        if load is not None:
            cls = type(self)
            return await cls.get(session, self.id, load=load)
        else:
            await session.refresh(self)
            return self
    
    async def update(
        self: B,
        session: AsyncSession,
        other: M,
        extra_data: dict = None,
        exclude_unset: bool = True,
    ) -> B:
        """
        更新当前实例
        
        :param session: 异步会话对象
        :param other: 用于更新的实例
        :param extra_data: 额外的数据字典
        :param exclude_unset: 是否排除未设置的字段
        :return: 更新后的实例
        """
        self.sqlmodel_update(
            other.model_dump(
                exclude_unset=exclude_unset
            ),
            update=extra_data
        )
        
        session.add(self)
        
        await session.commit()
        await session.refresh(self)
        
        return self
    
    @classmethod
    async def delete(
        cls: Type[B],
        session: AsyncSession,
        instance: B | list[B],
    ) -> None:
        """
        删除实例
        
        :param session: 异步会话对象
        :param instance: 实例或实例列表
        :return: None
        """
        
        if isinstance(instance, list):
            for inst in instance:
                await session.delete(inst)
        else:
            await session.delete(instance)
        
        await session.commit()
    
    @classmethod
    async def get(
            cls: Type[B],
            session: AsyncSession,
            condition: BinaryExpression | ClauseElement | None,
            *,
            offset: int | None = None,
            limit: int | None = None,
            fetch_mode: Literal["one", "first", "all"] = "first",
            join: Type[B] | tuple[Type[B], _OnClauseArgument] | None = None,
            options: list | None = None,
            load: Union[Relationship, None] = None,
            order_by: list[ClauseElement] | None = None
    ) -> B | List[B] | None:
        """
        异步获取模型实例

        参数:
            session: 异步数据库会话
            condition: SQLAlchemy查询条件，如Model.id == 1
            offset: 结果偏移量
            limit: 结果数量限制
            options: 查询选项，如selectinload(Model.relation)，异步访问关系属性必备，不然会报错
            fetch_mode: 获取模式 - "one"/"all"/"first"
            join: 要联接的模型类

        返回:
            根据fetch_mode返回相应的查询结果
        """
        statement = select(cls)

        if condition is not None:
            statement = statement.where(condition)

        if join is not None:
            statement = statement.join(*join)

        if options:
            statement = statement.options(*options)

        if load:
            statement = statement.options(selectinload(load))

        if order_by is not None:
            statement = statement.order_by(*order_by)

        if offset:
            statement = statement.offset(offset)

        if limit:
            statement = statement.limit(limit)

        result = await session.exec(statement)

        if fetch_mode == "one":
            return result.one()
        elif fetch_mode == "first":
            return result.first()
        elif fetch_mode == "all":
            return list(result.all())
        else:
            raise ValueError(f"无效的 fetch_mode: {fetch_mode}")
    
    @classmethod
    async def get_exist_one(cls: Type[B], session: AsyncSession, id: int, load: Union[Relationship, None] = None) -> B:
        """此方法和 await session.get(cls, 主键)的区别就是当不存在时不返回None，
        而是会抛出fastapi 404 异常"""
        instance = await cls.get(session, cls.id == id, load=load)
        if not instance:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Not found")
        return instance