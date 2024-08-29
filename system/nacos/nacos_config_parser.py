import json
import os
from traceback import format_exc
from nacos import NacosClient
from system.utils import spr, AsyncYamlParser
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from config.constant import DEFAULT_RUN_DEV, SYS_RUN_CONFIG, NACOS_DATA_ID


class SysRunConfigGet:

    def __nacosConfigWatcherHandel(self, args):
        spr.info("nacos配置已刷新!")
        SYS_RUN_CONFIG.clear()
        SYS_RUN_CONFIG.update(args.get("raw_content"))

    async def sysRunConfigGet(self):
        global env
        try:
            env = os.environ.get('RUNNINGENV', DEFAULT_RUN_DEV)
            nac = (await AsyncYamlParser("config/src.yaml")).get(env)
            if nac:
                await spr.ainfo(f"已从本地文件中获取到系统运行配置!\n")
                SYS_RUN_CONFIG.update(nac)
            else:
                conn = await AsyncYamlParser("config/nacos.yaml")  # 注意这里使用了await
                client = NacosClient(
                    server_addresses=f'{conn["host"]}:{conn["port"]}',  # 直接使用字典访问，假设get()返回一个dict
                    namespace=conn["namespace"],
                    username=conn["username"],
                    password=conn["password"],
                )
                dataId, group = env + NACOS_DATA_ID, env
                nc = client.get_config(dataId, group)
                if nc:
                    await spr.ainfo("已从nacos获取系统运行配置!\n")
                    SYS_RUN_CONFIG.update(json.loads(nc))
                    # 此设置可以使得更新nacos配置后不用重启应用就可以实现获取新配置
                    client.add_config_watcher(dataId, group, self.__nacosConfigWatcherHandel)
                else:
                    awaitsp.aerror("未从nacos中获取到系统运行配置\n!")
        except Exception:
            await spr.aerror({"msg": "系统运行配置失败!", "run_env": env, "err": format_exc()})


srcg = SysRunConfigGet()
