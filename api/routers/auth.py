import grpc
from fastapi import APIRouter, HTTPException, Depends, status, Request
from api.schemas import RegisterSchema, LoginSchema, TokenUpdateSchema
from api.client import AsyncSSOClient

router = APIRouter(prefix="/auth", tags=["Authentication"])

def get_sso_client(request: Request) -> AsyncSSOClient:
    """Получение клиента из state приложения (инициализирован в main.py)"""
    return request.app.state.sso_client

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    data: RegisterSchema,
    client: AsyncSSOClient = Depends(get_sso_client)
):
    try:
        user_id = await client.register(data)
        return {"user_id": user_id, "message": "User registered successfully"}
    except grpc.RpcError as e:
        # Обработка gRPC ошибок (например, если юзер уже существует)
        if e.code() == grpc.StatusCode.ALREADY_EXISTS:
            raise HTTPException(status_code=409, detail="User already exists")
        raise HTTPException(status_code=500, detail=e.details())

@router.post("/login")
async def login(
    data: LoginSchema,
    client: AsyncSSOClient = Depends(get_sso_client)
):
    try:
        token = await client.login(data)
        return {"access_token": token, "token_type": "bearer"}
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.UNAUTHENTICATED:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        if e.code() == grpc.StatusCode.NOT_FOUND:
            raise HTTPException(status_code=404, detail="User not found")
        raise HTTPException(status_code=500, detail=e.details())

@router.post("/refresh")
async def refresh_token(
    data: TokenUpdateSchema,
    client: AsyncSSOClient = Depends(get_sso_client)
):
    try:
        new_token = await client.update_token(data)
        return {"access_token": new_token, "token_type": "bearer"}
    except grpc.RpcError as e:
        raise HTTPException(status_code=401, detail="Invalid refresh token")