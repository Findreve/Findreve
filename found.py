'''
Author: 于小丘 海枫
Date: 2024-10-02 15:23:34
LastEditors: Yuerchu admin@yuxiaoqiu.cn
LastEditTime: 2024-11-29 20:35:19
FilePath: /Findreve/found.py
Description: Findreve 物品详情页 found

Copyright (c) 2018-2024 by 于小丘Yuerchu, All Rights Reserved. 
'''

from nicegui import ui
from fastapi import Request
from model import Database
from tool import format_phone

def create() -> None:
    @ui.page('/found')
    async def found_page(key: str = "") -> None:
        with ui.header() \
            .classes('items-center duration-300 py-2 px-5 no-wrap') \
            .style('box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1)'):

            ui.button(icon='menu').props('flat color=white round')
            ui.button(text="Findreve").classes('text-lg').props('flat color=white no-caps')

        if key == "" or key == None:
            ui.navigate.to('/404')
        
        # 加载dialog
        with ui.dialog().props('persistent') as loading, ui.card():
            with ui.row(align_items='center'):
                ui.spinner(size='lg')
                with ui.column():
                    ui.label('数据加载中...')
                    ui.label('Loading...').classes('text-xs text-gray-500 -mt-3')
        
        loading.open()

        db = Database()
        await db.init_db()
        object_data = await db.get_object(key=key)
        
        if not object_data:
            with ui.card().classes('absolute-center w-3/4 h-2/3'):

                # 添加标题
                ui.button(icon='error', color='red').props('outline round').classes('mx-auto w-auto shadow-sm w-fill max-md:hidden')
                ui.label('物品不存在').classes('text-h5 w-full text-center')
                ui.label('Object not found').classes('text-xs w-full text-center text-gray-500 -mt-3')

                ui.label('请输入正确的序列号').classes('text-md w-full text-center')
                ui.label('Please enter the correct serial number').classes('text-md w-full text-center')
        
        else:
            # 物品存在, 但未标记为丢失
            with ui.card().classes('absolute-center w-3/4 h-3/4'):

                    # 添加标题
                    ui.button(icon=object_data[3]).props('outline round').classes('mx-auto w-auto shadow-sm w-fill max-md:hidden')
                    ui.label('关于此 '+ object_data[2]).classes('text-h5 w-full text-center')
                    ui.label('About this '+ object_data[2]).classes('text-xs w-full text-center text-gray-500 -mt-3')

                    ui.label('序列号(Serial number)：'+ object_data[1]).classes('text-md w-full text-center')
                
                    ui.label('物主(Owner)：'+ format_phone(object_data[5], private=True)).classes('text-md w-full text-center')
                    
                    ui.space()

                    ui.label('如果你意外捡到了此物品，请尽快联系物主。').classes('text-md w-full text-center')
                    ui.label('If you accidentally picked it up, please contact the owner as soon as possible. ').classes('text-xs w-full text-center text-gray-500 -mt-3')

                    
                    ui.button('返回首页', 
                            on_click=lambda: ui.navigate.to('/')) \
                        .classes('items-center w-full').props('rounded')

        
        loading.close()
        loading.clear()
        return

if __name__ not in {"__main__", "__mp_main__"}:
    raise Exception('不支持单测模式，请从main.py启动')