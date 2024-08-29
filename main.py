from uvicorn import run
from config.constant import *
from src.routers import routers
from system.gateway.dependences import depends
from system.gateway.middlewares import middlewares
from fastapi import FastAPI, APIRouter
from system.exception_rewriting import ExceptionRewritingHandlers
from system.lifespan_register import LifespanRegistrator
from system.utils import OpenapiDefaultResponseRemover, ApplicationStartLog, DataCenterIdWorkerIdProcessIdGet
from fastapi.openapi.utils import get_openapi
from utils.snowflake_id_generator import SnowflakeIdGenerator
from fastapi.middleware.cors import CORSMiddleware


def application():
    app = FastAPI(
        title=TITLE, version=VERSION,
        exception_handlers=ExceptionRewritingHandlers,
        lifespan=LifespanRegistrator,
    )

    for middleware in middlewares:
        app.add_middleware(middleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_methods=['*'],
        allow_headers=['*'],
        allow_credentials=True
    )

    apiRouter = APIRouter()
    for router in routers:
        apiRouter.include_router(router)

    app.include_router(apiRouter, prefix=ROOT_PREFIX, dependencies=depends)

    app.openapi = OpenapiDefaultResponseRemover(app)

    SNOWFLAKE_ID_GENERATORS.append(SnowflakeIdGenerator(*DataCenterIdWorkerIdProcessIdGet()))

    return app


app = application()

if __name__ == '__main__':
    ApplicationStartLog(app)
    run(
        app="main:app",
        host=HOST,
        port=PORT,
        workers=WORKERS,
        log_level=LOG_LEVEL,
        reload=APP_HOT_RELOAD,
        access_log=ACCESS_LOG,
        reload_delay=RELOAD_DELAY
    )
