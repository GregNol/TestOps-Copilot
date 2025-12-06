from app.domain.models import OptimizationContext
from app.use_cases.base import BaseUseCase

class OptimizationUseCase(BaseUseCase):
    def __init__(self):
        super().__init__("prompt_optimization.txt")

    async def execute(self, context: OptimizationContext) -> str:
        return await self._execute_llm(context.__dict__)