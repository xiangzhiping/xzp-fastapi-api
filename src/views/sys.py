from random import randint
from system.utils import spr, MailboxMailSender, PhoneSmsSender
from traceback import format_exc
from src.models.sys import SystemCaptchaSendModel
from starlette.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT
from utils.pure_digital_uuid_generator import PureDigitalUuidGenerator
from system.response_rewriting import JsonResponse, HttpException, StreamResponse
from utils.captcha_generator import ImageCaptchaGenerator
from system.orms.aio_redis_orm import aro


class ImageCaptchaIdGetView:
    async def __call__(self):
        try:
            return await JsonResponse(HTTP_200_OK, '图像验证码id获取成功', await PureDigitalUuidGenerator())
        except Exception:
            raise HttpException(HTTP_500_INTERNAL_SERVER_ERROR, '图像验证码id获取失败', format_exc())


class ImageCaptchaImageGetView:
    def __init__(self, captchaId):
        self.captchaId = captchaId

    async def __call__(self):
        try:
            text, image = await ImageCaptchaGenerator()
            await aro.set(self.captchaId, text, expire=3000)
            await spr.ainfo({"captcha_id": self.captchaId, "captcha_str": text})
            return await StreamResponse("image/png", f"{self.captchaId}.png", image)
        except Exception:
            raise HttpException(HTTP_500_INTERNAL_SERVER_ERROR, '图形验证码获取失败', format_exc())


class IdentityCaptchaSendView:
    def __init__(self, rb):
        self.rb = rb
        self.names = {"email": "邮箱", "phone": "短信"}

    async def emailTransmitter(self, account, atype, captcha):
        body = f'【xzp-fastapi-api】验证码 {captcha} 用于身份验证，3分钟内有效，请勿泄露和转发。如非本人操作，请忽略此信息。'
        await MailboxMailSender(f'【xzp-fastapi-api】{self.names[atype]}验证码', body, account)
        await aro.set(account, captcha, expire=3000)
        return await JsonResponse(HTTP_200_OK, f'已向 {account} 发送验证码，请注意查收', True)

    async def smsTransmitter(self, account, atype, captcha):
        body = f'【xzp-fastapi-api】验证码 {captcha} 用于身份验证，3分钟内有效，请勿泄露和转发。如非本人操作，请忽略此信息。'
        await MailboxMailSender(f'【xzp-fastapi-api】{self.names[atype]}验证码', body, account)
        await aro.set(account, captcha, expire=3000)
        return await JsonResponse(HTTP_200_OK, f'已向 {account} 发送验证码，请注意查收', True)

    async def __call__(self):
        global type
        try:
            account, scene, type, captcha = list(dict(self.rb).values()) + [randint(100000, 999999)]
            if scene == "login":
                if type == "email":
                    if await SystemCaptchaSendModel.IsThisEmailRegistered(account):
                        return await self.emailTransmitter(account, type, captcha)
                    else:
                        return await JsonResponse(HTTP_404_NOT_FOUND, f'此{self.names[type]}未注册', None)
                else:
                    if await SystemCaptchaSendModel.IsThisPhoneRegistered(account):
                        return await self.smsTransmitter(account, type, captcha)
                    else:
                        return await JsonResponse(HTTP_404_NOT_FOUND, f'此{self.names[type]}未注册', None)
            else:
                if type == "email":
                    if not await SystemCaptchaSendModel.IsThisEmailRegistered(account):
                        return await self.emailTransmitter(account, type, captcha)
                    else:
                        return await JsonResponse(HTTP_409_CONFLICT, f'此{self.names[type]}已注册', None)
                else:
                    if not await SystemCaptchaSendModel.IsThisPhoneRegistered(account):
                        return await self.smsTransmitter(account, type, captcha)
                    else:
                        return await JsonResponse(HTTP_409_CONFLICT, f'此{self.names[type]}已注册', None)
        except Exception:
            raise HttpException(HTTP_500_INTERNAL_SERVER_ERROR, f'{self.names[type]}验证码发送失败', format_exc())
