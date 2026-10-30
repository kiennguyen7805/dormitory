from datetime import date
from uuid import UUID

from .schemas import MeterCreate, MeterReadingCreate, UtilityTariffCreate


class UtilityService:
    def __init__(self, repository) -> None:
        self.repository = repository

    def list_utilities(self):
        return self.repository.list_utilities()

    def list_meters(self, room_id: UUID | None = None):
        return self.repository.list_meters(room_id)

    def create_meter(self, data: MeterCreate):
        return self.repository.create_meter(data)

    def list_tariffs(self, utility_id: UUID | None = None):
        return self.repository.list_tariffs(utility_id)

    def create_tariff(self, data: UtilityTariffCreate, user_id: UUID):
        return self.repository.create_tariff(data, user_id)

    def create_reading(self, data: MeterReadingCreate, user_id: UUID):
        return self.repository.create_reading(data, user_id)

    def list_readings(self, meter_id: UUID | None = None, period_start: date | None = None):
        return self.repository.list_readings(meter_id, period_start)
