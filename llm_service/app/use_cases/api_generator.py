from app.domain.models import ApiTestContext
from app.services.openapi_service import OpenAPIService
from app.use_cases.base import BaseUseCase


class ApiTestGeneratorUseCase(BaseUseCase):
    def __init__(self):
        super().__init__("prompt_api_test.txt")
        self.openapi_service = OpenAPIService()

    async def execute(self, context: ApiTestContext) -> str:
        spec_content = ""

        # Вариант 1: Если контент файла уже передан (через загрузку файла)
        if context.spec_content:
            spec_content = context.spec_content

        # Вариант 2: Если передан URL (старый способ или ссылка на raw)
        elif context.url:
            spec_content = await self.openapi_service.fetch_spec(context.url)

        else:
            return "Error: No specification content or URL provided."

        # Обновляем контекст финальным контентом (обрезаем для токенов)
        context.spec_content = spec_content[:45000]  # Чуть увеличили лимит

        return await self._execute_llm(context.__dict__)