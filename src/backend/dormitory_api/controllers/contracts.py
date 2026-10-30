from uuid import UUID

from fastapi import APIRouter, Depends, Response, status

from dormitory_application.contracts import (
    AssignRoomRequest,
    ContractRead,
    ContractService,
    HousingApplicationCreate,
    HousingApplicationRead,
    HousingApplicationReject,
    TerminateContractRequest,
)
from dormitory_infrastructure.persistence.repositories import AuthUser

from dormitory_api.dependencies import (
    admin_or_staff,
    get_contract_service,
    get_current_user,
)

router = APIRouter(tags=["Contracts"])


@router.post("/housing-applications", response_model=HousingApplicationRead, status_code=201)
def create_application(
    payload: HousingApplicationCreate,
    user: AuthUser = Depends(get_current_user),
    service: ContractService = Depends(get_contract_service),
):
    if user.role.name != "Student":
        from fastapi import HTTPException

        raise HTTPException(
            status_code=403,
            detail={"errorCode": "STUDENT_ONLY", "message": "Chỉ sinh viên được gửi đăng ký."},
        )
    return service.create_application(user.id, payload)


@router.get("/housing-applications", response_model=list[HousingApplicationRead])
def list_applications(
    status: str | None = None,
    user: AuthUser = Depends(get_current_user),
    service: ContractService = Depends(get_contract_service),
):
    return service.list_applications(user.id, user.role.name, status)


@router.post(
    "/housing-applications/{application_id}/approve",
    response_model=HousingApplicationRead,
    dependencies=[Depends(admin_or_staff)],
)
def approve_application(
    application_id: UUID,
    user: AuthUser = Depends(get_current_user),
    service: ContractService = Depends(get_contract_service),
):
    return service.approve_application(application_id, user.id)


@router.post(
    "/housing-applications/{application_id}/reject",
    response_model=HousingApplicationRead,
    dependencies=[Depends(admin_or_staff)],
)
def reject_application(
    application_id: UUID,
    payload: HousingApplicationReject,
    user: AuthUser = Depends(get_current_user),
    service: ContractService = Depends(get_contract_service),
):
    return service.reject_application(application_id, user.id, payload.reason)


@router.post(
    "/contracts/{application_id}/assign-room",
    response_model=ContractRead,
    status_code=201,
    dependencies=[Depends(admin_or_staff)],
)
def assign_room(
    application_id: UUID,
    payload: AssignRoomRequest,
    service: ContractService = Depends(get_contract_service),
):
    return service.assign_room(application_id, payload)


@router.get("/contracts", response_model=list[ContractRead])
def list_contracts(
    user: AuthUser = Depends(get_current_user),
    service: ContractService = Depends(get_contract_service),
):
    return service.list_contracts(user.id, user.role.name)


@router.get("/contracts/me", response_model=ContractRead | None)
def my_contract(
    user: AuthUser = Depends(get_current_user),
    service: ContractService = Depends(get_contract_service),
):
    return service.get_my_contract(user.id)


@router.get("/contracts/{contract_id}", response_model=ContractRead)
def get_contract(
    contract_id: UUID,
    user: AuthUser = Depends(get_current_user),
    service: ContractService = Depends(get_contract_service),
):
    return service.get_contract(contract_id, user.id, user.role.name)


@router.post(
    "/contracts/{contract_id}/terminate",
    response_model=ContractRead,
    dependencies=[Depends(admin_or_staff)],
)
def terminate(
    contract_id: UUID,
    payload: TerminateContractRequest,
    service: ContractService = Depends(get_contract_service),
):
    return service.terminate(contract_id, payload.termination_date)
