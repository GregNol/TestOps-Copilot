import asyncio
from app.domain.models import TestContext
from app.services.html_service import HTMLService
from app.services.llm_service import LLMService
from app.config import settings


class ManualTestGeneratorUseCase:
    def __init__(self):
        self.html_service = HTMLService()
        self.llm_service = LLMService()
        self.template_path = settings.RESOURCES_DIR / "prompt_template.txt"

    def _load_prompt_template(self) -> str:
        if not self.template_path.exists():
            raise FileNotFoundError(f"Файл шаблона не найден: {self.template_path}")

        with open(self.template_path, "r", encoding="utf-8") as f:
            return f.read()

    async def execute(self, context: TestContext) -> str:
        # 1. Загрузка шаблона
        template = self._load_prompt_template()

        # 2. Получение HTML
        html_content = await self.html_service.fetch_page(context.url)
        truncated_html = html_content[:30000] if html_content else "HTML недоступен (ошибка загрузки)"

        # 3. Формирование промта
        # Используем __dict__ датакласса для подстановки в {переменные} шаблона
        try:
            filled_prompt = template.format(
                html_content=truncated_html,
                **context.__dict__
            )
        except KeyError as e:
            return f"Ошибка шаблона: пропущена переменная {e}"

        # 4. Запрос к LLM (асинхронная обертка над синхронным вызовом)
        result = await asyncio.to_thread(self.llm_service.send_request, filled_prompt)

        return result