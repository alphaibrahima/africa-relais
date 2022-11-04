.PHONY: docs clean

COMMAND = python3 manage.py

all: build test

build:
	docker-compose build

run:
	docker-compose up

migrate:
	$(COMMAND) migrate

collectstatic:
	$(COMMAND) collectstatic


test:
	cd src && pytest

runserver:
	$(COMMAND) runserver

migration:
	$(COMMAND) makemigrations

superuser:
	$(COMMAND) createsuperuser

codestyle:
	pipenv run flake8
	pipenv run black  --exclude migrations --check .