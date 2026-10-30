"""Check the public API surface without connecting to a database."""

from dormitory_api.main import app


spec = app.openapi()
tags = {item["name"]: item["description"] for item in spec["tags"]}
assert "Bài 2" not in tags["Students"]

housing = {
    (method, path)
    for path, operations in spec["paths"].items()
    for method, operation in operations.items()
    if "Housing" in operation.get("tags", [])
}
assert housing == {
    ("get", "/api/v1/buildings"),
    ("post", "/api/v1/buildings"),
    ("get", "/api/v1/rooms"),
    ("post", "/api/v1/rooms"),
}, housing

for path in (
    "/api/v1/room-matrix",
    "/api/v1/contracts/{contract_id}/assignment-history",
    "/api/v1/contracts/{contract_id}/transfer",
    "/api/v1/contracts/{application_id}/assign-bed",
):
    assert path not in spec["paths"], path
    assert not any(getattr(route, "path", None) == path for route in app.routes), path

for path in (
    "/api/v1/contracts/{application_id}/assign-room",
    "/api/v1/bills/generate",
    "/api/v1/bills/{bill_id}",
    "/api/v1/bills/{bill_id}/confirm-payment",
):
    assert path in spec["paths"], path

assert "room_id" in spec["components"]["schemas"]["BillGenerateRequest"]["required"]

print("OpenAPI scope OK")
