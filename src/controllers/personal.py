from typing import Literal
from fastapi import APIRouter, Request, File, UploadFile
from src.views.personal import *
from src.examples.personal import *
from pydantic import BaseModel, Field

router = APIRouter(prefix='/personal', tags=['个人管理'])


@router.post(path='/avatar/upload', name='个人头像上传', responses=PersonalAvatarUploadExample)
async def PersonalAvatarUploadController(req: Request, avatar: UploadFile = File(..., alias='avatar', title='头像数据')):
    return await PersonalAvatarUploadView(req, avatar)()


@router.post(path='/avatar/delete', name='个人头像删除', responses=PersonalAvatarDeleteExample)
async def UserAvatarUploadController(req: Request):
    return await PersonalAvatarDeleteView(req)()


@router.get(path='/avatar/download/link/get', name='个人头像下载链接获取',
            responses=PersonalAvatarDownloadLinkGetExample)
async def UserAvatarDownloadLinkGetController(req: Request):
    return await UserAvatarDownloadLinkGetView(req)()


class PersonalInfoUpdateReqBody(BaseModel):
    """个人信息修改请求体"""
    key: Literal['username', 'phone', 'email'] = Field(..., title="修改的字段名称", alias='key')
    value: str = Field(..., title="修改的字段值", alias='value')


@router.patch(path='/update', name='个人信息修改', responses=PersonalInfoUpdateExample)
async def PersonalInfoUpdateController(rb: PersonalInfoUpdateReqBody, req: Request):
    return await PersonalInfoUpdateView(rb, req)()


@router.get(path='/query', name='个人信息查询', responses=PersonalInfoGetExample)
async def PersonalInfoGetController(req: Request):
    return await PersonalInfoGetView(req)()
