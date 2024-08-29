from utils.example_responder import *

UserPermissionCreateExample = {
    HTTP_200_OK: Http200JsonExample(HTTP_200_OK, "用户权限创建成功", 'null'),
    HTTP_422_UNPROCESSABLE_ENTITY: Http422RequestErrorExample(),
    HTTP_500_INTERNAL_SERVER_ERROR: Http500ServerErrorExample(HTTP_500_INTERNAL_SERVER_ERROR, "用户权限创建失败")
}

UserPermissionUpdateExample = {
    HTTP_200_OK: Http200JsonExample(HTTP_200_OK, "用户权限修改成功", 'null'),
    HTTP_422_UNPROCESSABLE_ENTITY: Http422RequestErrorExample(),
    HTTP_500_INTERNAL_SERVER_ERROR: Http500ServerErrorExample(HTTP_500_INTERNAL_SERVER_ERROR, "用户权限修改失败")
}

UserPermissionGetExample = {
    HTTP_200_OK: Http200JsonExample(HTTP_200_OK, "用户权限列表获取成功", {'total': '显示条数', 'permissions': ()}),
    HTTP_422_UNPROCESSABLE_ENTITY: Http422RequestErrorExample(),
    HTTP_500_INTERNAL_SERVER_ERROR: Http500ServerErrorExample(HTTP_500_INTERNAL_SERVER_ERROR, "用户权限列表获取失败")
}
