# ~/models/database.py
from contextlib import asynccontextmanager
from typing import AsyncGenerator
import os
from dotenv import load_dotenv

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from .migration import migration

# 加载环境变量
load_dotenv('.env')

# 获取 DEBUG 配置
DEBUG = os.getenv("DEBUG", "false").lower() in ("true", "1", "yes")

ASYNC_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///data.db")

engine: AsyncEngine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=DEBUG,  # 根据 DEBUG 配置决定是否输出 SQL 日志
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

    @staticmethod
    @asynccontextmanager
    async def session_context() -> AsyncGenerator[AsyncSession, None]:
        """
        提供异步上下文管理器用于直接获取数据库会话
        
        使用示例:
            async with Database.session_context() as session:
                # 执行数据库操作
                pass
        """
        async with _async_session_factory() as session:
            yield session

    async def init_db(self, url: str = ASYNC_DATABASE_URL):
        """创建数据库结构"""
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

        # For internal use, create a temporary context manager
        async with self.session_context() as session:
            await migration(session)  # 执行迁移脚本