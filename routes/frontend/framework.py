from contextlib import asynccontextmanager
from nicegui import ui

@asynccontextmanager
async def frame():
    
    ui.add_head_html(
        '''
        <script>
            async function is_login() {
                const accessToken = localStorage.getItem('access_token');
                if (!accessToken) {
                    return false;
                }
                try {
                    const response = await fetch('/api/admin', {
                        method: 'GET',
                        headers: {
                            'Authorization': `Bearer ${accessToken}`,
                        }
                    })
                    
                    if (!response.ok) {
                        return false;
                    }
                    
                    return true;
                }
                catch (error) {
                    return false;
                }
            }
            
            function logout() {
                localStorage.removeItem('access_token');
                window.location.href = '/login';
            }
        </script>
    ''')
    
    await ui.context.client.connected()
    is_login = await ui.run_javascript('is_login()', timeout=3)
    if str(is_login).lower() != 'true':
        ui.navigate.to('/login?redirect_to=/admin')
    
    with ui.header() \
    .classes('items-center py-2 px-5 no-wrap').props('elevated'):
            ui.button(icon='menu', on_click=lambda: left_drawer.toggle()).props('flat color=white round')
            ui.button(text="Findreve 仪表盘").classes('text-lg').props('flat color=white no-caps')

    with ui.left_drawer() as left_drawer:
        with ui.column(align_items='center').classes('w-full'):
            ui.image('/static/Findreve.png').classes('w-1/2 mx-auto')
            ui.label('Findreve').classes('text-2xl text-bold')
            ui.label("免费版，无需授权").classes('text-sm text-gray-500')

        ui.button('首页 & 信息', icon='fingerprint', on_click=lambda: ui.navigate.to('/admin/home')) \
            .classes('w-full').props('flat no-caps')
        ui.button('物品 & 库存', icon='settings', on_click=lambda: ui.navigate.to('/admin/items')) \
            .classes('w-full').props('flat no-caps')
        ui.button('产品 & 授权', icon='settings', on_click=lambda: ui.navigate.to('/admin/auth')) \
            .classes('w-full').props('flat no-caps')
        ui.button('关于 & 反馈', icon='settings', on_click=lambda: ui.navigate.to('/admin/about')) \
            .classes('w-full').props('flat no-caps')
    
    with ui.column().classes('w-full'):
        yield