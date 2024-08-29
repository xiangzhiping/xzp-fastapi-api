from utils.example_responder import *

UserRoleCreateExample = {
    HTTP_200_OK: Http200JsonExample(HTTP_200_OK, "用户角色创建成功", 'null'),
    HTTP_422_UNPROCESSABLE_ENTITY: Http422RequestErrorExample(),
    HTTP_500_INTERNAL_SERVER_ERROR: Http500ServerErrorExample(HTTP_500_INTERNAL_SERVER_ERROR, "用户角色创建失败")
}

UserRoleDeleteExample = {
    HTTP_200_OK: Http200JsonExample(HTTP_200_OK, "用户角色删除成功", 'null'),
    HTTP_422_UNPROCESSABLE_ENTITY: Http422RequestErrorExample(),
    HTTP_500_INTERNAL_SERVER_ERROR: Http500ServerErrorExample(HTTP_500_INTERNAL_SERVER_ERROR, "用户角色删除失败")
}

UserRoleUpdateExample = {
    HTTP_200_OK: Http200JsonExample(HTTP_200_OK, "用户角色修改成功", 'null'),
    HTTP_422_UNPROCESSABLE_ENTITY: Http422RequestErrorExample(),
    HTTP_500_INTERNAL_SERVER_ERROR: Http500ServerErrorExample(HTTP_500_INTERNAL_SERVER_ERROR, "用户角色修改失败")
}

UserRoleGetExample = {
    HTTP_200_OK: Http200JsonExample(HTTP_200_OK, "用户角色列表获取成功", {'total': '数据条数', 'roles': ()}),
    HTTP_500_INTERNAL_SERVER_ERROR: Http500ServerErrorExample(HTTP_500_INTERNAL_SERVER_ERROR, "用户角色列表获取失败")
}
