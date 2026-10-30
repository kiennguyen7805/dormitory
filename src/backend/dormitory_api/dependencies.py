from collections.abc import Callable
from uuid import UUID

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from dormitory_application.housing import HousingService
from dormitory_application.contracts import ContractService
from dormitory_application.billing import BillingService
from dormitory_application.utilities import UtilityService
from dormitory_domain.common import RoleName
from dormitory_infrastructure.identity import decode_access_token
from dormitory_infrastructure.persistence import get_db
from dormitory_infrastructure.persistence.models import RoleModel, UserModel
from dormitory_infrastructure.persistence.repositories import SqlAlchemyHousingRepository
from dormitory_infrastructure.persistence.contract_repositories import (
    SqlAlchemyContractRepository,
)
from dormitory_infrastructure.persistence.billing_repositories import (
    SqlAlchemyBillingRepository,
)
from dormitory_infrastructure.persistence.utility_repositories import (
    SqlAlchemyUtilityRepository,
)

bearer_scheme = HTTPBearer(auto_error=False)


def get_housing_service(db: Session = Depends(get_db)) -> HousingService:
    return HousingService(SqlAlchemyHousingRepository(db))


def get_contract_service(db: Session = Depends(get_db)) -> ContractService:
    return ContractService(SqlAlchemyContractRepository(db))


def get_utility_service(db: Session = Depends(get_db)) -> UtilityService:
    return UtilityService(SqlAlchemyUtilityRepository(db))


def get_billing_service(db: Session = Depends(get_db)) -> BillingService:
    return BillingService(SqlAlchemyBillingRepository(db))


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> UserModel:
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={"errorCode": "AUTH_INVALID_TOKEN", "message": "Phiên đăng nhập không hợp lệ."},
        headers={"WWW-Authenticate": "Bearer"},
    )
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise unauthorized

    try:
        payload = decode_access_token(credentials.credentials)
        user_id = payload.get("sub")
        if not user_id:
            raise unauthorized
    except jwt.InvalidTokenError as exc:
        raise unauthorized from exc

    user = db.scalar(
        select(UserModel)
        .options(selectinload(UserModel.role).selectinload(RoleModel.permissions))
        .where(UserModel.id == UUID(user_id))
    )
    if user is None or not user.is_active:
        raise unauthorized
    return user


def require_roles(*roles: RoleName) -> Callable:
    allowed = {role.value for role in roles}

    def role_dependency(user: UserModel = Depends(get_current_user)) -> UserModel:
        if user.role.name not in allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"errorCode": "AUTH_FORBIDDEN", "message": "Bạn không có quyền thực hiện thao tác này."},
            )
        return user

    return role_dependency


def require_permissions(*permission_codes: str) -> Callable:
    required = set(permission_codes)

    def permission_dependency(user: UserModel = Depends(get_current_user)) -> UserModel:
        granted = {permission.code for permission in user.role.permissions}
        if not required.issubset(granted):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"errorCode": "AUTH_FORBIDDEN", "message": "Bạn không có quyền thực hiện thao tác này."},
            )
        return user

    return permission_dependency


admin_only = require_roles(RoleName.ADMIN)
admin_or_staff = require_roles(RoleName.ADMIN, RoleName.STAFF)
