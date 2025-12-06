from pydantic import BaseModel, Field
from dataclasses import dataclass

# --- DTOs (Data Transfer Objects) для API ---
class GenerateTestsRequest(BaseModel):
    url: str = Field(..., description="URL веб-приложения")
    general_description: str = Field(..., description="Общее описание")
    modules: str | None = None
    buttons_description: str | None = None
    special_scenarios: str | None = None  # Исправлена опечатка scnarios -> scenarios
    bugs_and_issues: str | None = None
    testing_recommendations: str | None = None

class OptimizationTestsRequest(GenerateTestsRequest):
    test_cases: list[str]

class ReviewTestsRequest(OptimizationTestsRequest):
    rules: str

# --- Domain Entities (Внутренние сущности) ---
@dataclass
class TestContext:
    """Сущность, описывающая контекст для бизнес-логики"""
    url: str
    general_description: str
    modules: str = "Все доступные на странице"
    buttons_description: str = "Стандартные элементы управления"
    special_scenarios: str = "Нет"
    bugs_and_issues: str = "Нет известных проблем"
    testing_recommendations: str = "Стандартный подход (BVA, EP)"