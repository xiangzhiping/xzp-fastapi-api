import os
import shutil
import logging
from asyncio import create_task
from contextlib import asynccontextmanager
from datetime import datetime
from aioconsole import aprint
from colorama import Fore
from config.constant import GLOBAL_STORE, COLORS
from system.nacos.nacos_config_parser import srcg
from system.orms.aio_mysql_orm import amo
from system.utils import EnvironmentVariableParser
from system.request_log_processor import srlp
from socket import gethostname, gethostbyname


async def UserRoleMapGet():
    sql = "SELECT role_id AS roleId, role_name AS roleName, role_level AS roleLevel, paths AS apiPaths FROM user_role"
    GLOBAL_STORE["role"] = {
        role["roleId"]: {"apiPaths": loads(role["apiPaths"]) if role["apiPaths"] else None} for role in
        await amo.fetchall(sql)}


async def NoAuthorizationAccessiblePathsGet():
    sql = "SELECT paths AS apiPaths FROM sys_api WHERE auth_access = 0"
    paths = ["/xzp/user/login", "/xzp/sys/captcha/get", "/xzp/sys/swagger/json/get"] + GLOBAL_STORE['SWAGGER_UI_PATHS']
    GLOBAL_STORE['NO_AUTHORIZATION_ACCESSIBLE_PATHS'].extend(paths)
    # GLOBAL_SHARE_RESOURCE["noCheckPaths"] = [path["apiPaths"] for path in await db.fetchall(sql)]


async def ReqPathIdMapGet():
    sql = "SELECT api_id, api_path FROM sys_api"
    GLOBAL_STORE["ReqPathIdMap"] = {path["api_path"]: path["api_id"] for path in await amo.fetchall(sql)}


async def RoutersInfoMapGet(routers):
    for route in routers:
        path = route.path
        GLOBAL_STORE['ROUTERS_MAP'][path] = {
            "path": path,
            "name": route.name,
            "method": tuple(route.methods)[0] if route.methods else None
        }


async def ConstantInitialization():
    COLORS.update({
        "red": Fore.LIGHTRED_EX,
        "green": Fore.LIGHTGREEN_EX,
        "blue": Fore.LIGHTBLUE_EX,
        "yellow": Fore.LIGHTYELLOW_EX,
        "cyan": Fore.LIGHTCYAN_EX,
        "magenta": Fore.LIGHTMAGENTA_EX,
        "black": Fore.LIGHTBLACK_EX,
        "white": Fore.LIGHTWHITE_EX
    })


async def nacosDataDirCleaner():
    nacosDataPath = "nacos-data"
    if os.path.exists(nacosDataPath):
        shutil.rmtree(nacosDataPath)


async def loggingLogLevelSet():
    logger = logging.getLogger()
    logger.setLevel(logging.CRITICAL)  # 设置最低日志级别


@asynccontextmanager
async def LifespanRegistrator(app):
    """app生命周期注册器"""
    await srcg.sysRunConfigGet()
    await loggingLogLevelSet()
    await EnvironmentVariableParser()
    await ConstantInitialization()
    await RoutersInfoMapGet(app.routes)
    await NoAuthorizationAccessiblePathsGet()
    await nacosDataDirCleaner()
    create_task(srlp.cleanupOldLogs())
    yield
    pass
