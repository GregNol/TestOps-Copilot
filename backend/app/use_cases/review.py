from app.domain.models import ReviewContext
from app.use_cases.base import BaseUseCase

class ReviewUseCase(BaseUseCase):
    def __init__(self):
        super().__init__("prompt_review.txt")

    async def execute(self, context: ReviewContext) -> str:
        return await self._execute_llm(context.__dict__)