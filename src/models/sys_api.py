from time import strftime, localtime
from starlette.status import *
from system.orms.aio_mysql_orm import amo


class SystemApiCreateModel:
    @staticmethod
    async def systemApiCreate(params):
        sql = "insert into sys_api (api_name, api_path, api_type, req_method, tag_name, tag_path, auth_access, operator_id) values (%s, %s, %s, %s, %s, %s, %s, %s)"
        await amo.execute_one(sql, params)


class SystemApiDeleteModel:
    @staticmethod
    async def systemApiDelete(params):
        sql = "UPDATE sys_api SET data_status=%s, operator=%s, delete_time=%s WHERE api_id=%s"
        await amo.execute_one(sql, params)


class SystemApiUpdateModel:
    @staticmethod
    async def SystemApiUpdate(conditionStr, params):
        await amo.execute_one(f"UPDATE user_role SET {conditionStr}, operator=%s, update_time=%s WHERE role_id=%s", params)


class SystemApisGetModel:
    @staticmethod
    async def systemApisGet(conditionStr, params):
        sql = (
            "SELECT api_id, api_name, api_path, api_type, req_method, tag_name, tag_path, auth_access, api_status, "
            "DATE_FORMAT(create_datetime, '%%y-%%m-%%d %%H:%%i:%%s') AS create_datetime, "
            "DATE_FORMAT(update_datetime, '%%y-%%m-%%d %%H:%%i:%%s') AS update_datetime, "
            "DATE_FORMAT(delete_datetime, '%%y-%%m-%%d %%H:%%i:%%s') AS delete_datetime FROM sys_api"
        )
        return await amo.query_all(sql + conditionStr, params)


class SystemApiAuthAccessUpdateModel:
    @staticmethod
    async def systemApiAuthAccessUpdate(params):
        sql = "UPDATE sys_api SET auth_access = %s, operator_id = %s, update_datetime = %s WHERE api_id = %s AND auth_access <> %s"
        await amo.execute_one(sql, params)
