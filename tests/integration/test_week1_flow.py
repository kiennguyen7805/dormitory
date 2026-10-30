from fastapi.testclient import TestClient


def login(client: TestClient, email: str, password: str) -> dict:
    response = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    assert response.status_code == 200, response.text
    return response.json()


def auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def test_health_and_public_scope(client: TestClient) -> None:
    assert client.get("/healthz").json() == {"status": "ok"}
    assert client.get("/readyz").json() == {"status": "ready", "database": "ok"}
    spec = client.get("/openapi.json").json()
    tags = {tag["name"]: tag["description"] for tag in spec["tags"]}
    assert "Bài 2" not in tags["Students"]
    for path in ("/api/v1/room-matrix", "/api/v1/contracts/{contract_id}/transfer",
                 "/api/v1/contracts/{application_id}/assign-bed"):
        assert path not in spec["paths"]
    assert "/api/v1/contracts/{application_id}/assign-room" in spec["paths"]


def test_three_roles_and_simple_room(client: TestClient) -> None:
    accounts = (
        ("admin@dormitory.local", "Admin@123", "Admin"),
        ("staff@dormitory.local", "Staff@123", "Staff"),
        ("student@dormitory.local", "Student@123", "Student"),
    )
    headers = {}
    for email, password, role in accounts:
        payload = login(client, email, password)
        assert payload["user"]["role"] == role
        headers[role] = auth_headers(payload["access_token"])

    building = client.post("/api/v1/buildings", headers=headers["Admin"],
                           json={"code": "A1", "name": "Khu A", "address": "", "floors": 3})
    assert building.status_code == 201, building.text
    room = client.post("/api/v1/rooms", headers=headers["Staff"],
                       json={"building_id": building.json()["id"], "code": "101",
                             "floor": 1, "capacity": 2, "monthly_rate": 500000})
    assert room.status_code == 201, room.text
    assert room.json()["capacity"] == 2
    assert client.get("/api/v1/rooms", headers=headers["Student"]).status_code == 200
    assert client.post("/api/v1/rooms", headers=headers["Student"],
                       json={"building_id": building.json()["id"], "code": "102",
                             "floor": 1, "capacity": 2, "monthly_rate": 500000}).status_code == 403
    meters = client.get("/api/v1/meters", headers=headers["Staff"])
    assert meters.status_code == 200
    assert len([meter for meter in meters.json() if meter["room_id"] == room.json()["id"]]) == 2
