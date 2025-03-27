'''
Author: 于小丘 海枫
Date: 2024-10-02 15:23:34
LastEditors: Yuerchu admin@yuxiaoqiu.cn
LastEditTime: 2024-11-29 20:04:41
FilePath: /Findreve/main.py
Description: Findreve

Copyright (c) 2018-2024 by 于小丘Yuerchu, All Rights Reserved. 
'''

from nicegui import app, ui
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import RedirectResponse, JSONResponse
import traceback

import notfound
import main_page
import found
import login
import admin
import model
import asyncio
import logging

notfound.create()
main_page.create()
found.create()
login.create()
admin.create()

# 中间件配置文件
AUTH_CONFIG = {
    "restricted_routes": {'/admin'},
    "login_url": "/login",
    "cookie_name": "session",
    "session_expire": 3600  # 会话过期时间
}

def is_restricted_route(path: str) -> bool:
    """判断路径是否为需要认证的受限路由"""
    # NiceGUI 路由不受限制
    if path.startswith('/_nicegui'):
        return False

    # 静态资源路径不受限制
    if path.startswith('/static'):
        return False
    
    # 主题路径不受限制
    if path.startswith('/theme'):
        return False
        
    # 后台路径始终受限
    if path.startswith('/admin'):
        return True
        
    # 检查是否为受限的客户端页面路由
    if path.startswith('/dash') or path.startswith('/user'):
        return True
        
class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            if not app.storage.user.get('authenticated', False):
                path = request.url.path
                
                if is_restricted_route(path):
                    logging.warning(f"未认证用户尝试访问: {path}")
                    return RedirectResponse(f'/login?redirect_to={path}')
                    
            return await call_next(request)
        except Exception as e:
            logging.error(f"服务器错误 Server error: {str(traceback.format_exc())}")
            return JSONResponse(status_code=500, content={"detail": e})

# 添加中间件 Add middleware
app.add_middleware(AuthMiddleware)

# 添加静态文件目录
try:
    app.add_static_files(url_path='/static', local_directory='static')
except RuntimeError:
    logging.error('无法挂载静态目录')

# 启动函数 Startup function
def startup():
    asyncio.run(model.Database().init_db())
    ui.run(
        host='0.0.0.0',
        favicon='🚀',
        port=8080,
        title='Findreve',
        native=False,
        storage_secret='findreve',
        language='zh-CN',
        fastapi_docs=False)

if __name__ in {"__main__", "__mp_main__"}:
    startup()