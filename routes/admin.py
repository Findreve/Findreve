from fastapi import APIRouter
from typing import Annotated, Literal
from fastapi import Depends, Query
from fastapi import HTTPException
import JWT
import jwt
from jwt import InvalidTokenError
from model import database
from model.response import DefaultResponse
from model.items import Item
from sqlmodel.ext.asyncio.session import AsyncSession
from model import Setting

# 验证是否为管理员
async def is_admin(
        token: Annotated[str, Depends(JWT.oauth2_scheme)],
        session: Annotated[AsyncSession, Depends(database.Database.get_session)]
) -> Literal[True]:
    '''
    验证是否为管理员。
    
    使用方法：
    >>> APIRouter(dependencies=[Depends(is_admin)])
    '''
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, JWT.get_secret_key(), algorithms=[JWT.ALGORITHM])
        username = payload.get("sub")
        if username is None or not await Setting.get(session, Setting.name == 'account') == username:
            raise credentials_exception
        else:
            return True
    except InvalidTokenError:
        raise credentials_exception
        

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
async def verity_admin() -> DefaultResponse:
    '''
    使用 API 验证是否为管理员。
    
    - 若为管理员，返回 `True`
    - 若不是管理员，抛出 `401` 错误
    '''
    return DefaultResponse(data=True)

@Router.get(
    path='/items',
    summary='获取物品信息',
    description='返回物品信息列表',
    response_model=DefaultResponse,
    response_description='物品信息列表'
)
async def get_items(
    id: int | None = Query(default=None, ge=1, description='物品ID'),
    key: str | None = Query(default=None, description='物品序列号')):
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
                type=i[1],
                key=i[2],
                name=i[3],
                icon=i[4],
                status=i[5],
                phone=i[6],
                lost_description=i[7],
                find_ip=i[8],
                create_time=i[9],
                lost_time=i[10]
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
    type: Literal['normal', 'car'],
    name: str,
    icon: str,
    phone: str
) -> DefaultResponse:
    '''
    添加物品信息。
    
    - **key**: 物品的关键字
    - **type**: 物品的类型
    - **name**: 物品的名称
    - **icon**: 物品的图标
    - **phone**: 联系电话
    '''
    
    try:
        await database.Database().add_object(
            key=key, 
            type=type,
            name=name, 
            icon=icon, 
            phone=phone
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    else:
        return DefaultResponse(data=True)

@Router.patch(
    path='/items',
    summary='更新物品信息',
    description='更新现有物品的信息',
    response_model=DefaultResponse,
    response_description='更新物品成功'
)
async def update_items(
    id: int = Query(ge=1),
    key: str | None = None,
    name: str | None = None,
    icon: str | None = None,
    status: str | None = None,
    phone: int | None = None,
    lost_description: str | None = None,
    find_ip: str | None = None,
    lost_time: str | None = None
    ) -> DefaultResponse:
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
        return DefaultResponse(data=True)

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
        return DefaultResponse(data=True)