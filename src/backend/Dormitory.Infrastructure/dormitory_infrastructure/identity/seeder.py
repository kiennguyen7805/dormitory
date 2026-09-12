from sqlalchemy import select
from sqlalchemy.orm import Session

from dormitory_domain.common import RoleName

from dormitory_infrastructure.identity.security import hash_password
from dormitory_infrastructure.persistence.models import RoleModel, UserModel


DEMO_USERS = (
    ("admin@dormitory.local", "Quản trị viên", RoleName.ADMIN, "Admin@123"),
    ("staff@dormitory.local", "Cán bộ ký túc xá", RoleName.STAFF, "Staff@123"),
    ("student@dormitory.local", "Sinh viên demo", RoleName.STUDENT, "Student@123"),
)


def seed_identity(db: Session) -> None:
    roles: dict[RoleName, RoleModel] = {}
    for role_name in RoleName:
        role = db.scalar(select(RoleModel).where(RoleModel.name == role_name.value))
        if role is None:
            role = RoleModel(name=role_name.value)
            db.add(role)
            db.flush()
        roles[role_name] = role

    for email, full_name, role_name, password in DEMO_USERS:
        if db.scalar(select(UserModel).where(UserModel.email == email)) is None:
            db.add(
                UserModel(
                    email=email,
                    full_name=full_name,
                    password_hash=hash_password(password),
                    role_id=roles[role_name].id,
                )
            )
    db.commit()
