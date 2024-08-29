from system.orms.aio_mysql_orm import amo


class SystemCaptchaSendModel:
    @staticmethod
    async def IsThisEmailRegistered(account):
        return await amo.fetchone("SELECT email FROM user WHERE email = %s", account)

    @staticmethod
    async def IsThisPhoneRegistered(account):
        return await amo.fetchone("SELECT phone FROM user WHERE phone = %s", account)
