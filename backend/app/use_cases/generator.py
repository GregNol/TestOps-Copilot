from app.domain.models import ManualTestContext
from app.services.html_service import HTMLService
from app.use_cases.base import BaseUseCase


class ManualTestGeneratorUseCase(BaseUseCase):
    def __init__(self):
        super().__init__("prompt_template.txt")
        self.html_service = HTMLService()

    async def execute(self, context: ManualTestContext) -> str:
        # Специфичная логика для этого кейса: загрузка HTML
        html_content = await self.html_service.fetch_page(context.url)
        truncated_html = html_content[:30000] if html_content else "HTML недоступен"

        data = context.__dict__.copy()
        data['html_content'] = truncated_html

        return await self._execute_llm(data)