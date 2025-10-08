.PHONY: up down logs build clean types

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
	docker system prune -f

types:
	cd apps/api && poetry run python ../../scripts/generate-openapi.py
	cd apps/web && pnpm openapi-typescript ../../openapi.json --output src/types/api.d.ts

# Композитные команды (не нужны в .PHONY)
rebuild: down build up logs

seed:
	docker compose exec api python scripts/seed_products.py

migrate:
	docker compose exec api alembic upgrade head

dev: down build up logs