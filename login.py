'''
Author: 于小丘 海枫
Date: 2024-10-02 15:23:34
LastEditors: Yuerchu admin@yuxiaoqiu.cn
LastEditTime: 2024-11-29 20:29:26
FilePath: /Findreve/login.py
Description: Findreve 登录界面 Login

Copyright (c) 2018-2024 by 于小丘Yuerchu, All Rights Reserved. 
'''

from nicegui import ui, app
from typing import Optional
import traceback
import asyncio
import model
import tool
from fastapi.responses import RedirectResponse

def create() -> Optional[RedirectResponse]:
    @ui.page('/login')
    async def session():
        # 检测是否已登录
        if app.storage.user.get('authenticated', False):
            return ui.navigate.to('/admin')
        
        ui.page_title('登录 Findreve')
        async def try_login() -> None:
            app.storage.user.update({'authenticated': True})
            # 跳转到用户上一页
            ui.navigate.to(app.storage.user.get('referrer_path', '/'))

        async def login():
            if username.value == "" or password.value == "":
                ui.notify('账号或密码不能为空', color='negative')
                return
            
            # 验证账号和密码
            account = await model.Database().get_setting('account')
            stored_password = await model.Database().get_setting('password')

            if account != username.value or not tool.verify_password(stored_password, password.value, debug=True):
                ui.notify('账号或密码错误', color='negative')
                return
            
            # 存储用户信息
            app.storage.user.update({'authenticated': True})
            # 跳转到用户上一页
            ui.navigate.to(app.storage.user.get('referrer_path', '/'))
            
        
        with ui.header() \
            .classes('items-center duration-300 py-2 px-5 no-wrap') \
            .style('box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1)'):

            ui.button(icon='menu').props('flat color=white round')
            appBar_appName = ui.button(text="HeyPress" if not unitTest else 'HeyPress 单测模式').classes('text-lg').props('flat color=white no-caps')

        # 创建一个绝对中心的登录卡片
        with ui.card().classes('absolute-center round-lg').style('width: 70%; max-width: 500px'):
            # 登录标签
            ui.button(icon='lock').props('outline round').classes('mx-auto w-auto shadow-sm w-fill')
            ui.label('登录 HeyPress').classes('text-h5 w-full text-center')
            # 用户名/密码框
            username = ui.input('账号').on('keydown.enter', try_login) \
                .classes('block w-full text-gray-900').props('rounded outlined')
            password = ui.input('密码', password=True, password_toggle_button=True) \
                .on('keydown.enter', try_login).classes('block w-full text-gray-900').props('rounded outlined')
            
            # 按钮布局
            ui.button('登录', on_click=lambda: login()).classes('items-center w-full').props('rounded')


if __name__ not in {"__main__", "__mp_main__"}:
    raise Exception('不支持单测模式，请从main.py启动')