.PHONY: all run test lint black log_clear

all:
	@echo "run				- run web app"
	@echo "test				- run testing"
	@echo "lint				- run linter checker"
	@echo "black				- run black for our code"
	@echo "log_clear			- delete all files in logs/ dir"

run: redis 
	python -m link_loader

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

