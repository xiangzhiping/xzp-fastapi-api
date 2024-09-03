import sys
import inspect
from os import getpid, environ
from yaml import safe_load
from aiofiles import open
from typing import Any
from aioconsole import aprint
from time import perf_counter
from colorama import Style
from datetime import datetime
from config.constant import *
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.header import Header
from traceback import format_exc
from requests import get
from ipaddress import IPv4Network, ip_network
from socket import socket, AF_INET, SOCK_DGRAM, gethostname, gethostbyname
from os import getpid
from hashlib import sha256
from system.gateway.middlewares import *
from fastapi.openapi.utils import get_openapi


def OpenapiDefaultResponseRemover(app):
    """openapi默认响应去除器"""

    def inner():
        if app.openapi_schema is None:
            openapiSchema = get_openapi(title=app.title, version=app.version, routes=app.routes)
            for path, schema in openapiSchema['paths'].items():
                for _, sch in schema.items():
                    res = sch.get('responses')
                    if res:
                        r2 = res.get("200")
                        if r2:
                            r2d, r2c = r2.get('description'), r2.get('content')
                            if r2d == "Successful Response":
                                del res['200']
                            elif len(r2c) >= 2:
                                if r2c.get('application/json'):
                                    del r2c['application/json']
                        r4 = res.get('422')
                        if r4 and r4.get('description') == "Validation Error":
                            del res['422']
            app.openapi_schema = openapiSchema
        return app.openapi_schema

    return inner


async def EnvironmentVariableParser():
    """环境变量解析器"""
    for arg in sys.argv[1:]:
        key, value = arg.split('=', 1)
        os.environ[key] = value


async def AsyncYamlParser(path: str) -> dict:
    """异步yaml解析器
    :param path: str - 文件路径；
    """
    async with open(path, mode='r') as file:
        return safe_load(await file.read())


def SyncYamlParser(path: str) -> dict:
    """同步yaml解析器
    :param path: str - 文件路径；
    """
    with open(path, "r") as file:
        return safe_load(file)


async def MailboxMailSender(subject, body, receiver, src=None):
    """邮箱邮件发送器
        :param subject: str - 邮件主题；
        :param body: str - 邮件消息；
        :param receiver: str - 收件人邮件地址；
        :param src: {'smtp_server': 'xxxx', 'smtp_port': 465, 'sender_email': 'xxxx', 'password': 'xxxx'} - 邮箱连接配置信息；
    """
    try:
        src = SYS_RUN_CONFIG['email']
    except KeyError:
        if not src:
            raise ValueError('未配置 SMTP 连接信息')
    ss, sp, se = src.get('smtp_server'), src.get('smtp_port'), src.get('sender_email')
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = se
    msg['To'] = receiver
    with SMTP_SSL(ss, sp) as server:
        if sp == 587:
            server.starttls()
        server.login(se, src.get('password'))
        server.sendmail(se, [receiver], msg.as_string())


async def PhoneSmsSender(subject, body, receiver_email, src=None) -> bool:
    """电话短信发送器
        :param subject: str - 邮件主题；
        :param body: str - 邮件消息；
        :param receiver_email: str - 收件人邮件地址；
        :param src: {'smtp_server': 'xxxx', 'smtp_port': 465, 'sender_email': 'xxxx', 'password': 'xxxx'} - 邮箱连接配置信息；
    """
    try:
        try:
            src = SYS_RUN_CONFIG['phone']
        except Exception:
            if not src:
                await spr.aerror('未配置 SMTP 连接信息')
                raise False
        ss, sp, se = src.get('smtp_server'), src.get('smtp_port'), src.get('sender_email')
        msg = MIMEText(body, 'plain', 'utf-8')
        msg['Subject'] = Header(subject, 'utf-8')
        msg['From'] = se
        msg['To'] = receiver_email
        with SMTP(ss, sp) as server:
            if sp == 587:
                server.starttls()
            elif sp == 465:
                server.startssl()
            else:
                server.connect(ss, sp)
            server.login(se, src.get('password'))
            server.sendmail(se, [receiver_email], msg.as_string())
        return True
    except Exception:
        await spr.aerror(format_exc())
        return False


def ApplicationStartLog(app):
    """应用启动日志"""
    time, title = f"{COLORS['cyan']}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", f"{COLORS['green']}APP-START-INFO"
    l, r, t, c = f"{COLORS['blue']}[", f"{COLORS['blue']}]", f"{COLORS['magenta']}-> ", f"{COLORS['magenta']}-"
    prefix = f"{l}{title}{r}{c}{l}{time}{r}{t}"
    print(f"{prefix}{COLORS['white']}app    title: {COLORS['yellow']}{app.title}")
    print(f"{prefix}{COLORS['white']}app  version: {COLORS['green']}{app.version}")
    print(f"{prefix}{COLORS['white']}uvicorn host: http://{HOST}:{PORT}")
    print(f"{prefix}{COLORS['white']}local   host: http://{gethostbyname(gethostname())}:{PORT}")
    print(f"{prefix}{COLORS['white']}swagger docs: http://{gethostbyname(gethostname())}:{PORT}/docs")
    print(f"{prefix}{COLORS['white']}app      pid: {COLORS['cyan']}{getpid()}")
    print(f"{prefix}{COLORS['white']}running  env: {COLORS['red']}{environ.get('RUNNINGENV', DEFAULT_RUN_DEV)}")


class SysPrinter:
    """系统打印器"""

    def __init__(self):
        self.l, self.r = f"{COLORS['blue']}[", f"{COLORS['blue']}]"
        self.t, self.c = f"{COLORS['blue']}-> ", f"{COLORS['white']}-"

    async def __abuilder(self, data: Any, color: str, title: str):
        """系统异步打印日志构建器包括打印时间和堆栈帧"""
        stack = inspect.stack()[2]
        title, frame = f"{COLORS[color]}{title}", f"{COLORS['magenta']}{stack.filename}:{stack.lineno}"
        time, i = f"{COLORS['cyan']}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", f"{self.r}{self.c}{self.l}"
        await aprint(f"{self.l}{title}{i}{time}{i}{frame}{self.r}{self.t}{COLORS[color]}{data}")

    def __builder(self, data: Any, color: str, title: str):
        """系统打印日志构建器包括打印时间和堆栈帧"""
        stack = inspect.stack()[2]
        title, frame = f"{COLORS[color]}{title}", f"{COLORS['magenta']}{stack.filename}:{stack.lineno}"
        time, i = f"{COLORS['cyan']}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", f"{self.r}{self.c}{self.l}"
        print(f"{self.l}{title}{i}{time}{i}{frame}{self.r}{self.t}{COLORS[color]}{data}")

    async def ainfo(self, data: Any):
        """系统INFO日志异步打印器"""
        await self.__abuilder(data, "green", "INFO")

    async def awarning(self, data: Any):
        """系统WARNING日志异步打印器"""
        await self.__abuilder(data, "yellow", "WARN")

    async def aerror(self, data: Any):
        """系统ERROR日志异步打印器"""
        await self.__abuilder(data, "red", "ERR")

    def info(self, data: Any):
        """系统INFO日志打印器"""
        self.__builder(data, "green", "INFO")

    def warning(self, data: Any):
        """系统WARNING日志打印器"""
        self.__builder(data, "yellow", "WARN")

    def error(self, data: Any):
        """系统ERROR日志打印器"""
        self.__builder(data, "red", "ERR")


spr = SysPrinter()


class MysqlLogProcessor:
    """mysql日志处理器"""

    def __init__(self):
        self.line, self.key = f"{COLORS['magenta']} | ", COLORS["cyan"]
        self.l, self.r = f"{COLORS['cyan']}[", f"{COLORS['cyan']}]"

    async def __constructor(self, level, consuming, sql, color) -> list:
        level, consuming = f"{COLORS[color]}{level}", f"{COLORS[color]}{consuming} ms"
        sqlType, sql = f"{COLORS[color]}{sql.split(' ')[0].lower()}", f"{COLORS[color]}{sql}"
        date = f"{COLORS[color]}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        return [level, consuming, sql, sqlType, date]

    async def processor(self, sql: str, st: float):
        consuming = round((perf_counter() - st) * 1000, 5)
        level = "fast" if consuming <= 100 else "medium" if consuming <= 5000 else "slow"
        color = "green" if consuming <= 100 else "yellow" if consuming <= 5000 else "red"
        level, consuming, sql, sqlType, date = await self.__constructor(level, consuming, sql, color)
        logParts = (
            f"{self.line}{self.key}time{Style.RESET_ALL}: {date}",
            f"{self.line}{self.key}type{Style.RESET_ALL}: {sqlType}",
            f"{self.line}{self.key}level{Style.RESET_ALL}: {level}",
            f"{self.line}{self.key}consuming{Style.RESET_ALL}: {consuming}",
            f"{self.line}{self.key}sql{Style.RESET_ALL}: {sql}"
        )
        await aprint(f"{COLORS[color]}{self.l}{COLORS[color]}MYSQL{self.r}{COLORS['white']}:{''.join(logParts)}")


mlp = MysqlLogProcessor()


def DataCenterIdWorkerIdProcessIdGet() -> list:
    """DataCenterID、WorkerID、ProcessID获取"""
    global sk
    try:
        response = get('https://api.ipify.org?format=json')
        response.raise_for_status()
        ip = response.json()['ip']
    except requests.RequestException as e:
        try:
            sk = socket(AF_INET, SOCK_DGRAM)
            sk.connect(('10.255.255.255', 1))
            ip = sk.getsockname()[0]
        except Exception:
            ip = '127.0.0.1'
        finally:
            sk.close()
    datacenterId = int(str(ip_network(f"{ip}/24", strict=False).network_address).split('.')[0]) % (1 << 5)
    workerId, processId = int(sha256(gethostname().encode()).hexdigest()[:8], 16) % (MAX_WORKER_ID + 1), getpid()
    return datacenterId, workerId, processId
