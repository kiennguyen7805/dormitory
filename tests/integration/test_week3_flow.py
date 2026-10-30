from fastapi.testclient import TestClient

from test_week1_flow import auth_headers, login
from test_week2_flow import create_room


def test_one_room_bill_for_electricity_and_water(client: TestClient) -> None:
    admin = auth_headers(login(client, "admin@dormitory.local", "Admin@123")["access_token"])
    student = auth_headers(login(client, "student@dormitory.local", "Student@123")["access_token"])
    room_id = create_room(client, admin, "U1")
    application = client.post("/api/v1/housing-applications", headers=student,
                              json={"term_code": "HK1-2026", "room_id": room_id})
    assert application.status_code == 201, application.text
    application_id = application.json()["id"]
    client.post(f"/api/v1/housing-applications/{application_id}/approve",
                headers=admin).raise_for_status()
    contract = client.post(f"/api/v1/contracts/{application_id}/assign-room",
                           headers=admin,
                           json={"start_date": "2026-10-01", "end_date": "2027-06-30"})
    assert contract.status_code == 201, contract.text

    utilities = {item["code"]: item for item in client.get(
        "/api/v1/utilities", headers=admin).json()}
    meters = {next(code for code, utility in utilities.items()
                   if utility["id"] == meter["utility_id"]): meter
              for meter in client.get("/api/v1/meters", headers=admin).json()
              if meter["room_id"] == room_id}
    assert set(meters) == {"ELECTRICITY", "WATER"}

    for code, price, current in (("ELECTRICITY", 1000, 80), ("WATER", 15000, 10)):
        tariff = client.post("/api/v1/utility-tariffs", headers=admin,
                             json={"utility_id": utilities[code]["id"],
                                   "name": "Giá " + code, "effective_from": "2026-10-01",
                                   "calculation_type": "Flat",
                                   "tiers": [{"tier_order": 1, "from_quantity": 0,
                                              "to_quantity": None, "unit_price": price}]})
        assert tariff.status_code == 201, tariff.text
        reading = client.post("/api/v1/meter-readings", headers=admin,
                              json={"meter_id": meters[code]["id"],
                                    "period_start": "2026-10-01", "period_end": "2026-10-31",
                                    "previous_reading": 0, "current_reading": current})
        assert reading.status_code == 201, reading.text

    payload = {"room_id": room_id, "period_start": "2026-10-01",
               "period_end": "2026-10-31", "issued_date": "2026-11-01",
               "due_date": "2026-11-15", "idempotency_key": "room-u1-oct-2026"}
    bill = client.post("/api/v1/bills/generate", headers=admin, json=payload)
    assert bill.status_code == 201, bill.text
    assert bill.json()["total_amount"] == "230000.00"
    assert bill.json()["room_id"] == room_id
    assert len(bill.json()["items"]) == 2
    assert {item["item_type"] for item in bill.json()["items"]} == {"Electricity", "Water"}
    repeated = client.post("/api/v1/bills/generate", headers=admin, json=payload)
    assert repeated.status_code == 201
    assert repeated.json()["id"] == bill.json()["id"]

    mine = client.get("/api/v1/bills", headers=student)
    assert mine.status_code == 200
    assert [item["id"] for item in mine.json()] == [bill.json()["id"]]
    paid = client.post(f"/api/v1/bills/{bill.json()['id']}/confirm-payment",
                       headers=admin, json={"method": "Cash", "reference": "TEST-001"})
    assert paid.status_code == 200, paid.text
    assert paid.json()["status"] == "Paid"
    assert paid.json()["balance_amount"] == "0.00"
    assert client.post(f"/api/v1/bills/{bill.json()['id']}/confirm-payment",
                       headers=admin, json={"method": "Cash"}).status_code == 409
    assert client.post(f"/api/v1/bills/{bill.json()['id']}/confirm-payment",
                       headers=student, json={"method": "Cash"}).status_code == 403
