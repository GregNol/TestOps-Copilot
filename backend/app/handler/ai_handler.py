from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse

# Models
from app.domain.models import (
    GenerateTestsRequest, ManualTestContext,
    RedactRequest, RedactContext,
    GenerateAutoTestsRequest, AutoTestContext,
    OptimizationRequest, OptimizationContext,
    ReviewRequest, ReviewContext
)

# Use Cases
from app.use_cases.generator import ManualTestGeneratorUseCase
from app.use_cases.redactor import RedactorUseCase
from app.use_cases.codegen import AutoTestGeneratorUseCase
from app.use_cases.optimization import OptimizationUseCase
from app.use_cases.review import ReviewUseCase

router = APIRouter()

# --- Dependencies ---
def get_manual_gen() -> ManualTestGeneratorUseCase: return ManualTestGeneratorUseCase()
def get_redactor() -> RedactorUseCase: return RedactorUseCase()
def get_auto_gen() -> AutoTestGeneratorUseCase: return AutoTestGeneratorUseCase()
def get_optimizer() -> OptimizationUseCase: return OptimizationUseCase()
def get_reviewer() -> ReviewUseCase: return ReviewUseCase()

# --- Endpoints ---

@router.post('/generate-manual-tests-case')
async def generate_manual_test_case(
    request: GenerateTestsRequest,
    use_case: ManualTestGeneratorUseCase = Depends(get_manual_gen)
):
    """Генерация ручного тест-плана (Анализ UI/Docs)"""
    try:
        context = ManualTestContext(**request.model_dump(exclude_none=True))
        result = await use_case.execute(context)
        return JSONResponse(content={"message": result})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/redact-test-case')
async def redact_test_case(
    request: RedactRequest,
    use_case: RedactorUseCase = Depends(get_redactor)
):
    """Редактор: внесение правок в любой текст (тесты или код)"""
    try:
        context = RedactContext(**request.model_dump())
        result = await use_case.execute(context)
        return JSONResponse(content={"message": result})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/generate-auto-tests-case')
async def generate_auto_test_case(
    request: GenerateAutoTestsRequest,
    use_case: AutoTestGeneratorUseCase = Depends(get_auto_gen)
):
    """Генерация Pytest кода на основе утвержденного плана"""
    try:
        context = AutoTestContext(
            url=request.url,
            general_description=request.general_description,
            test_plan=request.approved_test_plan
        )
        result = await use_case.execute(context)
        return JSONResponse(content={"message": result})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/optimization-tests-case')
async def optimization_test_case(
    request: OptimizationRequest,
    use_case: OptimizationUseCase = Depends(get_optimizer)
):
    """Анализ покрытия и поиск дубликатов"""
    try:
        context = OptimizationContext(**request.model_dump())
        result = await use_case.execute(context)
        return JSONResponse(content={"message": result})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/review-tests-case')
async def review_test_case(
    request: ReviewRequest,
    use_case: ReviewUseCase = Depends(get_reviewer)
):
    """Линтинг и проверка на соответствие стандартам (Allure, AAA)"""
    try:
        context = ReviewContext(**request.model_dump())
        result = await use_case.execute(context)
        return JSONResponse(content={"message": result})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))