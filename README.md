# Link loader

Project for add/store/delete and check link availability.
---

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)   
  - [Installation](#installation)
  - [Running the App](#running)
    - [Local](#running-local)
    - [Using Docker](#running-using-docker-compose)
- [Endpoints](#endpoints)
- [Testing](#testing)
- [Linting](#linting)

# Getting Started

## Prerequisites

- Python 3.9 or higher
- Poetry (for local development)
- Docker 

### Installation
Make sure you have Python 3.10 installed.
Project use poetry for control dependencies.

```bash
# Clone the repository
git clone <this repo url>

# Change into the project directory
cd Link-loader

# Install project dependencies and update them
poetry install && poetry update

# Activate virtual environment
poetry shell
```
All settings in setting.yaml file. 

All secrets can be setup using .env file or directly setup with "LINKER_APP_" prefix.

When settings vars duplicate, then used this priority: cmd_args > vars from .env > direct env vars > config.yaml 

### Running
Simple way to run app is using [docker compose](#running-using-docker-compose), 
but if you want to install it locally and setup url to database or message-queue by yourself
use follow [local](#running-local) installation option instruction.


- #### Running local:
In that way you can setup arguments as you want
```bash
# use -h flag for see help 
poetry run app [-h] [--config-file CONFIG_FILE] [--host HOST] [--port PORT] [--message-queue MESSAGE_QUEUE] [--channel CHANNEL]
           [--cors-allowed-origins CORS_ALLOWED_ORIGINS] [--log-buffer-size LOG_BUFFER_SIZE]
```

- #### Running using docker-compose
```bash
# build and run app and all necessary containers using docker-compose
make run-all 
```
# Endpoints
WIP
# Testing
For run test, ensure you install dev dependencies and run `make test`
```bash 
# install devs dependencies
make devenv

# activate vitrual envirnoment
poetry shell

# run tests
make test
```

# Linting
For run linting (using flake8), ensure you install dev dependencies and run `make lint`
```bash 
# install devs dependencies
make devenv

# activate vitrual envirnoment
poetry shell

# run linter
make lint
```


