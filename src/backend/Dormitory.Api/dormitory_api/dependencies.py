from collections.abc import Callable
from uuid import UUID

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from dormitory_application.housing import HousingService
from dormitory_domain.common import RoleName
from dormitory_infrastructure.identity import decode_access_token
from dormitory_infrastructure.persistence import get_db
from dormitory_infrastructure.persistence.models import UserModel
from dormitory_infrastructure.persistence.repositories import SqlAlchemyHousingRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_housing_service(db: Session = Depends(get_db)) -> HousingService:
    return HousingService(SqlAlchemyHousingRepository(db))


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> UserModel:
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={"errorCode": "AUTH_INVALID_TOKEN", "message": "Phiên đăng nhập không hợp lệ."},
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        if not user_id:
            raise unauthorized
    except jwt.InvalidTokenError as exc:
        raise unauthorized from exc

    user = db.scalar(
        select(UserModel).options(selectinload(UserModel.role)).where(UserModel.id == UUID(user_id))
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


admin_only = require_roles(RoleName.ADMIN)
admin_or_staff = require_roles(RoleName.ADMIN, RoleName.STAFF)
