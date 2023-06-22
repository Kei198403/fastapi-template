# Pythonのバージョンを変える場合はイメージを変更する
FROM python:3.11-slim-bookworm

USER root

# sudoとmakeを利用できるようにする
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends sudo build-essential

RUN groupadd -g 1000 developer && \
    useradd -u 1000 -g developer -G sudo -m -s /bin/bash vscode && \
    echo 'vscode:password' | chpasswd && \
    echo 'Defaults visiblepw'               >> /etc/sudoers && \
    echo 'vscode ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

# /appを/workspace/appへのシンボリックリンクとして作成
RUN \
    mkdir -p /workspace/.venv \
    && mkdir -p /workspace/app \
    && chown vscode:developer -R /workspace \
    && ln -s /workspace/app /app

USER vscode

ENV PATH /home/vscode/.local/bin:$PATH

WORKDIR /home/vscode

RUN pip3 --disable-pip-version-check --no-cache-dir install poetry

# 現在のプロジェクトディレクトリの下にvenv環境を作る。.venvディレクトリができる。
RUN poetry config virtualenvs.in-project true
# プロジェクトディレクトリ直下の.venvにdocker環境へのシンボリックリンクが存在していると
# Dev Containerが「EACCES: permission denied」で起動しなくなるので仮想環境をコピーするようにする
RUN poetry config virtualenvs.options.always-copy true

ENV LANG ja_JP.UTF-8
ENV TZ Asia/Tokyo
