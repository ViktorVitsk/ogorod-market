.PHONY: up down logs seed api web

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

seed:
	cd apps/api && poetry run python scripts/seed_database.py

api:
	cd apps/api && poetry run uvicorn app.main:app --reload --port 8000

web:
	cd apps/web && pnpm dev	

dev: up
		make api & 
		make web