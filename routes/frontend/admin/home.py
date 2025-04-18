'''
Author: 于小丘 海枫
Date: 2024-10-02 15:23:34
LastEditors: Yuerchu admin@yuxiaoqiu.cn
LastEditTime: 2024-12-14 20:03:49
FilePath: /Findreve/admin.py
Description: Findreve 后台管理 admin

Copyright (c) 2018-2024 by 于小丘Yuerchu, All Rights Reserved. 
'''

from nicegui import ui, app
from fastapi import Request
from fastapi.responses import RedirectResponse
from tool import *
from ..framework import frame


def create():
    @app.get('/admin')
    async def jump():
        return RedirectResponse(url='/admin/home')

    @ui.page('/admin/home')
    async def admin_home(request: Request):
        async with frame(request=request):
            with ui.tab_panel('main_page'):
                ui.label('首页配置').classes('text-2xl text-bold')
                ui.label('暂不支持，请直接修改main_page.py').classes('text-md text-gray-600').classes('w-full')