'''
Author: 于小丘 海枫
Date: 2024-10-02 15:23:34
LastEditors: Yuerchu admin@yuxiaoqiu.cn
LastEditTime: 2024-11-29 20:43:28
FilePath: /Findreve/admin.py
Description: Findreve 后台管理 admin

Copyright (c) 2018-2024 by 于小丘Yuerchu, All Rights Reserved. 
'''

from nicegui import ui, app
from typing import Optional
from typing import Dict
import model
import qrcode
import base64
from io import BytesIO
from fastapi import Request
from tool import *


def create(unitTest: bool = False):
    @ui.page('/admin' if not unitTest else '/')
    async def admin(request: Request):

        dark_mode = ui.dark_mode(value=True)

        # 表格列的显示隐藏开关
        def tableToggle(column: Dict, visible: bool, table) -> None:
            column['classes'] = '' if visible else 'hidden'
            column['headerClasses'] = '' if visible else 'hidden'
            table.update()

        with ui.header() \
        .classes('items-center duration-300 py-2 px-5 no-wrap') \
        .style('box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1)'):
            with ui.tabs(value='main_page') as tabs:
                ui.button(icon='menu', on_click=lambda: left_drawer.toggle()).props('flat color=white round')
                ui.button(text="Findreve 仪表盘" if not unitTest else 'Findreve 仪表盘 单测模式').classes('text-lg').props('flat color=white no-caps')
        
        with ui.left_drawer() as left_drawer:
            ui.image('https://bing.img.run/1366x768.php').classes('w-full')
            with ui.row(align_items='center').classes('w-full'):
                ui.label('Findreve').classes('text-2xl text-bold')
                ui.chip('Pro').classes('text-xs -left-3').props('floating outline')
            ui.label("本地模式无需授权").classes('text-gray-600 -mt-3')

            ui.button('物品 & 库存', icon='settings', on_click=lambda: tabs.set_value('item')) \
                .classes('w-full').props('flat no-caps')
            ui.button('产品 & 授权', icon='settings', on_click=lambda: tabs.set_value('auth')) \
                .classes('w-full').props('flat no-caps')
            ui.button('关于 & 反馈', icon='settings', on_click=lambda: tabs.set_value('about')) \
                .classes('w-full').props('flat no-caps')
        
        with ui.tab_panels(tabs, value='item').classes('w-full').props('vertical'):

                # 物品一览
                with ui.tab_panel('item'):
                    
                    # 添加物品
                    async def addObject():
                        dialogAddObjectIcon.disable()
                        if object_name.value == "" or object_icon == "" or object_phone == "":
                            ui.notify('必填字段不能为空', color='negative')
                            dialogAddObjectIcon.enable()
                            return
                        
                        if not object_phone.validate():
                            ui.notify('号码输入有误，请检查！', color='negative')
                            dialogAddObjectIcon.enable()
                            return
                        
                        if object_key.value == "":
                            object_key.set_value(generate_password())
                        
                        try:
                            await model.Database().add_object(key=object_key.value, name=object_name.value, icon=object_icon.value, phone=object_phone.value)
                        except ValueError as e:
                            ui.notify(str(e), color='negative')
                        else:
                            await reloadTable(tips=False)
                            with ui.dialog() as addObjectSuccessDialog, ui.card().style('width: 90%; max-width: 500px'):
                                ui.button(icon='done').props('outline round').classes('mx-auto w-auto shadow-sm w-fill')
                                ui.label('添加成功').classes('w-full text-h5 text-center')

                                ui.label('你可以使用下面的链接来访问这个物品')
                                ui.code(request.base_url.hostname+ '/found?key=' + object_key.value).classes('w-full')
                                
                                # 生成二维码
                                qr_data = request.base_url.hostname + '/found?key=' + object_key.value
                                qr = qrcode.QRCode(
                                    version=1,
                                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                                    box_size=10,
                                    border=4,
                                )
                                qr.add_data(qr_data)
                                qr.make(fit=True)
                                img = qr.make_image(fill='black', back_color='white')

                                # 将二维码转换为Base64
                                buffered = BytesIO()
                                img.save(buffered, format="PNG")
                                img_str = base64.b64encode(buffered.getvalue()).decode()

                                # 展示二维码
                                ui.image(f'data:image/png;base64,{img_str}')
                                
                                # 添加下载二维码按钮
                                ui.button("下载二维码", on_click=lambda: ui.download(buffered.getvalue(), 'qrcode.png')) \
                                    .classes('w-full').props('flat rounded')

                                ui.button("返回", on_click=lambda: (addObjectDialog.close(), addObjectSuccessDialog.close(), addObjectSuccessDialog.delete())) \
                                        .classes('w-full').props('flat rounded')
                            
                            addObjectSuccessDialog.open()

                        

                    # 添加物品对话框
                    with ui.dialog() as addObjectDialog, ui.card().style('width: 90%; max-width: 500px'):
                        ui.button(icon='add_circle').props('outline round').classes('mx-auto w-auto shadow-sm w-fill')
                        ui.label('添加物品').classes('w-full text-h5 text-center')

                        with ui.scroll_area().classes('w-full'):
                            object_name = ui.input('物品名称').classes('w-full')
                            object_name_tips = ui.label('显示的物品名称').classes('-mt-3')
                            with ui.row(align_items='center').classes('w-full'):
                                with ui.column().classes('w-1/2 flex-grow'):
                                    object_icon = ui.input('物品图标').classes('w-full')
                                    with ui.row(align_items='center').classes('-mt-3'):
                                        ui.label('将在右侧实时预览图标')
                                        object_icon_link = ui.link('图标列表', 'https://fonts.google.com/icons?icon.set=Material+Icons')
                                object_icon_preview = ui.icon('').classes('text-2xl flex-grow').bind_name_from(object_icon, 'value')
                            object_phone = ui.input('物品绑定手机号', validation={'请输入中国大陆格式的11位手机号': lambda value: len(value) == 11 and value.isdigit()}).classes('w-full')
                            object_phone_tips = ui.label('目前仅支持中国大陆格式的11位手机号').classes('-mt-3')
                            object_key = ui.input('物品Key(可选，不填自动生成)').classes('w-full')
                            object_key_tips = ui.label('物品Key为物品的唯一标识，可用于物品找回').classes('-mt-3')
                
                        async def handle_add_object():
                            await addObject()
                        
                        dialogAddObjectIcon = ui.button("添加并生成二维码", icon='qr_code', on_click=handle_add_object) \
                                .classes('items-center w-full').props('rounded')
                        ui.button("返回", on_click=addObjectDialog.close) \
                                .classes('w-full').props('flat rounded')
                    
                    async def reloadTable(tips: bool = True):
                        # 获取所有物品
                        objects = [dict(zip(['id', 'key', 'name', 'icon', 'status', 'phone', 'context',
                                            'find_ip', 'create_at', 'lost_at'], obj)) for obj in await model.Database().get_object()]
                        status_map = {'ok': '正常', 'lost': '丢失'}
                        for obj in objects:
                            obj['status'] = status_map.get(obj['status'], obj['status'])
                            if obj['create_at']:
                                obj['create_at'] = format_time_diff(obj['create_at'])
                            if obj['lost_at']:
                                obj['lost_at'] = format_time_diff(obj['lost_at'])
                        object_table.update_rows(objects)
                        if tips:
                            ui.notify('刷新成功')

                    # 获取所有物品
                    objects = [dict(zip(['id', 'key', 'name', 'icon', 'status', 'phone', 'context',
                                         'find_ip', 'create_at', 'lost_at'], obj)) for obj in await model.Database().get_object()]
                    status_map = {'ok': '正常', 'lost': '丢失'}
                    for obj in objects:
                        obj['status'] = status_map.get(obj['status'], obj['status'])
                        if obj['create_at']:
                            obj['create_at'] = format_time_diff(obj['create_at'])
                        if obj['lost_at']:
                            obj['lost_at'] = format_time_diff(obj['lost_at'])
                    object_columns=[
                            {'name': 'id', 'label': '内部ID', 'field': 'id', 'required': True, 'align': 'left'},
                            {'name': 'key', 'label': '物品Key', 'field': 'key', 'required': True, 'align': 'left'},
                            {'name': 'name', 'label': '物品名称', 'field': 'name', 'required': True, 'align': 'left'},
                            {'name': 'icon', 'label': '物品图标', 'field': 'icon', 'required': True, 'align': 'left'},
                            {'name': 'phone', 'label': '物品绑定手机', 'field': 'phone', 'required': True, 'align': 'left'},
                            {'name': 'create_at', 'label': '物品创建时间', 'field': 'create_at', 'required': True, 'align': 'left'}
                            ]
                    object_table = ui.table(
                        title='物品 & 库存',
                        row_key='id',
                        pagination=10,
                        selection='single',
                        columns=object_columns,
                        rows=objects
                    ).classes('w-full').props('flat')


                    with object_table.add_slot('top-right'):

                        ui.input('搜索物品').classes('px-2') \
                            .bind_value(object_table, 'filter') \
                            .props('rounded outlined dense clearable')

                        ui.button(icon='refresh', on_click=lambda: reloadTable()).classes('px-2').props('flat fab-mini')

                        with ui.button(icon='menu').classes('px-2').props('flat fab-mini'):
                            with ui.menu(), ui.column().classes('gap-0 p-4'):
                                for column in object_columns:
                                    ui.switch(column['label'], value=True, on_change=lambda e,
                                            column=column: tableToggle(column=column, visible=e.value, table=object_table))
                    # FAB按钮
                    with ui.page_sticky(x_offset=24, y_offset=24) as addObjectFAB:
                        ui.button(icon='add', on_click=addObjectDialog.open) \
                            .props('fab')
                
                # Findreve 授权
                with ui.tab_panel('auth'):

                    ui.label('Findreve 授权').classes('text-2xl text-bold')
                    
                    with ui.element('div').classes('p-2 bg-orange-100 w-full'):
                        with ui.row(align_items='center'):
                            ui.icon('favorite').classes('text-rose-500 text-2xl')
                            ui.label('感谢您使用 Findreve').classes('text-rose-500 text-bold')
                        with ui.column():
                            ui.markdown('> 使用付费版本请在下方进行授权验证'
                                        '<br>'
                                        'Findreve 是一款良心、厚道的好产品！创作不易，支持正版，从我做起！'
                                        '<br>'
                                        '如需在生产环境部署请前往 `auth.yxqi.cn` 购买正版'
                                        ).classes('text-rose-500')
                            ui.markdown('- Findreve 官网：[https://auth.yxqi.cn](https://auth.yxqi.cn)\n'
                                        '- 作者联系方式：QQ 2372526808\n'
                                        '- 管理我的授权：[https://auth.yxqi.cn/product/5](https://auth.yxqi.cn/product/5)\n'
                                        ).classes('text-rose-500')
                    ui.label('您正在使用免费版本，无需授权可体验完整版Findreve。').classes('text-bold')
                
                # 关于 Findreve
                with ui.tab_panel('about'):
                    ui.label('关于 Findreve').classes('text-2xl text-bold')

                    ui.label('还在做')

if __name__ in {"__main__", "__mp_main__"}:
    create(unitTest=True)
    ui.run(
        host='0.0.0.0',
        favicon='🚀',
        port=8080,
        title='Findreve',
        native=False,
        storage_secret='findreve',
        language='zh-CN',
        fastapi_docs=False)