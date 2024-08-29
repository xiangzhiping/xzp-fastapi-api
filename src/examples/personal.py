from utils.example_responder import *

PersonalAvatarUploadExample = {
    HTTP_200_OK: Http200JsonExample(HTTP_200_OK, "个人头像上传成功", 'null'),
    HTTP_422_UNPROCESSABLE_ENTITY: Http422RequestErrorExample(),
    HTTP_500_INTERNAL_SERVER_ERROR: Http500ServerErrorExample(HTTP_500_INTERNAL_SERVER_ERROR, "个人头像上传失败")
}

PersonalAvatarDeleteExample = {
    HTTP_200_OK: Http200JsonExample(HTTP_200_OK, "个人头像删除成功", 'null'),
    HTTP_422_UNPROCESSABLE_ENTITY: Http422RequestErrorExample(),
    HTTP_500_INTERNAL_SERVER_ERROR: Http500ServerErrorExample(HTTP_500_INTERNAL_SERVER_ERROR, "个人头像删除失败")
}

PersonalAvatarDownloadLinkGetExample = {
    HTTP_200_OK: Http200JsonExample(HTTP_200_OK, "个人头像下载链接获取成功", '个人头像下载链接'),
    HTTP_500_INTERNAL_SERVER_ERROR: Http500ServerErrorExample(HTTP_500_INTERNAL_SERVER_ERROR, "个人头像下载链接获取失败")
}

PersonalInfoUpdateExample = {
    HTTP_200_OK: Http200JsonExample(HTTP_200_OK, "个人xx修改成功", 'null'),
    HTTP_422_UNPROCESSABLE_ENTITY: Http422RequestErrorExample(),
    HTTP_500_INTERNAL_SERVER_ERROR: Http500ServerErrorExample(HTTP_500_INTERNAL_SERVER_ERROR, "个人xx修改失败")
}

PersonalInfoGetExample = {
    HTTP_200_OK: Http200JsonExample(HTTP_200_OK, "个人信息获取成功", {
        "user_id": "个人id",
        "username": "用户名",
        "phone": "电话",
        "email": "邮箱",
        "login_status": "登陆状态",
        "login_time": "登录时间",
        "create_time": "注册时间"
    }),
    HTTP_500_INTERNAL_SERVER_ERROR: Http500ServerErrorExample(HTTP_500_INTERNAL_SERVER_ERROR, "个人信息获取失败")
}
