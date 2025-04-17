'''
Author: 于小丘 海枫
Date: 2024-10-02 15:23:34
LastEditors: Yuerchu admin@yuxiaoqiu.cn
LastEditTime: 2024-12-14 20:03:49
FilePath: /Findreve/admin.py
Description: Findreve 后台管理 admin

Copyright (c) 2018-2024 by 于小丘Yuerchu, All Rights Reserved. 
'''

import asyncio
from nicegui import ui
from typing import Dict
import qrcode
import base64
import json
from io import BytesIO
from fastapi import Request
from tool import *
from ..framework import frame, loding_process


def create():      
    @ui.page('/admin/items')
    async def admin_items(request: Request):
        
        ui.add_head_html("""
            <script type="text/javascript" src="/static/js/main.js"></script>
            """)

        dark_mode = ui.dark_mode(value=True)

        async with frame():
            # 表格列的显示隐藏开关
            def tableToggle(column: Dict, visible: bool, table) -> None:
                column['classes'] = '' if visible else 'hidden'
                column['headerClasses'] = '' if visible else 'hidden'
                table.update()

            # 列表选择函数
            async def objectTableOnSelect():
                try:
                    status = str(object_table.selected[0]['status'])
                except:
                    status = None
                # 刷新FAB按钮状态
                if status:
                    # 选中正常物品，显示编辑按钮
                    addObjectFAB.set_visibility(False)
                    editObjectFAB.set_visibility(True)
                else:
                    addObjectFAB.set_visibility(True)
                    editObjectFAB.set_visibility(False)
                    
                try:
                    # 预填充编辑表单
                    if object_table.selected:
                        selected_item = object_table.selected[0]
                        edit_object_name.set_value(selected_item.get('name', ''))
                        edit_object_icon.set_value(selected_item.get('icon', ''))
                        edit_object_phone.set_value(selected_item.get('phone', ''))
                        edit_object_key.set_value(selected_item.get('key', ''))
                        # 设置丢失状态开关
                        edit_set_object_lost.set_value(selected_item.get('status') == '丢失')
                        # 设置物主留言
                        lostReason.set_value(selected_item.get('lost_description', ''))
                except:
                    # 当物品列表未选中，显示添加物品按钮，其他按钮不显示
                    addObjectFAB.set_visibility(True)
                    return

            # 添加物品
            async def addObject():
                dialogAddObjectIcon.disable()
                
                async def on_success():
                    await reloadTable(tips=False)
                    
                    # 清空输入框
                    object_name.set_value('')
                    object_icon.set_value('')
                    object_phone.set_value('')
                    object_key.set_value('')
                    
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
                        with ui.row(align_items='center').classes('w-full'):
                            ui.space()
                            ui.image(f'data:image/png;base64,{img_str}').classes('w-1/3')
                            ui.space()
                        
                        with ui.row(align_items='center').classes('w-full'):
                            ui.space()
                            
                            ui.button("下载二维码", on_click=lambda: ui.download(buffered.getvalue(), 'qrcode.png')) \
                                .props('flat rounded')

                            ui.button("返回", on_click=lambda: (addObjectDialog.close(), addObjectSuccessDialog.close(), addObjectSuccessDialog.delete())) \
                                    .props('flat rounded')
                    
                    addObjectSuccessDialog.open()
                
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
                
                async with loding_process(
                    success_content='添加成功',
                    on_success=on_success,
                    on_finally=dialogAddObjectIcon.enable()
                ):
                    # 正确序列化字符串参数
                    key = json.dumps(object_key.value)
                    name = json.dumps(object_name.value)
                    icon = json.dumps(object_icon.value)
                    phone = json.dumps(object_phone.value)
                    
                    result = await ui.run_javascript(
                        f'addItems({key}, {name}, {icon}, {phone})'
                    )
                    
                    if result.get('status') == 'failed':
                        raise Exception(f"添加失败: {result.get('detail', '未知错误')}")

            # 添加物品对话框
            with ui.dialog() as addObjectDialog, ui.card().style('width: 90%; max-width: 500px'):
                ui.button(icon='add_circle').props('outline round').classes('mx-auto w-auto shadow-sm w-fill')
                ui.label('添加物品').classes('w-full text-h5 text-center')

                with ui.scroll_area().classes('w-full'):
                    object_name = ui.input('物品名称').classes('w-full')
                    ui.label('显示的物品名称').classes('-mt-3')
                    with ui.row(align_items='center').classes('w-full'):
                        with ui.column().classes('w-1/2 flex-grow'):
                            object_icon = ui.input('物品图标').classes('w-full')
                            with ui.row(align_items='center').classes('-mt-3'):
                                ui.label('将在右侧实时预览图标')
                                ui.link('图标列表', 'https://fonts.google.com/icons?icon.set=Material+Icons')
                        ui.icon('').classes('text-2xl flex-grow').bind_name_from(object_icon, 'value')
                    object_phone = ui.input('物品绑定手机号', validation={'请输入中国大陆格式的11位手机号': lambda value: len(value) == 11 and value.isdigit()}).classes('w-full')
                    ui.label('目前仅支持中国大陆格式的11位手机号').classes('-mt-3')
                    object_key = ui.input('物品Key(可选，不填自动生成)').classes('w-full')
                    ui.label('物品Key为物品的唯一标识，可用于物品找回').classes('-mt-3')
        
                async def handle_add_object():
                    await addObject()
                
                dialogAddObjectIcon = ui.button("添加并生成二维码", icon='qr_code', on_click=handle_add_object) \
                        .classes('items-center w-full').props('rounded')
                ui.button("返回", on_click=addObjectDialog.close) \
                        .classes('w-full').props('flat rounded')
            
            async def editObjectPrepare():
                '''
                读取选中物品的ID，并预填充编辑表单
                '''
                try:
                    # 获取选中物品的ID
                    item_id = str(object_table.selected[0]['id'])
                    id_json = json.dumps(item_id)
                    
                    result: dict = await ui.run_javascript(f'getItem({id_json})')
                    
                    if result.get('status') == 'failed':
                        ui.notify(f"获取物品信息失败: {result.get('detail', '未知错误')}", color='negative')
                        return
                        
                except Exception as e:
                    ui.notify(f"操作失败: {str(e)}", color='negative')
                    return
                else:
                    result = result['data']['data'][0]

                    # 预填充编辑表单
                    edit_object_name.set_value(result['name'])
                    edit_object_icon.set_value(result['icon'])
                    edit_object_phone.set_value(result['phone'])
                    edit_object_key.set_value(result['key'])
                    edit_set_object_lost.set_value(result['status'] == 'lost')
                    lostReason.set_value(result['lost_description'])
                    editObjectDialog.open()
            
            async def editObject():
                dialogEditObjectIcon.disable()
                
                async def on_success():
                    await reloadTable(tips=False)
                    
                    edit_object_name.set_value('')
                    edit_object_icon.set_value('')
                    edit_object_phone.set_value('')
                    edit_object_key.set_value('')
                    lostReason.set_value('')
                    edit_set_object_lost.set_value(False)
                    
                    editObjectDialog.close()
                
                if edit_object_name.value == "" or edit_object_icon.value == "" or edit_object_phone.value == "":
                    ui.notify('必填字段不能为空', color='negative')
                    dialogEditObjectIcon.enable()
                    return
                
                if not edit_object_phone.validate():
                    ui.notify('号码输入有误，请检查！', color='negative')
                    dialogEditObjectIcon.enable()
                    return
                
                if edit_object_key.value == "":
                    ui.notify('物品Key不能为空', color='negative')
                    dialogEditObjectIcon.enable()
                    return
                
                async with loding_process(
                    success_content='更新成功',
                    on_success=on_success,
                    on_error=dialogEditObjectIcon.enable(),
                    on_finally=dialogEditObjectIcon.enable()
                ):
                    # 获取选中物品的ID
                    item_id = str(object_table.selected[0]['id'])
                    
                    # 正确序列化字符串参数
                    id_json = json.dumps(item_id)
                    key = json.dumps(edit_object_key.value)
                    name = json.dumps(edit_object_name.value)
                    icon = json.dumps(edit_object_icon.value)
                    phone = json.dumps(edit_object_phone.value)
                    
                    # 处理状态和物主留言
                    status = json.dumps('lost' if edit_set_object_lost.value else 'ok')
                    context = json.dumps(lostReason.value if edit_set_object_lost.value else '')
                    
                    result = await ui.run_javascript(
                        f'updateItems({id_json}, {key}, {name}, {icon}, {phone}, {status}, {context})'
                    )
                    
                    if result.get('status') == 'failed':
                        raise Exception(f"更新失败: {result.get('detail', '未知错误')}")


            # 编辑物品对话框
            with ui.dialog() as editObjectDialog, ui.card().style('width: 90%; max-width: 500px'):
                ui.button(icon='edit').props('outline round').classes('mx-auto w-auto shadow-sm w-fill')
                ui.label('编辑物品信息').classes('w-full text-h5 text-center')
                
                with ui.scroll_area().classes('w-full'):
                    edit_object_name = ui.input('物品名称').classes('w-full')
                    ui.label('显示的物品名称').classes('-mt-3')
                    with ui.row(align_items='center').classes('w-full'):
                        with ui.column().classes('w-1/2 flex-grow'):
                            edit_object_icon = ui.input('物品图标').classes('w-full')
                            with ui.row(align_items='center').classes('-mt-3'):
                                ui.label('将在右侧实时预览图标')
                                ui.link('图标列表', 'https://fonts.google.com/icons?icon.set=Material+Icons')
                        ui.icon('').classes('text-2xl flex-grow').bind_name_from(edit_object_icon, 'value')
                    edit_object_phone = ui.input('物品绑定手机号').classes('w-full')
                    ui.label('目前仅支持中国大陆格式的11位手机号').classes('-mt-3')
                    edit_object_key = ui.input('物品Key').classes('w-full').props('readonly')
                    ui.label('物品Key为物品的唯一标识，不可修改').classes('-mt-3')
                    
                    edit_set_object_lost = ui.switch('设置物品状态为丢失').classes('w-full')
                    ui.label('确定要设置这个物品为丢失吗？').bind_visibility_from(edit_set_object_lost, 'value').classes('-mt-3')
                    ui.html('设置为丢失以后，<b>你的电话号码将会被完整地显示在物品页面</b>(不是“*** **** 8888”而是“188 8888 8888”)，以供拾到者能够记下你的电话号码。此外，在页面底部将会显示一个按钮，这个按钮能够一键拨打预先设置好的电话。').bind_visibility_from(edit_set_object_lost, 'value').classes('-mt-3')
                    lostReason = ui.input('物主留言') \
                        .classes('block w-full text-gray-900').bind_visibility_from(edit_set_object_lost, 'value').classes('-mt-3')
                    ui.label('非必填，但建议填写，以方便拾到者联系你').classes('-mt-3').bind_visibility_from(edit_set_object_lost, 'value').classes('-mt-3')

                    ui.separator().classes('my-4')
                    with ui.card().classes('w-full bg-red-50 dark:bg-red-900 q-pa-md'):
                        ui.label('危险区域').classes('text-red-500 font-bold')
                        ui.button('删除物品', icon='delete_forever') \
                            .classes('w-full text-red-500').props('flat').on_click(lambda: delete_confirmation_dialog.open())
                    
                async def handle_edit_object():
                    await editObject()

                dialogEditObjectIcon = ui.button("确认提交", on_click=handle_edit_object) \
                    .classes('items-center w-full').props('rounded')
                ui.button("返回", on_click=editObjectDialog.close) \
                    .classes('w-full').props('flat rounded')
            
            # 删除确认对话框
            with ui.dialog() as delete_confirmation_dialog, ui.card().style('width: 90%; max-width: 500px'):
                ui.button(icon='warning').props('outline round').classes('mx-auto w-auto shadow-sm w-fill text-red-500')
                ui.label('确认删除物品').classes('w-full text-h5 text-center text-red-500')
                ui.label('此操作不可撤销，删除后物品数据将永久丢失！').classes('w-full text-center text-red-500')
                
                async def handle_delete_item():
                    
                    async def on_success():
                        await reloadTable(tips=False)
                        delete_confirmation_dialog.close()
                        editObjectDialog.close()
                    
                    async with loding_process(
                        success_content='物品已删除',
                        on_success=on_success
                    ):
                        # 获取选中物品的ID
                        item_id = str(object_table.selected[0]['id'])
                        id_json = json.dumps(item_id)
                        
                        result = await ui.run_javascript(f'deleteItem({id_json})')
                        
                        if result.get('status') == 'failed':
                            raise Exception(f"删除失败: {result.get('detail', '未知错误')}")
                
                with ui.row().classes('w-full'):
                    ui.space()
                    ui.button('取消', icon='close', on_click=delete_confirmation_dialog.close).props('flat')
                    ui.button('确认删除', icon='delete_forever', on_click=handle_delete_item).classes('text-red-500').props('flat')
            
            async def fetch_and_process_objects():
                """获取并处理所有物品数据"""
                try:
                    # 调用前端JavaScript获取数据
                    response = await ui.run_javascript('getItems()')
                    
                    if response['status'] == 'failed':
                        if str(response['detail']).find('Unauthorized'):
                            ui.notify('未登录或登录已过期，请重新登录', color='negative')
                            await asyncio.sleep(2)
                            ui.navigate.to('/login?redirect_to=/admin/items')
                        ui.notify(response['detail'], color='negative')
                        return []
                    
                    # 从response中提取数据
                    raw_data = response.get('data', {})
                    objects = raw_data.get('data', []) if isinstance(raw_data, dict) else raw_data
                    
                    # 进行数据处理，类似旧版本的逻辑
                    status_map = {'ok': '正常', 'lost': '丢失'}
                    processed_objects = []
                    
                    for obj in objects:
                        # 确保obj是字典
                        if isinstance(obj, dict):
                            # 复制对象避免修改原始数据
                            processed_obj = obj.copy()
                            
                            # 状态映射
                            if 'status' in processed_obj:
                                processed_obj['status'] = status_map.get(processed_obj['status'], processed_obj['status'])
                            
                            # 时间格式化
                            if 'create_time' in processed_obj and processed_obj['create_time']:
                                processed_obj['create_time'] = format_time_diff(processed_obj['create_time'])
                            
                            if 'lost_time' in processed_obj and processed_obj['lost_time']:
                                processed_obj['lost_time'] = format_time_diff(processed_obj['lost_time'])
                            
                            processed_objects.append(processed_obj)
                    
                    return processed_objects
                except Exception as e:
                    ui.notify(f"获取数据失败: {str(e)}", color='negative')
                    print(f"Error in fetch_and_process_objects: {str(e)}")
                    return []

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
                {'name': 'create_time', 'label': '物品创建时间', 'field': 'create_time', 'required': True, 'align': 'left'},
                {'name': 'lost_time', 'label': '物品丢失时间', 'field': 'lost_time', 'required': True, 'align': 'left'}
            ]

            objects = await fetch_and_process_objects()
            object_table = ui.table(
                title='物品 & 库存',
                row_key='id',
                pagination=10,
                selection='single',
                columns=object_columns,
                rows=objects,
                # on_select=lambda: objectTableOnSelect()
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
            with ui.page_sticky(x_offset=24, y_offset=24) \
                .bind_visibility_from(object_table, 'selected', backward=lambda x: not x) as addObjectFAB:
                ui.button(icon='add', on_click=addObjectDialog.open) \
                    .props('fab')
            with ui.page_sticky(x_offset=24, y_offset=24) \
                .bind_visibility_from(addObjectFAB, 'visible', backward=lambda x: not x) as editObjectFAB:
                ui.button(icon='edit', on_click=editObjectPrepare) \
                    .props('fab')