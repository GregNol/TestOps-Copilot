from pydantic import BaseModel, Field
from dataclasses import dataclass
from enum import Enum
from datetime import datetime

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

# --- Database Domain Entities ---


@dataclass
class User:
    """Доменная сущность пользователя"""
    id: int
    login: str
    password_hash: str
    created_on: datetime
    updated_on: datetime


@dataclass
class Chat:
    """Доменная сущность чата"""
    id: int
    user_id: int
    title: str
    created_on: datetime
    updated_on: datetime
    model: str = "gpt-3.5-turbo"


class MessageRole(str, Enum):
    """Роли сообщений"""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


@dataclass
class Message:
    """Доменная сущность сообщения"""
    id: int
    chat_id: int
    role: MessageRole
    content: str
    created_on: datetime
    updated_on: datetime
