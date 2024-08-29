from bcrypt import hashpw


async def BcryptCipher(data: str) -> str:
    """Bcrypt加密器"""
    return hashpw(data.encode('utf-8'), b'$2b$12$M2wR6ftyEtO6ha4g8HSEcO').decode('utf-8')

# async def main():
#     print(await BcryptCipher('633124'))
#
#
# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(main())

