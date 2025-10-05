from fastapi import APIRouter
from fastapi import Depends
from model.response import DefaultResponse

from middleware.admin import is_admin
        

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