from typing import Literal
from fastapi import APIRouter, Request, BackgroundTasks, Depends
from src.views.user import *
from config.constant import DATETIME
from pydantic import BaseModel, Field, constr
from src.examples.user import *

router = APIRouter(prefix='/user', tags=['用户管理'])


class UserRegisterReqBody(BaseModel):
    account: str = Field(..., title="账号名（电话/邮箱）", alias='account', max_length=50)
    password: constr(strip_whitespace=True, min_length=8) = Field(..., title="密码", alias='password')
    captcha: int = Field(..., title="邮箱或短信验证码", alias='captcha')
    type: Literal['email', 'phone'] = Field(..., title="账号类型（email/phone）", alias='type')


@router.post(path='/register', name='用户注册', responses=UserRegisterExample)
async def UserRegisterController(rb: UserRegisterReqBody, req: Request):
    return await UserRegisterView(rb, req)()


class UserLoginAccountPasswordReqBody(BaseModel):
    account: str = Field(..., title="账号名（电话/邮箱）", alias='account')
    password: str = Field(..., title="密码", alias='password')
    captchaId: str = Field(..., title="图形验证码id", alias='captcha_id')
    captcha: str = Field(..., title="图形验证码", alias='captcha')


@router.post(path='/login/account/password', name='用户账号密码登录', responses=UserLoginAccountPasswordExample)
async def UserLoginAccountPasswordController(req: Request, bt: BackgroundTasks, rb: UserLoginAccountPasswordReqBody):
    return await UserLoginAccountPasswordView(rb, req, bt)()


class UserLoginCaptchaReqBody(BaseModel):
    account: str = Field(..., title="账号名（电话/邮箱）", alias='account')
    type: Literal['email', 'phone'] = Field(..., title="账号类型（email/phone）", alias='type')
    captcha: int = Field(..., title="邮箱或短信验证码", alias='captcha')


@router.post(path='/login/captcha', name='用户验证码登录', responses=UserLoginCaptchaExample)
async def UserCaptchaLoginController(rb: UserLoginCaptchaReqBody, req: Request, bt: BackgroundTasks):
    return await UserCaptchaLoginView(rb, req, bt)()


class UserAccountCancellationReqBody(BaseModel):
    account: str = Field(..., title="账号名（电话/邮箱）", alias='account')
    type: Literal['email', 'phone'] = Field(..., title="账号类型（电话/邮箱）", alias='type')
    captcha: str = Field(..., title="短信或者邮箱验证码", alias='captcha')


@router.delete(path='/account/cancellation', name='用户账号注销', responses=UserAccountCancellationExample)
async def UserAccountCancellationController(rb: UserAccountCancellationReqBody, req: Request):
    return await UserAccountCancellationView(rb, req)()


class UserAccountStatusUpdateReqBody(BaseModel):
    """用户账号状态更新请求体"""
    userId: int = Field(..., title="需要更改的账号状态用户id", alias='user_id')
    state: bool = Field(..., title="更新类型（有效 true， 无效 false）", alias='state')


@router.patch(path='/account/status/update', name='用户账号状态更改', responses=UserAccountStatusUpdateExample)
async def UserAccountStatusUpdateController(rb: UserAccountStatusUpdateReqBody, req: Request):
    return await UserAccountStatusUpdateView(rb, req)()


class UserPasswordForgetReqBody(BaseModel):
    account: str = Field(..., title="账号名（电话/邮箱）", alias='account')
    newpassword: str = Field(..., title="新密码", alias='new_password')
    captcha: int = Field(..., title="短信或者邮箱验证码", alias='captcha')
    atype: Literal['email', 'phone'] = Field(..., title="账号类型（电话/邮箱）", alias='type')


@router.patch(path='/password/retrieval', name='密码找回', responses=UserPasswordRetrievalExample)
async def UserPasswordRetrievalController(rb: UserPasswordForgetReqBody):
    return await UserPasswordRetrievalView(rb)()


@router.post(path='/logout', name='用户登出', responses=UserLogoutExample)
async def USerLogOutController(req: Request, bt: BackgroundTasks):
    return await UserLogOutView(req, bt)()


class UserQueryReqBody(BaseModel):
    phone: str | None = Field(None, title="用户电话", alias='phone')
    email: str | None = Field(None, title="用户邮箱", alias='email')
    loginStatus: bool | None = Field(None, title="登录状态", alias='login_status')
    accountStatus: bool | None = Field(None, title="账号状态", alias='account_status')
    userStatus: bool | None = Field(None, title="用户状态", alias='user_status')
    loginDatetime: str | None = Field(None, title="登录日期时间范围", alias='login_datetime', pattern=DATETIME)
    logoutDatetime: str | None = Field(None, title="登出日期时间范围", alias='logout_datetime', pattern=DATETIME)
    createDatetime: str | None = Field(None, title="创建日期时间范围", alias='create_datetime', pattern=DATETIME)
    updateDatetime: str | None = Field(None, title="更新日期时间范围", alias='update_datetime', pattern=DATETIME)
    deleteDatetime: str | None = Field(None, title="删除日期时间范围", alias='delete_datetime', pattern=DATETIME)
    numberPages: int = Field(1, title="当前页数", alias='number_pages')
    numberPieces: int = Field(100, title="显示条数", alias='number_pieces')


@router.get(path='/query', name='用户查询', responses=UserQueryExample)
async def UserQueryController(rb=Depends(UserQueryReqBody)):
    return await UserQueryView(rb)()


@router.get(path='/menu/query', name='用户枚举查询', responses=UserQueryExample)
async def UserMenuGetController():
    return await UserMenuGetView()()
