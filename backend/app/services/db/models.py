from datetime import datetime
from typing import cast

from sqlalchemy import Column, BigInteger, DateTime, Text, Enum, Integer, ForeignKey

# from core import domain
from app.services.db.base import Base
from app.domain.models import User, Chat, Message, MessageRole


class BaseModel(Base):
    __abstract__ = True

    created_on = Column(DateTime, default=datetime.now)
    updated_on = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class Users(BaseModel):
    """
    Таблиаца пользователей
    """

    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    login = Column(Text, unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)

    def to_domain(self) -> User:
        """Преобразование ORM модели в доменную сущность"""
        return User(
            id=self.id,  # type: ignore
            login=self.login,  # type: ignore
            password_hash=self.password_hash,  # type: ignore
            created_on=self.created_on,  # type: ignore
            updated_on=self.updated_on  # type: ignore
        )

    @staticmethod
    def from_domain(user: User) -> "Users":
        """Создание ORM модели из доменной сущности"""
        return Users(
            id=user.id,
            login=user.login,
            password_hash=user.password_hash,
            created_on=user.created_on,
            updated_on=user.updated_on
        )


class Chats(BaseModel):
    """
    Таблица чатов
    """

    __tablename__ = "chats"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    title = Column(Text, nullable=False)
    model = Column(Text, nullable=False, default="gpt-3.5-turbo")

    def to_domain(self) -> Chat:
        """Преобразование ORM модели в доменную сущность"""
        return Chat(
            id=self.id,  # type: ignore
            user_id=self.user_id,  # type: ignore
            title=self.title,  # type: ignore
            model=self.model,  # type: ignore
            created_on=self.created_on,  # type: ignore
            updated_on=self.updated_on  # type: ignore
        )

    @staticmethod
    def from_domain(chat: Chat) -> "Chats":
        """Создание ORM модели из доменной сущности"""
        return Chats(
            id=chat.id,
            user_id=chat.user_id,
            title=chat.title,
            model=chat.model,
            created_on=chat.created_on,
            updated_on=chat.updated_on
        )


class Messages(BaseModel):
    """
    Таблица сообщений
    """

    __tablename__ = "messages"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    chat_id = Column(BigInteger, ForeignKey("chats.id"), nullable=False)
    role = Column(Enum("user", "assistant", "system",
                  name="message_roles"), nullable=False)
    content = Column(Text, nullable=False)

    def to_domain(self) -> Message:
        """Преобразование ORM модели в доменную сущность"""
        return Message(
            id=self.id,  # type: ignore
            chat_id=self.chat_id,  # type: ignore
            role=MessageRole(self.role),  # type: ignore
            content=self.content,  # type: ignore
            created_on=self.created_on,  # type: ignore
            updated_on=self.updated_on  # type: ignore
        )

    @staticmethod
    def from_domain(message: Message) -> "Messages":
        """Создание ORM модели из доменной сущности"""
        return Messages(
            id=message.id,
            chat_id=message.chat_id,
            role=message.role.value,
            content=message.content,
            created_on=message.created_on,
            updated_on=message.updated_on
        )
