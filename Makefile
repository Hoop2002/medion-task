run-compose-dev:
	docker compose --env-file development.env up

stop-compose-dev:
	docker compose --env-file development.env down

rebuild-compose-dev:
	docker compose --env-file development.env up --build

drop-compose-dev:
	docker compose --env-file development.env rm

import-env:
	export $(grep -v '^#' development.env | xargs)

runserver-dev:
	poetry run python3 manage.py runserver 127.0.0.1:8000