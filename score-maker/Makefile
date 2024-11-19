# .PHONY: run_app

run_app:  # запускаем приложение FastApi
	python src/entrypoints/app.py
#     uvicorn src.app:app --host 0.0.0.0 --reload

mypy:
	python -m mypy .

test: ## Выполняем тесты на pytest
	pytest

rm_and_clean_containers:  ## Остановить, удалить и очистить все контейнеры
	docker stop $$(docker ps -a -q) &&  docker rm $$(docker ps -a -q) && docker system prune -f

rm_and_clean_images:  ## Удалить и очистить все образы
	docker rmi $$(docker images -a -q) && docker system prune -f

start: ## Запустить контейнеры Docker
	docker-compose up --build -d

psql:
	psql -U user -h 0.0.0.0 -p 5435 -d score_maker_db

alembic_init:
	alembic init -t async migrations
