"""Account/profile repository: calls PostgreSQL ``fn_*`` functions only."""

from uuid import UUID, uuid4

from sqlalchemy import text
from sqlalchemy.engine import Connection


class IdentityRepository:
    def __init__(self, db: Connection) -> None:
        self.db = db

    @staticmethod
    def _user(row) -> dict[str, object]:
        return {
            "id": row["user_id"], "email": row["email"],
            "full_name": row["full_name"], "role": row["role_name"],
            "is_active": row["is_active"],
        }

    def list_users(self, role: str | None = None) -> list[dict[str, object]]:
        rows = self.db.execute(
            text("SELECT * FROM public.fn_list_users(:role)"), {"role": role}
        ).mappings()
        return [self._user(row) for row in rows]

    def get_user(self, user_id: UUID) -> dict[str, object] | None:
        row = self.db.execute(
            text("SELECT * FROM public.fn_get_user(:user_id)"), {"user_id": user_id}
        ).mappings().first()
        return self._user(row) if row else None

    def create_user(
        self, email: str, full_name: str, password_hash: str, role_name: str
    ) -> UUID | None:
        user_id = uuid4()
        created = self.db.scalar(
            text(
                "SELECT public.fn_create_user(:user_id, :email, :full_name, "
                ":password_hash, :role_name)"
            ),
            {
                "user_id": user_id, "email": email, "full_name": full_name,
                "password_hash": password_hash, "role_name": role_name,
            },
        )
        return user_id if created else None

    def update_user(
        self, user_id: UUID, full_name: str, role_name: str,
        is_active: bool, actor_id: UUID,
    ) -> bool:
        return bool(self.db.scalar(
            text(
                "SELECT public.fn_update_user(:user_id, :full_name, :role_name, "
                ":is_active, :actor_id)"
            ),
            {
                "user_id": user_id, "full_name": full_name, "role_name": role_name,
                "is_active": is_active, "actor_id": actor_id,
            },
        ))

    def get_profile(self, user_id: UUID) -> dict[str, object] | None:
        row = self.db.execute(
            text("SELECT * FROM public.fn_get_student_profile(:user_id)"),
            {"user_id": user_id},
        ).mappings().first()
        return dict(row) if row else None

    def upsert_profile(self, user_id: UUID, values: dict[str, object]) -> None:
        self.db.scalar(
            text(
                "SELECT public.fn_upsert_student_profile("
                ":user_id, :student_code, :faculty, :cohort, :date_of_birth, "
                ":gender, :phone, :address, :identity_number, "
                ":emergency_contact_name, :emergency_contact_phone)"
            ),
            {"user_id": user_id, **values},
        )
