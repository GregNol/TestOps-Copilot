from pydantic import BaseModel


class GenerateTestsRequest(BaseModel):
    # url ссылки на веб-приложение для тестирования
    url:                        str

    # Общее описание веб-приложения
    general_description:        str

    # Модули веб-приложения
    modules:                    str | None = None

    # Описание кнопок веб-приложения
    buttons_description:        str | None = None

    # Особые сценарии веб-приложения
    special_scnarios:           str | None = None

    # Известные ошибки и проблемы веб-приложения
    bugs_and_issues:            str | None = None

    # Рекомендации по тестированию веб-приложения
    testing_recommendations:    str | None = None


class OptimizationTestsRequest(GenerateTestsRequest):
    # Список автоматических тест-кейсов для оптимизации
    test_cases: list[str]


class ReviewTestsRequest(OptimizationTestsRequest):
    # Правила для рецензирования тест-кейсов
    rules: str
