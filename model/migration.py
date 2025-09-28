from typing import Sequence
from sqlmodel import select
from .setting import Setting
import tool

default_settings: list[Setting] = [
    Setting(type='string', name='version', value='1.0.0'),
    Setting(type='int',    name='ver',     value='1'),
    Setting(type='string', name='account', value='admin@yuxiaoqiu.cn'),
]

async def migration(session):
    # 先准备基础配置
    settings: list[Setting] = default_settings.copy()

    # 生成初始密码与密钥
    admin_password = tool.generate_password()
    print(f"密码（请牢记，后续不再显示）: {admin_password}")

    settings.append(Setting(type='string', name='password',   value=tool.hash_password(admin_password)))
    settings.append(Setting(type='string', name='SECRET_KEY', value=tool.generate_password(64)))

    # 读取库里已存在的 name，避免主键冲突
    names = [s.name for s in settings]
    exist_stmt = select(Setting.name).where(Setting.name.in_(names))
    exist_rs = await session.exec(exist_stmt)
    existed: set[str] = set(exist_rs.all())

    to_insert = [s for s in settings if s.name not in existed]
    if to_insert:
        # 使用你写好的通用新增方法（是类方法），并传入会话
        await Setting.add(session, to_insert, refresh=False)

"""
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
                    print(f"账号: {account}")

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
"""