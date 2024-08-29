import aioredis
from config.constant import SYS_RUN_CONFIG


class AioRedisOrm:
    _instance = None
    pool = None
    configs = {}

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def __createConnPool(self, NACOS=SYS_RUN_CONFIG):
        c = NACOS['dbms']['redis']
        if self.configs.get('redis') != c:
            self.pool = await aioredis.create_redis_pool(
                (c.get('host'), c.get('port')),
                password=c.get('password'),
                encoding="utf-8",
                minsize=c.get('min_size'),
                maxsize=c.get('max_size'),
            )
            self.configs['redis'] = c

    async def __closeConnPool(self):
        if self.pool is not None:
            self.pool.close()
            await self.pool.wait_closed()

    async def set(self, key: str, value: str, expire=None):
        await self.__createConnPool()
        await self.pool.set(key, value, expire=expire)

    async def get(self, key: str):
        await self.__createConnPool()
        return await self.pool.get(key)
        # 新增：对列表的操作方法

    async def listPush(self, key: str, value: str):
        await self.__createConnPool()
        await self.pool.lpush(key, value)

    async def listDel(self, key: str, value: str):
        await self.__createConnPool()
        # 从列表中移除第一个匹配的值。如果需要移除所有匹配项，请使用 `lrem(key, count=0, value=value)`。
        await self.pool.lrem(key, 1, value)

    async def listGet(self, key: str, start: int, stop: int):
        await self.__createConnPool()
        return await self.pool.lrange(key, start, stop)

        # 新增：对哈希表的操作方法

    async def mapSet(self, key: str, field: str, value: str):
        await self.__createConnPool()
        await self.pool.hset(key, field, value)

    async def mapGet(self, key: str, field: str):
        await self.__createConnPool()
        return await self.pool.hget(key, field)

    async def mapDel(self, key: str, field: str):
        await self.__createConnPool()
        await self.pool.hdel(key, field)

    async def mapGetAll(self, key: str):
        await self.__createConnPool()
        return await self.pool.hgetall(key)

        # 新增：对集合的操作方法

    async def setAdd(self, key: str, member: str):
        await self.__createConnPool()
        await self.pool.sadd(key, member)

    async def setDel(self, key: str, member: str):
        await self.__createConnPool()
        await self.pool.srem(key, member)

    async def setGetAll(self, key: str):
        await self.__createConnPool()
        return await self.pool.smembers(key)

    async def deleteKey(self, key: str):
        await self.__createConnPool()
        await self.pool.delete(key)

    async def setExpireTime(self, key: str, expire: int):
        """为除字符串外的类型设置过期时间"""
        await self.__createConnPool()
        await self.pool.expire(key, expire)


aro = AioRedisOrm()
