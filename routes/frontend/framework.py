from contextlib import asynccontextmanager
from nicegui import ui
import asyncio
from typing import Optional, Literal

@asynccontextmanager
async def frame(
    page: Literal['admin', 'session', 'found'] = 'admin'
):
    
    ui.add_head_html("""
            <script type="text/javascript" src="/static/js/main.js"></script>
            """)
    
    await ui.context.client.connected()
    
    is_login = await ui.run_javascript('is_login()', timeout=3)
    if str(is_login).lower() != 'true' and page != 'session':
        ui.navigate.to('/login?redirect_to=/admin')
    
    with ui.header() \
    .classes('items-center py-2 px-5 no-wrap').props('elevated'):
            ui.button(icon='menu', on_click=lambda: left_drawer.toggle()).props('flat color=white round')
            ui.button(text="Findreve 仪表盘" if page == 'admin' else "Findreve").classes('text-lg').props('flat color=white no-caps')
            
            ui.space()
            
            if str(is_login).lower() == 'true':
                ui.button(icon='logout', on_click=lambda: ui.run_javascript('logout()')) \
                    .props('flat color=white fab-mini').tooltip('退出登录')

    with ui.left_drawer() as left_drawer:
        with ui.column(align_items='center').classes('w-full'):
            ui.image('/static/Findreve.png').classes('w-1/2 mx-auto')
            ui.label('Findreve').classes('text-2xl text-bold')
            ui.label("免费版，无需授权").classes('text-sm text-gray-500')
    

        if page == 'admin':
            ui.button('首页 & 信息', icon='fingerprint', on_click=lambda: ui.navigate.to('/admin/home')) \
                .classes('w-full').props('flat no-caps')
            ui.button('物品 & 库存', icon='settings', on_click=lambda: ui.navigate.to('/admin/items')) \
                .classes('w-full').props('flat no-caps')
            ui.button('产品 & 授权', icon='settings', on_click=lambda: ui.navigate.to('/admin/auth')) \
                .classes('w-full').props('flat no-caps')
            ui.button('关于 & 反馈', icon='settings', on_click=lambda: ui.navigate.to('/admin/about')) \
                .classes('w-full').props('flat no-caps')
    
    if page == 'found':
        left_drawer.hide()
    
    with ui.column().classes('w-full'):
        yield

@asynccontextmanager
async def loding_process(
    content: str = '正在处理，请稍后...',
    success_content: str = '操作成功',
    error_content: str = '操作失败',
    on_success: Optional[callable] = None,
    on_error: Optional[callable] = None,
    on_finally: Optional[callable] = None
    ):
    """
    加载提示框
    
    :param content: 提示内容
    :param success_content: 成功提示内容
    :param error_content: 失败提示内容
    :param on_success: 成功回调函数
    :param on_error: 失败回调函数
    
    ~~~
    使用方法
    >>> async with loding_process():
            # 处理代码
    """
    notify = ui.notification(
        message=content,
        timeout=None
    )
    notify.spinner = True
    
    try:
        yield
    except Exception as e:
        notify.spinner = False
        notify.type = 'negative'
        notify.message = error_content + ':' + str(e)
        await asyncio.sleep(3)
        notify.dismiss()
        if on_error:
            await on_error(e)
    else:
        notify.spinner = False
        notify.type = 'positive'
        notify.message = success_content
        if on_success:
            await on_success()
        await asyncio.sleep(3)
        notify.dismiss()
    finally:
        if on_finally:
            await on_finally()