import logging
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.db.models import Chats, Messages, Users
from app.domain.models import Chat, Message, MessageRole
from app.services.db.exceptions import (
    UserNotFoundException,
    ChatsNotFoundException,
    MessagesNotFoundException
)

logger = logging.getLogger(__name__)


class Manager:
    """Менеджер для работы с базой данных"""

    def __init__(self, session: AsyncSession):
        self._session = session

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
