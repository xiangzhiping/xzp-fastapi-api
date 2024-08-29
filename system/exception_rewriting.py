from fastapi import Request, HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from pydantic import ValidationError
from config.constant import HTTP_STATUS_CODE_MEAN_MAP
from system.response_rewriting import JsonResponse
from re import search
from ast import literal_eval


async def HttpExceptionHandler(req: Request, exc: HTTPException):
    """HTTPException异常重写"""
    detail, code = exc.detail, exc.status_code
    if isinstance(detail, dict):
        return await JsonResponse(code, detail.get("msg"), detail.get("data"))
    if isinstance(detail, str):
        return await JsonResponse(code, HTTP_STATUS_CODE_MEAN_MAP.get(code), detail)
    return await JsonResponse(code, HTTP_STATUS_CODE_MEAN_MAP.get(code, "未知异常http错误!"), exc)


async def RequestValidationExceptionHandler(req: Request, err: ValidationError):
    """RequestValidationError异常重写"""
    errs = []
    for exe in err.errors():
        ctx = exe.get('ctx')
        if ctx:
            error = ctx.get('error')
            if error:
                try:
                    raise ctx.get('error')
                except Exception as err:
                    if 'Expected UploadFile' in str(error):
                        errs.append({
                            "loc": exe["loc"][1] if len(exe["loc"]) >= 2 else None,
                            "msg": exe["msg"],
                            "type": exe["type"]
                        })
                    else:
                        errs.append({
                            "loc": args.get("loc"),
                            "msg": args.get("msg"),
                            "type": args.get("type")
                        })
            else:
                errs.append({
                    "loc": exe["loc"][1] if len(exe["loc"]) >= 2 else None,
                    "msg": exe["msg"],
                    "type": exe["type"]
                })
        else:
            errs.append({
                "loc": exe["loc"][1] if len(exe["loc"]) >= 2 else None,
                "msg": exe["msg"],
                "type": exe["type"]
            })
    return await JsonResponse(HTTP_422_UNPROCESSABLE_ENTITY, "请求参数错误!", errs)


# def get_file_names(directory):
#     file_names = []
#     for root, dirs, files in os.walk(directory):
#         for file in files:
#             if not file.endswith('.pyc'):  # 排除以 .pyc 结尾的文件
#                 file_path = os.path.join(root, file)
#                 file_name = os.path.splitext(file)[0]  # 去除文件后缀
#                 file_names.append("src.reqBody." + file_name)
#
#     return file_names
#
#
# directory = "../src/reqBody"  # 替换为你的目录路径
# files = get_file_names(directory)
#
# for file in files:
#     module = importlib.import_module(file)
#     print(module)
#
#     # 获取模块中的类名列表
#     class_names = [name for name in dir(module) if not name.startswith('_') and isinstance(getattr(module, name), type)]
#     print(class_names)


ExceptionRewritingHandlers = {
    HTTPException: HttpExceptionHandler,
    RequestValidationError: RequestValidationExceptionHandler,
}
