from fastapi.security import OAuth2PasswordBearer
from model import Setting
from model.database import Database

oauth2_scheme = OAuth2PasswordBearer(
    scheme_name='获取 JWT Bearer 令牌',
    description='用于获取 JWT Bearer 令牌,需要以表单的形式提交',
    tokenUrl="/api/token"
)

ALGORITHM = "HS256"

# 延迟加载 SECRET_KEY
_SECRET_KEY_CACHE = None

async def get_secret_key() -> str:
    """
    获取 JWT 密钥
    
    :return: JWT 密钥字符串
    """
    global _SECRET_KEY_CACHE
    
    if _SECRET_KEY_CACHE is None:
        async with Database.get_session() as session:
            setting = await Setting.get(
                session=session,
                condition=(Setting.name == 'SECRET_KEY')
            )
            if setting:
                _SECRET_KEY_CACHE = setting.value
            else:
                raise RuntimeError("SECRET_KEY not found in database")
    
    return _SECRET_KEY_CACHE