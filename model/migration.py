from loguru import logger
from .setting import Setting
from .user import User, UserTypeEnum
from pkg import Password

default_settings: list[Setting] = [
    Setting(type='string', name='version', value='2.0.0'),              # 版本号，用于考虑是否需要数据迁移
    Setting(type='int', name='jwt_token_exp', value='30'),              # JWT Token 访问令牌
    Setting(type='int', name='mentioned_channel', value='wechat_bot'),  # 通知推送通道
    Setting(type='string', name='server_chan_key', value=''),           # Server 酱推送密钥
    Setting(type='string', name='wechat_bot_key', value=''),            # 企业微信机器人推送密钥
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
        Setting.name in names,
        fetch_mode='all'
    )
    existed: set[str] = {s.name for s in (existed_settings or [])}

    to_insert = [s for s in settings if s.name not in existed]
    if to_insert:
        await Setting.add(session, to_insert)

    if not await User.get(session, User.role == UserTypeEnum.super_admin):
        # 生成初始密码与密钥
        admin_password = Password.generate()
        logger.warning("当前无管理员用户，已自动创建初始管理员用户:")
        logger.warning("邮箱: admin@yxqi.cn")
        logger.warning(f"密码: {admin_password}")

        User._initializing = True

        admin_user = User(
            email='admin@yxqi.cn',
            nickname='Admin',
            password=Password.hash(admin_password),
            role=UserTypeEnum.super_admin,
            _initializing=True
        )

        await User.add(session, admin_user)

        User._initializing = False
