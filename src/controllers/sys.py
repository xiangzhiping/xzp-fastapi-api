from fastapi import APIRouter, Query
from pydantic import BaseModel, Field
from typing import Literal
from src.views.sys import *
from src.examples.sys import *

router = APIRouter(prefix='/sys', tags=['系统管理'])


@router.get(path='/image/captcha/id/get', name='图像验证码id获取', responses=ImageCaptchaIdGetExample)
async def ImageCaptchaIdGetController():
    return await ImageCaptchaIdGetView()()


@router.get(path='/image/captcha/image/get', name='图像验证码图像获取', responses=ImageCaptchaImageGetExample)
async def ImageCaptchaImageGetController(captchaId: str = Query(..., title="图形验证码id", alias='captcha_id')):
    return await ImageCaptchaImageGetView(captchaId)()


class IdentityCaptchaSendReqBody(BaseModel):
    account: str = Field(..., title="账号名（电话/邮箱）", alias='account')
    scene: Literal['login', 'register'] = Field(..., title="操作场景（login/register）", alias='scene')
    type: Literal['email', 'phone'] = Field(..., title="账号类型（email/phone）", alias='type')


@router.post("/identity/captcha/send", summary="身份验证码发送", responses=IdentityCaptchaSendExample)
async def IdentityCaptchaSendController(rb: IdentityCaptchaSendReqBody):
    return await IdentityCaptchaSendView(rb)()
