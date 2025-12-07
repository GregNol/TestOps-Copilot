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
from fastapi.params import File, Form
from fastapi.datastructures import UploadFile
# Models
from app.domain.models import (
    GenerateUiTestsRequest, UiTestContext,
    GenerateApiTestsRequest, ApiTestContext,
    RedactRequest, RedactContext,
    GenerateAutoTestsRequest, AutoTestContext,
    OptimizationRequest, OptimizationContext,
    ReviewRequest, ReviewContext
)
# Нам понадобится сервис прямо в хендлере для парсинга
from app.services.openapi_service import OpenAPIService
from services.sso.models import (Token, UserCreate)

# Use Cases
from app.use_cases.generator import UiTestGeneratorUseCase  # <--- Исправленный импорт
from app.use_cases.api_generator import ApiTestGeneratorUseCase
from app.use_cases.redactor import RedactorUseCase
from app.use_cases.codegen import AutoTestGeneratorUseCase
from app.use_cases.optimization import OptimizationUseCase
from app.use_cases.review import ReviewUseCase


# --- Dependency Injection Factory ---
def get_ui_gen() -> UiTestGeneratorUseCase: return UiTestGeneratorUseCase() # <--- Обновили тип
def get_api_gen() -> ApiTestGeneratorUseCase: return ApiTestGeneratorUseCase()
def get_redactor() -> RedactorUseCase: return RedactorUseCase()
def get_auto_gen() -> AutoTestGeneratorUseCase: return AutoTestGeneratorUseCase()
def get_optimizer() -> OptimizationUseCase: return OptimizationUseCase()
def get_reviewer() -> ReviewUseCase: return ReviewUseCase()
def get_openapi_service() -> OpenAPIService: return OpenAPIService()


# --- JWT Auth Setup ---
ACCESS_TOKEN_EXPIRE_MINUTES = settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES

# --- Data Base setup ---
DATABASE_URL = settings.DATABASE_URL


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

@router.post('/generate-ui-tests')
async def generate_ui_tests(
    user_id: Annotated[int, Depends(verify_token_and_get_user_id)],
    request: GenerateUiTestsRequest,
    use_case: UiTestGeneratorUseCase = Depends(get_ui_gen)  # <--- Обновили тип
):
    """
    Генерация тестов для UI (анализ HTML страницы).
    """
    try:
        # Pydantic dump -> Dataclass creation
        context = UiTestContext(**request.model_dump(exclude_none=True))
        result = await use_case.execute(context)
        return JSONResponse(content={"message": result})
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"UI Generation Failed: {str(e)}")


@router.post('/generate-api-tests')
async def generate_api_tests(
        user_id: Annotated[int, Depends(verify_token_and_get_user_id)],
        # Файл обязателен
        file: Annotated[UploadFile, File(description="Файл спецификации (json/yaml)")],

        # Остальные поля принимаем как Form data
        general_description: Annotated[str, Form(
            description="Общее описание")] = "",
        modules: Annotated[str, Form(description="Фокус тестирования")] = "",
        special_scenarios: Annotated[str, Form(
            description="Особые сценарии")] = "",

        # Сервисы
        use_case: ApiTestGeneratorUseCase = Depends(get_api_gen),
        openapi_service: OpenAPIService = Depends(get_openapi_service)
):
    """
    Генерация тестов для API на основе загруженного файла (Swagger/OpenAPI).
    """
    try:
        # 1. Читаем байты файла
        file_content = await file.read()

        # 2. Валидируем и парсим файл через сервис
        parsed_spec = openapi_service.validate_and_parse_file(file_content, file.filename)

        if parsed_spec.startswith("Error"):
            raise HTTPException(status_code=400, detail=parsed_spec)

        # 3. Создаем контекст
        # URL оставляем пустым или пишем имя файла, т.к. мы работаем с контентом
        context = ApiTestContext(
            url=f"File: {file.filename}",
            general_description=general_description,
            modules=modules,
            special_scenarios=special_scenarios,
            spec_content=parsed_spec
        )

        # 4. Запускаем Use Case
        result = await use_case.execute(context)

        return JSONResponse(content={"message": result})

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"API Generation Failed: {str(e)}")

        # 2. Валидируем и парсим файл через сервис
        filename = file.filename or "uploaded_file"
        parsed_spec = openapi_service.validate_and_parse_file(
            file_content, filename)

        if parsed_spec.startswith("Error"):
            raise HTTPException(status_code=400, detail=parsed_spec)

        # 3. Создаем контекст
        # URL оставляем пустым или пишем имя файла, т.к. мы работаем с контентом
        context = ApiTestContext(
            url=f"File: {file.filename}",
            general_description=general_description,
            modules=modules,
            special_scenarios=special_scenarios,
            spec_content=parsed_spec
        )

        # 4. Запускаем Use Case
        result = await use_case.execute(context)

        return JSONResponse(content={"message": result})

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"API Generation Failed: {str(e)}")


@router.post('/redact-content')
async def redact_content(
    user_id: Annotated[int, Depends(verify_token_and_get_user_id)],
    request: RedactRequest,
    use_case: RedactorUseCase = Depends(get_redactor)
):
    try:
        context = RedactContext(**request.model_dump())
        result = await use_case.execute(context)
        return JSONResponse(content={"message": result})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/generate-code-pytest')
async def generate_code_pytest(
    user_id: Annotated[int, Depends(verify_token_and_get_user_id)],
    request: GenerateAutoTestsRequest,
    use_case: AutoTestGeneratorUseCase = Depends(get_auto_gen)
):
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


@router.post('/optimize-tests')
async def optimize_tests(
    user_id: Annotated[int, Depends(verify_token_and_get_user_id)],
    request: OptimizationRequest,
    use_case: OptimizationUseCase = Depends(get_optimizer)
):
    try:
        context = OptimizationContext(**request.model_dump())
        result = await use_case.execute(context)
        return JSONResponse(content={"message": result})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/review-code')
async def review_code(
    user_id: Annotated[int, Depends(verify_token_and_get_user_id)],
    request: ReviewRequest,
    use_case: ReviewUseCase = Depends(get_reviewer)
):
    try:
        context = ReviewContext(**request.model_dump())
        result = await use_case.execute(context)
        return JSONResponse(content={"message": result})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
