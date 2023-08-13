.PHONY: all run migrate build up down redis test lint log_clear clean

all:
	@echo "devenv			- create and setup development virtual env using poetry" 
	@echo "run			- run web app"
	@echo "migrate			- run db migrations and upgrade db"
	@echo "docker 			- run web app at container"
	@echo "build 			- docker compose build"
	@echo "up			- up docker compose"
	@echo "down 			- down docker compose"
	@echo "redis	 		- up redis container at 6379 port"
	@echo "rabbitmq 		- run web rabbitmq app at 5672 port"
	@echo "test			- run testing"
	@echo "lint			- run flake8 linting"
	@echo "log_clear		- delete all files in logs/ dir"
	@echo "clean 			- clear dist/ folder"

devenv:
	poetry install --with=DEV  && poetry update

run: 
	python entrypoint.py

migrate:
	flask db migrate || true 
	flask db upgrade 

clean:
	rm -rf dist/

sdidst:
	poetry build 

build:
	docker compose build

up: build 
	docker stop linker_app || true
	docker stop flask_redis || true
	docker compose up -d

down:
	docker compose down

docker:
	docker stop linker_app || true
	docker run --rm -d \
		--name=linker_app \
		-h localhost \
		-p 5000:5000 \
		-p 6379:6379 linker_app

redis:
	docker stop flask_redis || true
	docker run \
	-d \
	--rm \
	--name=flask_redis \
	-p 6379:6379 redis

postgres:
	docker stop linker_app_postgres || true
	docker run --rm \
		--name linker_app_postgres \
		-p 5432:5432 \
		-e POSTGRES_USER=test \
		-e POSTGRES_PASSWORD=test \
		-e POSTGRES_DB=test_db \
		-d postgres:latest

rabbitmq:
	docker compose -f docker-compose-rabbit.yaml up --build -d 
test: 
	pytest --disable-warnings

lint:
	flake8 .
	
log_clear:
	rm ./logs/*

