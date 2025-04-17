import random
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from model.database import Database
from model.response import DefaultResponse
import asyncio

Router = APIRouter(prefix='/api/object', tags=['object'])

@Router.get('/{item_key}')
async def get_object(item_key: str, request: Request):
    """
    获取物品信息 / Get object information
    """
    
    db = Database()
    await db.init_db()
    object_data = await db.get_object(key=item_key)
    
    if object_data:
        if object_data[4] == 'lost':
            # 物品已标记为丢失，更新IP地址
            await db.update_object(id=object_data[0], find_ip=str(request.client.host))
            
            # 添加一些随机延迟，类似JWT身份验证时根据延迟爆破引发的问题
            await asyncio.sleep(random.uniform(0.10, 0.30))
        else:
            await asyncio.sleep(random.uniform(0.10, 0.30))
        
        return DefaultResponse(
            data=object_data
        )
    else: return JSONResponse(
        status_code=404,
        content=DefaultResponse(
            code=404,
            msg='物品不存在或出现异常'
        ).model_dump()
    )