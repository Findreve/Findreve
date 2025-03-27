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
from typing import Dict
import model
import qrcode
import base64
from io import BytesIO
from fastapi import Request
from tool import *
from datetime import datetime


def create():
    @ui.page('/admin')
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
                ui.button(text="Findreve 仪表盘").classes('text-lg').props('flat color=white no-caps')
        
        siteDomain = request.base_url.hostname
        with ui.left_drawer() as left_drawer:
            with ui.column().classes('w-full'):
                ui.image('/static/Findreve.png').classes('w-1/2 mx-auto')
            with ui.row(align_items='center').classes('w-full'):
                ui.label('Findreve').classes('text-2xl text-bold')
            if siteDomain == "127.0.0.1" or siteDomain == "localhost":
                ui.label("本地模式无需授权").classes('text-gray-600 -mt-3')
            else:
                ui.label("免费版，无需授权").classes('text-red-600 -mt-3')

            ui.button('首页 & 信息', icon='fingerprint', on_click=lambda: tabs.set_value('main_page')) \
                .classes('w-full').props('flat no-caps')
            ui.button('物品 & 库存', icon='settings', on_click=lambda: tabs.set_value('item')) \
                .classes('w-full').props('flat no-caps')
            ui.button('产品 & 授权', icon='settings', on_click=lambda: tabs.set_value('auth')) \
                .classes('w-full').props('flat no-caps')
            ui.button('关于 & 反馈', icon='settings', on_click=lambda: tabs.set_value('about')) \
                .classes('w-full').props('flat no-caps')
        
        with ui.tab_panels(tabs, value='main_page').classes('w-full').props('vertical'):
                # 站点一览
                with ui.tab_panel('main_page'):
                    ui.label('首页配置').classes('text-2xl text-bold')
                    ui.label('暂不支持，请直接修改main_page.py').classes('text-md text-gray-600').classes('w-full')

                # 物品一览
                with ui.tab_panel('item'):

                    # 列表选择函数
                    async def objectTableOnClick():
                        try:
                            status = str(object_table.selected[0]['status'])
                        except:
                            # 当物品列表未选中，显示添加物品按钮，其他按钮不显示
                            addObjectFAB.set_visibility(True)
                            lostObjectFAB.set_visibility(False)
                            findObjectFAB.set_visibility(False)
                            return
                        
                        if status == "正常":
                            # 选中正常物品，显示丢失按钮
                            addObjectFAB.set_visibility(False)
                            lostObjectFAB.set_visibility(True)
                            findObjectFAB.set_visibility(False)
                        elif status == "丢失":
                            # 选中丢失物品，显示发现按钮
                            addObjectFAB.set_visibility(False)
                            lostObjectFAB.set_visibility(False)
                            findObjectFAB.set_visibility(True)
                        else:
                            # 选中其他状态，隐藏所有按钮
                            addObjectFAB.set_visibility(False)
                            lostObjectFAB.set_visibility(False)
                            findObjectFAB.set_visibility(False)

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
                    
                    async def lostObject():
                        try:
                            # 获取选中物品
                            object_id = object_table.selected[0]['id']
                            await model.Database().update_object(id=object_id, status='lost')
                            await model.Database().update_object(id=object_id, lost_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                            # 如果设置了留言，则更新留言
                            if lostReason.value != "":
                                await model.Database().update_object(id=object_id, context=lostReason.value)
                        except Exception as e:
                            ui.notify(str(e), color='negative')
                        else:
                            ui.notify('设置丢失成功', color='positive')
                            # 刷新表格
                            await reloadTable(tips=False)
                            lostObjectDialog.close()
                            # 将FAB设置为正常
                            addObjectFAB.set_visibility(True)
                            lostObjectFAB.set_visibility(False)
                            findObjectFAB.set_visibility(False)


                    # 设置物品丢失对话框
                    with ui.dialog() as lostObjectDialog, ui.card().style('width: 90%; max-width: 500px'):
                        ui.button(icon='gpp_bad', color='red').props('outline round').classes('mx-auto w-auto shadow-sm w-fill')
                        ui.label('设置物品丢失').classes('w-full text-h5 text-center')
                        
                        ui.label('确定要设置这个物品为丢失吗？')
                        ui.html('设置为丢失以后，<b>你的电话号码将会被完整地显示在物品页面</b>(不是“*** **** 8888”而是“188 8888 8888”)，以供拾到者能够记下你的电话号码。此外，在页面底部将会显示一个按钮，这个按钮能够一键拨打预先设置好的电话。')
                        lostReason = ui.input('物主留言') \
                            .classes('block w-full text-gray-900')
                        lostReasonTips = ui.label('非必填，但建议填写，以方便拾到者联系你').classes('-mt-3')

                        async def handle_lost_object():
                            await lostObject()

                        ui.button("确认提交", color='red', on_click=handle_lost_object) \
                            .classes('items-center w-full').props('rounded')
                        ui.button("返回", on_click=lostObjectDialog.close) \
                            .classes('w-full').props('flat rounded')
                    
                    async def findObject():
                        try:
                            object_id = object_table.selected[0]['id']
                            await model.Database().update_object(id=object_id, status='ok')
                            await model.Database().update_object(id=object_id, context=None)
                            await model.Database().update_object(id=object_id, find_ip=None)
                            await model.Database().update_object(id=object_id, lost_at=None)
                        except Exception as e:
                            ui.notify(str(e), color='negative')
                        else:
                            ui.notify('解除丢失成功', color='positive')
                            # 刷新表格
                            await reloadTable(tips=False)
                            findObjectDialog.close()
                            # 将FAB设置为正常
                            addObjectFAB.set_visibility(True)
                            lostObjectFAB.set_visibility(False)
                            findObjectFAB.set_visibility(False)

                    # 解除丢失对话框
                    with ui.dialog() as findObjectDialog, ui.card().style('width: 90%; max-width: 500px'):
                        ui.button(icon='remove_moderator').props('outline round').classes('mx-auto w-auto shadow-sm w-fill')
                        ui.label('解除丢失').classes('w-full text-h5 text-center')
                        
                        ui.label('确定物品已经找回了吗？')

                        async def handle_find_object():
                            await findObject()

                        ui.button("确认提交", on_click=handle_find_object) \
                            .classes('items-center w-full').props('rounded')
                        ui.button("返回") \
                            .classes('w-full').props('flat rounded')
                    
                    async def fetch_and_process_objects():
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
                        return objects

                    async def reloadTable(tips: bool = True):
                        objects = await fetch_and_process_objects()
                        object_table.update_rows(objects)
                        if tips:
                            ui.notify('刷新成功')

                    object_columns = [
                        {'name': 'id', 'label': '内部ID', 'field': 'id', 'required': True, 'align': 'left'},
                        {'name': 'key', 'label': '物品Key', 'field': 'key', 'required': True, 'align': 'left'},
                        {'name': 'name', 'label': '物品名称', 'field': 'name', 'required': True, 'align': 'left'},
                        {'name': 'icon', 'label': '物品图标', 'field': 'icon', 'required': True, 'align': 'left'},
                        {'name': 'status', 'label': '物品状态', 'field': 'status', 'required': True, 'align': 'left'},
                        {'name': 'phone', 'label': '物品绑定手机', 'field': 'phone', 'required': True, 'align': 'left'},
                        {'name': 'context', 'label': '丢失描述', 'field': 'context', 'required': True, 'align': 'left'},
                        {'name': 'find_ip', 'label': '物品发现IP', 'field': 'find_ip', 'required': True, 'align': 'left'},
                        {'name': 'create_at', 'label': '物品创建时间', 'field': 'create_at', 'required': True, 'align': 'left'},
                        {'name': 'lost_at', 'label': '物品丢失时间', 'field': 'lost_at', 'required': True, 'align': 'left'}
                    ]

                    objects = await fetch_and_process_objects()
                    object_table = ui.table(
                        title='物品 & 库存',
                        row_key='id',
                        pagination=10,
                        selection='single',
                        columns=object_columns,
                        rows=objects,
                        on_select=lambda: objectTableOnClick()
                    ).classes('w-full').props('flat')

                    object_table.add_slot('body-cell-status', '''
                        <q-td key="status" :props="props">
                            <q-badge :color="props.value === '正常' ? 'green' : 'red'">
                                {{ props.value }}
                            </q-badge>
                        </q-td>
                    ''')


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
                    with ui.page_sticky(x_offset=24, y_offset=24) as lostObjectFAB:
                        ui.button(icon='gpp_bad', color='red', on_click=lostObjectDialog.open) \
                            .props('fab')
                        # 单独拉出来默认隐藏，防止无法再设置其显示
                    lostObjectFAB.set_visibility(False)
                    with ui.page_sticky(x_offset=24, y_offset=24) as findObjectFAB:
                        ui.button(icon='remove_moderator', on_click=findObjectDialog.open) \
                            .props('fab')
                        # 单独拉出来默认隐藏，防止无法再设置其显示
                    findObjectFAB.set_visibility(False)
                
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
                    ui.label('关于 Findreve')
