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
from fastapi.responses import RedirectResponse
from fastapi import Request

def create() -> Optional[RedirectResponse]:
    @ui.page('/login')
    async def session(request: Request, redirect_to: str = "/"):
        ui.add_head_html("""
            <script>
                async function login(username, password) {
                    const url = '/api/token';
                    const data = new URLSearchParams();
                    data.append('username', username);
                    data.append('password', password);

                try {
                    const response = await fetch(url, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded',
                        },
                        body: data,
                    });

                    if (!response.ok) {
                        throw new Error('Invalid username or password');
                    }

                    const result = await response.json();

                    // 处理登录成功后的数据，返回access_token
                    localStorage.setItem('access_token', result.access_token);

                    return {'status': 'success'};

                } catch (error) {
                    return {'status': 'failed', 'detail': error.message};
                }
            }
            </script>
            """)
        
        ui.page_title('登录 Findreve')
        async def try_login() -> None:
            app.storage.user.update({'authenticated': True})
            # 跳转到用户上一页
            ui.navigate.to(app.storage.user.get('referrer_path', '/'))

        async def login():
            if username.value == "" or password.value == "":
                ui.notify('账号或密码不能为空', color='negative')
                return
            
            try:
                result = await ui.run_javascript(f"login('{username}', '{password}')")
                if result['status'] == 'success':
                    ui.navigate.to(redirect_to)
                else:
                    ui.notify("账号或密码错误", type="negative")
            except Exception as e:
                ui.notify(f"登录失败: {str(e)}", type="negative")
            
        
        with ui.header() \
            .classes('items-center duration-300 py-2 px-5 no-wrap') \
            .style('box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1)'):

            ui.button(icon='menu').props('flat color=white round')
            appBar_appName = ui.button(text="HeyPress").classes('text-lg').props('flat color=white no-caps')

        # 创建一个绝对中心的登录卡片
        with ui.card().classes('absolute-center round-lg').style('width: 70%; max-width: 500px'):
            # 登录标签
            ui.button(icon='lock').props('outline round').classes('mx-auto w-auto shadow-sm w-fill')
            ui.label('登录 Findreve').classes('text-h5 w-full text-center')
            # 用户名/密码框
            username = ui.input('账号').on('keydown.enter', try_login) \
                .classes('block w-full text-gray-900').props('filled')
            password = ui.input('密码', password=True, password_toggle_button=True) \
                .on('keydown.enter', try_login).classes('block w-full text-gray-900').props('filled')
            
            # 按钮布局
            ui.button('登录', on_click=lambda: login()).classes('items-center w-full').props('rounded')
