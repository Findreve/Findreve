from contextlib import asynccontextmanager
import aiosqlite
from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator

import warnings
from .migration import migration

ASYNC_DATABASE_URL = "sqlite+aiosqlite:///data.db"

engine: AsyncEngine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,
    connect_args={
        "check_same_thread": False
    } if ASYNC_DATABASE_URL.startswith("sqlite") else None,
    future=True,
    # pool_size=POOL_SIZE,
    # max_overflow=64,
)

_async_session_factory = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# 数据库类
class Database:
    
    # Database 初始化方法
    def __init__(
        self,                       # self 用于引用类的实例
        db_path: str = "data.db"    # db_path 数据库文件路径，默认为 data.db
    ):
        self.db_path = db_path
    
    @staticmethod
    @asynccontextmanager
    async def get_session() -> AsyncGenerator[AsyncSession, None]:
        async with _async_session_factory() as session:
            yield session

    async def init_db(
        self,
        url: str = ASYNC_DATABASE_URL
        ):
        """创建数据库结构"""
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
        
        async with self.get_session() as session:
            await migration(session)  # 执行迁移脚本
    
    async def add_object(self, key: str, name: str, icon: str = None, phone: str = None):
        """
        添加新对象
        
        :param key: 序列号
        :param name: 名称
        :param icon: 图标
        :param phone: 电话
        """
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT 1 FROM fr_objects WHERE key = ?", (key,)) as cursor:
                if await cursor.fetchone():
                    raise ValueError(f"序列号 {key} 已存在")
            
            now = datetime.now()
            now = now.strftime("%Y-%m-%d %H:%M:%S")
            await db.execute(
                "INSERT INTO fr_objects (key, name, icon, phone, create_at, status) VALUES (?, ?, ?, ?, ?, 'ok')",
                (key, name, icon, phone, now)
            )
            await db.commit()
    
    async def update_object(
        self, 
        id: int,
        key: str = None,
        name: str = None,
        icon: str = None,
        status: str = None,
        phone: int = None,
        lost_description: Optional[str] = None,
        find_ip: Optional[str] = None,
        lost_time: Optional[str] = None):
        """
        更新对象信息
        
        :param id: 对象ID
        :param key: 序列号
        :param name: 名称
        :param icon: 图标
        :param status: 状态
        :param phone: 电话
        :param lost_description: 丢失描述
        :param find_ip: 发现IP
        :param lost_time: 丢失时间
        """
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT 1 FROM fr_objects WHERE id = ?", (id,)) as cursor:
                if not await cursor.fetchone():
                    raise ValueError(f"ID {id} 不存在")
            
            async with db.execute("SELECT 1 FROM fr_objects WHERE key = ? AND id != ?", (key, id)) as cursor:
                if await cursor.fetchone():
                    raise ValueError(f"序列号 {key} 已存在")
                
            await db.execute(
                f"UPDATE fr_objects SET "
                f"key = COALESCE(?, key), "
                f"name = COALESCE(?, name), "
                f"icon = COALESCE(?, icon), "
                f"status = COALESCE(?, status), "
                f"phone = COALESCE(?, phone), "
                f"context = COALESCE(?, context), "
                f"find_ip = COALESCE(?, find_ip), "
                f"lost_at = COALESCE(?, lost_at) "
                f"WHERE id = ?",
                (key, name, icon, status, phone, lost_description, find_ip, lost_time, id)
            )
            await db.commit()
    
    async def get_object(self, id: int = None, key: str = None):
        """
        获取对象
        
        :param id: 对象ID
        :param key: 序列号
        """
        async with aiosqlite.connect(self.db_path) as db:
            if id is not None or key is not None:
                async with db.execute(
                    "SELECT * FROM fr_objects WHERE id = ? OR key = ?", (id, key)
                ) as cursor:
                    return await cursor.fetchone()
            else:
                async with db.execute("SELECT * FROM fr_objects") as cursor:
                    return await cursor.fetchall()
    
    async def delete_object(self, id: int):
        """
        删除对象
        
        :param id: 对象ID
        """
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("DELETE FROM fr_objects WHERE id = ?", (id,))
            await db.commit()
    
    async def set_setting(self, name: str, value: str):
        """
        设置配置项
        
        :param name: 配置项名称
        :param value: 配置项值
        """
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT OR REPLACE INTO fr_settings (name, value) VALUES (?, ?)",
                (name, value)
            )
            await db.commit()
    
    async def get_setting(self, name: str):
        """
        获取配置项
        
        :param name: 配置项名称
        """
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                "SELECT value FROM fr_settings WHERE name = ?", (name,)
            ) as cursor:
                result = await cursor.fetchone()
                return result[0] if result else None