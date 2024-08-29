import asyncio
from elasticsearch_async import AsyncElasticsearch
from datetime import datetime

class BaseAsyncElasticORM:
    def __init__(self, index_name, es=None):
        self.index_name = index_name
        if es is None:
            self.es = AsyncElasticsearch(
                [{'host': 'localhost', 'port': 9200, 'scheme': 'http'}],
                basic_auth=('elastic', '_tA_adwRdoT_NMnuNGbN'),
                verify_certs=False,  # 忽略 SSL 证书验证
            )
        else:
            self.es = es

    async def create_index(self):
        if not await self.es.indices.exists(index=self.index_name):
            await self.es.indices.create(index=self.index_name)

    async def delete_index(self):
        if await self.es.indices.exists(index=self.index_name):
            await self.es.indices.delete(index=self.index_name)

    async def insert_document(self, doc_id, document):
        return await self.es.index(index=self.index_name, id=doc_id, body=document)

    async def get_document(self, doc_id):
        return await self.es.get(index=self.index_name, id=doc_id)

    async def update_document(self, doc_id, update):
        return await self.es.update(index=self.index_name, id=doc_id, body={"doc": update})

    async def delete_document(self, doc_id):
        return await self.es.delete(index=self.index_name, id=doc_id)

    async def search_documents(self, query):
        return await self.es.search(index=self.index_name, body=query)


class AsyncLogEntry(BaseAsyncElasticORM):
    def __init__(self, es=None):
        super().__init__('log-index', es)

    async def create_log_entry(self, doc_id, log_entry):
        return await self.insert_document(doc_id, log_entry)

    async def get_log_entry(self, doc_id):
        return await self.get_document(doc_id)

    async def update_log_entry(self, doc_id, update):
        return await self.update_document(doc_id, update)

    async def delete_log_entry(self, doc_id):
        return await self.delete_document(doc_id)

    async def search_logs(self, query):
        return await self.search_documents(query)


# 示例使用
async def main():
    # 创建一个 AsyncLogEntry 实例
    async_log_entry = AsyncLogEntry()

    # 创建索引
    await async_log_entry.create_index()

    # 插入文档
    doc_id = 1
    log_data = {
        "time": "2024-07-26 10:11:05",
        "ip": "127.0.0.1:56913",
        "type": "http",
        "name": "个人信息获取",
        "path": "/xzp/personal/get",
        "method": "get",
        "consuming": 193.8674,
        "code": 200,
        "msg": "个人信息获取成功!",
        "data": "请求日志及响应结果已放入 ES"
    }
    res = await async_log_entry.create_log_entry(doc_id, log_data)
    print(res)

    # 查询文档
    res = await async_log_entry.get_log_entry(doc_id)
    print(res)

    # 更新文档
    update = {"msg": "更新后的消息"}
    res = await async_log_entry.update_log_entry(doc_id, update)
    print(res)

    # 删除文档
    res = await async_log_entry.delete_log_entry(doc_id)
    print(res)

    # 搜索文档
    query = {
        "query": {
            "match": {
                "ip": "127.0.0.1:56913"
            }
        }
    }
    results = await async_log_entry.search_logs(query)
    print(results)

# 运行异步函数
asyncio.run(main())
