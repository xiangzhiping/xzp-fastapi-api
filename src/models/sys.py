from system.orms.aio_mysql_orm import amo


class SystemCaptchaSendModel:
    @staticmethod
    async def IsThisEmailRegistered(account):
        return await amo.query_one("SELECT email FROM user WHERE email = %s", account)

    @staticmethod
    async def IsThisPhoneRegistered(account):
        return await amo.query_one("SELECT phone FROM user WHERE phone = %s", account)
