from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from dormitory_application.identity import LoginRequest, TokenResponse, UserRead
from dormitory_infrastructure.identity import create_access_token, verify_password
from dormitory_infrastructure.persistence import get_db
from dormitory_infrastructure.persistence.models import UserModel

from dormitory_api.dependencies import get_current_user

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    user = db.scalar(
        select(UserModel)
        .options(selectinload(UserModel.role))
        .where(UserModel.email == payload.email.lower())
    )
    if user is None or not user.is_active or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"errorCode": "AUTH_INVALID_CREDENTIALS", "message": "Email hoặc mật khẩu không đúng."},
        )
    user_read = UserRead(id=user.id, email=user.email, full_name=user.full_name, role=user.role.name)
    return TokenResponse(
        access_token=create_access_token(str(user.id), user.role.name),
        user=user_read,
    )


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(_: UserModel = Depends(get_current_user)) -> None:
    return None


@router.get("/me", response_model=UserRead)
def me(user: UserModel = Depends(get_current_user)) -> UserRead:
    return UserRead(id=user.id, email=user.email, full_name=user.full_name, role=user.role.name)
