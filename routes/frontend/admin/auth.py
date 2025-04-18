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
from tool import *
from fastapi import Request
from ..framework import frame


def create():  
    @ui.page('/admin/auth')
    async def admin_auth(request: Request):
        # Findreve 授权
        async with frame(request=request):

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