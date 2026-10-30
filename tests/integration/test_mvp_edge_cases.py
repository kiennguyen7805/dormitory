from fastapi.testclient import TestClient

from test_week1_flow import auth_headers, login
from test_week2_flow import create_room


def _utility_context(client: TestClient, headers: dict[str, str], room_id: str):
    utilities = {
        item["code"]: item
        for item in client.get("/api/v1/utilities", headers=headers).json()
    }
    meters = {
        meter["utility_code"]: meter
        for meter in client.get(
            "/api/v1/meters", headers=headers, params={"room_id": room_id}
        ).json()
    }
    return utilities, meters


def _create_flat_tariff(
    client: TestClient, headers: dict[str, str], utility_id: str, name: str
) -> None:
    response = client.post(
        "/api/v1/utility-tariffs",
        headers=headers,
        json={
            "utility_id": utility_id,
            "name": name,
            "effective_from": "2026-10-01",
            "calculation_type": "Flat",
            "tiers": [
                {
                    "tier_order": 1,
                    "from_quantity": 0,
                    "to_quantity": None,
                    "unit_price": 1000,
                }
            ],
        },
    )
    assert response.status_code == 201, response.text


def test_room_capacity_rejects_second_contract(client: TestClient) -> None:
    admin = auth_headers(
        login(client, "admin@dormitory.local", "Admin@123")["access_token"]
    )
    first = auth_headers(
        login(client, "student@dormitory.local", "Student@123")["access_token"]
    )
    registration = client.post(
        "/api/v1/auth/register",
        json={
            "email": "capacity.student@example.com",
            "full_name": "Capacity Student",
            "password": "Student@123",
            "student_code": "SV900001",
            "age": 20,
        },
    )
    assert registration.status_code == 201, registration.text
    second = auth_headers(
        login(client, "capacity.student@example.com", "Student@123")["access_token"]
    )

    building = client.post(
        "/api/v1/buildings",
        headers=admin,
        json={"code": "CAP", "name": "Capacity", "address": "", "floors": 1},
    )
    room = client.post(
        "/api/v1/rooms",
        headers=admin,
        json={
            "building_id": building.json()["id"],
            "code": "101",
            "floor": 1,
            "capacity": 1,
            "monthly_rate": 500000,
        },
    )
    room_id = room.json()["id"]

    for index, headers in enumerate((first, second), start=1):
        application = client.post(
            "/api/v1/housing-applications",
            headers=headers,
            json={"term_code": f"CAP-{index}", "room_id": room_id},
        )
        assert application.status_code == 201, application.text
        application_id = application.json()["id"]
        assert client.post(
            f"/api/v1/housing-applications/{application_id}/approve", headers=admin
        ).status_code == 200
        assignment = client.post(
            f"/api/v1/contracts/{application_id}/assign-room",
            headers=admin,
            json={"start_date": "2026-10-01", "end_date": "2027-06-30"},
        )
        assert assignment.status_code == (201 if index == 1 else 409), assignment.text
        if index == 2:
            assert assignment.json()["errorCode"] == "ROOM_FULL"


def test_reading_guards_and_incomplete_bill(client: TestClient) -> None:
    admin = auth_headers(
        login(client, "admin@dormitory.local", "Admin@123")["access_token"]
    )
    room_id = create_room(client, admin, "EDGE")
    utilities, meters = _utility_context(client, admin, room_id)
    _create_flat_tariff(
        client, admin, utilities["ELECTRICITY"]["id"], "Electricity edge"
    )

    invalid = client.post(
        "/api/v1/meter-readings",
        headers=admin,
        json={
            "meter_id": meters["ELECTRICITY"]["id"],
            "period_start": "2026-10-01",
            "period_end": "2026-10-31",
            "previous_reading": 10,
            "current_reading": 9,
        },
    )
    assert invalid.status_code == 400

    reading_payload = {
        "meter_id": meters["ELECTRICITY"]["id"],
        "period_start": "2026-10-01",
        "period_end": "2026-10-31",
        "previous_reading": 0,
        "current_reading": 10,
    }
    assert client.post(
        "/api/v1/meter-readings", headers=admin, json=reading_payload
    ).status_code == 201
    duplicate = client.post(
        "/api/v1/meter-readings", headers=admin, json=reading_payload
    )
    assert duplicate.status_code == 409
    assert duplicate.json()["errorCode"] == "METER_READING_ALREADY_EXISTS"

    incomplete = client.post(
        "/api/v1/bills/generate",
        headers=admin,
        json={
            "room_id": room_id,
            "period_start": "2026-10-01",
            "period_end": "2026-10-31",
            "issued_date": "2026-11-01",
            "due_date": "2026-11-15",
            "idempotency_key": "edge-incomplete-202610",
        },
    )
    assert incomplete.status_code == 422
    assert incomplete.json()["errorCode"] == "READINGS_INCOMPLETE"


def test_student_cannot_manage_core_resources(client: TestClient) -> None:
    student = auth_headers(
        login(client, "student@dormitory.local", "Student@123")["access_token"]
    )
    assert client.post(
        "/api/v1/buildings",
        headers=student,
        json={"code": "NO", "name": "Forbidden", "address": "", "floors": 1},
    ).status_code == 403
    assert client.post(
        "/api/v1/bills/generate",
        headers=student,
        json={
            "room_id": "00000000-0000-0000-0000-000000000000",
            "period_start": "2026-10-01",
            "period_end": "2026-10-31",
            "issued_date": "2026-11-01",
            "due_date": "2026-11-15",
            "idempotency_key": "student-cannot-generate",
        },
    ).status_code == 403
