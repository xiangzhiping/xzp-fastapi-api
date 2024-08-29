from starlette.status import *
from system.orms.aio_mysql_orm import amo
from json import loads
from datetime import datetime


class UserRegisterModel:
    @staticmethod
    async def emailRegister(userId, email, password):
        sql = "INSERT INTO user (user_id, email, password) VALUES (%s, %s, %s)"
        await amo.execute(sql, (userId, email, password))

    @staticmethod
    async def phoneRegister(userId, phone, password):
        sql = "INSERT INTO user (user_id, phone, password) VALUES (%s, %s, %s)"
        await amo.execute(sql, (userId, phone, password))


class UserLoginAccountPasswordModel:
    @staticmethod
    async def emailLogin(username, password):
        sql = "SELECT user_id, account_status, user_status FROM user WHERE email = %s AND password = %s"
        return await amo.fetchone(sql, (username, password))

    @staticmethod
    async def phoneLogin(username, password):
        sql = "SELECT user_id, account_status, user_status FROM user WHERE phone = %s AND password = %s"
        return await amo.fetchone(sql, (username, password))

    @staticmethod
    async def loginLogsCreate(ip, res, code, msg, data, operator):
        sql = "INSERT INTO login_log (login_ip, login_res, login_code, login_msg, login_data, operator) VALUES (%s, %s, %s, %s, %s, %s)"
        await amo.execute(sql, (ip, res, code, msg, data, operator))

    @staticmethod
    async def loginUserUpdate(userId):
        sql = "UPDATE user SET login_Status = %s, login_datetime = %s Where user_id = %s"
        await amo.execute(sql, (1, datetime.now(), userId))

    @staticmethod
    async def userPermissionGet(userId):
        sql = "SELECT role_id, paths FROM user_permission WHERE permission_status = 1 and user_id = %s"
        return await amo.fetchone(sql, userId, resType=dict)

    @staticmethod
    async def userRoleGet(roleId):
        sql = "SELECT role_level, paths FROM user_role WHERE role_status = 1 and role_id = %s"
        return await amo.fetchone(sql, roleId, resType=dict)


class UserCaptchaLoginModel:
    @staticmethod
    async def emailLogin(account):
        sql = "SELECT user_id, account_status, user_status FROM user WHERE email = %s"
        return await amo.fetchone(sql, account)

    @staticmethod
    async def phoneLogin(account):
        sql = "SELECT user_id, account_status, user_status FROM user WHERE phone = %s"
        return await amo.fetchone(sql, account)


class UserAccountCancellationModel:
    @staticmethod
    async def userEmailCancellation(userId, account, conn):
        sql = "UPDATE user SET user_status = %s, delete_datetime = %s Where user_id = %s AND email=%s"
        await amo.execute(sql, (0, datetime.now(), userId, account), conn=conn)
        sql = "UPDATE user_permission SET permission_status = %s, delete_datetime = %s Where user_id=%s"
        await amo.execute(sql, (0, datetime.now(), userId), conn=conn)

    @staticmethod
    async def userPhoneCancellation(userId, account, conn):
        sql = "UPDATE user SET user_status = %s, delete_datetime = %s Where user_id=%s AND phone=%s"
        await amo.execute(sql, (0, datetime.now(), userId, account), conn=conn)
        sql = "UPDATE user_permission SET permission_status = %s, delete_datetime = %s Where user_id=%s"
        await amo.execute(sql, (0, datetime.now(), userId), conn=conn)


class UserAccountStatusUpdateModel:
    @staticmethod
    async def userStatusGet(conn, userId):
        sql = "SELECT user_status FROM user WHERE user_id = %s"
        return await amo.fetchone(sql, userId, conn=conn)

    @staticmethod
    async def userAccountStatusUpdate(conn, userId, type, operator, time):
        sql = "UPDATE user SET account_status = %s, update_datetime = %s, operator = %s WHERE user_id = %s AND account_status <> %s"
        await amo.execute(sql, (type, time, operator, userId, type), conn=conn)
        sql = "UPDATE user_permission SET permission_status = %s, update_datetime = %s, operator = %s WHERE user_id = %s AND permission_status <> %s"
        await amo.execute(sql, (type, time, operator, userId, type), conn=conn)


class UserPasswordRetrievalModel:
    @staticmethod
    async def viaEmailResetPassword(newpassword, account):
        sql = "UPDATE user SET password = %s, update_datetime = %s Where email=%s"
        await amo.execute(sql, (newpassword, datetime.now(), account))

    @staticmethod
    async def viaPhonResetPassword(newpassword, account):
        sql = "UPDATE user SET password = %s, update_datetime = %s Where phone=%s"
        await amo.execute(sql, (newpassword, datetime.now(), account))


class UserLogoutModel:
    @staticmethod
    async def logoutUserUpdate(userId):
        sql = "UPDATE user SET login_status = %s, logout_datetime = %s Where user_id=%s"
        await amo.execute(sql, (0, datetime.now(), userId))


class UserQueryModel:
    @staticmethod
    async def userQuery(conditionStr, params):
        sql = (
            "SELECT CONVERT(user_id, CHAR) AS user_id, nickname, phone, email, avatar_key, login_status, "
            "account_status, user_status, CONVERT(operator, CHAR) AS operator, "
            "DATE_FORMAT(login_datetime, '%%y-%%m-%%d %%H:%%i:%%s') AS login_datetime, "
            "DATE_FORMAT(logout_datetime, '%%y-%%m-%%d %%H:%%i:%%s') AS logout_datetime, "
            "DATE_FORMAT(create_datetime, '%%y-%%m-%%d %%H:%%i:%%s') AS create_datetime, "
            "DATE_FORMAT(update_datetime, '%%y-%%m-%%d %%H:%%i:%%s') AS update_datetime, "
            "DATE_FORMAT(delete_datetime, '%%y-%%m-%%d %%H:%%i:%%s') AS delete_datetime FROM user"
        )
        return await amo.fetchall(sql + conditionStr, params)
