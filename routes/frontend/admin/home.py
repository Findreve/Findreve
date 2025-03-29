'''
Author: 于小丘 海枫
Date: 2024-10-02 15:23:34
LastEditors: Yuerchu admin@yuxiaoqiu.cn
LastEditTime: 2024-12-14 20:03:49
FilePath: /Findreve/admin.py
Description: Findreve 后台管理 admin

Copyright (c) 2018-2024 by 于小丘Yuerchu, All Rights Reserved. 
'''

from nicegui import ui
from tool import *
from ..framework import frame


def create():
    @ui.page('/admin')
    async def jump():
        ui.navigate.to('/admin/home')
        
    @ui.page('/admin/home')
    async def admin_home():

        dark_mode = ui.dark_mode(value=True)

        async with frame():
            with ui.tab_panel('main_page'):
                ui.label('首页配置').classes('text-2xl text-bold')
                ui.label('暂不支持，请直接修改main_page.py').classes('text-md text-gray-600').classes('w-full')