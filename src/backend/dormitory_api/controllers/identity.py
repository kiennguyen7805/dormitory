from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.engine import Connection

from dormitory_api.dependencies import admin_only, get_current_user
from dormitory_application.common import ConflictError, NotFoundError
from dormitory_application.identity import (
    StudentProfileRead,
    StudentProfileUpdate,
    UserCreate,
    UserRead,
    UserUpdate,
)
from dormitory_infrastructure.identity import hash_password
from dormitory_infrastructure.persistence import get_db
from dormitory_infrastructure.persistence.repositories import AuthUser, IdentityRepository

router = APIRouter(tags=["Identity"])


@router.get("/users", response_model=list[UserRead], dependencies=[Depends(admin_only)])
def list_users(role: str | None = None, db: Connection = Depends(get_db)):
    return [UserRead(**item) for item in IdentityRepository(db).list_users(role)]


@router.post("/users", response_model=UserRead, status_code=201, dependencies=[Depends(admin_only)])
def create_user(payload: UserCreate, actor: AuthUser = Depends(get_current_user), db: Connection = Depends(get_db)):
    repository = IdentityRepository(db)
    try:
        user_id = repository.create_user(
            payload.email.strip().lower(), payload.full_name.strip(),
            hash_password(payload.password), payload.role,
        )
        if user_id is None:
            raise NotFoundError("Role not found")
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise ConflictError("Email đã được sử dụng.") from exc
    return UserRead(**repository.get_user(user_id))


@router.put("/users/{user_id}", response_model=UserRead, dependencies=[Depends(admin_only)])
def update_user(user_id: UUID, payload: UserUpdate, actor: AuthUser = Depends(get_current_user), db: Connection = Depends(get_db)):
    repository = IdentityRepository(db)
    if not repository.update_user(
        user_id, payload.full_name.strip(), payload.role, payload.is_active, actor.id,
    ):
        raise NotFoundError("User or role not found")
    db.commit()
    return UserRead(**repository.get_user(user_id))


@router.get("/student-profile/me", response_model=StudentProfileRead)
def my_profile(user: AuthUser = Depends(get_current_user), db: Connection = Depends(get_db)):
    item = IdentityRepository(db).get_profile(user.id)
    if item is None:
        raise NotFoundError("Student profile not found")
    return StudentProfileRead(**item)


@router.put("/student-profile/me", response_model=StudentProfileRead)
def update_my_profile(payload: StudentProfileUpdate, user: AuthUser = Depends(get_current_user), db: Connection = Depends(get_db)):
    if user.role.name != "Student":
        raise NotFoundError("Student profile not found")
    repository = IdentityRepository(db)
    try:
        repository.upsert_profile(user.id, payload.model_dump())
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise ConflictError("Mã sinh viên đã được sử dụng.") from exc
    return StudentProfileRead(**repository.get_profile(user.id))
