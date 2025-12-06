from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from app.domain.models import GenerateTestsRequest, TestContext, OptimizationTestsRequest, ReviewTestsRequest
from app.use_cases.generator import ManualTestGeneratorUseCase



router = APIRouter()

# Dependency Injection для UseCase
# Это позволяет создавать новый экземпляр сервиса для каждого запроса (или переиспользовать, если настроить singleton)
def get_manual_test_generator() -> ManualTestGeneratorUseCase:
    return ManualTestGeneratorUseCase()

@router.post('/generate-manual-tests-case')
async def generate_manual_test_case(
    request: GenerateTestsRequest,
    use_case: ManualTestGeneratorUseCase = Depends(get_manual_test_generator)
):
    """
    Генерация ручных тест-кейсов.
    Преобразует API Request -> Domain Context -> Запускает UseCase.
    """
    try:
        # 1. Маппинг DTO (Request) -> Domain Entity (Context)
        # exclude_none=True удалит None поля, а TestContext подставит дефолтные значения
        context_data = request.model_dump(exclude_none=True)
        test_context = TestContext(**context_data)

        # 2. Выполнение бизнес-логики
        result_markdown = await use_case.execute(test_context)

        # 3. Возврат результата
        return JSONResponse(content={"message": result_markdown})

    except Exception as e:
        # Логируем ошибку здесь
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/generate-auto-tests-case')
async def generate_auto_test_case(request: GenerateTestsRequest):
    """
    Генерация автоматических тест-кейсов на основе предоставленной информации о веб-приложении.
    1. Принимает POST-запрос с JSON телом, соответствующим модели GenerateTestsRequest.
    2. Отправляет запрос к внешнему сервису (например, OpenAI) для генерации тест-кейсов.
    3. Возвращает сгенерированные тест-кейсы.
    """
    if not request:
        raise HTTPException(status_code=400, detail="Request body is required")

    # Simulate test case generation
    test_case = f"Generated test case based on prompt: {request.general_description}"

    return JSONResponse(content={"message": test_case})


@router.post('/optimization-tests-case')
async def optimization_test_case(request: OptimizationTestsRequest):
    """
    Оптимизация автоматических тест-кейсов на основе предоставленной информации о веб-приложении.
    1. Принимает POST-запрос с JSON телом, соответствующим модели OptimizationTestsRequest.
    2. Отправляет запрос к внешнему сервису (например, OpenAI) для оптимизации каждого тест-кейса.
    3. Возвращает оптимизированные тест-кейсы.
    """
    if not request:
        raise HTTPException(status_code=400, detail="Request body is required")

    # Simulate test case optimization
    response = []
    for test in request.test_cases:
        response.append(f"Optimized test case based on: {test}")

    return JSONResponse(content={"message": response})


@router.post('/review-tests-case')
async def review_test_case(request: ReviewTestsRequest):
    """
    Рецензирование автоматических тест-кейсов на основе предоставленной информации о веб-приложении.
    1. Принимает POST-запрос с JSON телом, соответствующим модели ReviewTestsRequest.
    2. Отправляет запрос к внешнему сервису (например, OpenAI) для рецензирования каждого тест-кейса.
    3. Возвращает отчет по каждому тест-кейсу.
    """
    if not request:
        raise HTTPException(status_code=400, detail="Request body is required")

    # Simulate test case optimization
    response = []
    for test in request.test_cases:
        response.append(f"Reviewed test case based on: {test}")

    response.append(f"Using rules: {request.rules}")
    return JSONResponse(content={"message": response})
