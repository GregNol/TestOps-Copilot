from services.db.manager import Manager
from services.sso.password import (
    verify_password, get_password_hash, create_access_token, verify_token_and_get_user_id
)
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import timedelta
from config import settings
from typing import Annotated, Optional

# Models
from app.domain.models import (
    GenerateTestsRequest, ManualTestContext,
    RedactRequest, RedactContext,
    GenerateAutoTestsRequest, AutoTestContext,
    OptimizationRequest, OptimizationContext,
    ReviewRequest, ReviewContext
)
from services.sso.models import (Token, UserCreate)

# Use Cases
from app.use_cases.generator import ManualTestGeneratorUseCase
from app.use_cases.redactor import RedactorUseCase
from app.use_cases.codegen import AutoTestGeneratorUseCase
from app.use_cases.optimization import OptimizationUseCase
from app.use_cases.review import ReviewUseCase


# --- Dependencies ---


def get_manual_gen() -> ManualTestGeneratorUseCase: return ManualTestGeneratorUseCase()
def get_redactor() -> RedactorUseCase: return RedactorUseCase()
def get_auto_gen() -> AutoTestGeneratorUseCase: return AutoTestGeneratorUseCase()
def get_optimizer() -> OptimizationUseCase: return OptimizationUseCase()
def get_reviewer() -> ReviewUseCase: return ReviewUseCase()


# --- JWT Auth Setup ---
ACCESS_TOKEN_EXPIRE_MINUTES = settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES

# --- Data Base setup ---
DATABASE_URL = settings.DATABASE_URL

# --- Endpoints ---

router = APIRouter()

# --- Auth Endpoints ---


@router.post("/register", response_model=Token)
async def register_user(user_in: UserCreate):
    manager = Manager(DATABASE_URL)
    # Проверка на существование
    if await manager.user_exists_by_login(user_in.login):
        raise HTTPException(
            status_code=400,
            detail="Пользователь с таким именем уже существует"
        )

    # Хеширование пароля
    hashed_password = get_password_hash(user_in.password)

    # Сохранение в "БД"
    new_user = await manager.create_user(login=user_in.login, password_hash=hashed_password)

    # Генерация токена сразу после регистрации
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # В токен кладем ID, а не username, как вы просили
    access_token = create_access_token(
        data={"sub": new_user.id},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    manager = Manager(DATABASE_URL)
    # Ищем пользователя
    user = await manager.get_user_by_login(form_data.username)

    # Проверяем пароль
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Генерируем токен с ID
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


# --- AI Handlers ---

@router.post('/generate-manual-tests-case')
async def generate_manual_test_case(
    user_id: Annotated[int, Depends(verify_token_and_get_user_id)],
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
    user_id: Annotated[int, Depends(verify_token_and_get_user_id)],
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
    user_id: Annotated[int, Depends(verify_token_and_get_user_id)],
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
    user_id: Annotated[int, Depends(verify_token_and_get_user_id)],
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
    user_id: Annotated[int, Depends(verify_token_and_get_user_id)],
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
