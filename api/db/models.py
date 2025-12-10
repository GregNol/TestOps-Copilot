from datetime import datetime

from sqlalchemy import Column, BigInteger, DateTime, Text

# from core import domain
from ..domain.user import User
from .base import Base


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
    email = Column(Text, unique=True, nullable=False)
    full_name = Column(Text, nullable=False)
    password_hash = Column(Text, nullable=False)
    created_on = Column(DateTime, default=datetime.now)
    updated_on = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def to_domain(self) -> User:
        """Преобразование ORM модели в доменную сущность"""
        return User(
            id=self.id,  # type: ignore
            login=self.login,  # type: ignore
            email=self.email,
            full_name=self.full_name,
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
