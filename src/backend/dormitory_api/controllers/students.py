from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.engine import Connection

from dormitory_api.dependencies import admin_or_staff
from dormitory_application.common import ConflictError, NotFoundError
from dormitory_application.identity import StudentCreate, StudentPage, StudentRead
from dormitory_infrastructure.identity import hash_password
from dormitory_infrastructure.persistence import get_db
from dormitory_infrastructure.persistence.repositories import AuthRepository, StudentRepository

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


def _student(item: dict[str, object]) -> StudentRead:
    return StudentRead(
        id=item["id"],
        student_code=item["student_code"],
        full_name=item["full_name"],
        age=_age(item["date_of_birth"]),
        email=item["email"],
        is_active=item["is_active"],
    )


@router.get(
    "",
    response_model=StudentPage,
    dependencies=[Depends(admin_or_staff)],
    summary="Lấy danh sách sinh viên có phân trang",
)
def list_students(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, alias="pageSize", ge=1, le=100),
    db: Connection = Depends(get_db),
) -> StudentPage:
    repository = StudentRepository(db)
    return StudentPage(
        items=[_student(item) for item in repository.list_students(page_size, (page - 1) * page_size)],
        page=page,
        page_size=page_size,
        total=repository.count_students(),
    )


@router.get(
    "/{student_id}",
    response_model=StudentRead,
    dependencies=[Depends(admin_or_staff)],
    summary="Lấy chi tiết sinh viên",
)
def get_student(student_id: UUID, db: Connection = Depends(get_db)) -> StudentRead:
    item = StudentRepository(db).get_student(student_id)
    if item is None:
        raise NotFoundError("Student not found")
    return _student(item)


@router.post(
    "",
    response_model=StudentRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(admin_or_staff)],
    summary="Tạo tài khoản và hồ sơ sinh viên",
)
def create_student(payload: StudentCreate, db: Connection = Depends(get_db)) -> StudentRead:
    try:
        user_id = AuthRepository(db).register_student(
            payload.email, payload.full_name.strip(), hash_password(payload.password),
            payload.student_code.upper(), _birth_date_for_age(payload.age),
        )
        if user_id is None:
            raise NotFoundError("Student role not found")
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise ConflictError("Email hoặc mã sinh viên đã được sử dụng.") from exc
    item = StudentRepository(db).get_student(user_id)
    return _student(item)
