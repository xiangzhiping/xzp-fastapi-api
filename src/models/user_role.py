from datetime import datetime
from system.orms.aio_mysql_orm import amo


class UserRoleCreateModel:
    @staticmethod
    async def userRoleCreate(roleName, roleLevel, apiPaths, operator):
        sql = "insert into user_role (role_name, role_level, paths, operator_id) values (%s, %s, %s, %s)"
        await amo.execute_one(sql, (roleName, roleLevel, apiPaths, operator))


class UserRoleDeleteModel:
    @staticmethod
    async def userRoleLogicalDelete(operator, roleId):
        sql = "UPDATE user_role SET role_status=%s, operator_id=%s, delete_datetime=%s WHERE role_id=%s"
        await amo.execute_one(sql, (0, operator, datetime.now(), roleId))

    @staticmethod
    async def userRolePhysicalDelete(roleId):
        await amo.execute_one("DELETE FROM user_role WHERE role_id = %s", roleId)


class UserRoleUpdateModel:
    @staticmethod
    async def userRoleGet(roleId):
        sql = "SELECT role_name, role_level, paths FROM user_role WHERE role_status = 1 AND role_id=%s"
        return await amo.query_one(sql, roleId)

    @staticmethod
    async def userRoleUpdate(conditionStr, params):
        await amo.execute_one(f"UPDATE user_role SET {conditionStr}, operator=%s, update_time=%s WHERE role_id=%s",
                              params)


class UserRoleGetModel:
    @staticmethod
    async def userRolesGet(conditionStr, params):
        sql = (
            "SELECT role_id, role_name, role_level, paths AS api_tabs, CONVERT(operator_id, CHAR) AS operator_id, role_status, "
            "DATE_FORMAT(create_datetime, '%%y-%%m-%%d %%H:%%i:%%s') AS create_datetime, "
            "DATE_FORMAT(update_datetime, '%%y-%%m-%%d %%H:%%i:%%s') AS update_datetime, "
            "DATE_FORMAT(delete_datetime, '%%y-%%m-%%d %%H:%%i:%%s') AS delete_datetime FROM user_role"
        )
        return await amo.query_all(sql + conditionStr, params)
