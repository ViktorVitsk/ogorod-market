from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.core.database import get_db
from app.core.middleware import setup_middleware
from app.modules.catalog.router import router as catalog_router

app = FastAPI(title="Ogorod Market API")

setup_middleware(app)

app.include_router(catalog_router, prefix="/api")
