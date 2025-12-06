from app.domain.models import RedactContext
from app.use_cases.base import BaseUseCase

class RedactorUseCase(BaseUseCase):
    def __init__(self):
        super().__init__("prompt_redactor.txt")

    async def execute(self, context: RedactContext) -> str:
        return await self._execute_llm(context.__dict__)