import time
import os
from config.constant import *


class SnowflakeIdGenerator:
    def __init__(self, datacenterId, workerId, processId):
        if workerId > MAX_WORKER_ID or workerId < 0:
            raise ValueError('workerId 值越界')
        if datacenterId > MAX_DATACENTER_ID or datacenterId < 0:
            raise ValueError('datacenterId 值越界')
        self.processId = processId % (MAX_PROCESS_ID + 1)
        if self.processId > MAX_PROCESS_ID or self.processId < 0:
            raise ValueError('processId 值越界')

        self.workerId = workerId
        self.datacenterId = datacenterId
        self.sequence = 0
        self.lastTimestamp = -1  # 上次生成ID的时间戳

    async def nextid(self):
        timestamp = int(time.time() * 1000)  # 获取当前毫秒时间戳
        if timestamp < self.lastTimestamp:
            raise RuntimeError("Clock moved backwards. Refusing to generate id")

        if timestamp == self.lastTimestamp:
            self.sequence = (self.sequence + 1) & MAX_SEQUENCE
            if self.sequence == 0:
                timestamp = await self._wait_for_next_timestamp(timestamp)
        else:
            self.sequence = 0

        self.lastTimestamp = timestamp
        return (timestamp << 22) | (self.datacenterId << 17) | (self.workerId << 12) | (
                self.processId << 7) | self.sequence

    async def _wait_for_next_timestamp(self, current_timestamp):
        while current_timestamp <= self.lastTimestamp:
            await asyncio.sleep(0.001)  # Wait for 1ms
            current_timestamp = int(time.time() * 1000)
        return current_timestamp


# sig = SnowflakeIdGenerator(*(26, 4, 34164))


# async def main():
#     x = []
#     for i in range(100000):
#         x.append(await sig.nextid())
#
#     print(len(set(x)), "SDCs")
#     print(x[0], len(str(x[0])))
#
#
# if __name__ == "__main__":
#     import asyncio
#
#     asyncio.run(main())

class SnowflakeIdGenerator1(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, datacenterId, workerId, sequence=0):
        """
        初始化方法
        :param datacenterId:数据id
        :param workerId:机器id
        :param sequence:序列码
        """
        if workerId > MAX_WORKER_ID or workerId < 0:
            raise ValueError('workerId 值越界')
        if datacenterId > MAX_DATACENTER_ID or datacenterId < 0:
            raise ValueError('datacenterId值越界')
        self.workerId = workerId
        self.datacenterId = datacenterId
        self.sequence = sequence
        self.lastTimestamp = -1

    async def clockCallbackProcessor(self, lastTimestamp):
        timestamp = int(time.time() * 1000)
        while timestamp <= lastTimestamp:
            timestamp = int(time.time() * 1000)
        return timestamp

    async def generator(self):
        timestamp = int(time.time() * 1000)
        if timestamp < self.lastTimestamp:  # 时钟回拨的情况
            timestamp = await self.clockCallbackProcessor(self.lastTimestamp)
        if timestamp == self.lastTimestamp:  # 同一毫秒的处理
            self.sequence = (self.sequence + 1) & SEQUENCE_MASK
            if self.sequence == 0:
                timestamp = await self.clockCallbackProcessor(self.lastTimestamp)
        else:
            self.sequence = 0
        self.lastTimestamp = timestamp
        return (
                ((timestamp - FIRST_YEAR_TIMESTAMP) << TIMESTAMP_LEFT_SHIFT) |
                (self.datacenterId << DATACENTER_ID_SHIFT) |
                (self.workerId << WORKER_ID_SHIFT)
        ) | self.sequence


sig = SnowflakeIdGenerator1(1, 2, 0)
#
# # async def main():
# #     for i in range(10):
# #         print(await sig.generator())
# #
# #
# # if __name__ == "__main__":
# #     import asyncio
# #
# #     asyncio.run(main())
# #
# #
# # print(len('1818853216104882178'))
