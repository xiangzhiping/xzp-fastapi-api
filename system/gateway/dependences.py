from traceback import format_exc
from fastapi import Request, Depends
from fastapi.security import HTTPBearer
from starlette.status import *
from config.constant import GLOBAL_STORE
from system.response_rewriting import JsonResponse


async def SwaggerUiAuthorizationVerification(authorization=Depends(HTTPBearer(auto_error=False))):
    pass


async def pathPermissionVerifier(path: str, userInfo: dict, roleInfo: dict) -> bool:
    paths, userPaths, rolePaths = [], userInfo.get("apiPaths"), roleInfo.get("apiPaths")
    pathId = GLOBAL_STORE["ReqPathIdMap"].get(path)
    if not pathId:
        return await JsonResponse(HTTP_404_NOT_FOUND, '无法匹配到请求路径ID, 请联系管理员!', None)
    if userPaths:
        paths.extend(userPaths)
    if rolePaths:
        paths.extend(rolePaths)
    if pathId in set(paths):
        return True
    return False


async def userPermissionsVerification(request: Request):
    try:
        path = request.scope.get('path')
        GLOBAL_STORE["user"][7130535699270471680] = {'role_id': 2, 'api_paths': [6, 7, 8, 9, 3, 4, 6]}
        GLOBAL_STORE["role"] = {1: {"role_level": 1}}
        if path not in GLOBAL_STORE.get("NoCheckPaths"):
            # print(GLOBAL_SHARE_RESOURCE)
            userId = request.state.user.get('userId')
            userInfo = GLOBAL_STORE.get('user').get(userId)
            # print(userId, userInfo)
            if userInfo:
                roleInfo = GLOBAL_STORE.get('role').get(userInfo.get("roleId"))
                # print(roleInfo)
                match roleInfo.get("roleLevel"):
                    case 1:
                        pass
                    case None:
                        msg, data = '未匹配到任何角色, 请联系管理员!', {"user_id": userId, "permission": userInfo}
                        return await JsonResponse(HTTP_404_NOT_FOUND, msg, data)
                    case _:
                        if await pathPermissionVerifier(path, userInfo, roleInfo):
                            pass
                        return await JsonResponse(HTTP_401_UNAUTHORIZED, '未获得当前资源访问权限!', None)
            return await JsonResponse(HTTP_404_NOT_FOUND, '未查到权限信息, 请重新登录!', None)
    except Exception as err:
        return await JsonResponse(HTTP_500_INTERNAL_SERVER_ERROR, '权限校验失败, 请联系管理员!', format_exc())


depends = (Depends(SwaggerUiAuthorizationVerification),)
# depends = ()
