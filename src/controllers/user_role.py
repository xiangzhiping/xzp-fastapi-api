from fastapi import APIRouter, Request, Depends
from pydantic import BaseModel, Field, model_validator
from src.views.user_role import *
from typing import Literal
from src.examples.user_role import *
from config.constant import DATETIME

router = APIRouter(prefix='/user/role', tags=['用户角色管理'])


class UserRoleCreateReqBody(BaseModel):
    """用户角色新增请求体"""
    roleName: str = Field(..., title="角色名称", alias='role_name')
    roleLevel: int = Field(..., title="角色等级", alias='role_level')
    pathIds: list[int] | None = Field(None, title="path路径id列表", alias='path_ids')


@router.post(path='/create', name='用户角色新增', responses=UserRoleCreateExample)
async def UserRoleCreateController(rb: UserRoleCreateReqBody, req: Request):
    return await UserRoleCreateView(rb, req)()


class UserRoleDeleteReqBody(BaseModel):
    """用户角色删除请求体"""
    roleId: int = Field(..., title="角色id", alias='role_id')
    type: Literal[0, 1] = Field(..., title="删除类型（物理删除 1， 逻辑删除 0）", alias='type')


@router.delete(path='/delete', name='用户角色删除', responses=UserRoleDeleteExample)
async def UserRoleDeleteController(rb: UserRoleDeleteReqBody, req: Request):
    return await UserRoleDeleteView(rb, req)()


class UserRoleUpdateReqBody(BaseModel):
    """用户角色修改请求体"""
    roleId: int = Field(..., title="角色id", alias='role_id')
    roleName: str | None = Field(None, title="角色名称", alias='role_name')
    roleLevel: int | None = Field(None, title="角色等级", alias='role_level')
    pathIds: list[int] | None = Field(None, title="路径id列表", alias='path_ids')

    @model_validator(mode='after')
    def multiParamsAllNullValidator(cls, fields):
        """多参数全空值校验器"""
        if not any(tuple(dict(fields).values())[1:]):
            raise ValueError({
                'loc': ('role_name', 'role_level', 'path_ids'),
                'msg': 'cannot be null at the same time!',
                'type': 'value_error'
            })
        return fields


@router.patch(path='/update', name='用户角色修改', responses=UserRoleUpdateExample)
async def UserRoleUpdateController(rb: UserRoleUpdateReqBody, req: Request):
    return await UserRoleUpdateView(rb, req)()


class UserRoleGetReqBody(BaseModel):
    """用户角色查询请求体"""
    roleName: str | None = Field(None, title="角色名称", alias='role_name')
    roleLevel: int | None = Field(None, title="角色等级", alias='role_level')
    roleStatus: bool | None = Field(None, title="角色状态", alias='role_status')
    operatorId: int | None = Field(None, title="操作者ID", alias='operator_id')
    createDatetime: str | None = Field(None, title="创建日期时间范围", alias='create_datetime', pattern=DATETIME)
    updateDatetime: str | None = Field(None, title="更新日期时间范围", alias='update_datetime', pattern=DATETIME)
    deleteDatetime: str | None = Field(None, title="删除日期时间范围", alias='delete_datetime', pattern=DATETIME)
    numberPages: int = Field(1, title="当前页数", alias='number_pages')
    numberPieces: int = Field(100, title="显示条数", alias='number_pieces')


@router.get(path='/query', name='用户角色查询', responses=UserRoleGetExample)
async def UserRoleGetController(rb=Depends(UserRoleGetReqBody)):
    return await UserRoleGetView(rb)()


@router.get(path='/menu/query', name='用户角色枚举查询', responses=UserRoleGetExample)
async def UserRoleMenuGetController():
    return await UserRoleMenuGetView()()
