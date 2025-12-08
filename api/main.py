import asyncio
import logging
from api.client import AsyncSSOClient
from api.schemas import RegisterSchema, LoginSchema, TokenUpdateSchema
from pydantic import ValidationError

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    # Использование через контекстный менеджер (автоматическое закрытие канала)
    async with AsyncSSOClient() as client:

        # 1. Проверка доступности
        is_alive = await client.ping()
        logger.info(f"Сервис доступен: {is_alive}")
        if not is_alive:
            return

        # 2. Регистрация (с валидацией данных)
        try:
            reg_data = RegisterSchema(
                login="async_master",
                email="async@python.org",
                full_name="Async Master",
                password="super_secure_pass"
            )
            user_id = await client.register(reg_data)
            logger.info(f"Зарегистрирован пользователь ID: {user_id}")
        except ValidationError as e:
            logger.error(f"Ошибка валидации данных: {e}")
            return
        except Exception as e:
            logger.error(f"Ошибка при регистрации (возможно юзер уже есть): {e}")
            user_id = 1  # Fallback ID для теста

        # 3. Логин
        try:
            login_data = LoginSchema(
                login="async_master",
                password="super_secure_pass",
                app_id=10
            )
            token = await client.login(login_data)
            logger.info(f"Токен получен: {token[:15]}...")
        except Exception as e:
            logger.error(f"Ошибка входа: {e}")
            return

        # 4. Получение информации (Идентификация)
        try:
            user_info = await client.get_user_info(user_id)
            logger.info(f"Данные пользователя: {user_info}")
        except Exception as e:
            logger.error(f"Не удалось получить инфо: {e}")

        # 5. Обновление токена
        try:
            update_data = TokenUpdateSchema(app_id=10, refresh_token=token)
            new_token = await client.update_token(update_data)
            logger.info(f"Новый токен: {new_token[:15]}...")
        except Exception as e:
            logger.error(f"Ошибка обновления токена: {e}")


if __name__ == "__main__":
    asyncio.run(main())