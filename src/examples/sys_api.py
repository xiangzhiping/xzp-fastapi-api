from utils.example_responder import *

SystemApiCreateExample = {
    HTTP_200_OK: Http200JsonExample(HTTP_200_OK, "系统接口创建成功", 'null'),
    HTTP_422_UNPROCESSABLE_ENTITY: Http422RequestErrorExample(),
    HTTP_500_INTERNAL_SERVER_ERROR: Http500ServerErrorExample(HTTP_500_INTERNAL_SERVER_ERROR, "系统接口创建失败")
}

SystemApiDeleteExample = {
    HTTP_200_OK: Http200JsonExample(HTTP_200_OK, "系统接口删除成功", 'null'),
    HTTP_422_UNPROCESSABLE_ENTITY: Http422RequestErrorExample(),
    HTTP_500_INTERNAL_SERVER_ERROR: Http500ServerErrorExample(HTTP_500_INTERNAL_SERVER_ERROR, "系统接口删除失败")
}

SystemApiUpdateExample = {
    HTTP_200_OK: Http200JsonExample(HTTP_200_OK, "系统接口更新成功", 'null'),
    HTTP_422_UNPROCESSABLE_ENTITY: Http422RequestErrorExample(),
    HTTP_500_INTERNAL_SERVER_ERROR: Http500ServerErrorExample(HTTP_500_INTERNAL_SERVER_ERROR, "系统接口更新失败")
}

SystemApisGetExample = {
    HTTP_200_OK: Http200JsonExample(HTTP_200_OK, "系统接口列表获取成功", {'total': '数据条数', 'apis': ()}),
    HTTP_422_UNPROCESSABLE_ENTITY: Http422RequestErrorExample(),
    HTTP_500_INTERNAL_SERVER_ERROR: Http500ServerErrorExample(HTTP_500_INTERNAL_SERVER_ERROR, "系统接口列表获取失败")
}

SystemApiAuthAccessExample = {
    HTTP_200_OK: Http200JsonExample(HTTP_200_OK, "系统校验访问更新成功", 'null'),
    HTTP_422_UNPROCESSABLE_ENTITY: Http422RequestErrorExample(),
    HTTP_500_INTERNAL_SERVER_ERROR: Http500ServerErrorExample(HTTP_500_INTERNAL_SERVER_ERROR, "系统校验访问更新失败")
}
