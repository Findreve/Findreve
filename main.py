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
import model.database
import asyncio
asyncio.run(model.database.Database().init_db())
import notfound
from routes.frontend import main_page
from routes.frontend import found
from routes.frontend import login
from routes.frontend.admin import home
from routes.frontend.admin import auth
from routes.frontend.admin import about
from routes.frontend.admin import items
from routes.backend import session
from routes.backend import admin
from routes.backend import object
import model
import logging

notfound.create()
main_page.create()
found.create()
login.create()
home.create()
auth.create()
about.create()
items.create()

app.include_router(admin.Router)
app.include_router(session.Router)
app.include_router(object.Router)

# 添加静态文件目录
try:
    app.add_static_files(url_path='/static', local_directory='static')
except RuntimeError:
    logging.error('无法挂载静态目录')

# 启动函数 Startup function
def startup():
    asyncio.run(model.database.Database().init_db())
    ui.run(
        host='0.0.0.0',
        favicon='🚀',
        port=8080,
        title='Findreve',
        native=False,
        language='zh-CN',
        fastapi_docs=True)

if __name__ in {"__main__", "__mp_main__"}:
    startup()