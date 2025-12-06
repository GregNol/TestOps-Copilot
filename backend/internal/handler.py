from fastapi import APIRouter, UploadFile, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
import io
from internal.models import GenerateTestsRequest, OptimizationTestsRequest, ReviewTestsRequest
router = APIRouter()


@router.get('/ping')
async def ping():
    return {"status": "ok", "message": "pong"}


@router.post('/generate-manual-tests-case')
async def generate_manual_test_case(request: GenerateTestsRequest):
    """
    Генерация ручных тест-кейсов на основе предоставленной информации о веб-приложении.
    1. Принимает POST-запрос с JSON телом, соответствующим модели GenerateTestsRequest.
    2. Отправляет запрос к внешнему сервису (например, OpenAI) для генерации тест-кейсов.
    3. Возвращает сгенерированные тест-кейсы.
    """
    if not request:
        raise HTTPException(status_code=400, detail="Request body is required")

    # Simulate test case generation
    test_case = f"Generated test case based on prompt: {request.general_description}"

    return JSONResponse(content={"message": test_case})


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
