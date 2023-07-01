.PHONY: all run test lint black log_clear

all:
	@echo "run				- run web app"
	@echo "test				- run testing"
	@echo "lint				- run linter checker"
	@echo "black				- run black for our code"
	@echo "log_clear			- delete all files in logs/ dir"

run:
	python -m link_loader

test: 
	pytest .

lint:
	flake8 .
	
black:
	black .

log_clear:
	rm ./logs/*

