from fastapi import APIRouter, Request, Depends
from src.examples.sys_api import *
from src.views.sys_api import *
from pydantic import BaseModel, Field, model_validator
from config.constant import DATETIME
from typing import Literal

router = APIRouter(prefix='/sys/api', tags=['系统接口管理'])


class SystemApiCreateReqBody(BaseModel):
    """系统接口新增请求体"""
    apiName: str = Field(..., title="接口名称", alias="api_name")
    apiPath: str = Field(..., title="接口路径", alias="api_path")
    apiType: str = Field(..., title="接口类型", alias="api_type")
    reqMethod: str | None = Field(None, title="请求方式", alias="req_method")
    tagName: str | None = Field(None, title="接口标签名称", alias="tag_name")
    tagPath: str | None = Field(None, title="接口标签路径", alias="tag_path")
    authAccess: Literal[0, 1] = Field(None, title="登录访问", alias='auth_access')


@router.post(path='/create', name='系统接口新增', responses=SystemApiCreateExample)
async def SystemApiCreateController(rb: SystemApiCreateReqBody, req: Request):
    return await SystemApiCreateView(rb, req)()


class SystemApiDeleteReqBody(BaseModel):
    """系统删除请求体"""
    apiId: int = Field(..., title="系统接口id", alias="api_id")


@router.delete(path='/delete', name='系统接口删除', responses=SystemApiDeleteExample)
async def SystemApiDeleteController(rb: SystemApiDeleteReqBody, req: Request):
    return await SystemApiDeleteView(rb, req)()


class SystemApiUpdateReqBody(BaseModel):
    """系统接口更新请求体"""
    apiId: int = Field(..., title="接口id", alias="api_id")
    apiName: str | None = Field(None, title="接口名称", alias="api_name")
    apiPath: str | None = Field(None, title="接口路径", alias="api_path")
    apiType: str | None = Field(None, title="接口类型", alias="api_type")
    reqMethod: str | None = Field(None, title="请求方式", alias="req_method")
    tagName: str | None = Field(None, title="接口标签名称", alias="tag_name")
    tagPath: str | None = Field(None, title="接口标签路径", alias="tag_path")

    @model_validator(mode='after')
    def multiParamsAllNullValidator(cls, fields):
        """多参数全空值校验器"""
        vs = tuple(dict(fields).values())[1:]
        if not any(vs):
            raise ValueError({
                'loc': vs,
                'msg': 'cannot be null at the same time!',
                'type': 'value_error'
            })
        return fields


@router.patch(path='/update', name='系统接口更新', responses=SystemApiUpdateExample)
async def SystemApiUpdateController(rb: SystemApiUpdateReqBody, req: Request):
    return await SystemApiUpdateView(rb, req)()


class SystemApisGetReqBody(BaseModel):
    """系统接口列表查询请求体"""
    apiName: str | None = Field(None, title="接口名称", alias="api_name")
    tagName: str | None = Field(None, title="接口标签名称", alias="tag_name")
    apiType: str | None = Field(None, title="接口类型", alias="api_type")
    reqMethod: str | None = Field(None, title="请求体名称", alias="req_method")
    authAccess: int | None = Field(None, title="登录访问", alias='auth_access', ge=0, le=1)
    dataStatus: int | None = Field(None, title="接口状态", alias='data_status', ge=0, le=1)
    cts: str | None = Field(None, title="创建时间起始", alias='create_time_start', pattern=DATETIME)
    cte: str | None = Field(None, title="创建时间结束", alias='create_time_end', pattern=DATETIME)
    uts: str | None = Field(None, title="更新时间起始", alias='update_time_start', pattern=DATETIME)
    ute: str | None = Field(None, title="更新时间结束", alias='update_time_end', pattern=DATETIME)
    dts: str | None = Field(None, title="删除时间起始", alias='delete_time_start', pattern=DATETIME)
    dte: str | None = Field(None, title="删除时间结束", alias='delete_time_end', pattern=DATETIME)
    numberPages: int = Field(1, title="当前页数", alias='number_pages')
    numberPieces: int = Field(100, title="显示条数", alias='number_pieces')


@router.get(path='/get', name='系统接口列表查询', responses=SystemApisGetExample)
async def SystemApisGetController(rb=Depends(SystemApisGetReqBody)):
    return await SystemApisGetView(rb)()


class AuthAccessReqBody(BaseModel):
    """系统接口登录访问更改请求体"""
    apiId: int = Field(..., title="接口id", alias="api_id")
    authAccess: Literal[0, 1] = Field(..., title="身份校验访问", alias="auth_access")


@router.patch(path='/auth/access/update', name='系统接口身份校验访问修改', responses=SystemApiAuthAccessExample)
async def SystemApiAuthAccessController(rb: AuthAccessReqBody, req: Request):
    return await SystemApiAuthAccessView(rb, req)()
