# Ogorod Market

Ogorod Market is an unfinished prototype of a small online shop for a family farm. The author built it independently in 2025 and used AI coding assistants as helpers. It was never put into operation. It is not a video-course exercise and it is not a commercial store.

## Architecture

The repository is a monorepo.

- `apps/api` is a FastAPI application. Business code lives in the `auth`, `catalog`, and `cart` modules. Each module separates SQLAlchemy models, Pydantic schemas, a service, and a router. Database access is asynchronous.
- `apps/web` is a Next.js App Router application. The catalog and account pages are client components. TanStack Query loads data through an Axios client. The TypeScript types in `apps/web/src/types/api.d.ts` are generated from `openapi.json`.
- PostgreSQL 15 is the intended database. Alembic owns the schema. Docker Compose starts Postgres, applies migrations, seeds a few products, and serves the API and the built web app.

```text
browser (Next.js, port 3000)
        |
        |  http://localhost:8000/api
        v
FastAPI (port 8000) ---- async SQLAlchemy ----> PostgreSQL (port 5432)
```

The browser has to call a host it can resolve. `http://api:8000` works only inside the Compose network, so the web image is built with `http://localhost:8000`. `NEXT_PUBLIC_API_URL` is the API origin without a `/api` suffix. The client adds that prefix. A value that already ends in `/api` is accepted and is not doubled.

## What is implemented

- `GET /api/health`. This checks that the process responds. It does not check the database.
- Catalog reads are public: list, read by id, and read by slug. They return active products only. Create, partial update, and soft delete require a signed-in user with `is_superuser`. Registration cannot set that flag. There is no admin screen; the flag is changed in the database, for example `UPDATE users SET is_superuser = true WHERE email = '...'`. The seed script inserts five vegetables directly and does not go through this check.
- Accounts: email registration, login, and `GET /api/auth/me`. Passwords are hashed with PBKDF2-SHA256 and must be at least 8 characters. Login returns a JWT access token. The storefront keeps that token in `localStorage`.
- Cart API for a signed-in user: read the cart, set a line quantity, change that quantity, and remove a line. The line price is copied from the catalog when the line is created. The client cannot choose the price. `PATCH` and `DELETE` use the cart line id.
- Storefront: home page, catalog, login, registration, and a header that shows the signed-in account. The catalog button "В корзину" is disabled. The page does not call the cart API.

## What is not implemented

- Checkout, orders, payments, and delivery.
- A cart page, and adding a product from the catalog UI.
- Refresh tokens, server-side logout, OAuth, and an admin interface. `is_superuser` only gates catalog writes.
- Categories. `category_id` is a nullable integer with no related table.
- Product images. The seed data refers to paths the app does not serve.
- Stock checks. A cart line can request more units than `stock_quantity`.

## Stack

- Python 3.11+, FastAPI 0.116, SQLAlchemy 2.0, Alembic, Pydantic 2, asyncpg, PyJWT, passlib
- PostgreSQL 15
- Next.js 15.5, React 19, TypeScript 5.9, Tailwind CSS 4, TanStack Query 5, Axios
- Poetry, pnpm 10.17, Docker Compose

Exact versions are in `apps/api/poetry.lock` and `apps/web/pnpm-lock.yaml`.

## Run with Docker Compose

Compose is the intended way to run Postgres, the API, and the web app together. The API refuses to start when `JWT_SECRET_KEY` is missing or shorter than 32 characters.

```bash
cp .env.example .env
docker compose up --build
```

- Storefront: http://localhost:3000
- API docs: http://localhost:8000/docs
- Health: http://localhost:8000/api/health

The JWT value in `.env.example` is public, because it is committed. It is only for a local demo. Replace it before exposing the API beyond your own machine. The Compose database password is the local default `postgres`.

```bash
docker compose up -d      # make up
docker compose logs -f    # make logs
docker compose down       # make down
docker compose down -v    # make clean; this deletes the database volume
```

`make dev` runs `docker compose up --build`.

On startup the API container waits briefly, applies Alembic migrations, seeds products when the catalog is empty, then starts Uvicorn.

## Run locally without Compose

You still need PostgreSQL and the variables from `.env.example`. Settings are read from the environment, `apps/api/.env`, or the repository root `.env`.

```bash
cd apps/api
poetry install --extras dev
poetry run alembic upgrade head
poetry run python scripts/seed_products.py
poetry run uvicorn app.main:app --reload --port 8000
```

```bash
cd apps/web
pnpm install
pnpm dev
```

For a browser on the same machine, set `NEXT_PUBLIC_API_URL=http://localhost:8000`.

After an API schema change, regenerate the OpenAPI document and the TypeScript types. This does not need a running server. It does need `JWT_SECRET_KEY`, Poetry, and pnpm.

```bash
make types
```

## Checks

The API tests use an in-memory SQLite database. They cover token rejection, registration and login, catalog permissions, and the cart rules described above. They do not apply the Alembic migrations and they are not a substitute for PostgreSQL.

Docker Compose was not started during this preparation. Docker is not available in the environment where the repository was reviewed, so migration on PostgreSQL is still unchecked.

```bash
cd apps/api
poetry install --extras dev
poetry run pytest
```

Frontend:

```bash
cd apps/web
pnpm install
pnpm lint
pnpm exec tsc --noEmit
pnpm build
```

`apps/web/.npmrc` hoists the ESLint plugins that pnpm otherwise hides from `eslint-config-next`. `package.json` allows install scripts for Tailwind, Sharp, and the resolver ESLint needs. Without those scripts, `pnpm install` on pnpm 10 can leave the production build unable to compile CSS.

## Limitations

- There is no screen or API for granting `is_superuser`. A database update is the only way, and that is easy to forget on a fresh install.
- The access token is stored in `localStorage`. There is no refresh token. A stolen token stays valid until it expires, which is 60 minutes by default.
- The example JWT secret and the Compose database password are development defaults, and both are visible in the repository.
- CORS allows the local web origins. `app/core/middleware.py` still contains placeholder production domains. That is not a deployment configuration.
- SQL logging is off unless `SQL_ECHO=true`.
- `updated_at` changes when SQLAlchemy updates a row. PostgreSQL does not maintain that column on its own.
- Hiding a product does not remove cart lines that already reference it. A hidden product cannot be added again.
- Sending `POST /api/cart/items` again for the same product sets the quantity. It does not increase the existing quantity.
- An empty cart is `404`, not an empty object. The first successful `POST /api/cart/items` creates the cart.

## Use of AI assistants

AI coding assistants helped with scaffolding, some features, and a later review of defects. `AI_README.md` and `AGENTS.md` were written as context for those assistants and are not a course syllabus. The git history still contains experimental and incomplete commits from 2025, and that history was left intact.

The review fixed confirmed defects, including a built-in JWT signing key, cart pricing, and open catalog writes. It did not finish the shop: there is still no checkout, and the catalog page does not call the cart API.
