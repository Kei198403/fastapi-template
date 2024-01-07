# -*- coding: utf-8 -*-

import os

from contextlib import asynccontextmanager
from typing import AsyncGenerator, Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def create_app() -> FastAPI:
    env = os.getenv("FAST_API_ENV", "production").lower()

    if env in ("test", "development"):
        # 開発環境用の設定
        app = FastAPI(lifespan=lifespan, debug=True)
    else:
        # 本番環境用の設定
        #  docs:無効
        #  redoc:無効
        #  OpenAPI:無効
        app = FastAPI(lifespan=lifespan, docs_url=None, redoc_url=None, openapi_url=None)

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

    return app


async def startup(app: FastAPI) -> None:
    # 起動時に実行する処理
    pass


async def shutdown(app: FastAPI) -> None:
    # 終了時に実行する処理
    pass


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
    """see: https://fastapi.tiangolo.com/advanced/events/
    """
    await startup(app)
    try:
        yield
    finally:
        await shutdown(app)


app = create_app()


@app.get("/")
def read_root() -> dict:
    return {"Hello": "World"}
