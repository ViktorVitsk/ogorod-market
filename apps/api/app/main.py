from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.core.database import get_db
from app.modules.catalog.router import router as catalog_router

app = FastAPI(title="Ogorod Market API")

app.include_router(catalog_router)

@app.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    # Простая проверка, что приложение и БД работают
    await db.execute(text("SELECT 1"))
    return {"status": "OK"}