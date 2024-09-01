from json import dumps, loads
from traceback import format_exc
from starlette.status import *
from datetime import datetime
from src.models.user_role import *
from itertools import zip_longest
from system.response_rewriting import JsonResponse, HttpException


class UserRoleCreateView:
    def __init__(self, rb, req):
        self.rb = rb
        self.req = req

    async def __call__(self):
        try:
            roleName, roleLevel, apiTabs = dict(self.rb).values()
            print(roleName, roleLevel, apiTabs)
            pathIds, userId = dumps(apiTabs) if apiTabs else None, self.req.state.user.get("user_id")
            await UserRoleCreateModel.userRoleCreate(roleName, roleLevel, pathIds, userId)
            return await JsonResponse(HTTP_200_OK, '用户角色创建成功', None)
        except Exception:
            raise HttpException(HTTP_500_INTERNAL_SERVER_ERROR, '用户角色创建失败', format_exc())


class UserRoleDeleteView:
    def __init__(self, rb, req):
        self.rb = rb
        self.req = req

    async def __call__(self):
        try:
            roleId, type = dict(self.rb).values()
            if type == 0:
                await UserRoleDeleteModel.userRoleLogicalDelete(self.req.state.user.get("user_id"), roleId)
                return await JsonResponse(HTTP_200_OK, '用户角色删除成功!', None)
            else:
                await UserRoleDeleteModel.userRolePhysicalDelete(roleId)
                return await JsonResponse(HTTP_200_OK, '用户角色删除成功!', None)
        except Exception:
            raise HttpException(HTTP_500_INTERNAL_SERVER_ERROR, '用户角色删除失败!', format_exc())


class UserRoleUpdateView:
    def __init__(self, rb, req):
        self.rb = rb
        self.req = req

    async def __call__(self):
        try:
            reqs, conditions, params = tuple(self.rb.dict(by_alias=True).items()), [], []
            role = await UserRoleUpdateModel.userRoleGet(reqs[0][1])
            if role:
                for key, value in reqs[1:]:
                    if value is not None:
                        if key != "path_ids":
                            conditions.append(f"{key}=%s")
                            params.append(value)
                        else:
                            conditions.append(f"{key}=%s")
                            pathIds = role.get("path_ids")
                            value = value + loads(pathIds) if pathIds else value if value else pathIds
                            params.append(dumps(tuple(set(value))))
                params.extend([self.req.state.user.get("user_id"), datetime.now(), reqs[0][1]])
                await UserRoleUpdateModel.userRoleUpdate(", ".join(conditions), params)
                return await JsonResponse(HTTP_200_OK, '用户角色更新成功!', None)
            else:
                return await JsonResponse(HTTP_200_OK, '用户角色不存在!', None)
        except Exception:
            raise HttpException(HTTP_500_INTERNAL_SERVER_ERROR, '用户角色更新失败!', format_exc())


class UserRoleGetView:
    def __init__(self, rb):
        self.rb = rb

    async def __call__(self):
        try:
            conditions, params, reqs = [], [], tuple(self.rb.dict(by_alias=True).items())
            for key, value in reqs[0:1]:
                if value is not None:
                    conditions.append(f"{key} LIKE %s")
                    params.append(f"{value}%")
            for key, value in reqs[1:4]:
                if value is not None:
                    conditions.append(f"{key} = %s")
                    params.append(value)
            for key, value in reqs[4:-2]:
                if value is not None:
                    conditions.append(f"{key} >= %s and {key} <= %s")
                    params.extend(value.split(', '))
                    continue
            numbers = [r[1] for r in reqs[-2:]]
            params.extend([(numbers[0] - 1) * numbers[1], numbers[1]])
            conditionStr = f" WHERE {" AND ".join(conditions)} limit %s, %s" if conditions else " limit %s, %s"
            roles = await UserRoleGetModel.userRolesGet(conditionStr, params)
            total = len(roles)
            if total != 0:
                for role in roles:
                    role['role_status'] = True if role['role_status'] == 1 else False
                return await JsonResponse(HTTP_200_OK, "用户角色查询成功", {'total': total, 'roles': roles})
            else:
                return await JsonResponse(HTTP_204_NO_CONTENT, "没有符合条件的数据", {'total': 0, 'roles': []})
        except Exception:
            raise HttpException(HTTP_500_INTERNAL_SERVER_ERROR, '用户角色查询失败', format_exc())


class UserRoleMenuGetView:
    async def __call__(self):
        try:
            menu = {
                'role_levels': [
                    {'label': '超级管理员', 'value': 1},
                    {'label': '普通用户', 'value': 0},
                    {'label': '管理员', 'value': 2},
                ],
                'role_states': [
                    {'label': '全部', 'value': None},
                    {'label': '启用', 'value': True},
                    {'label': '禁用', 'value': False}
                ],
                'api_tabs': [
                    {'key': '用户管理', 'enabled': False, 'value': []},
                    {'key': '用户角色管理', 'enabled': False, 'value': []},
                    {'key': '用户权限管理', 'enabled': False, 'value': []},
                    {'key': '系统管理', 'enabled': False, 'value': []},
                    {'key': '系统接口管理', 'enabled': False, 'value': []},
                ]
            }
            return await JsonResponse(HTTP_200_OK, "用户角色枚举查询成功", menu)
        except Exception:
            raise HttpException(HTTP_500_INTERNAL_SERVER_ERROR, '用户角色枚举查询失败', format_exc())
