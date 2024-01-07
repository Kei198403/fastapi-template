# プロジェクト構築

Dev Containersの環境ができていれば、リポジトリをクローンして、VS Codeで開けば使える状態になります。

# 環境情報
- Python：3.12
- パッケージ管理： poetry
- Linter: flake8、mypy
- Formatter: autopep8

.devcontainer/Dockerfileで指定しているイメージのバージョンを変更すれば、別のバージョンでも利用できるはずです。  

## Dev Containersの環境でのアプリ実行

### make dev

live reloadありでuvicornを実行。

### make start

live reloadなしでuvicornを実行。

# venv環境について

プロジェクトルート直下に.venvディレクトリを作るようになっています。  
Dev Containersで開いた際、.devcontainer/init.shでpoetry installを実行しています。  
なお、初回はパッケージインストールより前にunittestのDiscoverが動いてエラーが出ることがありますが、
パッケージのインストールが終われば正常にテストができるようになります。

venv環境をリセットする場合は、.venvを削除してコンテナをリビルドしてください。

## venvの設定(poetry config --list)
- virtualenvs.options.always-copy: true  
  WindowsのWSL+Docker+Dev Containers環境で、.venv内にシンボリックリンクが含まれていて、Windowsおよびwslからアクセスできない場合、Dev Containers環境が起動しなくなる問題を回避するため、シンボリックリンクを作らないようにファイルをコピーする。
- virtualenvs.in-project: true  
  プロジェクト内に.venvを作成する。.vscode/settings.jsonでの各種ツールのパスを固定化するため。

# Production環境について（docker composeの場合）

## docker-compose.ymlのサンプル

本テンプレートを元に作成したアプリを./build/fastapi_appnameにclone。

```
services:
  nginx:
    image: nginx:stable-alpine
    restart: always
    volumes:
      - ./nginx/docs:/usr/share/nginx/html:ro
      - ./nginx/nginx.conf:/etc/nginx/conf.d/default.conf:ro
    ports:
      - "80:80"
    depends_on:
      - fastapi_appname
  fastapi_appname:
    build:
      context: ./build/fastapi_appname
      dockerfile: Dockerfile
    image: fastapi_appname:latest
    restart: always
    environment:
      PORT: 8080
      FAST_API_ENV: production

```

# nginx.confのサンプル

```
server {
  listen       80;
  location / {
      root   /usr/share/nginx/html;
      index  index.html index.htm;
  }

  error_page  404              /404.html;

  # redirect server error pages to the static page /50x.html
  #
  error_page   500 502 503 504  /50x.html;
  location = /50x.html {
      root   /usr/share/nginx/html;
  }

  # リバースプロキシ関係
  proxy_set_header    Host                $host;
  proxy_set_header    X-Forwarded-Host    $http_host;
  proxy_set_header    X-Forwarded-Port    $server_port;
  proxy_set_header    X-Forwarded-Proto   $scheme;
  proxy_set_header    X-Forwarded-For     $proxy_add_x_forwarded_for;
  proxy_set_header    X-Real-IP           $remote_addr;

  # Swaggerをリバースプロキシ経由で利用する場合はsub_filterを活用する。
  location /appname/ {
    proxy_pass http://fastapi_appname:8080/;
  }
}
```


# GitコミットのPrefixルール

- feat: 新しい機能
- fix: バグの修正
- docs: ドキュメントのみの変更
- style: 空白、フォーマット、セミコロン追加など
- refactor: 仕様に影響がないコード改善(リファクタ)
- perf: パフォーマンス向上関連
- test: テスト関連
- chore: ビルド、補助ツール、ライブラリ関連

参考：https://qiita.com/numanomanu/items/45dd285b286a1f7280ed

# Poetryコマンドリファレンス

| コマンド | 備考 |
| ---- | ---- |
| poetry shell | venv環境へ接続 |
| poetry config --list | poetryの設定一覧を表示 |
| poetry add パッケージ | パッケージを追加 |
| poetry add -G dev パッケージ | 開発パッケージを追加 |
| poetry show | パッケージを表示 |
| poetry show --outdated | アップデート可能なパッケージを表示 |
| poetry update --dry-run | アップデート処理の仮実行 |
| poetry update パッケージ | 特定のパッケージを更新 |
| poetry update | アップデートの実行 |
| poetry shell | venv環境をアクティベートする |
| poetry install | dependencies、dev-dependenciesをインストール |
| poetry install --no-dev | dependenciesのみをインストール |
| poetry check | pyproject.tomlの検証 |
| poetry env info | venv環境情報を表示 |

ドキュメント：https://python-poetry.org/docs/

# Dev Containersについて

[VS CodeでDocker開発コンテナを便利に使おう](https://qiita.com/Yuki_Oshima/items/d3b52c553387685460b0)

