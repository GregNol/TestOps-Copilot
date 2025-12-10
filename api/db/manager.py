import logging
from sqlalchemy import select
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

from ..domain.user import User
from .models import Users
from .exceptions import UserNotFoundException
logger = logging.getLogger(__name__)


class Manager:
    """Менеджер для работы с базой данных"""

    def __init__(self, db_uri: str):
        engine = create_async_engine(
            db_uri,
            echo=False,
            future=True,
            poolclass=NullPool,
        )
        sessionmaker = async_sessionmaker(
            bind=engine,
            expire_on_commit=False,
            class_=AsyncSession,
        )
        self._engine = engine
        self._sessionmaker = sessionmaker
        self._session = sessionmaker()

    async def user_exists_by_login(self, login: str) -> bool:
        """Проверяет наличие пользователя по логину"""
        try:
            result = await self._session.execute(
                select(Users.id).where(Users.login == login)
            )
            return result.scalar_one_or_none() is not None
        except Exception as e:
            logger.error(f"Error checking user existence login={login}: {e}")
            raise

    async def create_user(self, login: str, email: str, full_name: str, password_hash: str) -> User:
        """Создание нового пользователя"""
        try:
            user_db = Users(login=login, email=email,
                            full_name=full_name, password_hash=password_hash)
            self._session.add(user_db)
            await self._session.flush()
            await self._session.refresh(user_db)
            await self._session.commit()
            return user_db.to_domain()
        except Exception as e:
            await self._session.rollback()
            logger.error(f"Error creating user login={login}: {e}")
            raise

    async def get_user_by_id(self, user_id: int) -> User:
        """
        Получение пользователя по ID

        Args:
            user_id: ID пользователя

        Returns:
            Доменный объект User

        Raises:
            UserNotFoundException: Если пользователь не найден
        """
        try:
            result = await self._session.execute(
                select(Users).where(Users.id == user_id)
            )
            user_db = result.scalar_one_or_none()

            if not user_db:
                raise UserNotFoundException(user_id=user_id)

            return user_db.to_domain()
        except UserNotFoundException:
            raise
        except Exception as e:
            logger.error(f"Error getting user by id user_id={user_id}: {e}")
            raise

    async def get_user_by_login(self, login: str) -> User:
        """
        Получение пользователя по логину

        Args:
            login: Логин пользователя

        Returns:
            Доменный объект User

        Raises:
            UserNotFoundException: Если пользователь не найден
        """
        try:
            result = await self._session.execute(
                select(Users).where(Users.login == login)
            )
            user_db = result.scalar_one_or_none()

            if not user_db:
                raise UserNotFoundException(login=login)

            return user_db.to_domain()
        except UserNotFoundException:
            raise
        except Exception as e:
            logger.error(f"Error getting user by login login={login}: {e}")
            raise

    async def change_password(
            self, user_id: int, new_password_hash: str
    ):
        """Изменение пароля пользователя"""
        result = await self._session.execute(
            select(Users).where(Users.id == user_id)
        )
        user_db = result.scalar_one_or_none()
        if not user_db:
            raise UserNotFoundException(user_id=user_id)
        user_db.password_hash = new_password_hash
        await self._session.commit()
        await self._session.refresh(user_db)
