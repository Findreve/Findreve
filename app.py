from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi import Request, HTTPException
from contextlib import asynccontextmanager
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from routes import (session, admin, object)
import model.database
import os, asyncio
import pkg.conf

# 初始化数据库
asyncio.run(model.database.Database().init_db())

# Findreve 的生命周期
@asynccontextmanager
async def lifespan(app: FastAPI):
    await model.database.Database().init_db()
    yield

# 定义 Findreve 服务器
app = FastAPI(
    title=pkg.conf.APP_NAME,
    version=pkg.conf.VERSION,
    summary=pkg.conf.summary,
    description=pkg.conf.description,
    lifespan=lifespan
)

# 挂载后端路由
app.include_router(admin.Router)
app.include_router(session.Router)
app.include_router(object.Router)

# 挂载Slowapi限流中间件
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/")
def read_root():
    if not os.path.exists("dist/index.html"):
        raise HTTPException(status_code=404)
    return FileResponse("dist/index.html")

# 回退路由
@app.get("/{path:path}")
async def serve_spa(request: Request, path: str):
    if not os.path.exists("dist/index.html"):
        raise HTTPException(status_code=404)
    
    # 排除API路由
    if path.startswith("api/"):
        raise HTTPException(status_code=404)
    
    # 检查是否是静态资源请求
    if path.startswith("assets/") and os.path.exists(f"dist/{path}"):
        return FileResponse(f"dist/{path}")
    
    # 检查文件是否存在于dist目录
    dist_file_path = os.path.join("dist", path)
    if os.path.exists(dist_file_path) and not os.path.isdir(dist_file_path):
        return FileResponse(dist_file_path)
        
    # 对于所有其他前端路由，返回index.html让Vue Router处理
    return FileResponse("dist/index.html")