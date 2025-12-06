from app.domain.models import AutoTestContext
from app.use_cases.base import BaseUseCase

class AutoTestGeneratorUseCase(BaseUseCase):
    def __init__(self):
        super().__init__("prompt_codegen_pytest.txt")

    async def execute(self, context: AutoTestContext) -> str:
        return await self._execute_llm(context.__dict__)