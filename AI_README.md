# 🥒 Ogorod Market - Документация для AI Agents

> Этот файл — ранний бриф. Часть статуса ниже устарела: аутентификация и API корзины уже есть, модулей заказов и AI нет. Текущее описание проекта — корневой `README.md`.



## 📁 Структура проекта (Monorepo)

```
ogorod-market/
├── apps/
│   ├── api/                    # FastAPI бэкенд
│   │   ├── app/
│   │   │   ├── core/          # Конфигурация, БД, middleware
│   │   │   ├── modules/       # Бизнес-модули (auth, catalog, orders, ai)
│   │   │   └── main.py        # Точка входа
│   │   ├── alembic/           # Миграции БД
│   │   └── pyproject.toml     # Python зависимости
│   └── web/                   # Next.js 15 фронтенд
│       ├── src/
│       │   ├── app/           # App Router ((shop), (auth), (dashboard))
│       │   ├── components/    # UI и функциональные компоненты
│       │   └── types/         # TypeScript типы
│       └── package.json       # Node.js зависимости
├── shared/                    # Общие ресурсы (пока пусто)
├── docker-compose.yml         # Dev инфраструктура
└── Makefile                   # Автоматизация
```

## 🏗️ Технологический стек (September 2025)

### Backend
- **Python 3.11+** с FastAPI, SQLAlchemy 2.0 (async), Pydantic v2
- **PostgreSQL** через AsyncPG
- **Alembic** для миграций
- **Poetry** для управления зависимостями

### Frontend  
- **Next.js 15** с App Router и Turbopack
- **React 19** с хуками
- **TypeScript 5.9+** для типобезопасности
- **Tailwind CSS 4** для стилей
- **TanStack Query** для управления состоянием API

### Инфраструктура
- **Docker Compose** для разработки
- **pnpm** как менеджер пакетов фронтенда

## 🔌 API Specification

### Base URL
- Development: `http://localhost:8000/api`
- Все эндпоинты имеют префикс `/api`

### Key Endpoints
```
GET    /api/health
GET    /api/products/
GET    /api/products/{id}
GET    /api/products/by-slug/{slug}
POST   /api/auth/register
POST   /api/auth/login
GET    /api/auth/me
GET    /api/cart/
POST   /api/cart/items
PATCH  /api/cart/items/{item_id}
DELETE /api/cart/items/{item_id}
```

### CORS Configuration
- Разрешены: `localhost:3000`, `127.0.0.1:3000`
- Методы: ALL
- Заголовки: ALL

## 🎯 Архитектурные принципы

### Backend (FastAPI)
- **Модульность**: Каждая бизнес-логика в отдельной папке `modules/`
- **Слоистая архитектура**: Models → Services → Routers
- **Асинхронность**: Весь код async/await
- **Автодокументация**: OpenAPI через Swagger UI (`/docs`)

### Frontend (Next.js 15)
- **App Router**: Современная routing система
- **Server Components**: По умолчанию, клиентские только при необходимости
- **Type Safety**: Строгая типизация между фронтендом и бэкендом

### База данных
- **Асинхронные запросы** через SQLAlchemy 2.0
- **Миграции** через Alembic с автогенерацией
- **PostgreSQL 15** с индексами для производительности

## 🚀 Команды разработки

```bash
# Запуск всей инфраструктуры
make up

# Запуск бэкенда
cd apps/api && poetry run uvicorn app.main:app --reload --port 8000

# Запуск фронтенда  
cd apps/web && pnpm dev

# Миграции БД
cd apps/api && poetry run alembic upgrade head

# Наполнение тестовыми данными
make seed
```

## 📝 Code Style Guidelines

### Python
- **Именование**: `snake_case` для переменных и функций
- **Типизация**: Полная аннотация типов с Pydantic
- **Документация**: Docstrings в Google Style
- **Импорты**: Группировка (stdlib, third-party, local)

### TypeScript
- **Именование**: `camelCase` для переменных, `PascalCase` для компонентов
- **Типизация**: Строгая типизация, избегать `any`
- **Компоненты**: Functional components с хуками
- **Стили**: Tailwind CSS классы, избегать inline styles

## 🔮 Планы развития (Roadmap)

### Short-term (сейчас)
- [x] Аутентификация JWT (без Redis и refresh-токенов)
- [x] API корзины (UI корзины нет)
- [ ] Оформление заказов

### Medium-term 
- [ ] Панель администратора
- [ ] Загрузка изображений
- [ ] Email уведомления

### Long-term
- [ ] AI консультант (модуль `ai/`)
- [ ] PWA функциональность
- [ ] Мобильное приложение

## 🐛 Troubleshooting Guide

### Common Issues
1. **CORS ошибки**: Проверить middleware в `app/core/middleware.py`
2. **Нет подключения к БД**: Убедиться что Docker контейнер запущен
3. **Миграции не применяются**: Проверить `alembic.ini` и подключение к БД
4. **Типы не генерируются**: Запустить скрипт генерации из OpenAPI

### Debug Commands
```bash
# Проверка БД
docker ps | grep postgres

# Логи бэкенда
cd apps/api && poetry run uvicorn app.main:app --reload

# Проверка API
curl http://localhost:8000/api/health
```

## 💡 Для AI Agents (Важно!)

**При генерации кода учитывать:**
- Актуальные версии технологий (September 2025)
- Асинхронную архитектуру 
- Модульную структуру проекта
- TypeScript типизацию на фронтенде
- Pydantic схемы на бэкенде

**Избегать:**
- Устаревших подходов (class components, sync SQLAlchemy)
- Жестких зависимостей между модулями
- Кода без типизации

---

*Документация обновлена: September 2025*  
*Версия проекта: 0.1.0*
