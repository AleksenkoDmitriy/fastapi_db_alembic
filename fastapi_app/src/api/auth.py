from typing import Annotated
from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from src.schemas.auth import Token
from src.domain.auth.use_cases.authenticate_user import (
    AuthenticateUserUseCase,
    WrongPasswordException,
    UserNotFoundByLoginException
)
from src.domain.auth.use_cases.create_access_token import CreateAccessTokenUseCase
from src.api.depends import (
    create_access_token_use_case,
    authenticate_user_use_case
)
from src.core.exceptions import handle_domain_auth_error

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/token", response_model=Token, summary="Получение токена")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_use_case: Annotated[AuthenticateUserUseCase, Depends(authenticate_user_use_case)],
    create_token_use_case: CreateAccessTokenUseCase = Depends(create_access_token_use_case),
) -> Token:
    try:
        user = await auth_use_case.execute(login=form_data.username, password=form_data.password)
    except (WrongPasswordException, UserNotFoundByLoginException) as exc:
        raise handle_domain_auth_error(exc)

    access_token = await create_token_use_case.execute(
        login=user.username,
        user_id=user.id,
        is_superuser=user.is_superuser, 
        is_staff=user.is_staff 
    )

    return Token(access_token=access_token, token_type="bearer")