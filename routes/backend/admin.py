from nicegui import app
from typing import Annotated, Optional
from fastapi import Depends
from fastapi import HTTPException, status
from jwt import InvalidTokenError
import jwt, JWT
from model import database
from model import token as Token
from model.response import DefaultResponse
from model.items import Item

async def is_admin(token: Annotated[str, Depends(JWT.oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Login required",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT.SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    if not username == await database.Database().get_setting('account'):
        raise credentials_exception
    return True

@app.get('/api/admin')
async def is_admin(
    is_admin: Annotated[str, Depends(is_admin)]
):
    return is_admin

@app.get('/api/admin/items')
async def get_items(
    is_admin: Annotated[str, Depends(is_admin)],
    id: int = None,
    key: str = None):
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

@app.post('/api/admin/items')
async def add_items(
    is_admin: Annotated[str, Depends(is_admin)],
    key: str,
    name: str,
    icon: str,
    phone: str):
    await database.Database().add_object(
        key=key, name=name, icon=icon, phone=phone)

@app.patch('/api/admin/items')
async def update_items(
    is_admin: Annotated[str, Depends(is_admin)],
    id: int,
    key: str = None,
    name: str = None,
    icon: str = None,
    status: str = None,
    phone: int = None,
    lost_description: Optional[str] = None,
    find_ip: Optional[str] = None,
    lost_time: Optional[str] = None):
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

@app.delete('/api/admin/items')
async def delete_items(
    is_admin: Annotated[str, Depends(is_admin)],
    id: int):
    try:
        await database.Database().delete_object(id=id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    else:
        return DefaultResponse()