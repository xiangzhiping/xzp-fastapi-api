from uuid import uuid4
from secrets import choice


async def PureDigitalUuidGenerator() -> str:
    """纯数字UUID生成器"""
    id = str(int(uuid4().hex[:25], 16))
    desiredLength, actualLength = 31, len(id)
    if actualLength < desiredLength:
        id = id + ''.join(choice('0123456789') for _ in range(desiredLength - actualLength))
    return id

# if __name__ == '__main__':
#     import asyncio
#
#     for i in range(100):
#         print(asyncio.run(PureDigitalUuidGenerator()))
