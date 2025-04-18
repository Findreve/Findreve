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
from fastapi import Request
from tool import *
from ..framework import frame


def create():
    @ui.page('/admin/about')
    async def admin_about(request: Request):
        ui.add_head_html("""
            <style type="text/css" src="/static/css/about.css"></style>
            <script type="text/javascript" src="/static/js/main.js"></script>
            """)
        
        async with frame(request=request):
            
            # 关于 Findreve
            with ui.tab_panel('about'):
                ui.label('关于 Findreve').classes('text-2xl font-bold')
                about = ui.markdown('''加载中...''')
            
            try:
                # 延长超时时间到10秒
                about_text = await ui.run_javascript('get_about()', timeout=10.0)
                if isinstance(about_text, dict) and 'status' in about_text and about_text['status'] == 'failed':
                    about.set_content(f'加载失败: {about_text.get("detail", "未知错误")}')
                else:
                    about.set_content(about_text)
            except Exception as e:
                ui.notify(f'加载失败: {str(e)}', color='negative')
                about.set_content(f'### 无法加载内容\n\n出现错误: {str(e)}')
                