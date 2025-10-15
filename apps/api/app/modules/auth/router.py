from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.modules.auth import schemas, service
from app.modules.auth.dependencies import get_current_user

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/register', response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
async def register(
    user_in: schemas.UserCreate,
    db: AsyncSession = Depends(get_db),
):
    user = await service.register_user(db, user_in)
    return user


@router.post('/login', response_model=schemas.Token)
async def login(credentials: schemas.UserLogin, db: AsyncSession = Depends(get_db)):
    return await service.authenticate_user(db, credentials.email, credentials.password)


@router.get('/me', response_model=schemas.UserRead)
async def read_me(current_user=Depends(get_current_user)):
    return current_user
