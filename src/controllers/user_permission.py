from fastapi import APIRouter, Request, Depends
from pydantic import BaseModel, Field, model_validator
from src.views.user_permission import *
from src.examples.user_permission import *
from config.constant import DATETIME

router = APIRouter(prefix='/user/permission', tags=['用户权限管理'])


class UserPermissionCreateReqBody(BaseModel):
    """用户权限新增请求体"""
    userId: int = Field(..., title="用户id", alias="user_id")
    roleId: int = Field(..., title="角色id", alias="role_id")
    paths: list[int] | None = Field(default=None, title="角色路径id列表", alias="paths")


@router.post(path='/create', name='用户权限新增', responses=UserPermissionCreateExample)
async def UserPermissionCreateController(rb: UserPermissionCreateReqBody, req: Request):
    return await UserPermissionCreateView(rb, req)()


class UserPermissionUpdateReqBody(BaseModel):
    """用户权限修改请求体"""
    userId: int = Field(..., title="用户id", alias="user_id")
    roleId: int | None = Field(..., title="角色id", alias="role_id")
    paths: list[int] | None = Field(default=None, title="角色路径id列表", alias="paths")

    @model_validator(mode='after')
    def multiParamsAllNullValidator(cls, fields):
        """多参数全空值校验器"""
        values = tuple(dict(fields).values())[1:]
        if not any(values):
            raise ValueError({
                'loc': values,
                'msg': 'cannot be null at the same time!',
                'type': 'value_error'
            })
        return fields


@router.patch(path='/update', name='用户权限修改', responses=UserPermissionUpdateExample)
async def UserPermissionUpdateController(rb: UserPermissionUpdateReqBody, req: Request):
    return await UserPermissionUpdateView(rb, req)()


class UserPermissionGetReqBody(BaseModel):
    """用户权限信息查询请求体"""
    userId: int | None = Field(None, title="用户id", alias="user_id")
    dataStatus: int | None = Field(None, title="角色状态", alias='data_status', ge=0, le=1)
    operator: int | None = Field(None, title="操作者", alias='operator')
    cts: str | None = Field(None, title="创建时间起始", alias='create_time_start', pattern=DATETIME)
    cte: str | None = Field(None, title="创建时间结束", alias='create_time_end', pattern=DATETIME)
    uts: str | None = Field(None, title="更新时间起始", alias='update_time_start', pattern=DATETIME)
    ute: str | None = Field(None, title="更新时间结束", alias='update_time_end', pattern=DATETIME)
    dts: str | None = Field(None, title="删除时间起始", alias='delete_time_start', pattern=DATETIME)
    dte: str | None = Field(None, title="删除时间结束", alias='delete_time_end', pattern=DATETIME)
    numberPages: int = Field(1, title="当前页数", alias='number_pages')
    numberPieces: int = Field(100, title="显示条数", alias='number_pieces')


@router.get(path='/query', name='用户权限查询', responses=UserPermissionGetExample)
async def UserPermissionGetController(rb=Depends(UserPermissionGetReqBody)):
    return await UserPermissionGetView(rb)()
