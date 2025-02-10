'''
Author: 于小丘 海枫
Date: 2024-10-02 15:23:34
LastEditors: Yuerchu admin@yuxiaoqiu.cn
LastEditTime: 2024-11-29 20:05:13
FilePath: /Findreve/notfound.py
Description: Findreve 404

Copyright (c) 2018-2024 by 于小丘Yuerchu, All Rights Reserved. 
'''

from nicegui import ui
from fastapi import Request

def create() -> None:
    @ui.page('/404')
    async def not_found_page(request: Request, ref="") -> None:
        with ui.header() \
            .classes('items-center duration-300 py-2 px-5 no-wrap') \
            .style('box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1)'):

            ui.button(icon='menu').props('flat color=white round')
            ui.button(text="HeyPress").classes('text-lg').props('flat color=white no-caps')
        
        with ui.card().classes('absolute-center w-3/4 h-2/3'):

                # 添加标题
                ui.button(icon='error', color='red').props('outline round').classes('mx-auto w-auto shadow-sm w-fill')
                ui.label('404').classes('text-h3 w-full text-center')

                ui.space()

                ui.label('页面不存在').classes('text-2xl w-full text-center')
                ui.label('Page Not Found').classes('text-2xl w-full text-center')
                
                ui.space()
                
                ui.button('返回首页', 
                          on_click=lambda: ui.navigate.to('/')) \
                    .classes('items-center w-full').props('rounded')
