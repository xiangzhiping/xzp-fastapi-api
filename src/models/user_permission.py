from time import strftime, localtime
from starlette.status import *
from system.orms.aio_mysql_orm import amo


class UserPermissionCreateModel:
    @staticmethod
    async def userRolePathsGet(roleId):
        return await amo.fetchone("select paths from user_role where role_id=%s", roleId)

    @staticmethod
    async def userPermissionCreate(userId, roleId, paths, operator):
        sql = "insert into user_permission (user_id, role_id, paths, operator) values (%s, %s, %s, %s)"
        await amo.execute(sql, (userId, roleId, paths, operator))


class UserPermissionUpdateModel:
    @staticmethod
    async def userPermissionGet(userId):
        sql = "SELECT role_id, paths FROM user_permission WHERE data_status = 1 AND user_id=%s"
        return await amo.fetchone(sql, userId)

    @staticmethod
    async def userPermissionUpdate(cs, params):
        await amo.execute(f"UPDATE user_permission SET {cs}, operator=%s, update_time=%s WHERE role_id=%s", params)


class UserPermissionsGetModel:

    @staticmethod
    async def UserPermissionsGet(conditionStr, params):
        sql = (
            "SELECT CONVERT(user_id, CHAR) AS user_id, role_id, paths, data_status, "
            "CONVERT(operator, CHAR) AS operator, "
            "DATE_FORMAT(create_time, '%%y-%%m-%%d %%H:%%i:%%s') AS create_time, "
            "DATE_FORMAT(update_time, '%%y-%%m-%%d %%H:%%i:%%s') AS update_time, "
            "DATE_FORMAT(delete_time, '%%y-%%m-%%d %%H:%%i:%%s') AS delete_time FROM user_permission")
        return await amo.fetchall(sql + conditionStr, params)
