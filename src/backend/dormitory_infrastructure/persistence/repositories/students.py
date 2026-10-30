"""Student repository: calls PostgreSQL ``fn_*`` functions only."""

from uuid import UUID

from sqlalchemy import text
from sqlalchemy.engine import Connection


class StudentRepository:
    def __init__(self, db: Connection) -> None:
        self.db = db

    @staticmethod
    def _row(row) -> dict[str, object]:
        return {
            "id": row["user_id"],
            "student_code": row["student_code"],
            "full_name": row["full_name"],
            "date_of_birth": row["date_of_birth"],
            "email": row["email"],
            "is_active": row["is_active"],
        }

    def count_students(self) -> int:
        return int(self.db.scalar(text("SELECT public.fn_count_students()")) or 0)

    def list_students(self, limit: int, offset: int) -> list[dict[str, object]]:
        rows = self.db.execute(
            text("SELECT * FROM public.fn_list_students(:limit, :offset)"),
            {"limit": limit, "offset": offset},
        ).mappings()
        return [self._row(row) for row in rows]

    def get_student(self, user_id: UUID) -> dict[str, object] | None:
        row = self.db.execute(
            text("SELECT * FROM public.fn_get_student(:user_id)"),
            {"user_id": user_id},
        ).mappings().first()
        return self._row(row) if row is not None else None
