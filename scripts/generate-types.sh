#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.."

echo "Generating OpenAPI schema..."
(
  cd apps/api
  poetry run python ../../scripts/generate-openapi.py
)

echo "Generating TypeScript types..."
(
  cd apps/web
  pnpm exec openapi-typescript ../../openapi.json --output src/types/api.d.ts
)

echo "TypeScript types generated: apps/web/src/types/api.d.ts"
