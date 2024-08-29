import base64
import zlib
from json import dumps, loads
from typing import Any
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


# noinspection SpellCheckingInspection
class AesCryptor:
    """aes加解密"""
    def __init__(self):
        self.key: bytes = base64.urlsafe_b64decode(b'pT8ZDjwCvnWkfPEYBm12q2p9srNkM-nWC6Ss9aAcMEw2')[:32]

    async def encrypt(self, value: Any) -> str:
        # 压缩明文数据
        compressedPlaintData = zlib.compress(bytes(dumps(value).encode("utf-8")))
        # 创建一个PKCS7填充器对象
        padder = padding.PKCS7(128).padder()
        # 对压缩后的明文进行填充
        plaintextFiling = padder.update(compressedPlaintData) + padder.finalize()
        # 创建加密器对象，使用 AES 算法和 ECB 模式
        encryptor = Cipher(algorithms.AES(self.key), modes.ECB()).encryptor()
        # 使用 base64 编码表示加密后的数据
        return base64.b64encode(encryptor.update(plaintextFiling) + encryptor.finalize()).decode()

    async def decrypt(self, value: Any) -> Any:
        # 创建解密器对象，使用 AES 算法和 ECB 模式
        decryptor = Cipher(algorithms.AES(self.key), modes.ECB()).decryptor()
        # 解密数据
        decryptedData = decryptor.update(base64.b64decode(value)) + decryptor.finalize()
        # 使用 PKCS7 反向填充
        unpadder = padding.PKCS7(128).unpadder()
        decompressed_data = unpadder.update(decryptedData) + unpadder.finalize()
        # 返回解密并解压缩后的明文
        return loads(zlib.decompress(decompressed_data).decode("utf-8"))


ac = AesCryptor()


# async def main():
#     data = "633124"
#     encryptRes = await ac.encrypt(data)
#     print("加密后的结果：", encryptRes)
#
#     # 解密示例
#     decryptRes = await ac.decrypt(encryptRes)
#     print("解密后的结果：", decryptRes)
#
#
# if __name__ == "__main__":
#     asyncio.run(main())
