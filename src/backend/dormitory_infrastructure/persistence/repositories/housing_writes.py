"""Write-side stored-function calls used by the housing repository."""

import json
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.engine import Connection

from dormitory_application.common import ConflictError


class StoredHousingWrites:
    def __init__(self, db: Connection) -> None:
        self.db = db

    def save(self, entity: str, item_id: UUID, data: BaseModel, create: bool) -> bool:
        try:
            saved = self.db.scalar(
                text(
                    "SELECT public.fn_save_housing("
                    ":entity, :item_id, CAST(:data AS jsonb), :create)"
                ),
                {
                    "entity": entity, "item_id": item_id,
                    "data": json.dumps(data.model_dump(mode="json"), ensure_ascii=False),
                    "create": create,
                },
            )
            if saved:
                self.db.commit()
            else:
                self.db.rollback()
            return bool(saved)
        except IntegrityError as exc:
            self.db.rollback()
            raise ConflictError("Duplicate code/name or referenced record is invalid") from exc

    def create_room(self, item_id: UUID, data: BaseModel) -> None:
        try:
            result = self.db.scalar(
                text("SELECT public.fn_create_simple_room(:id, :building_id, :code, :floor, :capacity, :monthly_rate)"),
                {"id": item_id, **data.model_dump()},
            )
            if result != "OK":
                self.db.rollback()
                from dormitory_application.common import BusinessRuleError, NotFoundError
                if result == "BUILDING_NOT_FOUND":
                    raise NotFoundError("Building not found")
                raise BusinessRuleError(result, "Tòa nhà hoặc tầng không hợp lệ.", 422)
            self.db.commit()
        except IntegrityError as exc:
            self.db.rollback()
            raise ConflictError("Room code already exists in this building") from exc

    def deactivate(self, entity: str, item_id: UUID) -> int:
        result = int(self.db.scalar(
            text("SELECT public.fn_deactivate_housing(:entity, :item_id)"),
            {"entity": entity, "item_id": item_id},
        ))
        if result == 1:
            self.db.commit()
        else:
            self.db.rollback()
        return result

    def bulk_update_gender(
        self, room_ids: list[UUID], building_id: UUID | None, floor: int | None,
        gender_policy: str, actor_id: UUID, is_admin: bool,
    ) -> int:
        result = int(self.db.scalar(
            text(
                "SELECT public.fn_bulk_update_room_gender("
                ":room_ids, :building_id, :floor, :gender_policy, :actor_id, :is_admin)"
            ),
            {
                "room_ids": room_ids, "building_id": building_id, "floor": floor,
                "gender_policy": gender_policy, "actor_id": actor_id,
                "is_admin": is_admin,
            },
        ))
        if result > 0:
            self.db.commit()
        else:
            self.db.rollback()
        return result
