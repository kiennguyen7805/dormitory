from uuid import UUID

from fastapi import APIRouter, Depends, Response, status

from dormitory_application.contracts import (
    AssignBedRequest,
    BedAssignmentRead,
    ContractRead,
    ContractService,
    HousingApplicationCreate,
    HousingApplicationRead,
    HousingApplicationReject,
    TerminateContractRequest,
    TransferBedRequest,
)
from dormitory_infrastructure.persistence.models import UserModel

from dormitory_api.dependencies import (
    admin_or_staff,
    get_contract_service,
    get_current_user,
)

router = APIRouter(prefix="/api", tags=["Contracts"])


@router.post("/housing-applications", response_model=HousingApplicationRead, status_code=201)
def create_application(
    payload: HousingApplicationCreate,
    user: UserModel = Depends(get_current_user),
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
    user: UserModel = Depends(get_current_user),
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
    user: UserModel = Depends(get_current_user),
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
    user: UserModel = Depends(get_current_user),
    service: ContractService = Depends(get_contract_service),
):
    return service.reject_application(application_id, user.id, payload.reason)


@router.post(
    "/contracts/{application_id}/assign-bed",
    response_model=ContractRead,
    status_code=201,
    dependencies=[Depends(admin_or_staff)],
)
def assign_bed(
    application_id: UUID,
    payload: AssignBedRequest,
    service: ContractService = Depends(get_contract_service),
):
    return service.assign_bed(application_id, payload)


@router.get("/contracts", response_model=list[ContractRead])
def list_contracts(
    user: UserModel = Depends(get_current_user),
    service: ContractService = Depends(get_contract_service),
):
    return service.list_contracts(user.id, user.role.name)


@router.get("/contracts/me", response_model=ContractRead | None)
def my_contract(
    user: UserModel = Depends(get_current_user),
    service: ContractService = Depends(get_contract_service),
):
    return service.get_my_contract(user.id)


@router.get("/contracts/{contract_id}", response_model=ContractRead)
def get_contract(
    contract_id: UUID,
    user: UserModel = Depends(get_current_user),
    service: ContractService = Depends(get_contract_service),
):
    return service.get_contract(contract_id, user.id, user.role.name)


@router.get(
    "/contracts/{contract_id}/assignment-history",
    response_model=list[BedAssignmentRead],
)
def assignment_history(
    contract_id: UUID,
    user: UserModel = Depends(get_current_user),
    service: ContractService = Depends(get_contract_service),
):
    return service.assignment_history(contract_id, user.id, user.role.name)


@router.post(
    "/contracts/{contract_id}/transfer",
    response_model=ContractRead,
    dependencies=[Depends(admin_or_staff)],
)
def transfer(
    contract_id: UUID,
    payload: TransferBedRequest,
    service: ContractService = Depends(get_contract_service),
):
    return service.transfer(contract_id, payload)


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
