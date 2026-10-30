from uuid import uuid4

from fastapi.testclient import TestClient


def _login(client: TestClient, prefix: str = "/api/v1") -> dict:
    response = client.post(
        f"{prefix}/auth/login",
        json={"email": "admin@dormitory.local", "password": "Admin@123"},
    )
    assert response.status_code == 200, response.text
    return response.json()


def _headers(access_token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {access_token}"}


def test_openapi_exposes_v1_and_keeps_legacy_routes_working(client: TestClient) -> None:
    paths = client.get("/openapi.json").json()["paths"]
    assert "/api/v1/auth/login" in paths
    assert "/api/v1/students" in paths
    assert "/api/auth/login" not in paths
    assert _login(client, "/api")["access_token"]


def test_refresh_token_rotates_and_logout_revokes_it(client: TestClient) -> None:
    login = _login(client)
    old_refresh_token = login["refresh_token"]
    assert login["expires_in"] == 15 * 60

    refreshed = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": old_refresh_token},
    )
    assert refreshed.status_code == 200, refreshed.text
    new_tokens = refreshed.json()
    assert new_tokens["refresh_token"] != old_refresh_token
    assert new_tokens["access_token"] != login["access_token"]

    reused = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": old_refresh_token},
    )
    assert reused.status_code == 401
    assert reused.headers["content-type"].startswith("application/problem+json")
    assert reused.json()["errorCode"] == "AUTH_INVALID_REFRESH_TOKEN"

    logout = client.post(
        "/api/v1/auth/logout",
        headers=_headers(new_tokens["access_token"]),
    )
    assert logout.status_code == 204
    revoked = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": new_tokens["refresh_token"]},
    )
    assert revoked.status_code == 401


def test_register_student_account(client: TestClient) -> None:
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "registered.student@example.com",
            "full_name": "Sinh viên đăng ký",
            "password": "Student@123",
            "student_code": "SV000001",
            "age": 20,
        },
    )
    assert response.status_code == 201, response.text
    assert response.json()["role"] == "Student"

    login = client.post(
        "/api/v1/auth/login",
        json={"email": "registered.student@example.com", "password": "Student@123"},
    )
    assert login.status_code == 200


def test_student_crud_read_and_pagination(client: TestClient) -> None:
    admin = _login(client)
    headers = _headers(admin["access_token"])
    created = client.post(
        "/api/v1/students",
        headers=headers,
        json={
            "email": "student.page@example.com",
            "full_name": "Sinh viên phân trang",
            "password": "Student@123",
            "student_code": "SV000002",
            "age": 22,
        },
    )
    assert created.status_code == 201, created.text
    student = created.json()
    assert student["age"] == 22

    page = client.get("/api/v1/students?page=1&pageSize=1", headers=headers)
    assert page.status_code == 200, page.text
    assert page.json()["page"] == 1
    assert page.json()["pageSize"] == 1
    assert page.json()["total"] >= 2
    assert len(page.json()["items"]) == 1

    detail = client.get(f"/api/v1/students/{student['id']}", headers=headers)
    assert detail.status_code == 200
    assert detail.json()["student_code"] == "SV000002"

    missing = client.get(f"/api/v1/students/{uuid4()}", headers=headers)
    assert missing.status_code == 404
    assert missing.headers["content-type"].startswith("application/problem+json")
    assert missing.json()["status"] == 404


def test_v1_validation_uses_rfc7807_problem_details(client: TestClient) -> None:
    admin = _login(client)
    response = client.post(
        "/api/v1/students",
        headers=_headers(admin["access_token"]),
        json={
            "email": "not-an-email",
            "full_name": "",
            "password": "short",
            "student_code": "123",
            "age": 12,
        },
    )
    assert response.status_code == 400
    assert response.headers["content-type"].startswith("application/problem+json")
    body = response.json()
    assert body["title"] == "Validation Failed"
    assert body["errorCode"] == "VALIDATION_ERROR"
    assert body["instance"] == "/api/v1/students"
    assert body["traceId"]
    assert body["errors"]
