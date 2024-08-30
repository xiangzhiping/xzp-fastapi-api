from time import strftime, localtime
from starlette.status import *
from system.orms.aio_mysql_orm import amo


class UserPermissionCreateModel:
    @staticmethod
    async def userRolePathsGet(roleId):
        return await amo.query_one("select paths from user_role where role_id=%s", roleId)

    @staticmethod
    async def userPermissionCreate(userId, roleId, paths, operator):
        sql = "insert into user_permission (user_id, role_id, paths, operator_id) values (%s, %s, %s, %s)"
        await amo.execute_one(sql, (userId, roleId, paths, operator))


class UserPermissionUpdateModel:
    @staticmethod
    async def userPermissionGet(userId):
        sql = "SELECT role_id, paths FROM user_permission WHERE permission_status = 1 AND user_id=%s"
        return await amo.query_one(sql, userId)

    @staticmethod
    async def userPermissionUpdate(cs, params):
        await amo.execute_one(f"UPDATE user_permission SET {cs}, operator=%s, update_time=%s WHERE role_id=%s", params)


class UserPermissionsGetModel:

    @staticmethod
    async def UserPermissionsGet(conditionStr, params):
        sql = (
            "SELECT CONVERT(user_id, CHAR) AS user_id, role_id, paths, permission_status, "
            "CONVERT(operator_id, CHAR) AS operator_id, "
            "DATE_FORMAT(create_datetime, '%%y-%%m-%%d %%H:%%i:%%s') AS create_datetime, "
            "DATE_FORMAT(update_datetime, '%%y-%%m-%%d %%H:%%i:%%s') AS update_datetime, "
            "DATE_FORMAT(delete_datetime, '%%y-%%m-%%d %%H:%%i:%%s') AS delete_datetime FROM user_permission")
        return await amo.query_all(sql + conditionStr, params)
