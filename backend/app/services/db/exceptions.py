"""Исключения для работы с базой данных"""


class UserNotFoundException(Exception):
    """Исключение: пользователь не найден"""

    def __init__(self, user_id: int):
        self.user_id = user_id
        super().__init__(f"Пользователь с ID {user_id} не найден")


class ChatsNotFoundException(Exception):
    """Исключение: чаты не найдены"""

    def __init__(self, user_id: int):
        self.user_id = user_id
        super().__init__(f"Чаты для пользователя с ID {user_id} не найдены")


class MessagesNotFoundException(Exception):
    """Исключение: сообщения не найдены"""

    def __init__(self, chat_id: int):
        self.chat_id = chat_id
        super().__init__(f"Сообщения для чата с ID {chat_id} не найдены")
