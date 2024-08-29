from asyncio import create_task
from json import loads, dumps
from time import perf_counter
from traceback import format_exc
from urllib.parse import unquote
from config.constant import GLOBAL_STORE, HTTP_STATUS_CODE_MEAN_MAP
from system.request_log_processor import srlp
from urllib.parse import unquote
from starlette.status import *
from starlette.middleware.base import BaseHTTPMiddleware
from system.response_rewriting import JsonResponse
from system.jwt_processor import jp
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware


class UserIdentityVerification(BaseHTTPMiddleware):
    """用户身份校验中间件"""

    async def dispatch(self, request, call_next) -> Response:
        try:
            request.state.user = {"start_time": perf_counter()}
            if request.scope.get("path") not in GLOBAL_STORE['NO_AUTHORIZATION_ACCESSIBLE_PATHS']:
                authorization = dict(request.scope.get('headers')).get(b'authorization')
                if authorization:
                    code, msg, data = await jp.jwtParser(authorization.decode('utf-8').split(" ")[-1])
                    if code == HTTP_200_OK:
                        request.state.user["user_id"] = data
                        return await call_next(request)
                    else:
                        return await JsonResponse(code, msg, data)
                else:
                    return await JsonResponse(HTTP_403_FORBIDDEN, '请求未携带身份凭证[authorization]!', 'AUTH_FAILED')
            else:
                return await call_next(request)
            # authorization = dict(request.scope.get('headers')).get(b'authorization')
            # print(authorization)
            # request.state.user = {"start_time": perf_counter(), "user_id": 7225449773631762432}
            # return await call_next(request)
        except Exception as err:
            return await JsonResponse(HTTP_500_INTERNAL_SERVER_ERROR, '身份校验失败!', format_exc())


class SystemResponseProcessor(BaseHTTPMiddleware):
    """系统响应处理中间件"""

    async def jsonResBuilder(self, request, code, msg, data):
        content = dumps({"code": code, "msg": msg, "data": data}).encode('utf-8')
        create_task(srlp.builder(request, code, msg, data))
        return Response(content=content, headers={"content-type": "application/json"})

    async def dispatch(self, request, call_next) -> Response:
        global res
        try:
            response, path = await call_next(request), request.scope.get("path")
            if path not in GLOBAL_STORE['SWAGGER_UI_PATHS']:
                code = response.status_code
                if response.headers.get("content-type") == "application/json":
                    async for chunk in response.body_iterator:
                        res = loads(chunk.decode('utf-8'))
                        break
                    if res:
                        msg = res.get("msg")
                        if msg:
                            return await self.jsonResBuilder(request, code, msg, res.get("data"))
                        else:
                            msg, data = HTTP_STATUS_CODE_MEAN_MAP.get(code, '未知状态信息!'), res.get("data")
                            return await self.jsonResBuilder(request, code, msg, data)
                    else:
                        msg = GLOBAL_STORE['ROUTERS_MAP'][path].get("name", path) + "操作成功!"
                        return await self.jsonResBuilder(request, code, msg, None)
                else:
                    msg = response.headers.get("file-name") + " 获取成功!"
                    create_task(srlp.builder(request, code, msg, None))
                    return response
            else:
                return response
        except Exception:
            create_task(srlp.builder(request, HTTP_500_INTERNAL_SERVER_ERROR, '系统响应处理失败!', format_exc()))
            return await JsonResponse(HTTP_500_INTERNAL_SERVER_ERROR, '系统响应处理失败!', format_exc())


middlewares = (
    UserIdentityVerification,
    SystemResponseProcessor,
    # 跨域中间件
    CORSMiddleware
)
