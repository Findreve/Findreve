# 初始化数据库
import asyncio
from model.database import Database
asyncio.run(Database().init_db())

# 导入库
from app import app
from fastapi.staticfiles import StaticFiles
import logging

# 添加静态文件目录
try:
    # 挂载静态文件目录
    app.mount("/dist", StaticFiles(directory="dist"), name="dist")
except RuntimeError as e:
    logging.warning(f'无法挂载静态目录: {str(e)}, 将启动纯后端模式')

# 作为主程序启动时
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(
        'app:app',
        host='0.0.0.0',
        port=8080
    )