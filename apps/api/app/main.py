from fastapi import FastAPI

from app.core.middleware import setup_middleware
from app.modules.catalog.router import router as catalog_router

app = FastAPI(title='Ogorod Market API')

setup_middleware(app)

app.include_router(catalog_router, prefix='/api')


@app.get('/api/health')
async def health_check():
    return {'status': 'ok'}
