dev:
	# Swagger-UIへのアクセス
	echo "Swagger: http://127.0.0.1:8000/docs"
	# /workspace/appのシンボリックリンクを/appに作成してあり、そこを参照するようにしている
	bash server/start-reload.sh

start:
	export PORT=80 && bash server/start.sh

install:
	poetry install --no-root

update-check:
	poetry show --outdated

update-test:
	poetry update --dry-run

update:
	poetry update
