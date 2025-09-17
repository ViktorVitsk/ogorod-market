.PHONY: up down logs

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

seed:
	cd apps/api && poetry run python scripts/seed_database.py