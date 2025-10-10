# 导入库
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel.ext.asyncio.session import AsyncSession

from model import database
from model.response import TokenResponse
from services import session as session_service

Router = APIRouter(tags=["令牌 session"])

# FastAPI 登录路由 / FastAPI login route
@Router.post(
    path="/api/token",
    summary="获取访问令牌",
    description="使用用户名和密码获取访问令牌",
    response_model=TokenResponse,
    response_description="访问令牌"
)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[AsyncSession, Depends(database.Database.get_session)],
) -> TokenResponse:
    token_response = await session_service.login_for_access_token(
        session=session,
        username=form_data.username,
        password=form_data.password,
    )
    if not token_response:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return token_response
