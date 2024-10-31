# .PHONY: run_app

run_app:  # запускаем приложение FastApi
	python src/entrypoints/app.py
#     uvicorn src.app:app --host 0.0.0.0 --reload

mypy:
	python -m mypy .

test: ## Выполняем тесты на pytest
	pytest
