# Makefile

.PHONY: up down build rebuild logs

up:
	docker-compose up -d

down:
	docker-compose down

build:
	docker-compose build

rebuild:
	docker-compose down
	docker-compose build
	docker-compose up -d

logs:
	docker-compose logs -f --tail=50
