from json import dumps, loads
from datetime import datetime
from traceback import format_exc
from starlette.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR
from src.models.user_permission import *
from system.orms.aio_mysql_orm import amo
from itertools import zip_longest
from system.response_rewriting import JsonResponse, HttpException


class UserPermissionCreateView:
    def __init__(self, rb, req):
        self.rb = rb
        self.req = req

    async def __call__(self):
        try:
            userId, roleId, paths, operator = dict(self.rb).values() + [self.req.state.user.get("userId")]
            rps = loads(await UserPermissionCreateModel.userRolePathsGet(roleId))
            prps = dumps([path for path in paths]) if paths and any(path not in rps for path in paths) else None
            await UserPermissionCreateModel.userPermissionCreate(userId, roleId, prps, operator)
            return await JsonResponse(HTTP_200_OK, '用户权限创建成功', None)
        except Exception:
            raise HttpException(HTTP_500_INTERNAL_SERVER_ERROR, '用户权限创建失败', format_exc())


class UserPermissionUpdateView:
    def __init__(self, rb, req):
        self.rb = rb
        self.req = req

    async def __call__(self):
        try:
            reqs, conditions, params = tuple(self.rb.dict(by_alias=True).items()), [], []
            permissions = await UserPermissionUpdateModel.userPermissionGet(reqs[0][1])
            if permissions:
                for key, value in reqs[1:]:
                    if value is not None:
                        if key != "paths":
                            conditions.append(f"{key}=%s")
                            params.append(value)
                        else:
                            conditions.append(f"{key}=%s")
                            pathIds = permissions.get("paths")
                            value = value + loads(pathIds) if pathIds else value if value else pathIds
                            params.append(dumps(tuple(set(value))))
                params.extend([self.req.state.user.get("user_id"), datetime.now(), reqs[0][1]])
                await UserPermissionUpdateModel.userPermissionUpdate(", ".join(conditions), params)
                return await JsonResponse(HTTP_200_OK, '用户权限更新成功!', None)
            else:
                return await JsonResponse(HTTP_200_OK, '用户权限不存在!', None)
        except Exception:
            raise HttpException(HTTP_500_INTERNAL_SERVER_ERROR, '用户权限更新失败', format_exc())


class UserPermissionGetView:
    def __init__(self, rb):
        self.rb = rb

    async def __call__(self):
        try:
            conditions, params, reqs = [], [], tuple(self.rb.dict(by_alias=True).items())
            for key, value in reqs[0:1]:
                if value is not None:
                    conditions.append(f"{key} = %s")
                    params.append(value)
            times = reqs[1:-2]
            for tr in zip_longest(times[::2], times[1::2]):
                ts, te = tr
                tsz, tez, tso, teo = ts[0], te[0], ts[1], te[1]
                if tso is not None and teo is not None:
                    conditions.append(f"%s <= {TIME_FIELD_MAP[tsz]} <= %s")
                    params.extend([tso, teo])
                    continue
                if tso is not None:
                    conditions.append(f"{TIME_FIELD_MAP[tsz]} >= %s")
                    params.append(tso)
                    continue
                if teo is not None:
                    conditions.append(f"{TIME_FIELD_MAP[tez]} <= %s")
                    params.append(teo)
                    continue
            numbers = [r[1] for r in reqs[-2:]]
            params.extend([(numbers[0] - 1) * numbers[1], numbers[1]])
            cs = f" WHERE {" AND ".join(conditions)} limit %s, %s" if conditions else " limit %s, %s"
            permissions = await UserPermissionsGetModel.UserPermissionsGet(cs, params)
            total = len(permissions)
            if total == 0:
                return await JsonResponse(HTTP_204_NO_CONTENT, "没有符合条件的数据!", {'total': 0, 'roles': ()})
            else:
                for permission in permissions:
                    paths = permission.get("paths")
                    permission['paths'] = loads(paths) if paths else paths
                return await JsonResponse(HTTP_200_OK, "用户权限列表查询成功!",
                                          {'total': total, 'permissions': permissions})
        except Exception:
            raise HttpException(HTTP_500_INTERNAL_SERVER_ERROR, '用户权限列表查询失败', format_exc())
