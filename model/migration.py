from loguru import logger
from sqlmodel import select
from .setting import Setting
from .user import User
from pkg import Password

default_settings: list[Setting] = [
    Setting(type='string', name='version', value='1.0.0'),
    Setting(type='int', name='jwt_token_exp', value='30'),
    Setting(type='string', name='server_chan_key', value=''),
]

async def migration(session):
    # 先准备基础配置
    settings: list[Setting] = default_settings.copy()

    if await Setting.get(session, Setting.name == 'version'):
        # 已有数据，说明不是第一次运行，直接返回
        return
    
    settings.append(Setting(type='string', name='SECRET_KEY', value=Password.generate(64)))

    # 读取库里已存在的 name，避免主键冲突
    names = [s.name for s in settings]
    existed_settings = await Setting.get(
        session, 
        Setting.name.in_(names),
        fetch_mode="all"
    )
    existed: set[str] = {s.name for s in (existed_settings or [])}

    to_insert = [s for s in settings if s.name not in existed]
    if to_insert:
        await Setting.add(session, to_insert, refresh=False)
    
    if await User.get(session, User.id == 1):
        # 已有超级管理员用户，说明不是第一次运行

        # 修复数据库id为1的用户不是管理员的问题
        admin_user = await User.get(session, User.id == 1)
        if admin_user and not admin_user.is_admin:
            admin_user.is_admin = True
            await User.update(session, admin_user, refresh=False)
        
        # 已有用户，直接返回
        return

    # 生成初始密码与密钥
    admin_password = Password.generate()
    logger.warning("当前无管理员用户，已自动创建初始管理员用户:")
    logger.warning("邮箱: admin@yxqi.cn")
    logger.warning(f"密码: {admin_password}")

    admin_user = User(
        id=1,
        email='admin@yxqi.cn',
        username='Admin',
        password=Password.hash(admin_password),
        is_admin=True
    )

    await User.add(session, admin_user, refresh=False)