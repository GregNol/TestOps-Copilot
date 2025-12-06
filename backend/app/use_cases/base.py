import asyncio
from app.services.llm_service import LLMService
from app.config import settings


class BaseUseCase:
    def __init__(self, template_name: str):
        self.llm_service = LLMService()
        self.template_path = settings.RESOURCES_DIR / template_name

    def _load_prompt_template(self) -> str:
        if not self.template_path.exists():
            raise FileNotFoundError(f"Template not found: {self.template_path}")
        with open(self.template_path, "r", encoding="utf-8") as f:
            return f.read()

    async def _execute_llm(self, context_dict: dict) -> str:
        template = self._load_prompt_template()
        try:
            filled_prompt = template.format(**context_dict)
        except KeyError as e:
            return f"Template Error: Missing variable {e}"

        return await asyncio.to_thread(self.llm_service.send_request, filled_prompt)