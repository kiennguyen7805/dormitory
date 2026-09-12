from fastapi.testclient import TestClient


def login(client: TestClient, email: str, password: str) -> dict:
    response = client.post("/api/auth/login", json={"email": email, "password": password})
    assert response.status_code == 200, response.text
    return response.json()


def auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def test_health(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_three_seeded_roles_can_login(client: TestClient) -> None:
    accounts = (
        ("admin@dormitory.local", "Admin@123", "Admin"),
        ("staff@dormitory.local", "Staff@123", "Staff"),
        ("student@dormitory.local", "Student@123", "Student"),
    )
    for email, password, expected_role in accounts:
        payload = login(client, email, password)
        assert payload["user"]["role"] == expected_role
        assert payload["access_token"]


def test_student_cannot_access_housing_management(client: TestClient) -> None:
    token = login(client, "student@dormitory.local", "Student@123")["access_token"]
    response = client.get("/api/buildings", headers=auth_headers(token))
    assert response.status_code == 403


def test_week1_admin_creates_inventory_and_views_room_matrix(client: TestClient) -> None:
    token = login(client, "admin@dormitory.local", "Admin@123")["access_token"]
    headers = auth_headers(token)

    building = client.post(
        "/api/buildings",
        headers=headers,
        json={"code": "a1", "name": "Khu A", "address": "Cơ sở chính", "floors": 5},
    )
    assert building.status_code == 201, building.text
    building_id = building.json()["id"]
    assert building.json()["code"] == "A1"

    room_type = client.post(
        "/api/room-types",
        headers=headers,
        json={"name": "Phòng 4 sinh viên", "default_monthly_rate": 450000},
    )
    assert room_type.status_code == 201, room_type.text
    room_type_id = room_type.json()["id"]

    room = client.post(
        "/api/rooms",
        headers=headers,
        json={"building_id": building_id, "room_type_id": room_type_id, "code": "101", "floor": 1},
    )
    assert room.status_code == 201, room.text
    room_id = room.json()["id"]

    for bed_code in ("G1", "G2"):
        bed = client.post(
            "/api/beds",
            headers=headers,
            json={"room_id": room_id, "code": bed_code},
        )
        assert bed.status_code == 201, bed.text
        assert bed.json()["status"] == "Available"

    matrix = client.get("/api/room-matrix", headers=headers)
    assert matrix.status_code == 200, matrix.text
    data = matrix.json()
    assert data[0]["code"] == "A1"
    assert data[0]["rooms"][0]["code"] == "101"
    assert [bed["code"] for bed in data[0]["rooms"][0]["beds"]] == ["G1", "G2"]
