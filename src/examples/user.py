from utils.example_responder import *

UserRegisterExample = {
    HTTP_200_OK: Http200JsonExample(HTTP_200_OK, "注册成功", 'null'),
    HTTP_422_UNPROCESSABLE_ENTITY: Http422RequestErrorExample(),
    HTTP_500_INTERNAL_SERVER_ERROR: Http500ServerErrorExample(HTTP_500_INTERNAL_SERVER_ERROR, "注册失败")
}

UserLoginAccountPasswordExample = {
    HTTP_200_OK: Http200JsonExample(HTTP_200_OK, "登录成功", "token令牌"),
    HTTP_422_UNPROCESSABLE_ENTITY: Http422RequestErrorExample(),
    HTTP_500_INTERNAL_SERVER_ERROR: Http500ServerErrorExample(HTTP_500_INTERNAL_SERVER_ERROR, "登录失败")
}

UserLoginCaptchaExample = {
    HTTP_200_OK: Http200JsonExample(HTTP_200_OK, "登录成功", "token令牌"),
    HTTP_422_UNPROCESSABLE_ENTITY: Http422RequestErrorExample(),
    HTTP_500_INTERNAL_SERVER_ERROR: Http500ServerErrorExample(HTTP_500_INTERNAL_SERVER_ERROR, "登录失败")
}

UserAccountCancellationExample = {
    HTTP_200_OK: Http200JsonExample(HTTP_200_OK, "账号注销成功", 'null'),
    HTTP_422_UNPROCESSABLE_ENTITY: Http422RequestErrorExample(),
    HTTP_500_INTERNAL_SERVER_ERROR: Http500ServerErrorExample(HTTP_500_INTERNAL_SERVER_ERROR, "账号注销失败")
}

UserAccountStatusUpdateExample = {
    HTTP_200_OK: Http200JsonExample(HTTP_200_OK, "账号状态更新成功", 'null'),
    HTTP_422_UNPROCESSABLE_ENTITY: Http422RequestErrorExample(),
    HTTP_500_INTERNAL_SERVER_ERROR: Http500ServerErrorExample(HTTP_500_INTERNAL_SERVER_ERROR, "账号状态更新失败")
}

UserPasswordRetrievalExample = {
    HTTP_200_OK: Http200JsonExample(HTTP_200_OK, "密码重置成功", 'null'),
    HTTP_422_UNPROCESSABLE_ENTITY: Http422RequestErrorExample(),
    HTTP_500_INTERNAL_SERVER_ERROR: Http500ServerErrorExample(HTTP_500_INTERNAL_SERVER_ERROR, "密码重置失败")
}

UserLogoutExample = {
    HTTP_200_OK: Http200JsonExample(HTTP_200_OK, "登出成功", "token"),
    HTTP_500_INTERNAL_SERVER_ERROR: Http500ServerErrorExample(HTTP_500_INTERNAL_SERVER_ERROR, "登出失败")
}

UserQueryExample = {
    HTTP_200_OK: Http200JsonExample(HTTP_200_OK, "查询成功", {'total': '数据条数', 'users': [
        {
            'user_id': '用户id',
            'nickname': '昵称',
            'phone': '电话',
            'email': '邮箱',
            'avatar_key': '头像唯一key',
            'login_status': '登录状态',
            'account_status': '账号状态',
            'user_status': '用户状态',
            'login_time': '登录时间',
            'logout_time': '登出时间',
            'create_time': '创建时间',
            'update_time': '更新时间',
            'delete_time': '删除时间',
        }
    ]}),
    HTTP_422_UNPROCESSABLE_ENTITY: Http422RequestErrorExample(),
    HTTP_500_INTERNAL_SERVER_ERROR: Http500ServerErrorExample(HTTP_500_INTERNAL_SERVER_ERROR, "查询失败")
}
