from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os


def setup_cors_middleware(app: FastAPI) -> None:
    # Разрешаем несколько origin'ов для разработки
    origins = [
        'http://localhost:3000',  # Next.js dev
        'http://127.0.0.1:3000',  # Альтернативный localhost
        'http://localhost:8000',  # Для доступа к Swagger
    ]

    # В production можно добавить реальные домены
    if os.getenv('ENVIRONMENT') == 'production':
        origins.extend(
            [
                'https://yourdomain.com',
                'https://www.yourdomain.com',
            ]
        )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )


def setup_middleware(app: FastAPI) -> None:
    setup_cors_middleware(app)
