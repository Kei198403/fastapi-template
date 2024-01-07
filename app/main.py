# -*- coding: utf-8 -*-

import os
import pathlib
import importlib
from os.path import dirname, join, sep

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware


def get_submodules(name: str) -> Generator[str, None, None]:
    """指定したモジュール配下のサブモジュールを取得するジェネレータ

    :name: 対象モジュール名
    """

    # 起点となるモジュールを取得。
    root_module = importlib.import_module(name)
    # 対象モジュールには__init__.pyが必要。
    # __init__.pyが存在しない場合、AssertionErrorが発生する。
    assert root_module.__file__ is not None
    root_module_dir = dirname(root_module.__file__)
    top_dir = pathlib.Path(root_module_dir).parent

    for root, _, files in os.walk(root_module_dir):
        for f in files:
            if not f.endswith(".py"):
                continue

            path = join(root, f)

            # パス名からモジュール名を生成
            module_name = path.replace(".py", "") \
                .replace(str(top_dir), "") \
                .replace(sep, ".") \
                .replace(".__init__", "")

            if module_name.startswith("."):
                module_name = module_name[1:]

            yield module_name


def include_routers(app: FastAPI) -> None:
    """routersモジュール配下のサブモジュールを読み込んで、APIRouterを登録する。

    :app: FastAPIインスタンス
    """
    for module_name in get_submodules("routers"):
        module = importlib.import_module(module_name)
        for obj in module.__dict__.values():
            if isinstance(obj, APIRouter):
                app.include_router(obj)


def create_app() -> FastAPI:
    env = os.getenv("FAST_API_ENV", "production").lower()

    if env in ("test", "development"):
        # 開発環境用の設定
        app = FastAPI(debug=True)
    else:
        # 本番環境用の設定
        #  docs:無効
        #  redoc:無効
        #  OpenAPI:無効
        app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

    env_origins = os.getenv("CORS_ORIGINS", None)
    if env_origins:
        origins = [origin.strip() for origin in env_origins.split(",")]

        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["GET", "HEAD", "POST"],
            allow_headers=["*"],
        )

    # routers配下のAPIRouterのオブジェクトを探して登録する
    include_routers(app)

    return app


app = create_app()


@app.get("/")
def read_root() -> dict:
    return {"Hello": "World"}


@app.on_event("startup")
async def startup() -> None:
    # 起動時に実行する処理
    pass


@app.on_event("shutdown")
async def shutdown() -> None:
    # 終了時に実行する処理
    pass
