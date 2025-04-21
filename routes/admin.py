from fastapi import APIRouter
from typing import Annotated, Literal, Optional
from fastapi import Depends, Query
from fastapi import HTTPException
import JWT
from model import database
from model.response import DefaultResponse
from model.items import Item

# 验证是否为管理员
async def is_admin(token: Annotated[str, Depends(JWT.oauth2_scheme)]) -> Literal[True]:
    '''
    验证是否为管理员。
    
    使用方法：
    >>> APIRouter(dependencies=[Depends(is_admin)])
    '''
    return True

Router = APIRouter(
    prefix='/api/admin', 
    tags=['管理员 Admin'],
    dependencies=[Depends(is_admin)]
)

@Router.get(
    path='/',
    summary='验证管理员身份',
    description='返回管理员身份验证结果',
    response_model=DefaultResponse,
    response_description='当前为管理员'
)
async def verity_admin(
    is_admin: Annotated[str, Depends(is_admin)]
) -> Literal[True]:
    '''
    使用 API 验证是否为管理员。
    
    - 若为管理员，返回 `True`
    - 若不是管理员，抛出 `401` 错误
    '''
    return is_admin

@Router.get(
    path='/items',
    summary='获取物品信息',
    description='返回物品信息列表',
    response_model=DefaultResponse,
    response_description='物品信息列表'
)
async def get_items(
    id: Optional[int] = Query(default=None, ge=1, description='物品ID'),
    key: Optional[str] = Query(default=None, description='物品序列号')):
    '''
    获得物品信息。
    
    不传参数返回所有信息，否则可传入 `id` 或 `key` 进行筛选。
    '''
    results = await database.Database().get_object(id=id, key=key)
    
    if results is not None:
        if not isinstance(results, list):
            items = [results]
        else:
            items = results
        item = []
        for i in items:
            item.append(Item(
                id=i[0],
                key=i[1],
                name=i[2],
                icon=i[3],
                status=i[4],
                phone=i[5],
                lost_description=i[6],
                find_ip=i[7],
                create_time=i[8],
                lost_time=i[9]
            ))
        return DefaultResponse(data=item)
    else:
        return DefaultResponse(data=[])

@Router.post(
    path='/items',
    summary='添加物品信息',
    description='添加新的物品信息',
    response_model=DefaultResponse,
    response_description='添加物品成功'
)
async def add_items(
    key: str,
    name: str,
    icon: str,
    phone: str) -> DefaultResponse:
    '''
    添加物品信息。
    
    - **key**: 物品的关键字
    - **name**: 物品的名称
    - **icon**: 物品的图标
    - **phone**: 联系电话
    '''
    
    try:
        await database.Database().add_object(
            key=key, name=name, icon=icon, phone=phone)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    else:
        return DefaultResponse()

@Router.patch(
    path='/items',
    summary='更新物品信息',
    description='更新现有物品的信息',
    response_model=DefaultResponse,
    response_description='更新物品成功'
)
async def update_items(
    id: int = Query(ge=1),
    key: Optional[str] = None,
    name: Optional[str] = None,
    icon: Optional[str] = None,
    status: Optional[str] = None,
    phone: Optional[int] = None,
    lost_description: Optional[str] = None,
    find_ip: Optional[str] = None,
    lost_time: Optional[str] = None) -> DefaultResponse:
    '''
    更新物品信息。
    
    只有 `id` 是必填参数，其余参数都是可选的，在不传入任何值的时候将不做任何更改。
    
    - **id**: 物品的ID
    - **key**: 物品的序列号 **不建议修改此项，这样会导致生成的物品二维码直接失效**
    - **name**: 物品的名称
    - **icon**: 物品的图标
    - **status**: 物品的状态
    - **phone**: 联系电话
    - **lost_description**: 物品丢失描述
    - **find_ip**: 找到物品的IP
    - **lost_time**: 物品丢失时间
    
    '''
    try:
        await database.Database().update_object(
            id=id,
            key=key, name=name, icon=icon, status=status, phone=phone,
            lost_description=lost_description, find_ip=find_ip,
            lost_time=lost_time
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    else:
        return DefaultResponse()

@Router.delete(
    path='/items',
    summary='删除物品信息',
    description='删除指定的物品信息',
    response_model=DefaultResponse,
    response_description='删除物品成功'
)
async def delete_items(
    id: int) -> DefaultResponse:
    '''
    删除物品信息。
    
    - **id**: 物品的ID
    '''
    try:
        await database.Database().delete_object(id=id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    else:
        return DefaultResponse()