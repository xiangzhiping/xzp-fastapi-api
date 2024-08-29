# from aiobotocore.session import get_session
#
#
# class AioObjectMemory:
#     """异步对象存储（SSO）器"""
#
#     def __init__(self, aki, aks, region, bucket):
#         """
#         初始化
#         :param aki: str - 访问密钥ID；
#         :param aks: str - 访问密钥；
#         :param region: str - 地域（例如：oss-cn-shenzhen）；
#         :param bucket: str - 存储桶名称；
#         """
#         self.aki = aki
#         self.aks = aks
#         # 构建正确的endpoint URL，包含存储桶名称和地域
#         self.endpoint = f'https://{bucket}.{region}.aliyuncs.com'
#         self.bucket = bucket
#         self.client = None
#
#
#     async def __get_client(self):
#         if self.client is None:
#             async with get_session().create_client(
#                     's3', aws_access_key_id=self.aki,
#                     aws_secret_access_key=self.aks,
#                     endpoint_url=self.endpoint
#             ) as client:
#                 self.client = client
#         return self.client
#
#     async def uploader(self, key: str, file: bytes):
#         """
#         对象上传器
#         :param key: str - 对象在存储桶中的唯一键（路径）；
#         :param file: bytes - 要上传的文件内容；
#         """
#         client = await self.__get_client()
#         await client.put_object(Bucket=self.bucket, Key=key, Body=file)
#
#     async def downloader(self, key: str) -> str:
#         """
#         对象下载器（返回下载链接）
#         :param key: str - 要下载的对象在存储桶中的唯一键（路径）；
#         """
#         client = await self.__get_client()
#         return await client.generate_presigned_url(
#             ClientMethod='get_object',
#             Params={'Bucket': self.bucket, 'Key': key},
#             ExpiresIn=3600
#         )
#
#
#
#


import oss2
from config.constant import SYS_RUN_CONFIG


class AioObjectMemory:
    """异步对象存储（OSS）器"""
    bucket = None

    def __init__(self, src=None):
        self.src = src

    async def __createConn(self):
        try:
            self.src = SYS_RUN_CONFIG['dbms']['oss']
        except Exception:
            pass
        aki, aks = self.src.get('aki'), self.src.get('aks')
        endpoint, bucket = self.src.get('endpoint'), self.src.get('bucket')
        if not self.bucket:
            self.bucket = oss2.Bucket(oss2.Auth(aki, aks), endpoint, bucket)

    async def upload(self, key, data):

        """上传文件到OSS"""
        await self.__createConn()
        return self.bucket.put_object(key, data)

    async def file_exists(self, key: str) -> bool:
        """检查文件是否存在"""
        try:
            await self.__createConn()
            res = self.bucket.head_object(key)
            return True
        except oss2.exceptions.NoSuchKey:
            return False

    async def download(self, key):
        """从OSS下载文件到本地"""
        await self.__createConn()
        return self.bucket.sign_url('GET', key, 3600)

    async def files_get(self):
        """列出当前Bucket中的所有文件"""
        await self.__createConn()
        return [{
            'key': file.key,
            'last_modified': file.last_modified,
            'etag': file.etag,
            'type': file.type,
            'size': file.size,
            'storage_class': file.storage_class,
            'owner': file.owner,
        } for file in oss2.ObjectIterator(self.bucket)]

    async def delete(self, key):
        """删除OSS上的文件"""
        await self.__createConn()
        self.bucket.delete_object(key)


aom = AioObjectMemory()


