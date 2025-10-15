# 🥒 Ogorod Market - AI Agents Documentation

## 🏗️ Project Architecture Overview

### Monorepo Structure
```
ogorod-market/
├── apps/
│   ├── api/                    # FastAPI Backend
│   │   ├── app/
│   │   │   ├── core/          # Configuration, Database, Middleware
│   │   │   ├── modules/       # Business Modules (catalog, auth, cart*)
│   │   │   └── main.py        # App Factory
│   │   ├── alembic/           # Database Migrations
│   │   └── pyproject.toml     # Python Dependencies (Poetry)
│   └── web/                   # Next.js 15 Frontend
│       ├── src/
│       │   ├── app/           # App Router ((shop), (auth), (dashboard))
│       │   ├── components/    # UI & Feature Components
│       │   ├── hooks/         # Custom React Hooks
│       │   └── types/         # TypeScript Types (auto-generated)
│       └── package.json       # Node.js Dependencies (pnpm)
├── scripts/                   # Cross-project Scripts
├── docker-compose.yml         # Development Infrastructure
└── Makefile                   # Development Automation
```

### Technology Stack (September 2025)
- **Backend**: FastAPI, SQLAlchemy 2.0 (Async), PostgreSQL, Alembic, Pydantic v2, Poetry
- **Frontend**: Next.js 15 (App Router), React 19, TypeScript, Tailwind CSS 4, TanStack Query, pnpm
- **Infrastructure**: Docker, Docker Compose, pnpm, Poetry
- **Development**: ESLint, Ruff, Turbopack

## ✅ Completed Features

### Core Infrastructure
- [x] Monorepo setup with Docker Compose
- [x] PostgreSQL database with async SQLAlchemy
- [x] FastAPI with modular architecture
- [x] Next.js 15 with App Router
- [x] Automated TypeScript type generation from OpenAPI
- [x] TanStack Query for state management

### Business Features
- [x] Product catalog with CRUD API
- [x] Database seeding with sample vegetables
- [x] Type-safe API client
- [x] Responsive UI with Tailwind CSS
- [x] User registration and JWT-based login
- [x] Authenticated frontend (login/register forms, token handling)
- [x] Health-check endpoint for readiness probes

## 🚧 In Progress / Planned Features
- [ ] Authorization & session hardening (Redis-backed refresh tokens)
- [ ] Shopping cart functionality
- [ ] Order management system
- [ ] AI consultant integration
- [ ] Payment processing
- [ ] Admin dashboard

## 🔧 Development Workflow

### Code Generation Rules

#### Backend (Python/FastAPI)
```python
# ✅ CORRECT - Modern async patterns
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone

class Product(Base):
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

# ❌ AVOID - Sync patterns and utcnow()
from datetime import datetime  # Don't use utcnow()
```

#### Frontend (TypeScript/Next.js)
```typescript
// ✅ CORRECT - Client components + TanStack Query
'use client'
import { useQuery } from '@tanstack/react-query'

export function ProductList() {
  const { data: products } = useProducts()
  
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      {products?.map(product => (
        <ProductCard key={product.id} product={product} />
      ))}
    </div>
  )
}

// ❌ AVOID - Client-side data fetching without caching
useEffect(() => { /* direct API calls */ }, [])
```

### API Design Principles
- **RESTful endpoints** with `/api` prefix
- **Authentication** endpoints (`/api/auth/register`, `/api/auth/login`, `/api/auth/me`)
- **Bearer-токен** в заголовке `Authorization` (хранится в localStorage, проксируется axios-интерцептором)
- **Health-check** endpoint at `/api/health`
- **Async/await** throughout the backend
- **Pydantic schemas** for request/response validation
- **Automatic OpenAPI** documentation
- **Type-safe client** with auto-generated TypeScript types

### Database Conventions
- **Async SQLAlchemy 2.0** with proper session management
- **Alembic migrations** with autogenerate
- **Foreign key constraints** and indexes
- **UTC timestamps** stored as timezone-aware values

## 🛠️ Development Commands

### Using Makefile (Recommended)
```bash
make dev          # Full stack development
make types        # Generate TypeScript types
make seed         # Seed database with sample data
make migrate      # Run database migrations
make up          # Запуск инфраструктуры
make down        # Остановка всего
make logs        # Просмотр логов
make rebuild     # Полная пересборка
```

### Manual Commands
```bash
# Backend
cd apps/api && poetry run uvicorn app.main:app --reload --port 8000

# Frontend  
cd apps/web && pnpm dev

# Database
docker compose up -d postgres
```

## 🎯 AI Agent Guidelines

### When Generating Code

#### DO:
- Use **async/await** for all database operations
- Follow **modular architecture** - one feature per module
- Generate **both backend and frontend** code when applicable
- Include **TypeScript types** for frontend code
- Use **Tailwind CSS** for styling
- Implement **proper error handling**
- Add **Pydantic schemas** for API validation

#### DON'T:
- Use **synchronous database calls**
- Create **circular imports**
- Skip **type annotations** in Python
- Use **deprecated methods** (like datetime.utcnow)
- Mix **client and server components** incorrectly in Next.js

### Code Review Checklist
- [ ] Async/await patterns used consistently
- [ ] Type safety maintained (TypeScript & Pydantic)
- [ ] Database operations use proper session management
- [ ] API endpoints follow RESTful conventions
- [ ] Frontend components use TanStack Query for data fetching
- [ ] Error handling implemented
- [ ] Code follows the project's modular structure

## 🔄 Auto-Generation System

### TypeScript Types
Types are automatically generated from FastAPI OpenAPI schema:
```bash
make types
# 1. Generates openapi.json from running FastAPI
# 2. Creates apps/web/src/types/api.d.ts via openapi-typescript
```

### API Client
Frontend uses auto-generated types for type-safe API calls:
```typescript
import { api, Product } from '@/app/api/client'
// Product type is auto-generated from backend schemas
```

## 🐛 Common Issues & Solutions

### Database Connection Issues
```bash
# Reset database
docker compose down -v
docker compose up -d postgres
make migrate
```

### Type Generation Failures
```bash
# Ensure API is running, then:
make types
# Or manually:
cd apps/api && poetry run uvicorn app.main:app --port 8000 &
cd apps/web && npx openapi-typescript ../../openapi.json --output src/types/api.d.ts
```

### Dependency Issues
```bash
# Backend
cd apps/api && poetry install

# Frontend
cd apps/web && pnpm install
```

## 📈 Project Roadmap

### Phase 1: MVP (Current)
- [x] Basic product catalog
- [x] Type-safe full-stack architecture
- [ ] User authentication (in progress)
- [ ] Shopping cart (in progress)

### Phase 2: E-commerce
- [ ] Order management
- [ ] Payment integration
- [ ] Inventory management

### Phase 3: Advanced Features
- [ ] AI product recommendations
- [ ] Advanced analytics
- [ ] Mobile app

---

*Last Updated: September 2025*  
*Project Version: 0.5.0*  
*Maintainer: Viktor Stoianov*
