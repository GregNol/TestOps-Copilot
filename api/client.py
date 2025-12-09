import grpc
import sys # <--- Добавляем
from pathlib import Path # <--- Добавляем
from typing import Optional, List, Tuple
from google.protobuf import empty_pb2

# Импортируем настройки и схемы
from api.settings import settings
from api.schemas import RegisterSchema, LoginSchema, UpdatePasswordSchema, TokenUpdateSchema

# --- ИСПРАВЛЕНИЕ ПУТЕЙ ИМПОРТА ---
# Добавляем папку 'generated' в sys.path, чтобы sso_pb2_grpc мог найти sso_pb2
sys.path.append(str(Path(__file__).parent / "generated"))
# ---------------------------------

# Теперь импорты заработают
from api.generated import sso_pb2
from api.generated import sso_pb2_grpc
# Импортируем сгенерированный код из подпапки
from api.generated import sso_pb2
from api.generated import sso_pb2_grpc


class AsyncSSOClient:
    def __init__(self):
        self.target = f"{settings.SSO_GRPC_HOST}:{settings.SSO_GRPC_PORT}"
        self.channel: Optional[grpc.aio.Channel] = None
        self.stub: Optional[sso_pb2_grpc.AuthStub] = None

    async def connect(self):
        """Инициализация асинхронного канала."""
        if not self.channel:
            self.channel = grpc.aio.insecure_channel(self.target)
            self.stub = sso_pb2_grpc.AuthStub(self.channel)

    async def close(self):
        """Закрытие канала."""
        if self.channel:
            await self.channel.close()
            self.channel = None
            self.stub = None

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    def _metadata(self, token: Optional[str]) -> List[Tuple[str, str]]:
        """Формирование метаданных (заголовков) с токеном."""
        if token:
            return [("authorization", f"Bearer {token}")]
        return []

    async def ping(self) -> bool:
        """Проверка доступности сервиса."""
        try:
            await self.stub.Ping(empty_pb2.Empty(), timeout=settings.SSO_TIMEOUT)
            return True
        except grpc.RpcError:
            return False

    async def register(self, data: RegisterSchema) -> int:
        """
        Регистрация пользователя.
        Принимает Pydantic схему, возвращает user_id.
        """
        request = sso_pb2.RegisterRequest(
            login=data.login,
            email=data.email,
            full_name=data.full_name,
            password=data.password
        )
        response = await self.stub.Register(request, timeout=settings.SSO_TIMEOUT)
        return response.user_id

    async def login(self, data: LoginSchema) -> str:
        """Авторизация. Возвращает JWT токен."""
        request = sso_pb2.LoginRequest(
            login=data.login,
            password=data.password,
            app_id=data.app_id
        )
        response = await self.stub.Login(request, timeout=settings.SSO_TIMEOUT)
        return response.token

    async def is_admin(self, user_id: int) -> bool:
        """Проверка прав администратора."""
        request = sso_pb2.IsAdminRequest(user_id=user_id)
        response = await self.stub.IsAdmin(request, timeout=settings.SSO_TIMEOUT)
        return response.is_admin

    async def get_user_info(self, user_id: int) -> dict:
        """
        Получение информации о пользователе.
        Возвращает словарь (dict) вместо protobuf объекта для удобства.
        """
        request = sso_pb2.UserInfoRequest(user_id=user_id)
        response: sso_pb2.User = await self.stub.UserInfo(request, timeout=settings.SSO_TIMEOUT)

        # Конвертация protobuf ответа в чистый Python dict
        return {
            "user_id": response.user_id,
            "login": response.login,
            "email": response.email,
            "full_name": response.full_name,
            "is_admin": response.is_admin,
            # Timestamp объекты можно конвертировать в datetime при необходимости
            "create_at": response.create_at.ToDatetime() if response.HasField("create_at") else None
        }

    async def update_password(self, data: UpdatePasswordSchema, token: str) -> str:
        """Обновление пароля. Требует токен."""
        request = sso_pb2.UpdatePasswordRequest(
            user_id=data.user_id,
            new_password=data.new_password
        )
        response = await self.stub.UpdatePassword(
            request,
            timeout=settings.SSO_TIMEOUT,
            metadata=self._metadata(token)
        )
        return response.message

    async def remove_user(self, user_id: int, token: str) -> str:
        """Удаление пользователя. Требует токен администратора."""
        request = sso_pb2.RemoveUserRequest(user_id=user_id)
        response = await self.stub.RemoveUser(
            request,
            timeout=settings.SSO_TIMEOUT,
            metadata=self._metadata(token)
        )
        return response.message

    async def update_token(self, data: TokenUpdateSchema) -> str:
        """Обновление токена (Refresh). Старый токен передается в заголовке."""
        request = sso_pb2.UpdateTokenRequest(app_id=data.app_id)
        response = await self.stub.UpdateToken(
            request,
            timeout=settings.SSO_TIMEOUT,
            metadata=self._metadata(data.refresh_token)
        )
        return response.token