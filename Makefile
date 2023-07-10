.PHONY: all run test lint black log_clear

all:
	@echo "run				- run web app"
	@echo "test				- run testing"
	@echo "lint				- run linter checker"
	@echo "black				- run black for our code"
	@echo "log_clear			- delete all files in logs/ dir"

run: 
	python -m link_loader

docker:
	docker stop linker_app || true
	docker run --rm -d \
		--name=linker_app \
		-h localhost \
		-p 5000:5000 \
		-p 6379:6379 linker_app

docker-build:
	docker build -t linker_app . 

redis:
	docker stop flask_redis || true
	docker run \
	-d \
	--rm \
	--name=flask_redis \
	-p 6379:6379 redis
test: 
	pytest .

lint:
	flake8 .
	
black:
	black .

log_clear:
	rm ./logs/*

