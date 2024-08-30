from traceback import format_exc
from aiomysql import IntegrityError
from datetime import datetime
from starlette.status import (
    HTTP_200_OK, HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_500_INTERNAL_SERVER_ERROR, HTTP_404_NOT_FOUND)
from src.models.personal import *
from system.orms.aio_object_memory import aom
from utils.pure_digital_uuid_generator import PureDigitalUuidGenerator
from system.response_rewriting import JsonResponse, HttpException


class PersonalAvatarUploadView:
    def __init__(self, req, avatar):
        self.req = req
        self.avatar = avatar

    async def __call__(self):
        try:
            name, size, type, file = self.avatar.filename.strip(), self.avatar.size, self.avatar.content_type, self.avatar.file
            if not name:
                return await JsonResponse(HTTP_422_UNPROCESSABLE_ENTITY, '文件名为空', None)
            if size > 1024 * 1024 * 3:
                return await JsonResponse(HTTP_422_UNPROCESSABLE_ENTITY, '文件大小不能超过3M', None)
            if type not in ("image/jpeg", "image/png", "image/gif"):
                return await JsonResponse(HTTP_422_UNPROCESSABLE_ENTITY, '文件类型错误', None)
            newAvatarKey = f'avatars/{await PureDigitalUuidGenerator()}.{type.split('/')[1]}'
            userId = self.req.state.user.get("user_id")
            await PersonalAvatarUploadModel.userAvatarUpdate((newAvatarKey, userId, datetime.now(), userId))
            await aom.upload(newAvatarKey, file)
            avatar = await PersonalAvatarUploadModel.personalAvatarKeyGet(self.req.state.user.get("user_id"))
            if avatar:
                key = avatar.get('avatar_key')
                if key:
                    if await aom.file_exists(key):
                        await aom.delete(key)
            return await JsonResponse(HTTP_200_OK, "个人头像上传成功", None)
        except Exception:
            raise HttpException(HTTP_500_INTERNAL_SERVER_ERROR, "个人头像上传失败", format_exc())


class PersonalAvatarDeleteView:
    def __init__(self, req):
        self.req = req

    async def __call__(self):
        try:
            avatar = await PersonalAvatarUploadModel.PersonalAvatarKeyGet(self.req.state.user.get("user_id"))
            if avatar:
                key = avatar.get('avatar_key')
                if key:
                    if await aom.file_exists(key):
                        await aom.delete(key)
                        return await JsonResponse(HTTP_200_OK, "个人头像删除成功", None)
            return await JsonResponse(HTTP_404_NOT_FOUND, "未上传个人头像", None)
        except Exception:
            raise HttpException(HTTP_500_INTERNAL_SERVER_ERROR, "个人头像删除失败", format_exc())


class UserAvatarDownloadLinkGetView:
    def __init__(self, req):
        self.req = req

    async def __call__(self):
        try:
            avatar = await PersonalAvatarUploadModel.PersonalAvatarKeyGet(self.req.state.user.get("user_id"))
            if avatar:
                key = avatar.get('avatar_key')
                if key:
                    if await aom.file_exists(key):
                        return await JsonResponse(HTTP_200_OK, "头像下载链接获取成功", await aom.download(key))
            return await JsonResponse(HTTP_404_NOT_FOUND, "未上传头像!", None)
        except Exception:
            raise HttpException(HTTP_500_INTERNAL_SERVER_ERROR, "头像下载链接获取失败", format_exc())


class PersonalInfoUpdateView:
    def __init__(self, rb, req):
        self.rb = rb
        self.req = req
        self.edits = {"username": "用户名", "phone": "电话", "email": "邮箱"}

    async def __call__(self):
        global key
        try:
            key, value = dict(self.rb).values()
            await UserPersonalUpdate.personalUpdate(key, value, self.req.state.user.get("user_id"))
            return await JsonResponse(HTTP_200_OK, f"{self.edits[key]}修改成功!", None)
        except aiomysql.IntegrityError:
            raise HttpException(HTTP_409_CONFLICT, f"{self.edits[key]}已存在!", format_exc())
        except Exception:
            raise HttpException(HTTP_500_INTERNAL_SERVER_ERROR, f"{self.edits[key]}修改失败!", format_exc())


class PersonalInfoGetView:
    def __init__(self, req):
        self.req = req

    async def __call__(self):
        try:
            personal = await PersonalInfoGet.personalInfoGet(self.req.state.user.get("user_id"))
            if personal:
                return await JsonResponse(HTTP_200_OK, "个人信息查询成功!", personal)
            else:
                return await JsonResponse(HTTP_204_NO_CONTENT, "个人信息不存在!", None)
        except Exception:
            raise HttpException(HTTP_500_INTERNAL_SERVER_ERROR, "个人信息获取失败!", format_exc())
