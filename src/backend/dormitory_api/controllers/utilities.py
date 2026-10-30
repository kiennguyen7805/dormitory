from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends

from dormitory_api.dependencies import admin_or_staff, get_current_user, get_utility_service
from dormitory_application.utilities import (
    MeterCreate,
    MeterRead,
    MeterReadingCreate,
    MeterReadingRead,
    UtilityRead,
    UtilityService,
    UtilityTariffCreate,
    UtilityTariffRead,
)
from dormitory_infrastructure.persistence.repositories import AuthUser

router = APIRouter(tags=["Utilities"])
read_access = get_current_user
manage_access = admin_or_staff


@router.get("/utilities", response_model=list[UtilityRead], dependencies=[Depends(read_access)])
def list_utilities(service: UtilityService = Depends(get_utility_service)):
    return service.list_utilities()


@router.get("/meters", response_model=list[MeterRead], dependencies=[Depends(read_access)])
def list_meters(room_id: UUID | None = None, service: UtilityService = Depends(get_utility_service)):
    return service.list_meters(room_id)


@router.post("/meters", response_model=MeterRead, status_code=201, dependencies=[Depends(manage_access)])
def create_meter(payload: MeterCreate, service: UtilityService = Depends(get_utility_service)):
    return service.create_meter(payload)


@router.get(
    "/utility-tariffs",
    response_model=list[UtilityTariffRead],
    dependencies=[Depends(read_access)],
)
def list_tariffs(
    utility_id: UUID | None = None, service: UtilityService = Depends(get_utility_service)
):
    return service.list_tariffs(utility_id)


@router.post(
    "/utility-tariffs",
    response_model=UtilityTariffRead,
    status_code=201,
    dependencies=[Depends(manage_access)],
)
def create_tariff(
    payload: UtilityTariffCreate,
    user: AuthUser = Depends(get_current_user),
    service: UtilityService = Depends(get_utility_service),
):
    return service.create_tariff(payload, user.id)


@router.get(
    "/meter-readings",
    response_model=list[MeterReadingRead],
    dependencies=[Depends(read_access)],
)
def list_readings(
    meter_id: UUID | None = None,
    period_start: date | None = None,
    service: UtilityService = Depends(get_utility_service),
):
    return service.list_readings(meter_id, period_start)


@router.post(
    "/meter-readings",
    response_model=MeterReadingRead,
    status_code=201,
    dependencies=[Depends(manage_access)],
)
def create_reading(
    payload: MeterReadingCreate,
    user: AuthUser = Depends(get_current_user),
    service: UtilityService = Depends(get_utility_service),
):
    return service.create_reading(payload, user.id)
