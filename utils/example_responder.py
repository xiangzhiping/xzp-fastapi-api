from starlette.status import HTTP_200_OK, HTTP_422_UNPROCESSABLE_ENTITY, HTTP_500_INTERNAL_SERVER_ERROR
from typing import Any


def Http200JsonExample(code: int, msg: str, data: Any) -> dict:
    return {
        "description": "请求成功响应描述",
        "content": {
            "application/json": {
                "example": {
                    "code": code,
                    "msg": msg,
                    "data": data
                }
            }
        }
    }


def Http200PngExample() -> dict:
    return {
        "description": "请求成功响应描述",
        "content": {
            "image/png": {
                "example": "图形验证码图片以及位于请求头的验证码id[captcha-id]和文件名[file-name]"
            }
        }
    }


def Http422RequestErrorExample() -> dict:
    return {
        "description": "请求参数错误响应描述",
        "content": {
            "application/json": {
                "example": {
                    "code": HTTP_422_UNPROCESSABLE_ENTITY,
                    "msg": "请求参数错误",
                    "data": [
                        {
                            "loc": "错误参数",
                            "msg": "错误信息",
                            "type": "错误类型"
                        }
                    ]
                }
            }
        }
    }


def Http500ServerErrorExample(code: int, msg: str) -> dict:
    return {
        "description": "请求错误响应描述",
        "content": {
            "application/json": {
                "example": {
                    "code": code,
                    "msg": msg,
                    "data": "错误原因或异常堆栈"
                }
            }
        }
    }
