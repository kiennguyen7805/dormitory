"""Seed demo accounts and utility catalog through PostgreSQL functions."""
from uuid import uuid4

from sqlalchemy import text
from sqlalchemy.engine import Connection

from dormitory_domain.common import RoleName
from dormitory_infrastructure.identity.security import hash_password


DEMO_USERS = (
    ("admin@dormitory.local", "Quản trị viên", RoleName.ADMIN, "Admin@123"),
    ("staff@dormitory.local", "Cán bộ ký túc xá", RoleName.STAFF, "Staff@123"),
    ("student@dormitory.local", "Sinh viên demo", RoleName.STUDENT, "Student@123"),
)

UTILITY_CATALOG = (
    ("ELECTRICITY", "Tiền điện", "kWh", 0),
    ("WATER", "Tiền nước", "m3", 0),
)


def seed_identity(db: Connection) -> None:
    for role_name in RoleName:
        db.execute(
            text("SELECT public.fn_seed_role(:id, :name)"),
            {"id": uuid4(), "name": role_name.value},
        )

    student_id = None
    for email, full_name, role_name, password in DEMO_USERS:
        user_id = db.scalar(
            text("SELECT public.fn_seed_user(:id, :email, :full_name, :password_hash, :role_name)"),
            {
                "id": uuid4(), "email": email, "full_name": full_name,
                "password_hash": hash_password(password), "role_name": role_name.value,
            },
        )
        if role_name == RoleName.STUDENT:
            student_id = user_id

    db.execute(
        text("SELECT public.fn_seed_student_profile(:user_id, :student_code)"),
        {"user_id": student_id, "student_code": "SV-DEMO-001"},
    )
    for code, name, unit, rounding_scale in UTILITY_CATALOG:
        db.execute(
            text("SELECT public.fn_seed_utility(:id, :code, :name, :unit, :rounding_scale)"),
            {
                "id": uuid4(), "code": code, "name": name,
                "unit": unit, "rounding_scale": rounding_scale,
            },
        )
    db.commit()
