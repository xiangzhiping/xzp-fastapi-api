from datetime import datetime
from system.orms.aio_mysql_orm import amo


class UserRoleCreateModel:
    @staticmethod
    async def userRoleCreate(roleName, roleLevel, apiPaths, operator):
        sql = "insert into user_role (role_name, role_level, paths, operator) values (%s, %s, %s, %s)"
        await amo.execute(sql, (roleName, roleLevel, apiPaths, operator))


class UserRoleDeleteModel:
    @staticmethod
    async def userRoleLogicalDelete(operator, roleId):
        sql = "UPDATE user_role SET data_status=%s, operator=%s, delete_time=%s WHERE role_id=%s"
        await amo.execute(sql, (0, operator, datetime.now(), roleId))

    @staticmethod
    async def userRolePhysicalDelete(roleId):
        await amo.execute("DELETE FROM user_role WHERE role_id = %s", roleId)


class UserRoleUpdateModel:
    @staticmethod
    async def userRoleGet(roleId):
        sql = "SELECT role_name, role_level, paths FROM user_role WHERE data_status = 1 AND role_id=%s"
        return await amo.fetchone(sql, roleId)

    @staticmethod
    async def userRoleUpdate(conditionStr, params):
        await amo.execute(f"UPDATE user_role SET {conditionStr}, operator=%s, update_time=%s WHERE role_id=%s", params)


class UserRoleGetModel:
    @staticmethod
    async def userRolesGet(conditionStr, params):
        sql = (
            "SELECT role_id, role_name, role_level, paths, CONVERT(operator_id, CHAR) AS operator_id, role_status, "
            "DATE_FORMAT(create_datetime, '%%y-%%m-%%d %%H:%%i:%%s') AS create_time, "
            "DATE_FORMAT(update_datetime, '%%y-%%m-%%d %%H:%%i:%%s') AS update_time, "
            "DATE_FORMAT(delete_datetime, '%%y-%%m-%%d %%H:%%i:%%s') AS delete_time FROM user_role")
        return await amo.fetchall(sql + conditionStr, params)
