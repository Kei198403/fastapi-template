#!/bin/bash

mkdir -p /workspace/.venv

cd /workspace
# ImportError回避のため
unset PYTHONPATH
# パッケージをvenvへinstall
poetry install --no-root
