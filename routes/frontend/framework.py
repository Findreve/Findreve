from contextlib import contextmanager
from nicegui import ui
from fastapi import Request

@contextmanager
def frame(request: Request):
    with ui.header() \
    .classes('items-center duration-300 py-2 px-5 no-wrap') \
    .style('box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1)'):
        with ui.tabs(value='main_page') as tabs:
            ui.button(icon='menu', on_click=lambda: left_drawer.toggle()).props('flat color=white round')
            ui.button(text="Findreve 仪表盘").classes('text-lg').props('flat color=white no-caps')

    with ui.left_drawer() as left_drawer:
        with ui.column().classes('w-full'):
            ui.image('/static/Findreve.png').classes('w-1/2 mx-auto')
            ui.label('Findreve').classes('text-2xl text-bold')
            ui.label("免费版，无需授权").classes('text-red-600 -mt-3')

        ui.button('首页 & 信息', icon='fingerprint', on_click=lambda: ui.navigate.to('/admin/home')) \
            .classes('w-full').props('flat no-caps')
        ui.button('物品 & 库存', icon='settings', on_click=lambda: ui.navigate.to('/admin/item')) \
            .classes('w-full').props('flat no-caps')
        ui.button('产品 & 授权', icon='settings', on_click=lambda: ui.navigate.to('/admin/auth')) \
            .classes('w-full').props('flat no-caps')
        ui.button('关于 & 反馈', icon='settings', on_click=lambda: ui.navigate.to('/admin/about')) \
            .classes('w-full').props('flat no-caps')
    
    yield