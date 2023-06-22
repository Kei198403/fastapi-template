# -*- coding: utf-8 -*-

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


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
