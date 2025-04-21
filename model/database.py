'''
Author: 于小丘 海枫
Date: 2024-10-02 15:23:34
LastEditors: Yuerchu admin@yuxiaoqiu.cn
LastEditTime: 2024-11-29 20:05:03
FilePath: /Findreve/model.py
Description: Findreve 数据库组件 model

Copyright (c) 2018-2024 by 于小丘Yuerchu, All Rights Reserved. 
'''

import aiosqlite
from datetime import datetime
import tool
import logging
from typing import Optional

# 数据库类
class Database:
    def __init__(self, db_path: str = "data.db"):
        self.db_path = db_path

    async def init_db(self):
        """初始化数据库和表"""
        logging.info("开始初始化数据库和表")
        
        create_objects_table = """
        CREATE TABLE IF NOT EXISTS fr_objects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT NOT NULL,
            name TEXT NOT NULL,
            icon TEXT,
            status TEXT,
            phone TEXT,
            context TEXT,
            find_ip TEXT,
            create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            lost_at TIMESTAMP
        )
        """
        
        create_settings_table = """
        CREATE TABLE IF NOT EXISTS fr_settings (
            type TEXT,
            name TEXT PRIMARY KEY,
            value TEXT
        )
        """
        
        async with aiosqlite.connect(self.db_path) as db:
            logging.info("连接到数据库")
            await db.execute(create_objects_table)
            logging.info("创建或验证fr_objects表")
            await db.execute(create_settings_table)
            logging.info("创建或验证fr_settings表")
            
            # 初始化设置表数据
            async with db.execute("SELECT name FROM fr_settings WHERE name = 'version'") as cursor:
                if not await cursor.fetchone():
                    await db.execute(
                        "INSERT INTO fr_settings (type, name, value) VALUES (?, ?, ?)",
                        ('string', 'version', '1.0.0')
                    )
                    logging.info("插入初始版本信息: version 1.0.0")

            async with db.execute("SELECT name FROM fr_settings WHERE name = 'ver'") as cursor:
                if not await cursor.fetchone():
                    await db.execute(
                        "INSERT INTO fr_settings (type, name, value) VALUES (?, ?, ?)", 
                        ('int', 'ver', '1')
                    )
                    logging.info("插入初始版本号: ver 1")

            async with db.execute("SELECT name FROM fr_settings WHERE name = 'account'") as cursor:
                if not await cursor.fetchone():
                    account = 'admin@yuxiaoqiu.cn'
                    await db.execute(
                        "INSERT INTO fr_settings (type, name, value) VALUES (?, ?, ?)", 
                        ('string', 'account', account)
                    )
                    logging.info(f"插入初始账号信息: {account}")

            async with db.execute("SELECT name FROM fr_settings WHERE name = 'password'") as cursor:
                if not await cursor.fetchone():
                    password = tool.generate_password()
                    hashed_password = tool.hash_password(password)
                    await db.execute(
                        "INSERT INTO fr_settings (type, name, value) VALUES (?, ?, ?)",
                        ('string', 'password', hashed_password)
                    )
                    logging.info("插入初始密码信息")
                    print(f"密码（请牢记，后续不再显示）: {password}")
            
            async with db.execute("SELECT name FROM fr_settings WHERE name = 'SECRET_KEY'") as cursor:
                if not await cursor.fetchone():
                    secret_key = tool.generate_password(64)
                    await db.execute(
                        "INSERT INTO fr_settings (type, name, value) VALUES (?, ?, ?)",
                        ('string', 'SECRET_KEY', secret_key)
                    )
                    logging.info("插入初始密钥信息")
            
            await db.commit()
            logging.info("数据库初始化完成并提交更改")
    
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