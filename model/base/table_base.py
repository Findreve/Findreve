import uuid
from datetime import datetime, timezone
from typing import Union, TypeVar, Type, Literal, override, Optional, Any

from fastapi import HTTPException
from sqlalchemy import DateTime, BinaryExpression, ClauseElement
from sqlalchemy.orm import selectinload
from sqlmodel import Field, select, Relationship, SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.sql._typing import _OnClauseArgument
from sqlalchemy.ext.asyncio import AsyncAttrs

T = TypeVar("T", bound="TableBase")
M = TypeVar("M", bound="SQLModel")

now = lambda: datetime.now()
now_date = lambda: datetime.now().date()

class TableBase(AsyncAttrs):
    id: int | None = Field(default=None, primary_key=True)

    created_at: datetime = Field(default_factory=now)
    updated_at: datetime = Field(
        sa_type=DateTime,
        sa_column_kwargs={"default": now, "onupdate": now},
        default_factory=now
    )

    @classmethod
    async def add(cls: Type[T], session: AsyncSession, instances: T | list[T], refresh: bool = True) -> T | list[T]:
        """
        新增一条记录
        :param session: 数据库会话
        :param instances:
        :param refresh:
        :return: 新增的实例对象

        usage:
        item1 = Item(...)
        item2 = Item(...)

        Item.add(session, [item1, item2])

        item1_id = item1.id
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

    async def save(self: T, session: AsyncSession, load: Optional[Relationship] = None) -> T:
        session.add(self)
        await session.commit()

        if load is not None:
            cls = type(self)
            return await cls.get(session, cls.id == self.id, load=load)
        else:
            await session.refresh(self)
            return self

    async def update(
            self: T,
            session: AsyncSession,
            other: M,
            extra_data: dict = None,
            exclude_unset: bool = True
    ) -> T:
        """
        更新记录
        :param session: 数据库会话
        :param other:
        :param extra_data:
        :param exclude_unset:
        :return:
        """
        self.sqlmodel_update(other.model_dump(exclude_unset=exclude_unset), update=extra_data)

        session.add(self)

        await session.commit()
        await session.refresh(self)

        return self

    @classmethod
    async def delete(cls: Type[T], session: AsyncSession, instances: T | list[T]) -> None:
        """
        删除一些记录
        :param session: 数据库会话
        :param instances:
        :return: None

        usage:
        item1 = Item.get(...)
        item2 = Item.get(...)

        Item.delete(session, [item1, item2])

        """
        if isinstance(instances, list):
            for instance in instances:
                await session.delete(instance)
        else:
            await session.delete(instances)

        await session.commit()

    @classmethod
    async def get(
            cls: Type[T],
            session: AsyncSession,
            condition: BinaryExpression | ClauseElement | None,
            *,
            offset: int | None = None,
            limit: int | None = None,
            fetch_mode: Literal["one", "first", "all"] = "first",
            join: Type[T] | tuple[Type[T], _OnClauseArgument] | None = None,
            options: list | None = None,
            load: Union[Relationship, None] = None,
            order_by: list[ClauseElement] | None = None
    ) -> T | list[T] | None:
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
    async def get_exist_one(cls: Type[T], session: AsyncSession, id: int, load: Union[Relationship, None] = None) -> T:
        """此方法和 await session.get(cls, 主键)的区别就是当不存在时不返回None，
        而是会抛出fastapi 404 异常"""
        instance = await cls.get(session, cls.id == id, load=load)
        if not instance:
            raise HTTPException(status_code=404, detail="Not found")
        return instance

class UUIDTableBase(TableBase):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    """override"""

    @override
    @classmethod
    async def get_exist_one(cls: Type[T], session: AsyncSession, id: uuid.UUID, load: Union[Relationship, None] = None) -> T:
        return await super().get_exist_one(session, id, load)
