build:
	docker compose build

down:
	docker compose down

start:
	docker compose up -d

restart: down start

up: build start migrate statics

statics:
	docker exec -ti backend python3 manage.py collectstatic --noinput

migrate:
	docker compose run --rm api python manage.py migrate

admin:
	docker compose run --rm api python manage.py createsuperuser

app:
	docker compose run --rm api python manage.py startapp $(app)

migrations:
	docker compose run --rm api python manage.py makemigrations

deps:
	docker compose run --rm api poetry install

lock:
	docker compose run --rm api poetry lock

bash:
	docker compose run --rm api /bin/sh

test: build migrate
	docker compose run --rm api python manage.py test

coverage: build migrate
	docker compose run --rm api coverage run --source='api' --omit='api/tests/*' manage.py test
	docker compose run --rm api coverage report
	docker compose run --rm api coverage xml

linter:
	docker compose run --rm api black .
	docker compose run --rm api isort .
	docker compose run --rm api flake8 .
	docker compose run --rm api pylint .