from traceback import format_exc
from motor.motor_asyncio import AsyncIOMotorClient
from config.constant import SYS_RUN_CONFIG


# noinspection PyMethodMayBeStatic
class MongoDBOrm:
    _instance = None
    pool = None
    db = None
    configs = {}

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __fieldsProcessor(self, fields=None) -> None | dict:
        if fields:
            fields = fields | {'_id': 0}
        else:
            fields = {'_id': 0}
        return fields

    async def __createConnPool(self, NACOS=SYS_RUN_CONFIG):
        c = NACOS['dbms']['mongodb']
        if self.configs.get('mongodb') != c:
            self.db = c.get('db')
            self.pool = AsyncIOMotorClient(
                f'mongodb://{c.get('username')}:'
                f'{c.get('password')}@'
                f'{c.get('host')}:'
                f'{c.get('port')}',
                maxPoolSize=c.get('max_size'),
                minPoolSize=c.get('min_size'),
            )
            self.configs['mongodb'] = c

    async def findOne(self, collection, condition=None, fields=None):
        try:
            await self.__createConnPool()
            return await self.pool[self.db][collection].find_one(condition, self.__fieldsProcessor(fields))
        except Exception:
            raise format_exc()

    async def insertOne(self, collection: str, document: dict):
        try:
            await self.__createConnPool()
            result = await self.pool[self.db][collection].insert_one(document)
            return result.inserted_id
        except Exception:
            raise format_exc()

    async def insertMany(self, collection: str, documents: list[dict]):
        try:
            await self.__createConnPool()
            result = await self.pool[self.db][collection].insert_many(documents)
            return result.inserted_ids
        except Exception:
            raise format_exc()

    async def updateOne(self, collection: str, filter: dict, update: dict, upsert=False):
        try:
            await self.__createConnPool()
            result = await self.pool[self.db][collection].update_one(filter, update, upsert=upsert)
            return result.modified_count
        except Exception:
            raise format_exc()

    async def updateMany(self, collection: str, filter: dict, update: dict, upsert=False):
        try:
            await self.__createConnPool()
            result = await self.pool[self.db][collection].update_many(filter, update, upsert=upsert)
            return result.modified_count
        except Exception:
            raise format_exc()

    async def deleteOne(self, collection: str, filter: dict):
        try:
            await self.__createConnPool()
            result = await self.pool[self.db][collection].delete_one(filter)
            return result.deleted_count
        except Exception:
            raise format_exc()

    async def deleteMany(self, collection: str, filter: dict):
        try:
            await self.__createConnPool()
            result = await self.pool[self.db][collection].delete_many(filter)
            return result.deleted_count
        except Exception:
            raise format_exc()

    async def findMany(self, collection: str, condition=None, fields=None, skip=0, limit=0, sort=None):
        """
            collection: 指定要查询的 MongoDB 集合名称。
            condition: 可选参数，表示查询条件（一个字典），如 { "field": "value" } 用于筛选满足特定条件的文档。
            fields: 可选参数，表示需要返回的字段列表或投影操作，如 { "field1": 1, "field2": 1 } 表示只返回 field1 和 field2 字段。
            skip: 可选参数，默认为0，用于跳过指定数量的文档。
            limit: 可选参数，默认为0，用于限制返回的文档数量。
            sort: 可选参数，表示排序规则，如 { "field": 1 } 表示按 field 升序排序，{ "field": -1 } 表示降序排序。
        """
        try:
            await self.__createConnPool()
            cursor = self.pool[self.db][collection].find(condition, self.__fieldsProcessor(fields))
            if skip:
                cursor.skip(skip)
            if limit:
                cursor.limit(limit)
            if sort:
                cursor.sort(sort)
            return [doc for doc in await cursor.to_list(length=None)]
        except Exception:
            raise format_exc()


mongo = MongoDBOrm()

# async def main():
#     x = await mongo.findOne("avatar", {"userId": 7130535699270471680}, {"data": 1})
#     y = await mongo.findMany("avatar", fields={"userId": 1}, limit=3, sort={"userId": 1})
#     z = await mongo.insertOne("avatar", {"userId": 7130535699270472002, "data": "7130535699270472002"})
#     w = await mongo.insertMany("avatar", [{"userId": 7130535699270472003, "data": "7130535699270472003"},
#                                           {"userId": 7130535699270472004, "data": "7130535699270472004"}])
#     e = await mongo.updateOne("avatar", {"userId": 7130535699270472003},
#                               {"$set": {"data": "7130535699270472003-updated"}})
#     print(x, y, z, w, e)
#
#
# if __name__ == "__main__":
#     asyncio.run(main())
