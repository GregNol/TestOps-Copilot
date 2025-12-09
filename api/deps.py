from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from api.settings import settings

# Схема авторизации: ожидает заголовок Authorization: Bearer <token>
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Проверяет валидность JWT токена.
    Если токен валиден, возвращает payload (данные пользователя).
    Если нет — выбрасывает 401.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Декодируем токен, используя секретный ключ
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception

        # Можно добавить проверку app_id или scope, если нужно
        return payload
    except JWTError:
        raise credentials_exception


async def get_token_header(token: str = Depends(oauth2_scheme)) -> str:
    """Возвращает чистый токен для передачи в downstream сервисы."""
    return token