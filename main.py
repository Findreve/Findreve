'''
Author: 于小丘 海枫
Date: 2024-10-02 15:23:34
LastEditors: Yuerchu admin@yuxiaoqiu.cn
FilePath: /Findreve/main.py
Description: 标记、追踪与找回 —— 就这么简单。

Copyright (c) 2018-2025 by 于小丘Yuerchu, All Rights Reserved. 
'''

# 导入库
from app import app
from fastapi.staticfiles import StaticFiles

from routes import (session, admin, object)
import logging

# 挂载路由
app.include_router(admin.Router)
app.include_router(session.Router)
app.include_router(object.Router)

# 添加静态文件目录
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except RuntimeError:
    logging.error('无法挂载静态目录')

# 作为主程序启动时
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8080,
        reload=True)