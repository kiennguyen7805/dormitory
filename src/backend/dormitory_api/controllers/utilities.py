from datetime import date
from io import BytesIO
from uuid import UUID

from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import StreamingResponse

from dormitory_api.dependencies import get_current_user, get_utility_service, require_permissions
from dormitory_application.utilities import (
    ImportConfirmRead,
    ImportPreviewRead,
    MeterCreate,
    MeterRead,
    MeterReadingCreate,
    MeterReadingRead,
    UtilityRead,
    UtilityService,
    UtilityTariffCreate,
    UtilityTariffRead,
)
from dormitory_infrastructure.persistence.models import UserModel

router = APIRouter(tags=["Utilities"])
read_access = require_permissions("utilities.read")
manage_access = require_permissions("utilities.manage")


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
    user: UserModel = Depends(get_current_user),
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
    user: UserModel = Depends(get_current_user),
    service: UtilityService = Depends(get_utility_service),
):
    return service.create_reading(payload, user.id)


@router.get("/meter-readings/template", dependencies=[Depends(manage_access)])
def download_template(service: UtilityService = Depends(get_utility_service)):
    return StreamingResponse(
        BytesIO(service.build_template()),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": 'attachment; filename="meter-readings-template.xlsx"'},
    )


@router.post(
    "/meter-readings/import/preview",
    response_model=ImportPreviewRead,
    dependencies=[Depends(manage_access)],
)
async def preview_import(
    file: UploadFile = File(...),
    user: UserModel = Depends(get_current_user),
    service: UtilityService = Depends(get_utility_service),
):
    content = await file.read()
    if not content or len(content) > 5 * 1024 * 1024:
        from dormitory_application.common import BusinessRuleError

        raise BusinessRuleError("INVALID_FILE_SIZE", "Tệp Excel phải có dung lượng từ 1 byte đến 5 MB.", 422)
    return service.preview_import(content, file.filename or "meter-readings.xlsx", file.content_type or "", user.id)


@router.post(
    "/meter-readings/import/{batch_id}/confirm",
    response_model=ImportConfirmRead,
    dependencies=[Depends(manage_access)],
)
def confirm_import(
    batch_id: UUID,
    user: UserModel = Depends(get_current_user),
    service: UtilityService = Depends(get_utility_service),
):
    return service.confirm_import(batch_id, user.id)
