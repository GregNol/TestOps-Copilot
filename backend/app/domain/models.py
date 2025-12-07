from pydantic import BaseModel, Field
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
# --- DTOs (Data Transfer Objects) ---


class GenerateTestsRequest(BaseModel):
    url: str = Field(..., description="URL веб-приложения")
    general_description: str = Field(..., description="Общее описание")
    modules: str | None = None
    buttons_description: str | None = None
    special_scenarios: str | None = None
    bugs_and_issues: str | None = None
    testing_recommendations: str | None = None


class RedactRequest(BaseModel):
    original_content: str = Field(...,
                                  description="Исходный текст (тест-план или код)")
    edit_instructions: str = Field(...,
                                   description="Что нужно изменить/добавить")


class GenerateAutoTestsRequest(GenerateTestsRequest):
    approved_test_plan: str = Field(...,
                                    description="Утвержденный ручной тест-план")


class OptimizationRequest(BaseModel):
    modules: str = Field(..., description="Список модулей приложения")
    test_cases: str = Field(...,
                            description="Список текущих тест-кейсов (текст или код)")


class ReviewRequest(BaseModel):
    code_snippet: str = Field(..., description="Код автотестов для проверки")
    rules: str = Field("Стандартные правила Allure и Pytest",
                       description="Доп. правила")


# --- Domain Entities (Внутренние сущности) ---

@dataclass
class ManualTestContext:
    url: str
    general_description: str
    modules: str = ""
    buttons_description: str = ""
    special_scenarios: str = ""
    bugs_and_issues: str = ""
    testing_recommendations: str = ""


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
