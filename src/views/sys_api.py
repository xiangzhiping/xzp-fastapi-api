from datetime import datetime
from json import dumps
from traceback import format_exc
from itertools import zip_longest
from src.models.sys_api import *
from config.constant import GLOBAL_STORE
from system.response_rewriting import HttpException, JsonResponse
from system.orms.aio_mysql_orm import amo


class SystemApiCreateView:
    def __init__(self, rb, req):
        self.req = req
        self.rb = rb

    async def __call__(self):
        try:
            params = list(dict(self.rb).values()) + [self.req.state.user.get("user_id")]
            await SystemApiCreateModel.systemApiCreate(params)
            return await JsonResponse(HTTP_200_OK, "系统接口新增成功", None)
        except Exception:
            raise HttpException(HTTP_500_INTERNAL_SERVER_ERROR, "系统接口新增失败", format_exc())


class SystemApiDeleteView:
    def __init__(self, rb, req):
        self.rb = rb
        self.req = req

    async def __call__(self):
        try:
            operator, td = self.req.state.user.get("user_id"), datetime.now(),
            await SystemApiDeleteModel.systemApiDelete((0, operator, td, self.rb.apiId))
            return await JsonResponse(HTTP_200_OK, "系统接口删除成功", None)
        except Exception:
            raise HttpException(HTTP_500_INTERNAL_SERVER_ERROR, "系统接口删除失败", format_exc())


class SystemApiUpdateView:
    def __init__(self, rb, req):
        self.req = req
        self.rb = rb

    async def __call__(self):
        try:
            reqs, conditions, params = tuple(self.rb.dict(by_alias=True).items()), [], []
            for key, value in reqs[1:]:
                if value is not None:
                    conditions.append(f"{key}=%s")
                    params.append(value)
            params.extend([self.req.state.user.get("user_id"), datetime.now(), reqs[0][1]])
            await SystemApiUpdateModel.SystemApiUpdate(", ".join(conditions), params)
            return await JsonResponse(HTTP_200_OK, '系统接口更新成功', None)
        except Exception:
            raise HttpException(HTTP_500_INTERNAL_SERVER_ERROR, "系统接口更新成功", format_exc())


class SystemApisGetView:
    def __init__(self, rb):
        self.rb = rb

    async def __call__(self):
        try:
            conditions, params, reqs = [], [], tuple(self.rb.dict(by_alias=True).items())
            for key, value in reqs[0:2]:
                if value is not None:
                    conditions.append(f"{key} LIKE %s")
                    params.append(f"%{value}%")
            for key, value in reqs[2:6]:
                if value is not None:
                    conditions.append(f"{key} = %s")
                    params.append(value)
            times = reqs[6:-2]
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
            numbers = [req[1] for req in reqs[-2:]]
            params.extend([(numbers[0] - 1) * numbers[1], numbers[1]])
            conditionStr = f" WHERE {" AND ".join(conditions)} limit %s, %s" if conditions else " limit %s, %s"
            apis = await SystemApisGetModel.systemApisGet(conditionStr, params)
            total = len(apis)
            if total == 0:
                return await JsonResponse(HTTP_204_NO_CONTENT, "没有符合条件的数据!", {'total': 0, 'apis': ()})
            else:
                return await JsonResponse(HTTP_200_OK, "系统接口列表查询成功", {'total': total, 'apis': apis})
        except Exception:
            raise HttpException(HTTP_500_INTERNAL_SERVER_ERROR, "系统接口查询失败", format_exc())


class SystemApiAuthAccessView:
    def __init__(self, rb, req):
        self.rb = rb
        self.req = req

    async def __call__(self):
        try:
            id, aa, operator = list(dict(self.rb).values()) + [self.req.state.user.get("user_id")]
            await SystemApiAuthAccessUpdateModel.systemApiAuthAccessUpdate((aa, operator, datetime.now(), id, type))
            return await JsonResponse(HTTP_200_OK, '系统接口身份校验访问修改成功', None)
        except Exception:
            raise HttpException(HTTP_500_INTERNAL_SERVER_ERROR, '系统接口身份校验访问修改失败', format_exc())
