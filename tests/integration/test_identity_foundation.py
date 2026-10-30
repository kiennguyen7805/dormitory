from fastapi.testclient import TestClient

from test_week1_flow import auth_headers, login


def test_permissions_user_management_and_profile(client: TestClient) -> None:
    admin = login(client, "admin@dormitory.local", "Admin@123")
    admin_headers = auth_headers(admin["access_token"])
    assert "identity.users.manage" in admin["user"]["permissions"]

    created = client.post(
        "/api/users",
        headers=admin_headers,
        json={
            "email": "student2@dormitory.local",
            "full_name": "Sinh viên thứ hai",
            "password": "Student2@123",
            "role": "Student",
        },
    )
    assert created.status_code == 201, created.text
    student_id = created.json()["id"]

    updated = client.put(
        f"/api/users/{student_id}",
        headers=admin_headers,
        json={"full_name": "Sinh viên 02", "role": "Student", "is_active": True},
    )
    assert updated.status_code == 200, updated.text

    student = login(client, "student@dormitory.local", "Student@123")
    profile_headers = auth_headers(student["access_token"])
    profile = client.put(
        "/api/student-profile/me",
        headers=profile_headers,
        json={
            "student_code": "SV-DEMO-001",
            "faculty": "Công nghệ thông tin",
            "cohort": "K2023",
            "phone": "0900000000",
            "address": "Ký túc xá",
            "emergency_contact_name": "Người thân",
            "emergency_contact_phone": "0911111111",
        },
    )
    assert profile.status_code == 200, profile.text
    assert profile.json()["faculty"] == "Công nghệ thông tin"

    forbidden = client.get("/api/users", headers=profile_headers)
    assert forbidden.status_code == 403


def test_deactivated_user_token_is_rejected(client: TestClient) -> None:
    admin_headers = auth_headers(login(client, "admin@dormitory.local", "Admin@123")["access_token"])
    student = login(client, "student@dormitory.local", "Student@123")
    users = client.get("/api/users", headers=admin_headers).json()
    item = next(user for user in users if user["email"] == "student@dormitory.local")
    response = client.put(
        f"/api/users/{item['id']}",
        headers=admin_headers,
        json={"full_name": item["full_name"], "role": "Student", "is_active": False},
    )
    assert response.status_code == 200
    assert client.get("/api/auth/me", headers=auth_headers(student["access_token"])).status_code == 401


def test_inventory_delete_deactivates_instead_of_removing(client: TestClient) -> None:
    headers = auth_headers(login(client, "admin@dormitory.local", "Admin@123")["access_token"])
    created = client.post(
        "/api/buildings",
        headers=headers,
        json={"code": "SAFE", "name": "Tòa lưu lịch sử", "address": "", "floors": 2},
    )
    building_id = created.json()["id"]
    assert client.delete(f"/api/buildings/{building_id}", headers=headers).status_code == 204
    retained = client.get(f"/api/buildings/{building_id}", headers=headers)
    assert retained.status_code == 200
    assert retained.json()["is_active"] is False
