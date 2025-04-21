import random
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from model.database import Database
from model.response import DefaultResponse, ObjectData
import asyncio

Router = APIRouter(prefix='/api/object', tags=['物品 Object'])

@Router.get(
    path='/{item_key}',
    summary="获取物品信息",
    description="根据物品键获取物品信息",
    response_model=DefaultResponse,
    response_description="物品信息"
)
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
        
        return DefaultResponse(data=ObjectData(
            id=object_data[0],
            key=object_data[1],
            name=object_data[2],
            icon=object_data[3],
            status=object_data[4],
            phone=object_data[5],
            context=object_data[6]
        ).model_dump())
    else: return JSONResponse(
        status_code=404,
        content=DefaultResponse(
            code=404,
            msg='物品不存在或出现异常'
        ).model_dump()
    )