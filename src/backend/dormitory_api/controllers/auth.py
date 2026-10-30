from datetime import UTC, date, datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.engine import Connection

from dormitory_api.dependencies import get_current_user
from dormitory_application.identity import (
    LoginRequest,
    RefreshTokenRequest,
    RegisterRequest,
    TokenResponse,
    UserRead,
)
from dormitory_infrastructure.identity import (
    create_access_token,
    create_refresh_token,
    hash_password,
    hash_refresh_token,
    verify_password,
)
from dormitory_infrastructure.persistence import get_db
from dormitory_infrastructure.persistence.repositories import AuthRepository, AuthUser
from dormitory_infrastructure.persistence.config import get_settings

router = APIRouter(prefix="/auth", tags=["Auth"])


def _user_read(user: AuthUser) -> UserRead:
    return UserRead(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        role=user.role.name,
        is_active=user.is_active,
    )


def _birth_date_for_age(age: int) -> date:
    today = date.today()
    try:
        return today.replace(year=today.year - age)
    except ValueError:
        return date(today.year - age, 2, 28)


def _as_utc(value: datetime) -> datetime:
    return value if value.tzinfo is not None else value.replace(tzinfo=UTC)


def _issue_tokens(user: AuthUser, repository: AuthRepository) -> tuple[str, str]:
    settings = get_settings()
    refresh_token = create_refresh_token()
    repository.set_refresh_token(
        user.id,
        hash_refresh_token(refresh_token),
        datetime.now(UTC) + timedelta(days=settings.refresh_token_expire_days),
    )
    access_token = create_access_token(str(user.id), user.role.name, user.email)
    return access_token, refresh_token


def _token_response(user: AuthUser, access_token: str, refresh_token: str) -> TokenResponse:
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=get_settings().access_token_expire_minutes * 60,
        user=_user_read(user),
    )


def _invalid_credentials() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={
            "errorCode": "AUTH_INVALID_CREDENTIALS",
            "message": "Email hoặc mật khẩu không đúng.",
        },
        headers={"WWW-Authenticate": "Bearer"},
    )


def _invalid_refresh_token() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={
            "errorCode": "AUTH_INVALID_REFRESH_TOKEN",
            "message": "Refresh token không hợp lệ hoặc đã hết hạn.",
        },
        headers={"WWW-Authenticate": "Bearer"},
    )


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Connection = Depends(get_db)) -> UserRead:
    repository = AuthRepository(db)
    try:
        user_id = repository.register_student(
            payload.email, payload.full_name.strip(), hash_password(payload.password),
            payload.student_code.upper(), _birth_date_for_age(payload.age),
        )
        if user_id is None:
            raise HTTPException(status_code=500, detail="Student role has not been seeded.")
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "errorCode": "STUDENT_ALREADY_EXISTS",
                "message": "Email hoặc mã sinh viên đã được sử dụng.",
            },
        ) from exc
    return _user_read(repository.find_user(user_id=user_id))


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Connection = Depends(get_db)) -> TokenResponse:
    repository = AuthRepository(db)
    user = repository.find_user(email=payload.email)
    succeeded = bool(
        user is not None
        and user.is_active
        and verify_password(payload.password, user.password_hash)
    )
    if not succeeded or user is None:
        raise _invalid_credentials()
    access_token, refresh_token = _issue_tokens(user, repository)
    db.commit()
    return _token_response(user, access_token, refresh_token)


@router.post("/refresh", response_model=TokenResponse)
def refresh(payload: RefreshTokenRequest, db: Connection = Depends(get_db)) -> TokenResponse:
    repository = AuthRepository(db)
    user = repository.find_user(
        refresh_hash=hash_refresh_token(payload.refresh_token)
    )
    now = datetime.now(UTC)
    if (
        user is None
        or not user.is_active
        or user.refresh_token_revoked_at is not None
        or user.refresh_token_expires_at is None
        or _as_utc(user.refresh_token_expires_at) <= now
    ):
        raise _invalid_refresh_token()
    access_token, refresh_token = _issue_tokens(user, repository)
    db.commit()
    return _token_response(user, access_token, refresh_token)



@router.get("/me", response_model=UserRead)
def me(user: AuthUser = Depends(get_current_user)) -> UserRead:
    return _user_read(user)
