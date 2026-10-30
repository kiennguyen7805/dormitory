from fastapi.testclient import TestClient

from test_week1_flow import auth_headers, login


def create_room(client: TestClient, admin: dict[str, str], code: str = "B1") -> str:
    building = client.post("/api/v1/buildings", headers=admin,
                           json={"code": code, "name": "Khu " + code, "address": "", "floors": 3})
    assert building.status_code == 201, building.text
    room = client.post("/api/v1/rooms", headers=admin,
                       json={"building_id": building.json()["id"], "code": "201",
                             "floor": 2, "capacity": 2, "monthly_rate": 500000})
    assert room.status_code == 201, room.text
    return room.json()["id"]


def test_application_approval_and_fixed_room_contract(client: TestClient) -> None:
    admin = auth_headers(login(client, "admin@dormitory.local", "Admin@123")["access_token"])
    staff = auth_headers(login(client, "staff@dormitory.local", "Staff@123")["access_token"])
    student = auth_headers(login(client, "student@dormitory.local", "Student@123")["access_token"])
    room_id = create_room(client, admin)

    application = client.post("/api/v1/housing-applications", headers=student,
                              json={"term_code": "HK1-2026", "room_id": room_id})
    assert application.status_code == 201, application.text
    assert application.json()["room_id"] == room_id
    application_id = application.json()["id"]

    premature = client.post(f"/api/v1/contracts/{application_id}/assign-room", headers=staff,
                            json={"start_date": "2026-10-01", "end_date": "2027-06-30"})
    assert premature.status_code == 409
    approved = client.post(f"/api/v1/housing-applications/{application_id}/approve", headers=staff)
    assert approved.status_code == 200, approved.text

    contract = client.post(f"/api/v1/contracts/{application_id}/assign-room", headers=staff,
                           json={"start_date": "2026-10-01", "end_date": "2027-06-30"})
    assert contract.status_code == 201, contract.text
    assert contract.json()["current_assignment"]["room_code"] == "201"
    assert client.get("/api/v1/contracts/me", headers=student).json()["id"] == contract.json()["id"]
    duplicate = client.post(f"/api/v1/contracts/{application_id}/assign-room", headers=staff,
                            json={"start_date": "2026-10-01", "end_date": "2027-06-30"})
    assert duplicate.status_code == 409


def test_only_student_submits(client: TestClient) -> None:
    admin = auth_headers(login(client, "admin@dormitory.local", "Admin@123")["access_token"])
    room_id = create_room(client, admin)
    response = client.post("/api/v1/housing-applications", headers=admin,
                           json={"term_code": "HK1-2026", "room_id": room_id})
    assert response.status_code == 403
