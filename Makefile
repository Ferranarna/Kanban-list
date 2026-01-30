# Variables
DOCKER_COMPOSE = docker compose

.PHONY: up down restart logs test

up:
	$(DOCKER_COMPOSE) up -d

down:
	$(DOCKER_COMPOSE) down -v

restart:
	$(DOCKER_COMPOSE) down && $(DOCKER_COMPOSE) up -d

logs:
	$(DOCKER_COMPOSE) logs -f

run:
	uv run uvicorn src.app.main:app --reload