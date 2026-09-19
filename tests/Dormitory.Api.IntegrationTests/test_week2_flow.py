from fastapi.testclient import TestClient

from test_week1_flow import auth_headers, login


def create_inventory(client: TestClient, headers: dict[str, str]) -> tuple[str, list[str]]:
    building = client.post(
        "/api/buildings",
        headers=headers,
        json={"code": "B1", "name": "Khu B", "address": "Cơ sở chính", "floors": 3},
    ).json()
    room_type = client.post(
        "/api/room-types",
        headers=headers,
        json={"name": "Phòng tiêu chuẩn", "default_monthly_rate": 500000},
    ).json()
    room = client.post(
        "/api/rooms",
        headers=headers,
        json={
            "building_id": building["id"],
            "room_type_id": room_type["id"],
            "code": "201",
            "floor": 2,
        },
    ).json()
    beds = [
        client.post(
            "/api/beds",
            headers=headers,
            json={"room_id": room["id"], "code": code},
        ).json()["id"]
        for code in ("G1", "G2")
    ]
    return room_type["id"], beds


def submit_and_approve(
    client: TestClient,
    student_headers: dict[str, str],
    staff_headers: dict[str, str],
    room_type_id: str,
    term_code: str,
) -> str:
    created = client.post(
        "/api/housing-applications",
        headers=student_headers,
        json={"term_code": term_code, "preferred_room_type_id": room_type_id},
    )
    assert created.status_code == 201, created.text
    application_id = created.json()["id"]
    approved = client.post(
        f"/api/housing-applications/{application_id}/approve",
        headers=staff_headers,
    )
    assert approved.status_code == 200, approved.text
    assert approved.json()["status"] == "Approved"
    return application_id


def test_week2_application_contract_transfer_and_termination(client: TestClient) -> None:
    admin_headers = auth_headers(
        login(client, "admin@dormitory.local", "Admin@123")["access_token"]
    )
    staff_headers = auth_headers(
        login(client, "staff@dormitory.local", "Staff@123")["access_token"]
    )
    student_headers = auth_headers(
        login(client, "student@dormitory.local", "Student@123")["access_token"]
    )
    room_type_id, beds = create_inventory(client, admin_headers)

    application_id = submit_and_approve(
        client, student_headers, staff_headers, room_type_id, "HK1-2026"
    )
    assigned = client.post(
        f"/api/contracts/{application_id}/assign-bed",
        headers=staff_headers,
        json={"bed_id": beds[0], "start_date": "2026-09-20", "end_date": "2027-01-31"},
    )
    assert assigned.status_code == 201, assigned.text
    contract = assigned.json()
    contract_id = contract["id"]
    assert contract["status"] == "Active"
    assert contract["current_assignment"]["bed_id"] == beds[0]

    matrix = client.get("/api/room-matrix", headers=staff_headers).json()
    statuses = {bed["id"]: bed["status"] for bed in matrix[0]["rooms"][0]["beds"]}
    assert statuses[beds[0]] == "Occupied"
    assert statuses[beds[1]] == "Available"

    second_application_id = submit_and_approve(
        client, student_headers, staff_headers, room_type_id, "HK2-2026"
    )
    conflict = client.post(
        f"/api/contracts/{second_application_id}/assign-bed",
        headers=staff_headers,
        json={"bed_id": beds[0], "start_date": "2026-10-01", "end_date": "2027-05-31"},
    )
    assert conflict.status_code == 409
    assert conflict.json()["errorCode"] == "BED_ASSIGNMENT_CONFLICT"

    transferred = client.post(
        f"/api/contracts/{contract_id}/transfer",
        headers=staff_headers,
        json={"bed_id": beds[1], "transfer_date": "2026-10-15"},
    )
    assert transferred.status_code == 200, transferred.text
    assert transferred.json()["current_assignment"]["bed_id"] == beds[1]

    history = client.get(
        f"/api/contracts/{contract_id}/assignment-history",
        headers=student_headers,
    )
    assert history.status_code == 200, history.text
    assert [item["status"] for item in history.json()] == ["Ended", "Active"]

    own_contract = client.get("/api/contracts/me", headers=student_headers)
    assert own_contract.status_code == 200
    assert own_contract.json()["id"] == contract_id

    terminated = client.post(
        f"/api/contracts/{contract_id}/terminate",
        headers=staff_headers,
        json={"termination_date": "2026-11-01"},
    )
    assert terminated.status_code == 200, terminated.text
    assert terminated.json()["status"] == "Terminated"
    assert terminated.json()["current_assignment"] is None

    matrix = client.get("/api/room-matrix", headers=staff_headers).json()
    statuses = {bed["id"]: bed["status"] for bed in matrix[0]["rooms"][0]["beds"]}
    assert statuses[beds[0]] == "Available"
    assert statuses[beds[1]] == "Available"


def test_only_student_can_submit_application(client: TestClient) -> None:
    admin_headers = auth_headers(
        login(client, "admin@dormitory.local", "Admin@123")["access_token"]
    )
    room_type_id, _ = create_inventory(client, admin_headers)
    response = client.post(
        "/api/housing-applications",
        headers=admin_headers,
        json={"term_code": "HK1-2026", "preferred_room_type_id": room_type_id},
    )
    assert response.status_code == 403
    assert response.json()["detail"]["errorCode"] == "STUDENT_ONLY"
