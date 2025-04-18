'''
Author: 于小丘 海枫
Date: 2024-10-02 15:23:34
LastEditors: Yuerchu admin@yuxiaoqiu.cn
LastEditTime: 2024-11-29 20:05:13
FilePath: /Findreve/notfound.py
Description: Findreve 404

Copyright (c) 2018-2024 by 于小丘Yuerchu, All Rights Reserved. 
'''

from nicegui import app
from fastapi import Request
from fastapi.responses import HTMLResponse

def create() -> None:
    @app.get('/404')
    async def not_found_page(request: Request) -> HTMLResponse:
        return HTMLResponse(status_code=404)
