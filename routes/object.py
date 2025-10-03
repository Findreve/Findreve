import random
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from model.database import Database
from model.response import DefaultResponse, ObjectData
import asyncio
import aiohttp

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
        if object_data[5] == 'lost':
            # 物品已标记为丢失，更新IP地址
            await db.update_object(id=object_data[0], find_ip=str(request.client.host))
            
        # 添加一些随机延迟，类似JWT身份验证时根据延迟爆破引发的问题
        await asyncio.sleep(random.uniform(0.10, 0.30))
        
        print(object_data)
        return DefaultResponse(data=ObjectData(
            id=object_data[0],
            type=object_data[1],
            key=object_data[2],
            name=object_data[3],
            icon=object_data[4],
            status=object_data[5],
            phone=object_data[6],
            lost_description=object_data[7],
            create_time=object_data[9],
            lost_time=object_data[10]
        ).model_dump())
    else: return JSONResponse(
        status_code=404,
        content=DefaultResponse(
            code=404,
            msg='物品不存在或出现异常'
        ).model_dump()
    )

@Router.put(
    path='/{item_id}',
    summary="通知车主进行挪车",
    description="向车主发送挪车通知",
    response_model=DefaultResponse,
    response_description="挪车通知结果"
)
async def notify_move_car(
    item_id: int,
    phone: str = None,
):
    """通知车主进行挪车 / Notify car owner to move the car

    Args:
        item_id (int): 物品ID / Item ID
        phone (str): 挪车发起者电话 / Phone number of the person initiating the move. Defaults to None.
    """
    db = Database()
    await db.init_db()
    
    # 检查是否存在该物品
    object_data = await db.get_object(id=item_id)
    if not object_data:
        return JSONResponse(
            status_code=404,
            content=DefaultResponse(
                code=404,
                msg='物品不存在或出现异常'
            ).model_dump()
        )
    
    # 检查物品类型是否为车辆
    if object_data[1] != 'car':
        return JSONResponse(
            status_code=400,
            content=DefaultResponse(
                code=400,
                msg='该物品不是车辆，无法发送挪车通知'
            ).model_dump()
        )
    
    # 发起挪车通知（目前仅适配Server酱）
    server_chan_key = await db.get_setting('server_chan_key')
    if not server_chan_key:
        return JSONResponse(
            status_code=500,
            content=DefaultResponse(
                code=500,
                msg='未配置Server酱，无法发送挪车通知'
            ).model_dump()
        )
    
    title = "挪车通知 - Findreve"
    description = f"您的车辆“{object_data[3]}”被请求挪车。\n\n"
    if phone:
        description += f"请求挪车者电话：[{phone}](tel:{phone})\n\n"    
    description += "请尽快联系请求者并挪车。"
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            url=f"https://sctapi.ftqq.com/{server_chan_key}.send",
            data={
                "title": title,
                "desp": description
            }
        ) as resp:
            if resp.status == 200:
                resp_json = await resp.json()
                if resp_json.get('code') == 0:
                    return DefaultResponse(msg='挪车通知发送成功')
                else:
                    return JSONResponse(
                        status_code=500,
                        content=DefaultResponse(
                            code=500,
                            msg=f"挪车通知发送失败，Server酱返回错误：{resp_json.get('message')}"
                        ).model_dump()
                    )
            else:
                return JSONResponse(
                    status_code=500,
                    content=DefaultResponse(
                        code=500,
                        msg=f"挪车通知发送失败，HTTP状态码：{resp.status}"
                    ).model_dump()
                )