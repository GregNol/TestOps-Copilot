from ..password import get_password_hash, verify_password
from ..db import manager
from ..settings import settings
from fastapi import APIRouter, HTTPException, Depends, status, Request
from ..schemas import RegisterSchema, LoginSchema, TokenUpdateSchema
from ..db.manager import Manager
from datetime import datetime, timedelta
from ..tokens import create_access_token, verify_token_and_get_user_id
router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    new_user: RegisterSchema,
):
    try:
        manager = Manager(settings.DB_USERS_URL)
        # Проверка на существование
        if await manager.user_exists_by_login(new_user.login):
            raise HTTPException(
                status_code=400,
                detail="Пользователь с таким именем уже существует"
            )

        # Хеширование пароля
        hashed_password = get_password_hash(new_user.password)

        # Сохранение в "БД"
        new_user = await manager.create_user(login=new_user.login, password_hash=hashed_password, email=new_user.email, full_name=new_user.full_name)

        # Генерация токена сразу после регистрации
        access_token_expires = timedelta(
            minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        # В токен кладем ID, а не username, как вы просили
        access_token = create_access_token(
            data={"sub": new_user.id},
            expires_delta=access_token_expires
        )

        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        # Обработка ошибок
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/login")
async def login(
    user_data: LoginSchema,
):
    try:
        manager = Manager(settings.DB_USERS_URL)
        # Ищем пользователя
        user = await manager.get_user_by_login(user_data.username)

        # Проверяем пароль
        if not user or not verify_password(user_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный логин или пароль",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Генерируем токен с ID
        access_token_expires = timedelta(
            minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.id},
            expires_delta=access_token_expires
        )

        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        # Обработка ошибок
        raise HTTPException(status_code=500, detail=e)


@router.post("/refresh")
async def refresh_token(
    data: TokenUpdateSchema,
):
    try:
        refresh_token = TokenUpdateSchema.refresh_token
        access_token_expires = timedelta(
            minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        user_id = verify_token_and_get_user_id(refresh_token)
        access_token = create_access_token(
            data={"sub": user_id},
            expires_delta=access_token_expires
        )

        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        # Обработка ошибок
        raise HTTPException(status_code=500, detail=e)
