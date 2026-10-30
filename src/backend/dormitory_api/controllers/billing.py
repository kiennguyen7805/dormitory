from uuid import UUID

from fastapi import APIRouter, Depends

from dormitory_api.dependencies import admin_or_staff, get_billing_service, get_current_user
from dormitory_application.billing import BillGenerateRequest, BillPaymentRequest, BillRead, BillingService
from dormitory_infrastructure.persistence.repositories import AuthUser

router = APIRouter(tags=["Billing"])
read_access = get_current_user
generate_access = admin_or_staff


@router.get("/bills", response_model=list[BillRead], dependencies=[Depends(read_access)])
def list_bills(
    room_id: UUID | None = None,
    user: AuthUser = Depends(get_current_user),
    service: BillingService = Depends(get_billing_service),
):
    return service.list_bills(user.id, user.role.name, room_id)


@router.get("/bills/{bill_id}", response_model=BillRead)
def get_bill(bill_id: UUID, user: AuthUser = Depends(get_current_user),
             service: BillingService = Depends(get_billing_service)):
    return service.get_bill(bill_id, user.id, user.role.name)


@router.post(
    "/bills/generate",
    response_model=BillRead,
    status_code=201,
    dependencies=[Depends(generate_access)],
)
def generate_bill(
    payload: BillGenerateRequest,
    user: AuthUser = Depends(get_current_user),
    service: BillingService = Depends(get_billing_service),
):
    return service.generate(payload, user.id)


@router.post("/bills/{bill_id}/confirm-payment", response_model=BillRead,
             dependencies=[Depends(admin_or_staff)])
def confirm_payment(bill_id: UUID, payload: BillPaymentRequest,
                    user: AuthUser = Depends(get_current_user),
                    service: BillingService = Depends(get_billing_service)):
    return service.confirm_payment(bill_id, payload.method, payload.reference, user.id)
