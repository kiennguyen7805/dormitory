from io import BytesIO

from fastapi.testclient import TestClient
from openpyxl import load_workbook

from test_week1_flow import auth_headers, login


def _create_contract(client: TestClient, admin: dict[str, str], student: dict[str, str]) -> tuple[str, str]:
    building = client.post(
        "/api/v1/buildings",
        headers=admin,
        json={"code": "U1", "name": "Khu tiện ích", "floors": 3},
    ).json()
    room_type = client.post(
        "/api/v1/room-types",
        headers=admin,
        json={"name": "Phòng tuần 3", "default_monthly_rate": 500000},
    ).json()
    room = client.post(
        "/api/v1/rooms",
        headers=admin,
        json={
            "building_id": building["id"],
            "room_type_id": room_type["id"],
            "code": "301",
            "floor": 3,
        },
    ).json()
    bed = client.post(
        "/api/v1/beds",
        headers=admin,
        json={"room_id": room["id"], "code": "G1"},
    ).json()
    application = client.post(
        "/api/v1/housing-applications",
        headers=student,
        json={"term_code": "HK1-2026-W3", "preferred_room_type_id": room_type["id"]},
    ).json()
    client.post(
        f"/api/v1/housing-applications/{application['id']}/approve", headers=admin
    ).raise_for_status()
    contract = client.post(
        f"/api/v1/contracts/{application['id']}/assign-bed",
        headers=admin,
        json={
            "bed_id": bed["id"],
            "start_date": "2026-09-01",
            "end_date": "2027-01-31",
        },
    )
    assert contract.status_code == 201, contract.text
    return room["id"], contract.json()["id"]


def _create_tariff(
    client: TestClient,
    headers: dict[str, str],
    utility_id: str,
    name: str,
    calculation_type: str,
    tiers: list[dict],
) -> None:
    response = client.post(
        "/api/v1/utility-tariffs",
        headers=headers,
        json={
            "utility_id": utility_id,
            "name": name,
            "effective_from": "2026-09-01",
            "calculation_type": calculation_type,
            "tiers": tiers,
        },
    )
    assert response.status_code == 201, response.text


def test_week3_manual_readings_excel_import_and_idempotent_bill(client: TestClient) -> None:
    admin = auth_headers(login(client, "admin@dormitory.local", "Admin@123")["access_token"])
    student = auth_headers(
        login(client, "student@dormitory.local", "Student@123")["access_token"]
    )
    room_id, contract_id = _create_contract(client, admin, student)

    utilities_response = client.get("/api/v1/utilities", headers=admin)
    assert utilities_response.status_code == 200, utilities_response.text
    utilities = {item["code"]: item for item in utilities_response.json()}
    assert set(utilities) == {"ELECTRICITY", "WATER"}

    _create_tariff(
        client,
        admin,
        utilities["ELECTRICITY"]["id"],
        "Điện hai bậc",
        "Tiered",
        [
            {"tier_order": 1, "from_quantity": 0, "to_quantity": 50, "unit_price": 1000},
            {"tier_order": 2, "from_quantity": 50, "to_quantity": None, "unit_price": 2000},
        ],
    )
    _create_tariff(
        client,
        admin,
        utilities["WATER"]["id"],
        "Nước đồng giá",
        "Flat",
        [{"tier_order": 1, "from_quantity": 0, "to_quantity": None, "unit_price": 15000}],
    )

    meters: dict[str, dict] = {}
    for code, utility_code in (("DIEN-U301", "ELECTRICITY"), ("NUOC-U301", "WATER")):
        response = client.post(
            "/api/v1/meters",
            headers=admin,
            json={
                "utility_id": utilities[utility_code]["id"],
                "room_id": room_id,
                "meter_code": code,
                "initial_reading": 0,
            },
        )
        assert response.status_code == 201, response.text
        meters[utility_code] = response.json()

    for utility_code, current in (("ELECTRICITY", 80), ("WATER", 10)):
        response = client.post(
            "/api/v1/meter-readings",
            headers=admin,
            json={
                "meter_id": meters[utility_code]["id"],
                "period_start": "2026-09-01",
                "period_end": "2026-09-30",
                "previous_reading": 0,
                "current_reading": current,
            },
        )
        assert response.status_code == 201, response.text
        assert response.json()["tariff_snapshot"]["tiers"]

    invalid = client.post(
        "/api/v1/meter-readings",
        headers=admin,
        json={
            "meter_id": meters["WATER"]["id"],
            "period_start": "2026-10-01",
            "period_end": "2026-10-31",
            "previous_reading": 10,
            "current_reading": 9,
        },
    )
    assert invalid.status_code == 400
    assert invalid.json()["errorCode"] == "VALIDATION_ERROR"

    bill_payload = {
        "contract_id": contract_id,
        "period_start": "2026-09-01",
        "period_end": "2026-09-30",
        "issued_date": "2026-10-01",
        "due_date": "2026-10-10",
        "idempotency_key": "week3-contract-september-2026",
    }
    bill = client.post("/api/v1/bills/generate", headers=admin, json=bill_payload)
    assert bill.status_code == 201, bill.text
    assert bill.json()["total_amount"] == "760000.00"
    assert {item["item_type"] for item in bill.json()["items"]} == {
        "Housing",
        "Electricity",
        "Water",
    }
    repeated = client.post("/api/v1/bills/generate", headers=admin, json=bill_payload)
    assert repeated.status_code == 201
    assert repeated.json()["id"] == bill.json()["id"]

    template = client.get("/api/v1/meter-readings/template", headers=admin)
    assert template.status_code == 200
    workbook = load_workbook(BytesIO(template.content))
    sheet = workbook.active
    sheet.cell(2, 1, "DIEN-U301")
    sheet.cell(2, 2, "2026-10-01")
    sheet.cell(2, 3, "2026-10-31")
    sheet.cell(2, 4, 80)
    sheet.cell(2, 5, 100)
    output = BytesIO()
    workbook.save(output)

    preview = client.post(
        "/api/v1/meter-readings/import/preview",
        headers=admin,
        files={
            "file": (
                "readings.xlsx",
                output.getvalue(),
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        },
    )
    assert preview.status_code == 200, preview.text
    assert preview.json()["valid_rows"] == 1
    confirm = client.post(
        f"/api/v1/meter-readings/import/{preview.json()['batch_id']}/confirm",
        headers=admin,
    )
    assert confirm.status_code == 200, confirm.text
    assert confirm.json()["created_readings"] == 1
