import asyncio
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from time import strftime, localtime, perf_counter
from aioconsole import aprint
from aiofiles import open
from colorama import Style
from config.constant import COLORS, GLOBAL_STORE


class SysRequestLogProcessor:
    def __init__(self):
        self.l, self.r = f"{COLORS['cyan']}[", f"{COLORS['cyan']}]"

    async def __colorLevelGet(self, code: int):
        color = "green" if code < 300 else "yellow" if 300 <= code < 500 else "red"
        level = "INFO" if code < 300 else "WARN" if 300 <= code < 500 else "ERR"
        return color, level

    async def __logPrinter(self, color: str, level: str, keys: tuple, values: tuple, data):
        colorKeys = [f"{COLORS['blue']}{key}{Style.RESET_ALL}" for key in keys]
        colorValues = [f"{COLORS[color]}{v}{Style.RESET_ALL}" for i, v in enumerate(values)]
        levelKey, line = f"{self.l}{COLORS[color]}{level}{Style.RESET_ALL}{self.r}", f"{COLORS['magenta']} | {Style.RESET_ALL}"
        printLogParts = [f"{key}: {value}" for key, value in zip(colorKeys, colorValues)]
        head = f"{levelKey}:{line}{line.join(printLogParts)}{line}{COLORS['blue']}{'data'}{Style.RESET_ALL}: "
        if isinstance(data, str):
            data = f"{COLORS[color]}{data}{Style.RESET_ALL}"
        else:
            data = f"{COLORS[color]}请求日志及响应结果已放入 ES{Style.RESET_ALL}"
        await aprint(head + data + '\n')

    async def cleanupOldLogs(self):
        while True:
            for path in Path("logs").iterdir():
                if path.stat().st_mtime < (datetime.now() - timedelta(days=15)).timestamp():
                    os.remove(path)
            await asyncio.sleep(24 * 60 * 60)

    async def __fileLogWriter(self, level: str, keys: tuple, values: tuple):
        async with open(Path("logs") / (datetime.now().strftime("%Y-%m-%d") + ".log"), mode="a") as file:
            await file.write(f"{level}: | {' | '.join((f"{key}: {value}" for key, value in zip(keys, values)))}\n")

    # noinspection PyTypeChecker
    async def builder(self, *args):
        request, code, msg, data = args
        resTime = round((perf_counter() - request.state.user.get("start_time")) * 1000, 5)
        color, level = await self.__colorLevelGet(code)
        data = "data项过长, 已省略!" if data and sys.getsizeof(data) > 3 * 1024 * 1024 else data
        date, resType = strftime("%Y-%m-%d %H:%M:%S", localtime()), request.scope.get("type")
        host = f"{request.scope.get('client')[0]}:{request.scope.get('client')[1]}"
        path = request.scope.get("path")
        paths = GLOBAL_STORE['ROUTERS_MAP'].get(path)
        if paths:
            method, name = paths.get("method").lower(), paths.get("name")
        else:
            method, name = request.scope.get('method').lower(), None
        keys = ("time", "host", "type", "name", "path", "method", "consuming", "code", "msg", "data")
        values = (date, host, resType, name, path, method, f"{resTime} ms", code, msg, data)
        await self.__fileLogWriter(level, keys, values)
        await self.__logPrinter(color, level, keys[:-1], values[:-1], data)


srlp = SysRequestLogProcessor()
