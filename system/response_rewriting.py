from fastapi.responses import ORJSONResponse, StreamingResponse
from fastapi.exceptions import HTTPException
from urllib.parse import quote
from json import dumps
from typing import Any
from io import BytesIO


async def JsonResponse(code: int, msg: str, data: Any):
    """json响应重写"""
    return ORJSONResponse(
        status_code=code,
        content={
            'code': code,
            'msg': msg,
            'data': data
        }
    )


class HttpException(HTTPException):
    """http异常重写"""

    def __init__(self, code: int, msg: str, data: Any):
        super().__init__(
            status_code=code,
            detail={
                'code': code,
                'msg': msg,
                'data': data
            })


async def StreamResponse(media: str, name: str, data: Any, header=None):
    """流式响应重写"""

    def jsonGenerator(data):
        yield dumps(data).encode("utf-8")

    def fileGenerator(path):
        with open(path, mode="rb") as byte:
            yield from byte

    name = quote(name.encode('utf-8')) if name else None
    match media:
        case "application/octet-stream":
            header = {'file-name': name} | (header or {})
            return StreamingResponse(jsonGenerator(data), media_type=media, headers={**{'file-name': name}, **header})
        case "text/event-stream":
            header = {"Cache-Control": "no-cache", "Connection": "keep-alive"}
            return StreamingResponse(data, media_type=media, headers=header)
        case "image/png":
            buffer = BytesIO()
            data.save(buffer, 'png')
            buffer.seek(0)
            return StreamingResponse(buffer, headers={'file-name': name}, media_type=media)
        case _:
            return StreamingResponse(fileGenerator(data), media_type=media,
                                     headers={**{'file-name': name}, **(header or {})})
