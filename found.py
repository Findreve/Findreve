'''
Author: 于小丘 海枫
Date: 2024-10-02 15:23:34
LastEditors: Yuerchu admin@yuxiaoqiu.cn
LastEditTime: 2024-11-29 20:03:58
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
    async def found_page(request: Request, key: str = "") -> None:
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

        elif object_data[4] == 'ok':
            # 物品存在, 但未标记为丢失
            with ui.card().classes('absolute-center w-3/4 h-3/4'):

                    # 添加标题
                    ui.button(icon=object_data[3]).props('outline round').classes('mx-auto w-auto shadow-sm w-fill max-md:hidden')
                    ui.label('关于此 '+ object_data[2]).classes('text-h5 w-full text-center')
                    ui.label('About this '+ object_data[2]).classes('text-xs w-full text-center text-gray-500 -mt-3')

                    ui.label('序列号(Serial number)：'+ object_data[1]).classes('text-md w-full text-center')
                
                    ui.label('物主(Owner)：'+ format_phone(object_data[5], private=True)).classes('text-md w-full text-center')
                    
                    ui.space()

                    ui.label('此物品尚未标记为丢失状态。如果你意外捡到了此物品，请尽快联系物主。').classes('text-md w-full text-center')
                    ui.label('This item has not been marked as lost. If you accidentally picked it up, please contact the owner as soon as possible. ').classes('text-xs w-full text-center text-gray-500 -mt-3')

                    
                    ui.button('返回首页', 
                            on_click=lambda: ui.navigate.to('/')) \
                        .classes('items-center w-full').props('rounded')
        
        elif object_data[4] == 'lost':
            # 物品存在, 且标记为丢失
            with ui.card().classes('absolute-center w-3/4 h-3/4'):

                    # 添加标题
                    ui.button(icon=object_data[3], color='red').props('outline round').classes('mx-auto w-auto shadow-sm w-fill max-md:hidden')
                    with ui.label('关于此 '+ object_data[2]).classes('text-h5 w-full text-center'):
                        ui.badge('已被标记为丢失 Already lost', color='red').classes('text-lg -right-10').props('floating')
                    ui.label('About this '+ object_data[2]).classes('text-xs w-full text-center text-gray-500 -mt-3')

                    ui.label('序列号(Serial number)：'+ object_data[1]).classes('text-md w-full text-center -mt-1')
                    
                    ui.label('物主(Owner)：'+ format_phone(object_data[5], private=False)).classes('text-md w-full text-center -mt-3')
                    
                    ui.label('丢失时间(Lost time)：'+ object_data[9]).classes('text-md w-full text-center -mt-3')
                    
                    ui.space()

                    try:
                        ui.label('物主留言(Owner message)：'+ object_data[6]) \
                            .classes('text-md w-full text-center')
                    except: pass

                    ui.space()

                    ui.label('此物品已被物主标记为丢失。您可以通过上面的电话号码来联系物主。').classes('text-md w-full text-center')
                    ui.label('This item has been marked as lost by the owner. You can contact the owner through the phone number above.').classes('text-xs w-full text-center text-gray-500 -mt-3')
                    
                    ui.button('联系物主', 
                            on_click=lambda: ui.navigate.to('tel:' + object_data[5])) \
                        .classes('items-center w-full').props('rounded')
                    
                    await db.update_object(id=object_data[0], find_ip=str(request.client.host))
        
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

                    ui.label('此物品状态信息已丢失。如果您捡到了这个物品，请尽快联系物主。如果你是物主，请修改物品信息状态。').classes('text-md w-full text-center')
                    ui.label('The item status information has been lost. If you have found this item, please contact the owner as soon as possible. If you are the owner, please modify the item status information.').classes('text-xs w-full text-center text-gray-500 -mt-3')

        
        loading.close()
        loading.clear()
        return