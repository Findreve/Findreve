from fastapi import APIRouter
from model.response import DefaultResponse
from pkg import conf

Router = APIRouter(prefix='/api/site', tags=['站点 Site'])

@Router.get(
    path='/ping',
    summary='站点健康检查',
    description='检查站点是否在线',
    response_model=DefaultResponse,
    response_description='站点在线'
)
async def ping():
    """
    站点健康检查接口。

    :return: Findreve 版本号
    """
    return DefaultResponse(data=conf.VERSION)