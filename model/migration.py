from loguru import logger
from sqlmodel import select
from .setting import Setting
from pkg import Password

default_settings: list[Setting] = [
    Setting(type='string', name='version', value='1.0.0'),
    Setting(type='int',    name='ver',     value='1'),
    Setting(type='string', name='account', value='admin@yuxiaoqiu.cn'),
]

async def migration(session):
    # 先准备基础配置
    settings: list[Setting] = default_settings.copy()

    if await Setting.get(session, Setting.name == 'version'):
        # 已有数据，说明不是第一次运行，直接返回
        return

    # 生成初始密码与密钥
    admin_password = Password.generate()
    logger.warning(f"密码（请牢记，后续不再显示）: {admin_password}")

    settings.append(Setting(type='string', name='password',   value=Password.hash(admin_password)))
    settings.append(Setting(type='string', name='SECRET_KEY', value=Password.generate(64)))

    # 读取库里已存在的 name，避免主键冲突
    names = [s.name for s in settings]
    exist_stmt = select(Setting.name).where(Setting.name.in_(names))
    exist_rs = await session.exec(exist_stmt)
    existed: set[str] = set(exist_rs.all())

    to_insert = [s for s in settings if s.name not in existed]
    if to_insert:
        # 使用你写好的通用新增方法（是类方法），并传入会话
        await Setting.add(session, to_insert, refresh=False)