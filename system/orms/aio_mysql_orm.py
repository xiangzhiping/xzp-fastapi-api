from time import perf_counter
from config.constant import SYS_RUN_CONFIG
from system.utils import mlp
import aiomysql
from utils.bcrypt_cipher import BcryptCipher
from traceback import format_exc
from asyncio import create_task
from typing import List
from functools import wraps


class AioMysqlOrm:
    _instance = None
    _pool = None
    _pools = {}

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, cps: dict = None):
        super().__init__()
        self.cps = cps
        self.aioMysqlOrmTransactional = self.__AioMysqlOrmTransactional()

    async def __resTypeGet(self, resType: dict | tuple):
        if resType == dict:
            return aiomysql.SSDictCursor
        if resType == tuple:
            return aiomysql.SSCursor
        raise '响应类型仅支持 dict 或者 tuple 两种类型!'

    async def __lastRowIdOrRowCountGet(self, sql: str, cursor):
        if sql.lower().startswith("insert into"):
            return cursor.lastrowid
        else:
            return cursor.rowcount

    async def __createConnPool(self, SRC=SYS_RUN_CONFIG):
        """创建连接池"""
        self.cps = SRC['dbms']['mysql'] if not self.cps else self.cps
        key = await BcryptCipher(''.join(map(str, self.cps.values())))
        if key in self._pools:
            self._pool = self._pools[key]
        else:
            self._pools[key] = await aiomysql.create_pool(
                host=self.cps.get('host'),
                port=self.cps.get('port'),
                user=self.cps.get('username'),
                password=self.cps.get('password'),
                db=self.cps.get('database'),
                minsize=self.cps.get('min_size'),
                maxsize=self.cps.get('max_size'),
            )
            self._pool = self._pools[key]

    async def get_conn(self):
        """从连接池获取连接"""
        await self.__createConnPool()
        async with self._pool.acquire() as conn:
            return conn

    async def close_conn_pool(self):
        """关闭连接池"""
        if self._pool:
            self._pool.close()
            await self._pool.wait_closed()

    async def fetchall(self, sql: str, params: any = None,
                       resType: dict | tuple = dict, conn=None) -> tuple[dict] | tuple[tuple]:
        """原生sql查询返回全部结果"""
        conn = conn if conn else await self.get_conn()
        async with conn.cursor(await self.__resTypeGet(resType)) as cursor:
            startTime = perf_counter()
            await cursor.execute(sql, params)
            create_task(mlp.processor(cursor.mogrify(sql, params), startTime))
            return await cursor.fetchall()

    async def fetchmany(self, sql: str, params: any = None,
                        resType: dict | tuple = dict, resNum: int = 10, conn=None) -> tuple[dict] | tuple[tuple]:
        """原生sql查询返回多条结果(可自定义返回条数,默认返回10条)"""
        conn = conn if conn else await self.get_conn()
        async with conn.cursor(await self.__resTypeGet(resType)) as cursor:
            startTime = perf_counter()
            await cursor.execute(sql, params)
            create_task(mlp.processor(cursor.mogrify(sql, params), startTime))
            return await cursor.fetchmany(resNum)

    async def fetchone(self, sql: str, params: any = None, resType: dict | tuple = dict, conn=None) -> dict | tuple:
        """原生sql查询返回单条结果"""
        conn = conn if conn else await self.get_conn()
        async with conn.cursor(await self.__resTypeGet(resType)) as cursor:
            startTime = perf_counter()
            await cursor.execute(sql, params)
            create_task(mlp.processor(cursor.mogrify(sql, params), startTime))
            return await cursor.fetchone()

    async def execute(self, sql: str, params: any = None, conn=None) -> int:
        """原生sql执行，并根据SQL类型返回相应信息"""
        try:
            if conn:
                async with conn.cursor() as cursor:
                    startTime = perf_counter()
                    await cursor.execute(sql, params)
                    create_task(mlp.processor(cursor.mogrify(sql, params), startTime))
                    return await self.__lastRowIdOrRowCountGet(sql, cursor)
            else:
                conn = await self.get_conn()
                await conn.begin()
                async with conn.cursor() as cursor:
                    startTime = perf_counter()
                    await cursor.execute(sql, params)
                    await conn.commit()
                    create_task(mlp.processor(cursor.mogrify(sql, params), startTime))
                    return await self.__lastRowIdOrRowCountGet(sql, cursor)
        except Exception as err:
            await conn.rollback()
            raise err

    async def executemany(self, sql: str, params: any = None, conn=None) -> int:
        """原生sql批量执行，并根据SQL类型返回相应信息"""
        try:
            if conn:
                async with conn.cursor() as cursor:
                    startTime = perf_counter()
                    await cursor.executemany(sql, params)
                    create_task(mlp.processor(cursor.mogrify(sql, params), startTime))
                    return await self.__lastRowIdOrRowCountGet(sql, cursor)
            else:
                conn = await self.get_conn()
                await conn.begin()
                async with conn.cursor() as cursor:
                    startTime = perf_counter()
                    await cursor.executemany(sql, params)
                    await conn.commit()
                    create_task(mlp.processor(cursor.mogrify(sql, params), startTime))
                    return await self.__lastRowIdOrRowCountGet(sql, cursor)
        except Exception as err:
            await conn.rollback()
            raise err

    def __AioMysqlOrmTransactional(self):
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                async with self.__AioMysqlOrmTransaction(self) as conn:
                    return await func(*args, conn=conn, **kwargs)

            return wrapper

        return decorator

    class __AioMysqlOrmTransaction:
        def __init__(self, amo):
            self.conn = None
            self.amo = amo

        async def __aenter__(self):
            self.conn = await self.amo.get_conn()
            await self.conn.begin()
            return self.conn

        async def __aexit__(self, exc_type, exc, tb):
            if exc_type:
                await self.conn.rollback()
            else:
                await self.conn.commit()


amo = AioMysqlOrm()

# async def main():
#     amo = AioMysqlOrm({
#         "host": "127.0.0.1",
#         "port": 3306,
#         "username": "xzp_dev_mysql_username",
#         "password": "xzp_dev_mysql_password",
#         "database": "xzp_dev_mysql",
#         "min_size": 1,
#         "max_size": 100,
#     })
#     from datetime import datetime
#     currentTime = datetime.now()
#     x = 1
#     sql = "UPDATE user SET account_status=%s, update_time=%s, operator=%s WHERE user_id=%s"
#     y = await amo.execute(sql, (x, currentTime, 1812007440141656064, 1812007440141656064))
#     print(await amo.fetchall("SELECT * FROM user_permission"))
#     sql = "UPDATE user_permission SET data_status=%s, update_time=%s, operator=%s WHERE user_id=%s"
#     z = await amo.execute(sql, (x, currentTime, 1812007440141656064, 1812007440141656064))
#     sql = "UPDATE user_permission SET data_status=%s, update_time=%s, operator=%s WHERE user_id=%s"
#     e = await amo.execute(sql, (x, currentTime, 1812007440141656064, 1812007440141656064))
#     print(y, z, e)
#     await amo.closeConnPool()
#
#
# if __name__ == "__main__":
#     import asyncio
#
#     asyncio.run(main())
