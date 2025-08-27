from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.core.database import get_db

app = FastAPI(title="Greenhouse API")

@app.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    # Простая проверка, что приложение и БД работают
    await db.execute(text("SELECT 1"))
    return {"status": "OK"}