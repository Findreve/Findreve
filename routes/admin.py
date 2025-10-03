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
from model.object import Object

# 验证是否为管理员
async def is_admin(
        token: Annotated[str, Depends(JWT.oauth2_scheme)],
        session: Annotated[AsyncSession, Depends(database.Database.get_session)],
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
        payload = jwt.decode(token, await JWT.get_secret_key(), algorithms=[JWT.ALGORITHM])
        username = payload.get("sub")
        stored_account = await Setting.get(session, Setting.name == 'account')
        if username is None or not stored_account.value == username:
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
    session: Annotated[AsyncSession, Depends(database.Database.get_session)],
    id: int | None = Query(default=None, ge=1, description='物品ID'),
    key: str | None = Query(default=None, description='物品序列号')):
    '''
    获得物品信息。
    
    不传参数返回所有信息，否则可传入 `id` 或 `key` 进行筛选。
    '''
    # 根据条件查询物品
    if id is not None:
        results = await Object.get(session, Object.id == id)
        results = [results] if results else []
    elif key is not None:
        results = await Object.get(session, Object.key == key)
        results = [results] if results else []
    else:
        results = await Object.get(session, None, fetch_mode="all")
    
    if results:
        items = []
        for obj in results:
            items.append(Item(
                id=obj.id,
                type=obj.type,
                key=obj.key,
                name=obj.name,
                icon=obj.icon or "",
                status=obj.status or "",
                phone=int(obj.phone) if obj.phone and obj.phone.isdigit() else 0,
                lost_description=obj.context,
                find_ip=obj.find_ip,
                create_time=obj.created_at.isoformat(),
                lost_time=obj.lost_at.isoformat() if obj.lost_at else None
            ))
        return DefaultResponse(data=items)
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
    session: Annotated[AsyncSession, Depends(database.Database.get_session)],
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
        # 创建新物品对象
        new_object = Object(
            key=key,
            type=type,
            name=name,
            icon=icon,
            phone=phone
        )
        # 使用 base.py 中的 add 方法
        await Object.add(session, new_object)
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
    session: Annotated[AsyncSession, Depends(database.Database.get_session)],
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
        # 获取现有物品
        obj = await Object.get_exist_one(session, id)
        
        # 更新字段
        if key is not None:
            obj.key = key
        if name is not None:
            obj.name = name
        if icon is not None:
            obj.icon = icon
        if status is not None:
            obj.status = status
        if phone is not None:
            obj.phone = str(phone)
        if lost_description is not None:
            obj.context = lost_description
        if find_ip is not None:
            obj.find_ip = find_ip
        if lost_time is not None:
            from datetime import datetime
            obj.lost_at = datetime.fromisoformat(lost_time)
        
        # 保存更新
        await obj.save(session)
    except HTTPException:
        raise
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
    session: Annotated[AsyncSession, Depends(database.Database.get_session)],
    id: int) -> DefaultResponse:
    '''
    删除物品信息。
    
    - **id**: 物品的ID
    '''
    try:
        # 获取现有物品
        obj = await Object.get_exist_one(session, id)
        # 使用 base.py 中的 delete 方法
        await Object.delete(session, obj)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    else:
        return DefaultResponse(data=True)