# ~/models/database.py
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from .migration import migration

ASYNC_DATABASE_URL = "sqlite+aiosqlite:///data.db"

engine: AsyncEngine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,
    connect_args={
        "check_same_thread": False
    } if ASYNC_DATABASE_URL.startswith("sqlite") else {},
    future=True,
    # pool_size=POOL_SIZE,
    # max_overflow=64,
)

_async_session_factory = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


# 数据库类
class Database:
    # Database 初始化方法
    def __init__(
        self,  # self 用于引用类的实例
        db_path: str = "data.db",  # db_path 数据库文件路径，默认为 data.db
    ):
        self.db_path = db_path

    @staticmethod
    async def get_session() -> AsyncGenerator[AsyncSession, None]:
        """FastAPI dependency to get a database session."""
        async with _async_session_factory() as session:
            yield session

    async def init_db(self, url: str = ASYNC_DATABASE_URL):
        """创建数据库结构"""
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

        # For internal use, create a temporary context manager
        get_session_cm = asynccontextmanager(self.get_session)
        async with get_session_cm() as session:
            await migration(session)  # 执行迁移脚本