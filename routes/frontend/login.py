'''
Author: 于小丘 海枫
Date: 2024-10-02 15:23:34
LastEditors: Yuerchu admin@yuxiaoqiu.cn
LastEditTime: 2024-11-29 20:29:26
FilePath: /Findreve/login.py
Description: Findreve 登录界面 Login

Copyright (c) 2018-2024 by 于小丘Yuerchu, All Rights Reserved. 
'''

from nicegui import ui
from typing import Optional
from fastapi.responses import RedirectResponse
from fastapi import Request
from .framework import frame

def create() -> Optional[RedirectResponse]:
    @ui.page('/login')
    async def session(redirect_to: str = "/"):
        ui.add_head_html("""
            <script type="text/javascript" src="/static/js/main.js"></script>
            """)
        
        ui.page_title('登录 Findreve')
        ui.dark_mode(True)
        
        async with frame(page='session'):
            async def login():
                if username.value == "" or password.value == "":
                    ui.notify('账号或密码不能为空', color='negative')
                    return
                
                try:
                    result = await ui.run_javascript(f"login('{username.value}', '{password.value}')")
                    if result['status'] == 'success':
                        ui.navigate.to(redirect_to)
                    else:
                        ui.notify(f"登录失败: {result['detail']}", type="negative")
                except Exception as e:
                    ui.notify(f"登录失败: {str(e)}", type="negative")

            # 创建一个绝对中心的登录卡片
            with ui.card().classes('absolute-center round-lg').style('width: 70%; max-width: 500px'):
                # 登录标签
                ui.button(icon='lock').props('outline round').classes('mx-auto w-auto shadow-sm w-fill')
                ui.label('登录 Findreve').classes('text-h5 w-full text-center')
                # 用户名/密码框
                username = ui.input('账号').on('keydown.enter', login) \
                    .classes('block w-full text-gray-900').props('filled')
                password = ui.input('密码', password=True, password_toggle_button=True) \
                    .on('keydown.enter', login).classes('block w-full text-gray-900').props('filled')
                
                # 按钮布局
                ui.button('登录', on_click=lambda: login()).classes('items-center w-full').props('rounded')
