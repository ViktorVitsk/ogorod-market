#!/bin/bash
cd "$(dirname "$0")/.."

# Генерируем OpenAPI схему
echo "Generating OpenAPI schema..."
python scripts/generate-openapi.py

# Генерируем TypeScript типы
echo "Generating TypeScript types..."
npx openapi-typescript ../openapi.json --output src/types/api.d.ts

echo "✅ TypeScript types generated: src/types/api.d.ts"