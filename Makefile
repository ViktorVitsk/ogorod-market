.PHONY: up down logs build clean types wait-api rebuild seed migrate dev test

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

build:
	docker compose build

clean:
	docker compose down -v

wait-api:
	@echo "Waiting for API to be ready..."
	@until curl -s http://localhost:8000/api/health >/dev/null; do \
		echo "Waiting for API..."; \
		sleep 2; \
	done
	@echo "API is ready!"

types:
	cd apps/api && poetry run python ../../scripts/generate-openapi.py
	cd apps/web && pnpm exec openapi-typescript ../../openapi.json --output src/types/api.d.ts

rebuild: down build up logs

seed:
	docker compose exec api python scripts/seed_products.py

migrate:
	docker compose exec api alembic upgrade head

dev:
	docker compose up --build

test:
	cd apps/api && poetry run pytest
