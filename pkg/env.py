"""
环境变量管理模块

负责 .env 文件的创建和环境变量的加载
"""

import os
from dotenv import load_dotenv
from typing import Tuple


def ensure_env_file(env_file_path: str = '.env') -> None:
    """
    确保 .env 文件存在，如果不存在则创建默认配置
    
    :param env_file_path: .env 文件路径
    """
    if not os.path.exists(env_file_path):
        default_env_content = """HOST=127.0.0.1
PORT=8167

DEBUG=false

DATABASE_URL=sqlite+aiosqlite:///data.db
"""
        with open(env_file_path, 'w', encoding='utf-8') as f:
            f.write(default_env_content)
        print(f"Created default .env file at {env_file_path}")


def load_config() -> Tuple[str, int, bool]:
    """
    加载配置信息
    
    :return: (host, port, debug) 元组
    """
    # 确保 .env 文件存在
    ensure_env_file()
    
    # 从.env文件加载环境变量
    load_dotenv('.env')
    
    # 从环境变量中加载主机、端口、调试模式等配置
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", 8167))
    debug = os.getenv("DEBUG", "false").lower() in ("true", "1", "yes")
    
    return host, port, debug
