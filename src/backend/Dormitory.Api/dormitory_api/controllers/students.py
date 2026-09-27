from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from dormitory_api.dependencies import require_permissions
from dormitory_application.common import ConflictError, NotFoundError
from dormitory_application.identity import StudentCreate, StudentPage, StudentRead
from dormitory_infrastructure.identity import hash_password
from dormitory_infrastructure.persistence import get_db
from dormitory_infrastructure.persistence.models import RoleModel, StudentProfileModel, UserModel

router = APIRouter(prefix="/students", tags=["Students"])


def _birth_date_for_age(age: int) -> date:
    today = date.today()
    try:
        return today.replace(year=today.year - age)
    except ValueError:
        return date(today.year - age, 2, 28)


def _age(birth_date: date | None) -> int | None:
    if birth_date is None:
        return None
    today = date.today()
    return today.year - birth_date.year - (
        (today.month, today.day) < (birth_date.month, birth_date.day)
    )


def _student(item: StudentProfileModel) -> StudentRead:
    return StudentRead(
        id=item.user_id,
        student_code=item.student_code,
        full_name=item.user.full_name,
        age=_age(item.date_of_birth),
        email=item.user.email,
        is_active=item.user.is_active,
    )


def _student_statement():
    return select(StudentProfileModel).options(selectinload(StudentProfileModel.user))


@router.get(
    "",
    response_model=StudentPage,
    dependencies=[Depends(require_permissions("students.read"))],
    summary="Lấy danh sách sinh viên có phân trang",
)
def list_students(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, alias="pageSize", ge=1, le=100),
    db: Session = Depends(get_db),
) -> StudentPage:
    total = db.scalar(select(func.count()).select_from(StudentProfileModel)) or 0
    statement = (
        _student_statement()
        .join(StudentProfileModel.user)
        .order_by(UserModel.full_name, StudentProfileModel.student_code)
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    return StudentPage(
        items=[_student(item) for item in db.scalars(statement).all()],
        page=page,
        page_size=page_size,
        total=total,
    )


@router.get(
    "/{student_id}",
    response_model=StudentRead,
    dependencies=[Depends(require_permissions("students.read"))],
    summary="Lấy chi tiết sinh viên",
)
def get_student(student_id: UUID, db: Session = Depends(get_db)) -> StudentRead:
    item = db.scalar(_student_statement().where(StudentProfileModel.user_id == student_id))
    if item is None:
        raise NotFoundError("Student not found")
    return _student(item)


@router.post(
    "",
    response_model=StudentRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_permissions("students.manage"))],
    summary="Tạo tài khoản và hồ sơ sinh viên",
)
def create_student(payload: StudentCreate, db: Session = Depends(get_db)) -> StudentRead:
    role = db.scalar(select(RoleModel).where(RoleModel.name == "Student"))
    if role is None:
        raise NotFoundError("Student role not found")
    user = UserModel(
        email=payload.email,
        full_name=payload.full_name.strip(),
        password_hash=hash_password(payload.password),
        role_id=role.id,
    )
    db.add(user)
    try:
        db.flush()
        db.add(
            StudentProfileModel(
                user_id=user.id,
                student_code=payload.student_code.upper(),
                date_of_birth=_birth_date_for_age(payload.age),
            )
        )
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise ConflictError("Email hoặc mã sinh viên đã được sử dụng.") from exc
    item = db.scalar(_student_statement().where(StudentProfileModel.user_id == user.id))
    return _student(item)
