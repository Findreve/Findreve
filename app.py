from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi import Request, HTTPException
from contextlib import asynccontextmanager
from routes import (session, admin, object)
import model.database
import os, asyncio

# 初始化数据库
asyncio.run(model.database.Database().init_db())

# 定义程序参数
APP_NAME: str = 'Findreve'
VERSION: str = '2.0.0-ootc'
summary='标记、追踪与找回 —— 就这么简单。'
description='Findreve 是一款强大且直观的解决方案，旨在帮助您管理个人物品，'\
            '并确保丢失后能够安全找回。每个物品都会被分配一个 唯一 ID ，'\
            '并生成一个 安全链接 ，可轻松嵌入到 二维码 或 NFC 标签 中。'\
            '当扫描该代码时，会将拾得者引导至一个专门的网页，上面显示物品详情和您的联系信息，'\
            '既保障隐私又便于沟通。无论您是在管理个人物品还是专业资产，'\
            'Findreve 都能以高效、简便的方式弥合丢失与找回之间的距离。'

# Findreve 的生命周期
@asynccontextmanager
async def lifespan(app: FastAPI):
    await model.database.Database().init_db()
    yield

# 定义 Findreve 服务器
app = FastAPI(
    title=APP_NAME,
    version=VERSION,
    summary=summary,
    description=description,
    lifespan=lifespan
)

# 挂载后端路由
app.include_router(admin.Router)
app.include_router(session.Router)
app.include_router(object.Router)

@app.get("/")
def read_root():
    if not os.path.exists("dist/index.html"):
        raise HTTPException(status_code=404, detail="Frontend not built. Please build the frontend first.")
    return FileResponse("dist/index.html")

# 回退路由
@app.get("/{path:path}")
async def serve_spa(request: Request, path: str):
    if not os.path.exists("dist/index.html"):
        raise HTTPException(status_code=404, detail="Frontend not built. Please build the frontend first.")
    
    # 排除API路由
    if path.startswith("api/"):
        raise HTTPException(status_code=404, detail="Not Found")
    
    # 检查是否是静态资源请求
    if path.startswith("assets/") and os.path.exists(f"dist/{path}"):
        return FileResponse(f"dist/{path}")
    
    # 检查文件是否存在于dist目录
    dist_file_path = os.path.join("dist", path)
    if os.path.exists(dist_file_path) and not os.path.isdir(dist_file_path):
        return FileResponse(dist_file_path)
        
    # 对于所有其他前端路由，返回index.html让Vue Router处理
    return FileResponse("dist/index.html")