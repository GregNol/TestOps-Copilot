import logging
from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

from app.services.db.models import Chats, Messages, Users
from app.domain.models import Chat, Message, MessageRole, User
from app.services.db.exceptions import (
    UserNotFoundException,
    ChatsNotFoundException,
    MessagesNotFoundException
)

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

    async def create_user(self, login: str, password_hash: str) -> User:
        """Создание нового пользователя"""
        try:
            user_db = Users(login=login, password_hash=password_hash)
            self._session.add(user_db)
            await self._session.flush()
            await self._session.refresh(user_db)
            await self._session.commit()
            return user_db.to_domain()
        except Exception as e:
            await self._session.rollback()
            logger.error(f"Error creating user login={login}: {e}")
            raise

    async def create_chat(self, user_id: int, title: str, model: str = "gpt-3.5-turbo") -> Chat:
        """Создание нового чата для пользователя"""
        try:
            # Убедимся, что пользователь существует, чтобы вернуть понятную ошибку
            user_result = await self._session.execute(
                select(Users).where(Users.id == user_id)
            )
            if user_result.scalar_one_or_none() is None:
                raise UserNotFoundException(user_id=user_id)

            chat_db = Chats(user_id=user_id, title=title, model=model)
            self._session.add(chat_db)
            await self._session.flush()
            await self._session.refresh(chat_db)
            await self._session.commit()
            return chat_db.to_domain()
        except UserNotFoundException:
            await self._session.rollback()
            raise
        except Exception as e:
            await self._session.rollback()
            logger.error(f"Error creating chat for user_id={user_id}: {e}")
            raise

    async def create_message(self, chat_id: int, role: MessageRole, content: str) -> Message:
        """Создание нового сообщения в чате"""
        try:
            message_db = Messages(
                chat_id=chat_id, role=role.value, content=content)
            self._session.add(message_db)
            await self._session.flush()
            await self._session.refresh(message_db)
            await self._session.commit()
            return message_db.to_domain()
        except Exception as e:
            await self._session.rollback()
            logger.error(f"Error creating message for chat_id={chat_id}: {e}")
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

    async def get_chats_by_user_id(self, user_id: int) -> List[Chat]:
        """
        Получение списка чатов по user_id

        Args:
            user_id: ID пользователя

        Returns:
            Список доменных объектов Chat

        Raises:
            UserNotFoundException: Если пользователь не найден
            ChatsNotFoundException: Если чаты не найдены
        """
        try:
            # Проверка существования пользователя
            user_result = await self._session.execute(
                select(Users).where(Users.id == user_id)
            )
            user = user_result.scalar_one_or_none()
            if not user:
                raise UserNotFoundException(user_id)

            # Получение чатов
            result = await self._session.execute(
                select(Chats).where(Chats.user_id == user_id).order_by(
                    Chats.created_on.desc())
            )
            chats_db = result.scalars().all()

            if not chats_db:
                raise ChatsNotFoundException(user_id)

            return [chat.to_domain() for chat in chats_db]
        except (UserNotFoundException, ChatsNotFoundException):
            raise
        except Exception as e:
            logger.error(f"Error getting chats for user_id={user_id}: {e}")
            raise

    async def get_messages_by_chat_id(self, chat_id: int) -> List[Message]:
        """
        Получение списка сообщений по chat_id

        Args:
            chat_id: ID чата

        Returns:
            Список доменных объектов Message

        Raises:
            MessagesNotFoundException: Если сообщения не найдены
        """
        try:
            # Проверка существования чата
            chat_result = await self._session.execute(
                select(Chats).where(Chats.id == chat_id)
            )
            chat = chat_result.scalar_one_or_none()
            if not chat:
                raise MessagesNotFoundException(chat_id)

            # Получение сообщений
            result = await self._session.execute(
                select(Messages).where(Messages.chat_id ==
                                       chat_id).order_by(Messages.id.asc())
            )
            messages_db = result.scalars().all()

            if not messages_db:
                raise MessagesNotFoundException(chat_id)

            return [msg.to_domain() for msg in messages_db]
        except MessagesNotFoundException:
            raise
        except Exception as e:
            logger.error(f"Error getting messages for chat_id={chat_id}: {e}")
            raise
