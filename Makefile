create_databases_for_dev:
	docker compose -f docker-compose.databases_for_dev.yml up -d
rm_and_clean_containers:  ## Остановить, удалить и очистить все контейнеры
	docker stop $$(docker ps -a -q) &&  docker rm $$(docker ps -a -q) && docker system prune -f

rm_and_clean_images:  ## Удалить и очистить все образы
	docker rmi $$(docker images -a -q) && docker system prune -f

start: ## Запустить контейнеры Docker
	docker-compose up --build -d
