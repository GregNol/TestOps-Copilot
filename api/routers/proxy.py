import httpx
from fastapi import APIRouter, Depends, Request, Response, HTTPException
from fastapi.responses import StreamingResponse
from ..settings import settings
# from deps import get_current_user

router = APIRouter(prefix="/ai", tags=["AI Copilot"])


async def _proxy_request(
        request: Request,
        path: str,
        user: dict
):
    """
    Внутренняя функция проксирования.
    Пересылает запрос в llm_service, добавляя информацию о пользователе.
    """
    url = f"{settings.LLM_URL}/api/v1/ai/{path}"

    # Заголовки (пробрасываем auth, но можем добавить user_id)
    headers = dict(request.headers)
    headers.pop("host", None)  # Host header не пересылаем
    headers["x-user-id"] = str(user.get("user_id", ""))

    async with httpx.AsyncClient() as client:
        try:
            # Читаем тело запроса
            body = await request.body()

            # Отправляем запрос в микросервис
            proxy_req = client.build_request(
                request.method,
                url,
                headers=headers,
                content=body,
                params=request.query_params,
                timeout=60.0  # LLM может думать долго
            )

            response = await client.send(proxy_req, stream=True)

            # Возвращаем потоковый ответ обратно клиенту
            return StreamingResponse(
                response.aiter_raw(),
                status_code=response.status_code,
                headers=dict(response.headers),
                background=None
            )
        except httpx.RequestError as exc:
            raise HTTPException(
                status_code=503, detail=f"LLM Service unavailable: {exc}")


# Wildcard route для перехвата всех запросов к /api/v1/ai/...
# Защищен dependency get_current_user
# @router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
# async def proxy_ai_requests(
#         path: str,
#         request: Request,
#         user: dict = Depends(get_current_user)  # 1. Проверка токена
# ):
#     # 2. Если токен ок, проксируем
#     return await _proxy_request(request, path, user)
