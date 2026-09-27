from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from dormitory_api.dependencies import get_current_user, require_permissions
from dormitory_application.common import ConflictError, NotFoundError
from dormitory_application.identity import (
    PermissionRead,
    ResetPasswordRequest,
    StudentProfileRead,
    StudentProfileUpdate,
    UserCreate,
    UserRead,
    UserUpdate,
)
from dormitory_infrastructure.identity import hash_password
from dormitory_infrastructure.persistence import get_db
from dormitory_infrastructure.persistence.models import (
    PermissionModel,
    RoleModel,
    StudentProfileModel,
    UserModel,
)

router = APIRouter(tags=["Identity"])


def _user(item: UserModel) -> UserRead:
    return UserRead(
        id=item.id, email=item.email, full_name=item.full_name,
        role=item.role.name, is_active=item.is_active,
        permissions=sorted(permission.code for permission in item.role.permissions),
    )


def _profile(item: StudentProfileModel) -> StudentProfileRead:
    return StudentProfileRead(
        user_id=item.user_id, email=item.user.email, full_name=item.user.full_name,
        student_code=item.student_code, faculty=item.faculty, cohort=item.cohort,
        date_of_birth=item.date_of_birth, gender=item.gender, phone=item.phone,
        address=item.address, identity_number=item.identity_number,
        emergency_contact_name=item.emergency_contact_name,
        emergency_contact_phone=item.emergency_contact_phone,
    )


def _user_statement():
    return select(UserModel).options(
        selectinload(UserModel.role).selectinload(RoleModel.permissions)
    )


@router.get("/users", response_model=list[UserRead], dependencies=[Depends(require_permissions("identity.users.manage"))])
def list_users(db: Session = Depends(get_db)):
    return [_user(item) for item in db.scalars(_user_statement().order_by(UserModel.full_name)).all()]


@router.post("/users", response_model=UserRead, status_code=201, dependencies=[Depends(require_permissions("identity.users.manage"))])
def create_user(payload: UserCreate, actor: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    role = db.scalar(select(RoleModel).where(RoleModel.name == payload.role))
    if role is None:
        raise NotFoundError("Role not found")
    item = UserModel(
        email=payload.email.strip().lower(), full_name=payload.full_name.strip(),
        password_hash=hash_password(payload.password), role_id=role.id,
    )
    db.add(item)
    try:
        db.flush()
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise ConflictError("Email đã được sử dụng.") from exc
    item = db.scalar(_user_statement().where(UserModel.id == item.id))
    return _user(item)


@router.put("/users/{user_id}", response_model=UserRead, dependencies=[Depends(require_permissions("identity.users.manage"))])
def update_user(user_id: UUID, payload: UserUpdate, actor: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    item = db.scalar(_user_statement().where(UserModel.id == user_id))
    role = db.scalar(select(RoleModel).where(RoleModel.name == payload.role))
    if item is None or role is None:
        raise NotFoundError("User or role not found")
    item.full_name = payload.full_name.strip()
    item.role_id = role.id
    item.is_active = payload.is_active
    item.updated_by = actor.id
    db.commit()
    item = db.scalar(_user_statement().where(UserModel.id == user_id))
    return _user(item)


@router.post("/users/{user_id}/reset-password", status_code=204, dependencies=[Depends(require_permissions("identity.users.manage"))])
def reset_password(user_id: UUID, payload: ResetPasswordRequest, actor: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    item = db.get(UserModel, user_id)
    if item is None:
        raise NotFoundError("User not found")
    item.password_hash = hash_password(payload.new_password)
    item.updated_by = actor.id
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/permissions", response_model=list[PermissionRead], dependencies=[Depends(require_permissions("identity.roles.manage"))])
def list_permissions(db: Session = Depends(get_db)):
    return [PermissionRead(code=x.code, name=x.name, module=x.module) for x in db.scalars(select(PermissionModel).order_by(PermissionModel.module, PermissionModel.code)).all()]


@router.get("/student-profile/me", response_model=StudentProfileRead)
def my_profile(user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    item = db.scalar(select(StudentProfileModel).options(selectinload(StudentProfileModel.user)).where(StudentProfileModel.user_id == user.id))
    if item is None:
        raise NotFoundError("Student profile not found")
    return _profile(item)


@router.put("/student-profile/me", response_model=StudentProfileRead)
def update_my_profile(payload: StudentProfileUpdate, user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    if user.role.name != "Student":
        raise NotFoundError("Student profile not found")
    item = db.get(StudentProfileModel, user.id)
    if item is None:
        item = StudentProfileModel(user_id=user.id, **payload.model_dump())
        db.add(item)
    else:
        for key, value in payload.model_dump().items():
            setattr(item, key, value)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise ConflictError("Mã sinh viên đã được sử dụng.") from exc
    item = db.scalar(select(StudentProfileModel).options(selectinload(StudentProfileModel.user)).where(StudentProfileModel.user_id == user.id))
    return _profile(item)
