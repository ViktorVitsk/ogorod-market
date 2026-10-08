# 🥒 Ogorod Market — AI Playbook

Этот файл — стартовая точка для любого AI-агента, подключающегося к проекту. Он описывает цели, текущую архитектуру, активные задачи и правила разработки. Соблюдайте его, чтобы синхронизироваться с продуктовой стратегией и не сломать уже работающую функциональность.

---

## 🎯 Продуктовое видение

- Построить типовое e-commerce приложение для фермерского маркетплейса овощей.
- MVP фокусируется на витрине, каталоге, базовой аутентификации и корзине.
- Проект рассчитан на дальнейшее расширение: заказы, платежи, AI-консультант, интеграции.

## 🔄 Текущий статус

Актуальный обзор для людей — корневой `README.md`. Кратко:

- ✅ Каталог: CRUD и сиды. Запись в каталог не требует авторизации. Это осознанный пробел прототипа.
- ✅ Аутентификация: регистрация, логин, `/api/auth/me`. JWT обязателен в окружении, запасного ключа в коде нет.
- ✅ Корзина: API есть. Цена берётся из каталога. UI корзины не подключён, кнопка в каталоге отключена.
- ✅ Фронтенд: главная, каталог, логин, регистрация, статус в шапке.
- ✅ Тесты API: `apps/api/tests`, SQLite, без прогона Alembic.
- ⏳ Не сделано: заказы, оплата, админка, refresh-токены, Google OAuth.

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

## 🛒 Корзина

- Таблицы `carts` и `cart_items`, одна корзина на пользователя, одна строка на товар.
- `GET /api/cart/` возвращает 404, пока корзины нет. `POST /api/cart/items` создаёт её и задаёт количество.
- `PATCH` и `DELETE` `/api/cart/items/{item_id}` адресуют id строки корзины, не id товара.
- Цена фиксируется из каталога при создании строки. Клиент цену не передаёт.
- Фронтовый UI корзины не начат.

## 📦 Среда разработки

- **Docker:** `docker compose up --build` поднимает PostgreSQL, FastAPI и собранный Next.js (`pnpm start`, не `next dev`). Перед этим нужен `.env` с `JWT_SECRET_KEY`.
- **Makefile:** `make dev`, `make types`, `make migrate`, `make seed`.
- **Локально:** `apps/api` → `poetry run uvicorn app.main:app --reload`; `apps/web` → `pnpm dev`.
- **OpenAPI генерация:** `make types` (если `poetry` не может в интернет — см. `scripts/generate-openapi.py`).

## 🧪 Проверка и стиль

- Python lint: `poetry run ruff check` (можно локально).
- TypeScript lint: `pnpm lint`.
- API: `cd apps/api && poetry run pytest`. Тесты поднимают SQLite, не PostgreSQL.
- Фронтенд: `pnpm lint`, `pnpm exec tsc --noEmit`, `pnpm build`. Playwright в проекте нет.

## 🚀 Дорожная карта MVP

1. **Спринт 1 (готово):** каталог, аутентификация, фронтовая витрина.
2. **Спринт 2 (частично):** API корзины готов, витрина к нему не подключена.
3. **Не начато:** заказы, платежи, email, Google OAuth, Redis refresh, админ-панель.

## 🆘 Частые проблемы

- **БД не поднимается:** `docker compose down -v && docker compose up -d postgres && make migrate`.
- **OpenAPI не генерится:** убедитесь, что API запущен; при проблемах используйте `python scripts/generate-openapi.py`.
- **CORS:** настройки в `app/core/middleware.py`; для новых доменов добавляйте там.
- **JWT 401:** проверьте, что токен есть в localStorage, и axios добавляет `Authorization: Bearer`.

---

**Контекст для новых агентов:** держите цель MVP в фокусе, фиксируйте изменения в документации и миграциях, и сообщайте о допущениях. Если возникает необходимость менять архитектуру — согласуйте перед реализацией. Отличной разработки! 🥒
