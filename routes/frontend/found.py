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
from .framework import frame
from tool import format_phone

def create_header(object_data, status):
    """创建卡片标题部分"""
    icon_color = 'red' if status == 'lost' else None
    ui.button(icon=object_data[3], color=icon_color).props('outline round').classes('mx-auto w-auto shadow-sm w-fill max-md:hidden')
    
    title = ui.label('关于此 '+ object_data[2]).classes('text-h5 w-full text-center')
    if status == 'lost':
        with title:
            ui.badge('已被标记为丢失 Already lost', color='red').classes('text-lg -right-10').props('floating')
    
    ui.label('About this '+ object_data[2]).classes('text-xs w-full text-center text-gray-500 -mt-3')

def create_basic_info(object_data):
    """创建基本信息部分"""
    ui.label('序列号(Serial number)：'+ object_data[1]).classes('text-md w-full text-center -mt-1')
    
    # 根据状态决定是否隐藏手机号
    is_private = object_data[4] != 'ok' and object_data[4] != 'lost'
    ui.label('物主(Owner)：'+ format_phone(object_data[5], private=is_private)).classes('text-md w-full text-center -mt-3')
    
    # 丢失时间（如果有）
    if object_data[4] == 'lost' and len(object_data) > 9 and object_data[9]:
        ui.label('丢失时间(Lost time)：'+ object_data[9]).classes('text-md w-full text-center -mt-3')

def create_status_message(object_data, status):
    """根据状态创建提示信息"""
    ui.space()
    
    # 如果是丢失状态且有留言，显示留言
    if status == 'lost' and len(object_data) > 6 and object_data[6]:
        ui.label('物主留言(Owner message)：'+ object_data[6]).classes('text-md w-full text-center')
        ui.space()
    
    messages = {
        'ok': ('此物品尚未标记为丢失状态。如果你意外捡到了此物品，请尽快联系物主。',
               'This item has not been marked as lost. If you accidentally picked it up, please contact the owner as soon as possible.'),
        'lost': ('此物品已被物主标记为丢失。您可以通过上面的电话号码来联系物主。',
                'This item has been marked as lost by the owner. You can contact the owner through the phone number above.'),
        'default': ('此物品状态信息已丢失。如果您捡到了这个物品，请尽快联系物主。如果你是物主，请修改物品信息状态。',
                   'The item status information has been lost. If you have found this item, please contact the owner as soon as possible. If you are the owner, please modify the item status information.')
    }
    
    msg = messages.get(status, messages['default'])
    ui.label(msg[0]).classes('text-md w-full text-center')
    ui.label(msg[1]).classes('text-xs w-full text-center text-gray-500 -mt-3')

def create_contact_button(phone_number):
    """创建联系按钮"""
    if phone_number:
        ui.button('联系物主', 
                on_click=lambda: ui.navigate.to('tel:' + phone_number)) \
            .classes('items-center w-full').props('rounded')

def display_item_card(object_data):
    """显示物品信息卡片"""
    status = object_data[4]
    
    with ui.card().classes('absolute-center w-3/4 h-3/4'):
        # 创建卡片各部分
        create_header(object_data, status)
        create_basic_info(object_data)
        create_status_message(object_data, status)
        
        # 只有状态为'ok'或'lost'时显示联系按钮
        if status in ['ok', 'lost']:
            create_contact_button(object_data[5])

def create() -> None:
    @ui.page('/found')
    async def found_page(request: Request, key: str = "") -> None:
        
        ui.add_head_html(
            '''
            <meta name="robots" content="noindex, nofollow">
            <script type="text/javascript" src="/static/js/main.js"></script>
            '''
        )
        
        await ui.context.client.connected()
        
        async with frame(page='found'):
            if key == "" or key == None:
                ui.navigate.to('/404')
                return
            
            # 加载dialog
            with ui.dialog().props('persistent') as loading, ui.card():
                with ui.row(align_items='center'):
                    ui.spinner(size='lg')
                    with ui.column():
                        ui.label('数据加载中...')
                        ui.label('Loading...').classes('text-xs text-gray-500 -mt-3')
            
            loading.open()

            try:
                object_data = await ui.run_javascript(f'getObject("{key}")')
                
                if object_data['status'] != 'success':
                    ui.navigate.to('/404')
                else:
                    object_data = object_data['data']
                    display_item_card(object_data)
            except Exception as e:
                ui.notify(f'加载失败: {str(e)}', color='negative')
                ui.navigate.to('/404')
            finally:
                loading.close()