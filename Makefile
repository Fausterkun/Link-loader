.PHONY: all run lint

all:
	@echo "run 				- run web app"
	@echo "lint				- run linter checker"
	@echo "black 			- run black for our code"
	@echo "log_clear 		- delete all files in logs/ dir"

run:
	python -m link_loader
lint:
	flake8 .
black:
	black .

log_clear:
	rm ./logs/*

test:
	@echo "still in WIP" 
	# pytest . 

