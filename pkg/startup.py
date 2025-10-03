"""
应用启动模块

负责应用启动时的初始化工作
"""

import asyncio
from loguru import logger
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from model.database import Database


async def init_database() -> None:
    """
    初始化数据库
    """
    await Database().init_db()


def mount_static_files(app: FastAPI) -> None:
    """
    挂载静态文件目录
    
    :param app: FastAPI 应用实例
    """
    try:
        app.mount("/dist", StaticFiles(directory="dist"), name="dist")
    except RuntimeError as e:
        logger.warning(f'Unable to mount static directory: {str(e)}, starting in backend-only mode')


def startup(app: FastAPI) -> None:
    """
    执行应用启动流程
    
    :param app: FastAPI 应用实例
    """
    # 初始化数据库
    asyncio.run(init_database())
    
    # 挂载静态文件
    mount_static_files(app)
