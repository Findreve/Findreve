from nicegui import app
from typing import Annotated
from fastapi import Depends
from fastapi import HTTPException, status
from jwt import InvalidTokenError
import jwt, JWT
from model import database
from model import token as Token
from model.response import DefaultResponse

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
    token_data = Token.TokenData(username=username)
    return True

@app.get('/api/items')
async def get_items(
    is_admin: Annotated[str, Depends(is_admin)],
    id: int = None,
    key: str = None):
    items = await database.Database().get_object(id=id, key=key)
    return DefaultResponse(data=items)

@app.post('/api/items')
async def add_items(
    is_admin: Annotated[str, Depends(is_admin)],
    key: str,
    name: str,
    icon: str,
    phone: str):
    try:
        await database.Database().add_object(
            key=key, name=name, icon=icon, phone=phone)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    else:
        return DefaultResponse()

@app.patch('/api/items')
async def update_items(
    is_admin: Annotated[str, Depends(is_admin)],
    id: int,
    **kwargs):
    try:
        await database.Database().update_object(
            id=id, **kwargs)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    else:
        return DefaultResponse()

@app.delete('/api/items')
async def delete_items(
    is_admin: Annotated[str, Depends(is_admin)],
    id: int):
    try:
        await database.Database().delete_object(id=id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    else:
        return DefaultResponse()