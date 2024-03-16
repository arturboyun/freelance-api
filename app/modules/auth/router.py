from typing import Annotated
from fastapi import APIRouter, Cookie, Depends, HTTPException, Request, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.config import settings

from app.core.uow.sqlalchemy_uow import SAUoW, get_uow
from app.modules.auth.schemes import AccessToken, TokensPair
from app.modules.auth.services import AuthService
from app.modules.users.schemes import UserCreate


router = APIRouter(prefix="/auth", tags=["Auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/register", response_model=AccessToken, status_code=201)
async def register(
    user: UserCreate,
    uow: Annotated[SAUoW, Depends(get_uow)],
    auth_service: Annotated[AuthService, Depends()],
    response: Response,
) -> AccessToken:
    try:
        tokens = await auth_service.register(uow, user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        httponly=True,
        max_age=settings.REFRESH_TOKEN_EXPIRE_SECONDS,
        samesite=settings.COOKIES_SAMESITE,
        secure=True,
    )
    return AccessToken(access_token=tokens.access_token)


@router.post("/token", response_model=AccessToken)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    uow: Annotated[SAUoW, Depends(get_uow)],
    auth_service: Annotated[AuthService, Depends()],
    response: Response,
) -> TokensPair:
    try:
        tokens = await auth_service.login(uow, form_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        httponly=True,
        max_age=settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60,
        samesite='none',
        secure=True,
    )
    return tokens


@router.post("/refresh-token", response_model=AccessToken)
async def refresh_token(
    uow: Annotated[SAUoW, Depends(get_uow)],
    auth_service: Annotated[AuthService, Depends()],
    response: Response,
    request: Request,
    refresh_token: Annotated[str | None, Cookie()] = None
) -> TokensPair:
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=400, detail="Refresh token not found.")
    
    try:
        tokens = await auth_service.refresh_token(uow, refresh_token)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        httponly=True,
        max_age=settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60,
        samesite='none',
        secure=True,
    )
    return tokens


@router.post("/logout")
async def logout(response: Response) -> None:
    response.delete_cookie(key="refresh_token")
    return