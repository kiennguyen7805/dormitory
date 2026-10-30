from decimal import Decimal

import pytest

from dormitory_domain.billing import TariffTier, calculate_utility_charge


def test_tiered_tariff_calculates_each_band_and_rounds_money() -> None:
    result = calculate_utility_charge(
        Decimal("80"),
        [
            TariffTier(1, Decimal("0"), Decimal("50"), Decimal("1000")),
            TariffTier(2, Decimal("50"), None, Decimal("2000")),
        ],
    )

    assert result.consumption == Decimal("80.000")
    assert result.total_amount == Decimal("110000.00")
    assert [item.billed_quantity for item in result.breakdown] == [
        Decimal("50.000"),
        Decimal("30.000"),
    ]


def test_flat_tariff_and_zero_consumption() -> None:
    tiers = [TariffTier(1, Decimal("0"), None, Decimal("15321.75"))]

    assert calculate_utility_charge(Decimal("10"), tiers, "Flat").total_amount == Decimal(
        "153217.50"
    )
    assert calculate_utility_charge(Decimal("0"), tiers, "Flat").total_amount == Decimal(
        "0.00"
    )


def test_tariff_rejects_gap_between_tiers() -> None:
    with pytest.raises(ValueError, match="liên tục"):
        calculate_utility_charge(
            Decimal("80"),
            [
                TariffTier(1, Decimal("0"), Decimal("50"), Decimal("1000")),
                TariffTier(2, Decimal("60"), None, Decimal("2000")),
            ],
        )
