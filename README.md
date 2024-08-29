# xzp-fastapi-api 通用后台系统

## 目录结构：

```
|——— xzp-fastapi-api                     ——|系统根目录
    |—— config                              ——|系统配置目录 
        |—— constant.py                        ——|系统静态配置
        |—— nacos.yaml                         ——|nacos连接参数配置
        |—— src.yaml                           ——|系统运行配置
    |—— logs                                ——|系统日志文件目录
    |—— src                                 ——|系统接口源码目录 
        |—— controllers                        ——|系统接口控制器源码目录
        |—— examples                           ——|系统接口响应示例源码目录
        |—— views                              ——|系统接口视图源码目录
        |—— models                             ——|系统接口模型源码目录
        |—— routers.py                         ——|系统控制器路由表
    |—— static                              ——|系统静态资源目录
        |—— excel                              ——|excel目录
        |—— html                               ——|html目录
        |—— xzp_fastapi_api.sql                ——|系统mysql表设计详情sql文档
    |—— system                              ——|系统全局组件目录
        |—— gateway                            ——|系统网关目录
            |—— dependences.py                    ——|系统依赖注入
            |—— middlewares.py                    ——|系统中间件
        |—— nacos                              ——|系统nacos目录
            |—— nacos_config_parser.py            ——|nacos配置解析器
            |—— uinx_start_nacos.sh               ——|uinx系统启动nacos脚本
            |—— win_start_nacos.bat               ——|windows系统启动nacos脚本
        |—— orms                               ——|系统orm工具目录
            |—— aio_mongodb_orm.py                ——|异步mongodb orm
            |—— aio_mysql_orm.py                  ——|异步mysql orm
            |—— aio_redis_orm.py                  ——|异步redis orm
        |—— exception_rewriting.py             ——|系统异常重写
        |—— jwt_processor.py                   ——|jwt身份验证处理器
        |—— lifespan_register.py               ——|系统生命周期事件注册器   
        |—— request_log_processor.py           ——|系统请求日志处理器
        |—— response_rewriting.py              ——|系统响应重写
        |—— utils.py                           ——|系统工具
    |—— test                                ——|系统测试目录
    |—— utils                               ——|接口工具目录
        |—— aes_cipher.py                      ——|aes加密器
        |—— bcrypt_cipher.py                   ——|bcrypt加密器
        |—— cpatcha_generator.py               ——|图像验证码生成器
        |—— pure_digital_uuid_generator.py     ——|纯数字uuid生成器
        |—— snowflake_id_generator.py          ——|雪花id生成器
        |—— username_type_vaildator.py         ——|用户名类型校验器
    |—— dockerfile                          ——|docker镜像构建文档
    |—— main.py                             ——|系统启动入口main.py
    |—— README.md                           ——|系统说明文档
    |—— requirements.txt                    ——|系统包管理文档
```

## 操作步骤：

```
1，在系统中安装 3.12 及以上版本的 python 解释器；

2，使用 git 克隆这个项目到你本地并选择合适的分支或者新建分支；

3，然后在代码编辑器中打开这个项目后在根目录下执行
   pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ 并等待依赖全部安装完成；

2，在根目录下执行 python main.py RUNNINGENV=%s，其中%s可选为 [dev, test, prd] 中其中一个，
   即可启动对应环境的连接参数，如果以 python main.py 启动则环境默认为 dev；
```
