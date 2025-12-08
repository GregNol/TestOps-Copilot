from pydantic import BaseModel, Field
from dataclasses import dataclass

# --- Base DTOs ---
class BaseTestRequest(BaseModel):
    general_description: str = Field(..., description="Общее описание тестируемой системы")
    modules: str | None = Field(None, description="Модули или методы для фокуса")
    special_scenarios: str | None = Field(None, description="Особые граничные случаи")
    bugs_and_issues: str | None = None
    testing_recommendations: str | None = None

# --- UI Testing DTOs ---
class GenerateUiTestsRequest(BaseTestRequest):
    url: str = Field(..., description="URL веб-интерфейса")
    buttons_description: str | None = None

# --- API Testing DTOs ---
class GenerateApiTestsRequest(BaseTestRequest):
    url: str = Field(..., description="URL Swagger/OpenAPI спецификации (json или yaml)")

# --- Helper DTOs ---
class RedactRequest(BaseModel):
    original_content: str
    edit_instructions: str

class GenerateAutoTestsRequest(GenerateUiTestsRequest):
    approved_test_plan: str

class OptimizationRequest(BaseModel):
    modules: str
    test_cases: str

class ReviewRequest(BaseModel):
    code_snippet: str
    rules: str = "Standard QA Rules"

# --- Domain Entities (Contexts) ---

@dataclass
class UiTestContext:  # <--- Используем это имя для UI
    url: str
    general_description: str
    modules: str = ""
    buttons_description: str = ""
    special_scenarios: str = ""
    bugs_and_issues: str = ""
    testing_recommendations: str = ""

@dataclass
class ApiTestContext:
    url: str
    general_description: str
    modules: str = ""
    special_scenarios: str = ""
    spec_content: str = ""

@dataclass
class RedactContext:
    original_content: str
    edit_instructions: str

@dataclass
class AutoTestContext:
    url: str
    general_description: str
    test_plan: str

@dataclass
class OptimizationContext:
    modules: str
    test_cases: str

@dataclass
class ReviewContext:
    code_snippet: str
    rules: str