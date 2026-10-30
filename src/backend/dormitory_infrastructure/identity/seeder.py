from sqlalchemy import select
from sqlalchemy.orm import Session

from dormitory_domain.common import RoleName

from dormitory_infrastructure.identity.security import hash_password
from dormitory_infrastructure.persistence.models import (
    PermissionModel,
    RoleModel,
    StudentProfileModel,
    UtilityModel,
    UserModel,
)


DEMO_USERS = (
    ("admin@dormitory.local", "Quản trị viên", RoleName.ADMIN, "Admin@123"),
    ("staff@dormitory.local", "Cán bộ ký túc xá", RoleName.STAFF, "Staff@123"),
    ("student@dormitory.local", "Sinh viên demo", RoleName.STUDENT, "Student@123"),
)

PERMISSIONS = (
    ("identity.users.manage", "Quản lý tài khoản", "identity"),
    ("identity.roles.manage", "Quản lý vai trò và quyền", "identity"),
    ("students.read", "Xem hồ sơ sinh viên", "identity"),
    ("students.manage", "Cập nhật hồ sơ sinh viên", "identity"),
    ("housing.read", "Xem cơ sở vật chất", "housing"),
    ("housing.manage", "Quản lý cơ sở vật chất", "housing"),
    ("contracts.review", "Duyệt đăng ký", "contracts"),
    ("contracts.assign", "Phân và chuyển giường", "contracts"),
    ("contracts.terminate", "Chấm dứt hợp đồng", "contracts"),
    ("utilities.read", "Xem công tơ, biểu giá và chỉ số", "utilities"),
    ("utilities.manage", "Quản lý công tơ, biểu giá và chỉ số", "utilities"),
    ("billing.read", "Xem hóa đơn", "billing"),
    ("billing.generate", "Sinh hóa đơn", "billing"),
)

ROLE_PERMISSION_CODES = {
    RoleName.ADMIN: {code for code, _, _ in PERMISSIONS},
    RoleName.STAFF: {
        "students.read", "students.manage", "housing.read", "housing.manage",
        "contracts.review", "contracts.assign", "contracts.terminate",
        "utilities.read", "utilities.manage", "billing.read", "billing.generate",
    },
    RoleName.STUDENT: {"housing.read", "billing.read"},
}

UTILITY_CATALOG = (
    ("ELECTRICITY", "Tiền điện", "kWh", 0),
    ("WATER", "Tiền nước", "m3", 0),
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

    permissions: dict[str, PermissionModel] = {}
    for code, name, module in PERMISSIONS:
        permission = db.scalar(select(PermissionModel).where(PermissionModel.code == code))
        if permission is None:
            permission = PermissionModel(code=code, name=name, module=module)
            db.add(permission)
            db.flush()
        permissions[code] = permission
    for role_name, role in roles.items():
        role.permissions = [permissions[code] for code in ROLE_PERMISSION_CODES[role_name]]

    for email, full_name, role_name, password in DEMO_USERS:
        user = db.scalar(select(UserModel).where(UserModel.email == email))
        if user is None:
            user = UserModel(
                    email=email,
                    full_name=full_name,
                    password_hash=hash_password(password),
                    role_id=roles[role_name].id,
                )
            db.add(user)
            db.flush()
        if role_name == RoleName.STUDENT and user.student_profile is None:
            db.add(StudentProfileModel(user_id=user.id, student_code="SV-DEMO-001"))

    for code, name, unit, rounding_scale in UTILITY_CATALOG:
        utility = db.scalar(select(UtilityModel).where(UtilityModel.code == code))
        if utility is None:
            db.add(
                UtilityModel(
                    code=code,
                    name=name,
                    unit=unit,
                    rounding_scale=rounding_scale,
                )
            )
    db.commit()
