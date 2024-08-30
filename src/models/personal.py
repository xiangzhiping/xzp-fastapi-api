from system.orms.aio_mysql_orm import amo


class PersonalAvatarUploadModel:
    @staticmethod
    async def PersonalAvatarKeyGet(userId):
        return await amo.query_one("SELECT avatar_key FROM user WHERE user_id = %s", userId)

    @staticmethod
    async def userAvatarUpdate(args):
        sql = "UPDATE user SET avatar_key = %s, operator_id = %s, update_datetime = %s WHERE user_id = %s"
        await amo.execute_one(sql, args)


class PersonalAvatarDownloadModel:
    @staticmethod
    async def personalAvatarKeyGet(userId):
        return await amo.query_one("SELECT avatar_key FROM user WHERE user_id = %s", userId)


class UserPersonalUpdate:
    @staticmethod
    async def personalUpdate(key, value, userId):
        await amo.execute_one(f"UPDATE user SET {key}=%s, update_time=%s WHERE user_id=%s", (value, datetime.now(), userId))


class PersonalInfoGet:
    @staticmethod
    async def personalInfoGet(userId):
        sql = (
            "SELECT CONVERT(user_id, CHAR) as user_id, nickname, phone, email, login_status, "
            "DATE_FORMAT(login_datetime, '%%y-%%m-%%d %%H:%%i:%%s') AS login_datetime, "
            "DATE_FORMAT(create_datetime, '%%y-%%m-%%d %%H:%%i:%%s') AS create_datetime FROM user WHERE user_id = %s")
        return await amo.query_one(sql, userId)
