from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP


MONEY = Decimal("0.01")
QUANTITY = Decimal("0.001")


@dataclass(frozen=True)
class TariffTier:
    tier_order: int
    from_quantity: Decimal
    to_quantity: Decimal | None
    unit_price: Decimal


@dataclass(frozen=True)
class TierCharge:
    tier_order: int
    from_quantity: Decimal
    to_quantity: Decimal | None
    billed_quantity: Decimal
    unit_price: Decimal
    amount: Decimal


@dataclass(frozen=True)
class BillingCalculation:
    consumption: Decimal
    total_amount: Decimal
    breakdown: tuple[TierCharge, ...]


def validate_tariff_tiers(tiers: list[TariffTier], calculation_type: str) -> None:
    if not tiers:
        raise ValueError("Biểu giá phải có ít nhất một bậc.")
    ordered = sorted(tiers, key=lambda item: item.tier_order)
    if [item.tier_order for item in ordered] != list(range(1, len(ordered) + 1)):
        raise ValueError("Thứ tự bậc giá phải liên tục từ 1.")
    if ordered[0].from_quantity != Decimal("0"):
        raise ValueError("Bậc giá đầu tiên phải bắt đầu từ 0.")
    if calculation_type == "Flat" and len(ordered) != 1:
        raise ValueError("Biểu giá đồng giá chỉ được có một bậc.")

    expected_from = Decimal("0")
    for index, tier in enumerate(ordered):
        if tier.from_quantity != expected_from:
            raise ValueError("Các bậc giá phải liên tục, không được hở hoặc chồng lấn.")
        if tier.unit_price < 0:
            raise ValueError("Đơn giá không được âm.")
        if tier.to_quantity is None:
            if index != len(ordered) - 1:
                raise ValueError("Chỉ bậc cuối cùng được để trống giới hạn trên.")
        else:
            if tier.to_quantity <= tier.from_quantity:
                raise ValueError("Giới hạn trên phải lớn hơn giới hạn dưới.")
            expected_from = tier.to_quantity

    if ordered[-1].to_quantity is not None:
        raise ValueError("Bậc giá cuối cùng phải không giới hạn.")


def calculate_utility_charge(
    consumption: Decimal,
    tiers: list[TariffTier],
    calculation_type: str = "Tiered",
) -> BillingCalculation:
    consumption = Decimal(consumption).quantize(QUANTITY)
    if consumption < 0:
        raise ValueError("Sản lượng tiêu thụ không được âm.")
    if calculation_type not in {"Flat", "Tiered"}:
        raise ValueError("Loại biểu giá không hợp lệ.")
    validate_tariff_tiers(tiers, calculation_type)
    ordered = sorted(tiers, key=lambda item: item.tier_order)

    if calculation_type == "Flat":
        amount = (consumption * ordered[0].unit_price).quantize(MONEY, ROUND_HALF_UP)
        charge = TierCharge(
            tier_order=1,
            from_quantity=Decimal("0"),
            to_quantity=None,
            billed_quantity=consumption,
            unit_price=ordered[0].unit_price,
            amount=amount,
        )
        return BillingCalculation(consumption, amount, (charge,))

    breakdown: list[TierCharge] = []
    total = Decimal("0")
    for tier in ordered:
        if consumption <= tier.from_quantity:
            billed_quantity = Decimal("0")
        else:
            upper = consumption if tier.to_quantity is None else min(consumption, tier.to_quantity)
            billed_quantity = max(Decimal("0"), upper - tier.from_quantity).quantize(QUANTITY)
        if billed_quantity == 0:
            continue
        amount = (billed_quantity * tier.unit_price).quantize(MONEY, ROUND_HALF_UP)
        total += amount
        breakdown.append(
            TierCharge(
                tier_order=tier.tier_order,
                from_quantity=tier.from_quantity,
                to_quantity=tier.to_quantity,
                billed_quantity=billed_quantity,
                unit_price=tier.unit_price,
                amount=amount,
            )
        )
    return BillingCalculation(
        consumption=consumption,
        total_amount=total.quantize(MONEY, ROUND_HALF_UP),
        breakdown=tuple(breakdown),
    )
