from uuid import UUID

from fastapi import APIRouter, Depends

from dormitory_api.dependencies import get_billing_service, get_current_user, require_permissions
from dormitory_application.billing import BillGenerateRequest, BillRead, BillingService
from dormitory_infrastructure.persistence.models import UserModel

router = APIRouter(tags=["Billing"])
read_access = require_permissions("billing.read")
generate_access = require_permissions("billing.generate")


@router.get("/bills", response_model=list[BillRead], dependencies=[Depends(read_access)])
def list_bills(
    contract_id: UUID | None = None,
    user: UserModel = Depends(get_current_user),
    service: BillingService = Depends(get_billing_service),
):
    return service.list_bills(user.id, user.role.name, contract_id)


@router.post(
    "/bills/generate",
    response_model=BillRead,
    status_code=201,
    dependencies=[Depends(generate_access)],
)
def generate_bill(
    payload: BillGenerateRequest,
    user: UserModel = Depends(get_current_user),
    service: BillingService = Depends(get_billing_service),
):
    return service.generate(payload, user.id)
