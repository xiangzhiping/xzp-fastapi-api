import asyncio


class ConcurrentSecureMap:
    def __init__(self):
        self._map = {
            "NoCheckPaths": [],
            "CaptchaMap": {},
            "ReqPathIdMap": {},
            "user": {},
            "role": {},
            "api": {}
        }
        self._lock = asyncio.Lock()

    async def get(self, key, default=None):
        async with self._lock:
            return self._map.get(key, default)

    async def set(self, key, value):
        async with self._lock:
            self._map[key] = value

    async def delete(self, key):
        async with self._lock:
            del self._map[key]

    async def keys(self):
        async with self._lock:
            return list(self._map.keys())

    async def values(self):
        async with self._lock:
            return list(self._map.values())

    async def items(self):
        async with self._lock:
            return list(self._map.items())

    def __repr__(self):
        return f'{self._map}'

# localMap = ConcurrentSecureMap()
#
#
# # 示例用法
# async def main():
#     print(localMap)
#     # 设置键值对
#     await localMap.set("key1", "value1")
#     await localMap.set("key2", "value2")
#     print(await localMap.items())
#     # 获取值
#     value1 = await localMap.get('key1')
#     value2 = await localMap.get('key2')
#     print(value1, value2)
#     print(localMap)
#
#     # 删除键值对
#     await localMap.delete('key1')
#     print(await localMap.items())
#     print(localMap)
#
#     # 遍历键、值、项
#     keys = await localMap.keys()
#     values = await localMap.values()
#     items = await localMap.items()
#     print(keys, values, items)
#
#
# # 运行示例
# asyncio.run(main())
