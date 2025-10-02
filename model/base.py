# model/base.py
from datetime import datetime, timezone
from typing import Optional, Type, TypeVar, Union, Literal, List

from sqlalchemy import DateTime, BinaryExpression, ClauseElement
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlmodel import SQLModel, Field, select, Relationship
from sqlalchemy.sql._typing import _OnClauseArgument

B = TypeVar('B', bound='TableBase')
M = TypeVar('M', bound='SQLModel')

utcnow = lambda: datetime.now(tz=timezone.utc)

class TableBase(AsyncAttrs, SQLModel):
    __abstract__ = True

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
        is_list = isinstance(instances, list)
        if is_list:
            session.add_all(instances)
        else:
            session.add(instances)
        await session.commit()
        if refresh:
            if is_list:
                for i in instances:
                    await session.refresh(i)
            else:
                await session.refresh(instances)
        return instances

    async def save(
        self: B,
        session: AsyncSession,
        load: Union[Relationship, None] = None,   # 设默认值，避免必须传
    ):
        session.add(self)
        await session.commit()
        if load is not None:
            cls = type(self)
            return await cls.get(session, cls.id == self.id, load=load)  # 若该模型没有 id，请别用 load 模式
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
        self.sqlmodel_update(
            other.model_dump(exclude_unset=exclude_unset),
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
        instance = await cls.get(session, cls.id == id, load=load)
        if not instance:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Not found")
        return instance


# 需要“自增 id 主键”的模型才混入它；Setting 不混入
class IdMixin(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True, description="主键ID")