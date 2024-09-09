from traceback import format_exc
from datetime import datetime
from json import loads, dumps
from config.constant import GLOBAL_STORE, SNOWFLAKE_ID_GENERATORS
from src.models.user import *
from system.orms.aio_redis_orm import aro
from system.orms.aio_mysql_orm import amo
from system.response_rewriting import JsonResponse, HttpException
from utils.bcrypt_cipher import BcryptCipher
from system.jwt_processor import jp
from system.request_log_processor import srlp
from itertools import zip_longest
from config.constant import TIME_FIELD_MAP


class UserRegisterView:
    def __init__(self, rb, req):
        self.rb = rb
        self.req = req

    async def __call__(self):
        try:
            account, password, captcha, atype = dict(self.rb).values()
            captchaStr = await aro.get(account)
            if captchaStr:
                if int(captchaStr) == captcha:
                    userId, password = await SNOWFLAKE_ID_GENERATORS[0].nextid(), await BcryptCipher(password)
                    if atype == "email":
                        await UserRegisterModel.emailRegister(userId, account, password)
                    else:
                        await UserRegisterModel.phoneRegister(userId, account, password)
                    return await JsonResponse(HTTP_200_OK, '注册成功', None)
                else:
                    return await JsonResponse(HTTP_400_BAD_REQUEST, '验证码错误', None)
            else:
                return await JsonResponse(HTTP_400_BAD_REQUEST, '验证码已过期', None)
        except Exception:
            raise HttpException(HTTP_500_INTERNAL_SERVER_ERROR, '注册失败', format_exc())


class UserLoginAccountPasswordView:

    def __init__(self, rb=None, req=None, bt=None):
        self.rb = rb
        self.req = req
        self.bt = bt

    async def loginFailProcessor(self, ip, code, msg, data, userId):
        await UserLoginAccountPasswordModel.loginLogsCreate(ip, 0, code, msg, data, userId)
        return await JsonResponse(code, msg, data)

    async def userLoginBackTask(self, ip, code, msg, data, userId):
        try:
            await UserLoginAccountPasswordModel.loginLogsCreate(ip, 1, code, msg, data, userId)
            await UserLoginAccountPasswordModel.loginUserUpdate(userId)
            permission = await UserLoginAccountPasswordModel.userPermissionGet(userId)
            if permission:
                roleId, pps = permission.get('role_id'), permission.get('paths')
                role = await UserLoginAccountPasswordModel.userRoleGet(roleId)
                if role:
                    prs, rps = [], role.get('paths')
                    if pps:
                        prs += pps
                    if rps:
                        prs += rps
                    levelPaths = {
                        "level": role.get('role_level'),
                        "paths": list(set(prs)) if prs else None
                    }
                else:
                    levelPaths = {"level": None, "paths": loads(pps)}
            else:
                levelPaths = {"level": None, "paths": None}
            GLOBAL_STORE["USER"][userId] = levelPaths
        except Exception:
            msg = f"用户ID为 {userId} 的登录后台任务失败"
            await srlp.builder(self.req, HTTP_500_INTERNAL_SERVER_ERROR, msg, format_exc())

    async def __call__(self):
        global host, account, user
        try:
            host = ":".join(str(item) for item in self.req.client)
            account, password, captchaId, captcha = tuple(dict(self.rb).values())
            cache = await aro.get(captchaId)
            if cache:
                if cache == captcha.lower():
                    password = await BcryptCipher(password)
                    if '@' in account:
                        user = await UserLoginAccountPasswordModel.emailLogin(account, password)
                    else:
                        user = await UserLoginAccountPasswordModel.phoneLogin(account, password)
                    if user:
                        if user.get('user_status') == 1:
                            if user.get('account_status') == 1:
                                userId, code, msg = user.get("user_id"), HTTP_200_OK, '登录成功'
                                self.bt.add_task(self.userLoginBackTask, host, code, msg, None, userId)
                                return await JsonResponse(code, msg, await jp.jwtCipher(userId))
                            else:
                                code, msg = HTTP_403_FORBIDDEN, '账号已失效'
                                return await self.loginFailProcessor(host, code, msg, None, account)
                        else:
                            code, msg = HTTP_410_GONE, '账号已删除'
                            return await self.loginFailProcessor(host, code, msg, None, account)
                    else:
                        code, msg = HTTP_401_UNAUTHORIZED, '账号名或密码错误'
                        return await self.loginFailProcessor(host, code, msg, None, account)
                else:
                    code, msg = HTTP_400_BAD_REQUEST, '图形验证码输入错误，请重新输入'
                    return await self.loginFailProcessor(host, code, msg, None, account)
            else:
                code, msg = HTTP_400_BAD_REQUEST, '图形验证码已过期，请重新生成'
                return await self.loginFailProcessor(host, code, msg, None, account)
        except Exception:
            try:
                code, msg = HTTP_500_INTERNAL_SERVER_ERROR, '登录失败'
                return await self.loginFailProcessor(host, code, msg, format_exc(), account)
            except Exception:
                raise HttpException(HTTP_500_INTERNAL_SERVER_ERROR, '登录失败日志记录失败', format_exc())


class UserCaptchaLoginView:
    def __init__(self, rb, req, bt):
        self.rb = rb
        self.req = req
        self.bt = bt
        self.names = {"email": "邮箱", "phone": "短信"}

    async def __call__(self):
        global host, userLogin, account
        try:
            host, account, atype, captcha = [":".join(str(c) for c in self.req.client)] + list(dict(self.rb).values())
            userLogin, cacheStr = UserLoginAccountPasswordView(), await aro.get(account)
            if cacheStr:
                if captcha == int(cacheStr):
                    if atype == "email":
                        user = await UserCaptchaLoginModel.emailLogin(account)
                    else:
                        user = await UserCaptchaLoginModel.phoneLogin(account)
                    if user:
                        if user.get('user_status') == 1:
                            if user.get('account_status') == 1:
                                userId, code, msg = user.get("user_id"), HTTP_200_OK, '登录成功'
                                self.bt.add_task(userLogin.userLoginBackTask, host, code, msg, None, userId)
                                return await JsonResponse(code, msg, await jp.jwtCipher(userId))
                            else:
                                code, msg = HTTP_403_FORBIDDEN, '账号已失效'
                                return await userLogin.loginFailProcessor(host, code, msg, None, account)
                        else:
                            code, msg = HTTP_410_GONE, '账号已删除'
                            return await userLogin.loginFailProcessor(host, code, msg, None, account)
                    else:
                        code, msg = HTTP_401_UNAUTHORIZED, f'此{self.names[opeType]}未注册'
                        return await userLogin.loginFailProcessor(host, code, msg, None, account)
                else:
                    code, msg = HTTP_400_BAD_REQUEST, '验证码错误'
                    return await userLogin.loginFailProcessor(host, code, msg, None, account)
            else:
                code, msg = HTTP_400_BAD_REQUEST, '验证码已过期'
                return await userLogin.loginFailProcessor(host, code, msg, None, account)
        except Exception:
            try:
                code, msg = HTTP_500_INTERNAL_SERVER_ERROR, '登录失败'
                return await userLogin.loginFailProcessor(host, code, msg, format_exc(), account)
            except Exception:
                raise HttpException(HTTP_500_INTERNAL_SERVER_ERROR, '登录失败日志记录失败', format_exc())


class UserAccountCancellationView:
    def __init__(self, rb, req):
        self.rb = rb
        self.req = req

    @amo.aioMysqlOrmTransactional
    async def __call__(self, conn):
        try:
            account, type, captcha, userId = list(dict(self.rb).values()) + [self.req.state.user.get("user_id")]
            cache = await aro.get(account)
            if cache:
                if cache == captcha:
                    if type == "email":
                        await UserAccountCancellationModel.userEmailCancellation(userId, account, conn)
                        return await JsonResponse(HTTP_200_OK, '账号注销成功', None)
                    else:
                        await UserAccountCancellationModel.userPhoneCancellation(userId, account, conn)
                        return await JsonResponse(HTTP_200_OK, '账号注销成功', None)
                else:
                    code, msg = HTTP_400_BAD_REQUEST, '验证码错误'
                    return await userLogin.loginFailProcessor(host, code, msg, None, account)
            else:
                code, msg = HTTP_400_BAD_REQUEST, '验证码已过期'
                return await userLogin.loginFailProcessor(host, code, msg, None, account)
        except Exception:
            raise HttpException(HTTP_500_INTERNAL_SERVER_ERROR, '账号注销失败', format_exc())


class UserAccountStatusUpdateView:
    def __init__(self, rb, req):
        self.req = req
        self.rb = rb
        self.types = {True: '启用', False: '禁用'}

    @amo.aioMysqlOrmTransactional
    async def __call__(self, conn):
        global opeType
        try:
            userId, opeType, operator = list(dict(self.rb).values()) + [self.req.state.user.get("user_id")]
            if (await UserAccountStatusUpdateModel.userStatusGet(conn, userId)).get('user_status'):
                await UserAccountStatusUpdateModel.userAccountStatusUpdate(conn, userId, opeType, operator,
                                                                           datetime.now())
                return await JsonResponse(HTTP_200_OK, f'用户账号{self.types[opeType]}成功!', None)
            else:
                return await JsonResponse(HTTP_403_FORBIDDEN, f'用户已注销账号，此操作无效', None)
        except Exception:
            print(f'用户账号{self.types[opeType]}失败!')
            raise HttpException(HTTP_500_INTERNAL_SERVER_ERROR, f'用户账号{self.types[opeType]}失败', format_exc())


class UserPasswordRetrievalView:
    def __init__(self, rb):
        self.rb = rb

    async def __call__(self):
        try:
            account, newpassword, captcha, atype = list(dict(self.rb).values())
            captchaStr = await aro.get(account)
            if captchaStr:
                if int(captchaStr) == captcha:
                    if atype == "email":
                        await UserPasswordRetrievalModel.viaEmailResetPassword(await BcryptCipher(newpassword), account)
                        return await JsonResponse(HTTP_200_OK, '密码重置成功', None)
                    else:
                        await UserPasswordRetrievalModel.viaPhonResetPassword(await BcryptCipher(newpassword), account)
                        return await JsonResponse(HTTP_200_OK, '密码重置成功', None)
                else:
                    return await JsonResponse(HTTP_400_BAD_REQUEST, '验证码错误', None)
            else:
                return await JsonResponse(HTTP_400_BAD_REQUEST, '验证码已过期', None)
        except Exception:
            raise HttpException(HTTP_500_INTERNAL_SERVER_ERROR, '密码重置失败', format_exc())


class UserLogOutView:

    def __init__(self, req, bt):
        self.req = req
        self.bt = bt

    async def userLogoutBackTask(self, userId):
        try:
            await UserLogoutModel.logoutUserUpdate(userId)
            del GLOBAL_STORE["USER"][userId]
        except Exception:
            msg = f"用户id为 {userId} 的登出成功后台任务执行失败"
            await srlp.builder(self.request, HTTP_500_INTERNAL_SERVER_ERROR, msg, format_exc())

    async def __call__(self):
        try:
            userId = self.req.state.user.get("user_id")
            self.bt.add_task(self.userLogoutBackTask, userId)
            return await JsonResponse(HTTP_200_OK, "登出成功", await jp.jwtCipher(userId, False))
        except Exception:
            raise HttpException(HTTP_500_INTERNAL_SERVER_ERROR, '登出失败', format_exc())


class UserQueryView:
    def __init__(self, rb):
        self.rb = rb

    async def __call__(self):
        try:
            conditions, params, reqs = [], [], tuple(self.rb.dict(by_alias=True).items())
            for key, value in reqs[0:2]:
                if value is not None:
                    conditions.append(f"{key} LIKE %s")
                    params.append(f"{value}%")
            for key, value in reqs[2:5]:
                if value is not None:
                    conditions.append(f"{key} = %s")
                    params.append(value)
            for key, value in reqs[5:-2]:
                if value is not None:
                    conditions.append(f"{key} >= %s and {key} <= %s")
                    params.extend(value.split(', '))
                    continue
            totalStr = f" WHERE {" AND ".join(conditions)}" if conditions else ""
            total = await UserQueryModel.userTotalQuery(totalStr, params)
            numbers = [r[1] for r in reqs[-2:]]
            params.extend([(numbers[0] - 1) * numbers[1], numbers[1]])
            users = await UserQueryModel.userQuery(f"{totalStr} limit %s, %s" if totalStr else " limit %s, %s", params)
            if total[0] != 0:
                for user in users:
                    user['login_status'] = True if user.get("login_status") == 1 else False
                    user["account_status"] = True if user.get("account_status") == 1 else False
                    user['user_status'] = True if user.get("user_status") == 1 else False
                return await JsonResponse(HTTP_200_OK, "用户列表查询成功!", {'total': total[0], 'users': users})
            else:
                return await JsonResponse(HTTP_204_NO_CONTENT, "没有符合条件的数据!", {'total': 0, 'users': ()})
        except Exception:
            raise HttpException(HTTP_500_INTERNAL_SERVER_ERROR, '用户列表查询失败!', format_exc())


class UserMenuGetView:
    async def __call__(self):
        try:
            menu = {
                'login_states': [
                    {'label': '全部', 'value': None},
                    {'label': '在线', 'value': True},
                    {'label': '离线', 'value': False},
                ],
                'account_states': [
                    {'label': '全部', 'value': None},
                    {'label': '有效', 'value': True},
                    {'label': '无效', 'value': False},
                ]
            }
            return await JsonResponse(HTTP_200_OK, "用户枚举查询成功", menu)
        except Exception:
            raise HttpException(HTTP_500_INTERNAL_SERVER_ERROR, '用户枚举查询失败', format_exc())
