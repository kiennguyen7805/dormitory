from collections.abc import Callable
from uuid import UUID

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.engine import Connection

from dormitory_application.housing import HousingService
from dormitory_application.contracts import ContractService
from dormitory_application.billing import BillingService
from dormitory_application.utilities import UtilityService
from dormitory_domain.common import RoleName
from dormitory_infrastructure.identity import decode_access_token
from dormitory_infrastructure.persistence import get_db
from dormitory_infrastructure.persistence.repositories import (
    AuthRepository,
    AuthUser,
    StoredBillingRepository,
    StoredContractRepository,
    StoredHousingRepository,
    StoredUtilityRepository,
)

bearer_scheme = HTTPBearer(auto_error=False)


def get_housing_service(db: Connection = Depends(get_db)) -> HousingService:
    return HousingService(StoredHousingRepository(db))


def get_contract_service(db: Connection = Depends(get_db)) -> ContractService:
    return ContractService(StoredContractRepository(db))


def get_utility_service(db: Connection = Depends(get_db)) -> UtilityService:
    return UtilityService(StoredUtilityRepository(db))


def get_billing_service(db: Connection = Depends(get_db)) -> BillingService:
    return BillingService(StoredBillingRepository(db))


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Connection = Depends(get_db),
) -> AuthUser:
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

    user = AuthRepository(db).find_user(user_id=UUID(user_id))
    if user is None or not user.is_active:
        raise unauthorized
    return user


def require_roles(*roles: RoleName) -> Callable:
    allowed = {role.value for role in roles}

    def role_dependency(user: AuthUser = Depends(get_current_user)) -> AuthUser:
        if user.role.name not in allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"errorCode": "AUTH_FORBIDDEN", "message": "Bạn không có quyền thực hiện thao tác này."},
            )
        return user

    return role_dependency


admin_only = require_roles(RoleName.ADMIN)
admin_or_staff = require_roles(RoleName.ADMIN, RoleName.STAFF)
