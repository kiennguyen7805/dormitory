"""Authentication repository: calls PostgreSQL ``fn_*`` functions only."""

from dataclasses import dataclass
from datetime import date, datetime
from uuid import UUID, uuid4

from sqlalchemy import text
from sqlalchemy.engine import Connection


@dataclass(frozen=True)
class RoleRef:
    name: str


@dataclass(frozen=True)
class AuthUser:
    id: UUID
    email: str
    full_name: str
    password_hash: str
    is_active: bool
    role: RoleRef
    refresh_token_expires_at: datetime | None
    refresh_token_revoked_at: datetime | None


class AuthRepository:
    def __init__(self, db: Connection) -> None:
        self.db = db

    def find_user(
        self, *, user_id: UUID | None = None, email: str | None = None,
        refresh_hash: str | None = None,
    ) -> AuthUser | None:
        row = self.db.execute(
            text("SELECT * FROM public.fn_auth_user(:user_id, :email, :refresh_hash)"),
            {"user_id": user_id, "email": email, "refresh_hash": refresh_hash},
        ).mappings().first()
        if row is None:
            return None
        return AuthUser(
            id=row["user_id"], email=row["email"], full_name=row["full_name"],
            password_hash=row["password_hash"], is_active=row["is_active"],
            role=RoleRef(row["role_name"]),
            refresh_token_expires_at=row["refresh_token_expires_at"],
            refresh_token_revoked_at=row["refresh_token_revoked_at"],
        )

    def register_student(
        self, email: str, full_name: str, password_hash: str,
        student_code: str, date_of_birth: date,
    ) -> UUID | None:
        user_id = uuid4()
        created = self.db.scalar(
            text(
                "SELECT public.fn_register_student(:user_id, :email, :full_name, "
                ":password_hash, :student_code, :date_of_birth)"
            ),
            {
                "user_id": user_id, "email": email, "full_name": full_name,
                "password_hash": password_hash, "student_code": student_code,
                "date_of_birth": date_of_birth,
            },
        )
        return user_id if created else None

    def set_refresh_token(
        self, user_id: UUID, token_hash: str, expires_at: datetime,
    ) -> None:
        self.db.scalar(
            text("SELECT public.fn_set_refresh_token(:user_id, :token_hash, :expires_at)"),
            {"user_id": user_id, "token_hash": token_hash, "expires_at": expires_at},
        )

