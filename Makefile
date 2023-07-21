.PHONY: all run test lint black log_clear

all:
	@echo "devenv 			- create and setup development virtual env using poetry" 
	@echo "run				- run web app"
	@echo "run-all 			- app all app due docker compose"
	@echo "run redis 		- up redis container at 6379 port"
	@echo "test				- run testing"
	@echo "lint				- run linter checker"
	@echo "black				- run black for our code"
	@echo "log_clear			- delete all files in logs/ dir"

devenv:
	poetry install  && poetry update

run: 
	poetry run app 

clean:
	rm -rf dist/

sdidst:
	poetry build 

run-all:
	docker stop linker_app || true
	docker stop flask_redis || true
	docker compose up --build  #-d

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

test: 
	pytest --disable-warnings

lint:
	flake8 .
	
black:
	black .

log_clear:
	rm ./logs/*

