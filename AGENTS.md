# 🥒 Ogorod Market — AI Playbook

Этот файл — стартовая точка для любого AI-агента, подключающегося к проекту. Он описывает цели, текущую архитектуру, активные задачи и правила разработки. Соблюдайте его, чтобы синхронизироваться с продуктовой стратегией и не сломать уже работающую функциональность.

---

## 🎯 Продуктовое видение

- Построить типовое e-commerce приложение для фермерского маркетплейса овощей.
- MVP фокусируется на витрине, каталоге, базовой аутентификации и корзине.
- Проект рассчитан на дальнейшее расширение: заказы, платежи, AI-консультант, интеграции.

## 🔄 Текущий статус (октябрь 2025)

- ✅ Каталог товаров: CRUD, сидирование тестовыми овощами.
- ✅ Аутентификация: регистрация/логин по email + JWT, клиентский UI.
- ✅ Фронтенд: Next.js 15 (App Router), TanStack Query, типобезопасный API-клиент.
- ✅ Генерация типов: OpenAPI → `apps/web/src/types/api.d.ts`.
- 🚧 Корзина: в работе бэкенд-модуль `cart`.
- ⏳ Следующие этапы: оформление заказа, платежи, админка, Google OAuth.

## 🧱 Архитектура (монорепозиторий)

```
ogorod-market/
├── apps/
│   ├── api/        # FastAPI + SQLAlchemy 2.0 (async)
│   │   ├── app/
│   │   │   ├── core/     # config, DB, middleware, security
│   │   │   ├── modules/
│   │   │   │   ├── auth      # users, JWT, OAuth2 схемы
│   │   │   │   ├── catalog   # товары, CRUD
│   │   │   │   └── cart*     # корзина (создаётся сейчас)
│   │   │   └── main.py   # FastAPI app factory
│   │   ├── alembic/      # миграции
│   │   └── pyproject.toml
│   └── web/          # Next.js 15 (App Router)
│       ├── src/
│       │   ├── app/        # маршруты ((shop), (auth))
│       │   ├── components/ # UI-компоненты
│       │   ├── hooks/      # TanStack Query hooks
│       │   └── types/      # OpenAPI-генерация
│       └── package.json
├── scripts/        # генерация OpenAPI и типов
├── docker-compose.yml
└── Makefile
```

**Backend ключевые моменты**

- Асинхронный SQLAlchemy 2.0 с `AsyncSession`.
- Пароли хэшируются через `passlib` (`pbkdf2_sha256`).
- Время в базе только `DateTime(timezone=True)` + `func.now()`.
- Модули (`app/modules/*`) придерживаются слоям: `models.py`, `schemas.py`, `service.py`, `router.py`.
- Alembic: каждая схема → новая миграция в `apps/api/alembic/versions`.

**Frontend ключевые моменты**

- Next.js App Router, компоненты по сегментам (`(shop)`, `(auth)`).
- TanStack Query для фетчинга; `useQuery`/`useMutation` в кастомных hooks.
- Axios клиент (`apps/web/src/app/api/client.ts`) добавляет Bearer-токен из `localStorage`.
- Tailwind CSS 4 через глобальные стили; минималистичная UI-компонентная база.
- Типы API берутся из `apps/web/src/types/api.d.ts` (генерируется командой `make types`).

## 🤖 Правила для AI-агентов

1. **Одна задача — один модуль.** Новая бизнес-логика = новая папка в `modules/` и свои схемы/сервисы.
2. **Async only.** Никаких синхронных запросов к БД или блокирующих операций.
3. **UUID не используется.** Идентификаторы — целочисленные автоинкременты; даты — с таймзоной.
4. **JWT Access в localStorage.** Refresh/Redis появится позже — не ломать текущее поведение.
5. **Type safety.** Python — полная типизация, Pydantic v2; TypeScript — без `any`.
6. **Error handling.** Любая операция, которая может упасть, должна отдать понятный `HTTPException`.
7. **Документация.** Изменили фичу → обязательно обновите этот файл + сгенерируйте OpenAPI/типы.
8. **Миграции.** Любая правка моделей = новая Alembic-ревизия; не редактировать старые миграции.
9. **Коммиты.** Стиль Conventional Commits (`feat:`, `fix:`, `refactor:` и т.д.).
10. **Соблюдайте Makefile.** Для типизации и генераций используйте `make` — так меньше расхождений.

## 🔐 Аутентификация

- Регистрация/логин: `/api/auth/register`, `/api/auth/login`.
- Профиль: `/api/auth/me` (Bearer token обязателен).
- Пароли ≥ 8 символов; хэш `pbkdf2_sha256`.
- План: позднее добавить Google OAuth и refresh-токены (держать в Roadmap).

## 🛒 Корзина (в работе)

- Цель: модуль `cart` с таблицами `carts`, `cart_items`, привязка к `users`.
- Логика: `GET /api/cart`, `POST /api/cart/items`, `PATCH /api/cart/items/{item_id}`, `DELETE /api/cart/items/{item_id}`.
- Цена позиции берётся из каталога на момент добавления (`Product.price`).
- После завершения бэкенда — перейти к фронтовому UI (TanStack Query + optimistic updates).

## 📦 Среда разработки

- **Docker:** `docker compose up -d` поднимает PostgreSQL, FastAPI, Next.js (dev-режим).
- **Makefile:** `make dev`, `make types`, `make migrate`, `make seed`.
- **Локально:** `apps/api` → `poetry run uvicorn app.main:app --reload`; `apps/web` → `pnpm dev`.
- **OpenAPI генерация:** `make types` (если `poetry` не может в интернет — см. `scripts/generate-openapi.py`).

## 🧪 Проверка и стиль

- Python lint: `poetry run ruff check` (можно локально).
- TypeScript lint: `pnpm lint`.
- Тестов пока нет — при добавлении новой логики приветствуются `pytest` и `playwright` smoke tests.

## 🚀 Дорожная карта MVP

1. **Спринт 1 (готово):** каталог, аутентификация, фронтовая витрина.
2. **Спринт 2 (текущий):** корзина + подготовка к заказам.
3. **Спринт 3:** оформление заказа, платежные моксы, email-уведомления.
4. **Будущее:** Google OAuth, Redis refresh, AI-консультант, админ-панель.

## 🆘 Частые проблемы

- **БД не поднимается:** `docker compose down -v && docker compose up -d postgres && make migrate`.
- **OpenAPI не генерится:** убедитесь, что API запущен; при проблемах используйте `python scripts/generate-openapi.py`.
- **CORS:** настройки в `app/core/middleware.py`; для новых доменов добавляйте там.
- **JWT 401:** проверьте, что токен есть в localStorage, и axios добавляет `Authorization: Bearer`.

---

**Контекст для новых агентов:** держите цель MVP в фокусе, фиксируйте изменения в документации и миграциях, и сообщайте о допущениях. Если возникает необходимость менять архитектуру — согласуйте перед реализацией. Отличной разработки! 🥒
