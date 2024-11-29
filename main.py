'''
Author: 于小丘 海枫
Date: 2024-10-02 15:23:34
LastEditors: Yuerchu admin@yuxiaoqiu.cn
LastEditTime: 2024-11-29 20:04:41
FilePath: /Findreve/main.py
Description: Findreve

Copyright (c) 2018-2024 by 于小丘Yuerchu, All Rights Reserved. 
'''

from nicegui import app, ui, Client
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import RedirectResponse, JSONResponse
import hashlib
import inspect

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

# 登录验证中间件 Login verification middleware
class AuthMiddleware(BaseHTTPMiddleware):
    # 异步处理每个请求
    async def dispatch(self, request: Request, call_next):
        try:
            logging.info(f"访问路径: {request.url.path},"
                         f"认证状态: {app.storage.user.get('authenticated')}")
            if not app.storage.user.get('authenticated', False):
                # 如果请求的路径在Client.page_routes.values()中，并且不在unrestricted_page_routes中
                if request.url.path in Client.page_routes.values() \
                and request.url.path in AUTH_CONFIG["restricted_routes"]:
                    logging.warning(f"未认证用户尝试访问: {request.url.path}")
                    # 记录用户想访问的路径 Record the user's intended path
                    app.storage.user['referrer_path'] = request.url.path
                    # 重定向到登录页面 Redirect to the login page
                    return RedirectResponse(AUTH_CONFIG["login_url"])
            # 否则，继续处理请求 Otherwise, continue processing the request
            return await call_next(request)

        except Exception as e:
            # 记录错误日志
            logging.error(f"认证中间件错误: {str(e)}")
            # 返回适当的错误响应
            return JSONResponse(
                status_code=500,
                content={"detail": "服务器内部错误"}
            )

# 添加中间件 Add middleware
app.add_middleware(AuthMiddleware)

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