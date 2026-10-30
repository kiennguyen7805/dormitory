"""Generate a self-contained Postman quick-run collection (v2.1)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def script(kind, code):
    return {"listen": kind, "script": {"type": "text/javascript", "exec": code.splitlines()}}


def req(name, method, path, role=None, body=None, code=200, tests="", pre="", system=False):
    request = {"method": method, "header": [], "url": "{{baseUrl}}" + ("" if system else "/api/v1") + path}
    request["auth"] = {"type": "bearer", "bearer": [{"key": "token", "value": "{{" + role + "Token}}", "type": "string"}]} if role else {"type": "noauth"}
    if body is not None:
        request["header"] = [{"key": "Content-Type", "value": "application/json"}]
        request["body"] = {"mode": "raw", "raw": json.dumps(body, ensure_ascii=False, indent=2), "options": {"raw": {"language": "json"}}}
    check = f"pm.test('HTTP {code}', () => pm.response.to.have.status({code}));\nif (pm.response.code !== {code}) {{ pm.execution.setNextRequest(null); throw new Error(pm.response.text()); }}\n" + tests
    events = [script("test", check)]
    if pre:
        events.insert(0, script("prerequest", pre))
    return {"name": name, "request": request, "event": events}


def save(key):
    return "pm.collectionVariables.set('" + key + "', pm.response.json().id);"


def login(role):
    return req("Dang nhap " + role, "POST", "/auth/login", body={"email": "{{" + role + "Email}}", "password": "{{" + role + "Password}}"}, tests="const token = pm.response.json().access_token; pm.expect(token).to.be.a('string').and.not.empty; pm.collectionVariables.set('" + role + "Token', token); pm.collectionVariables.set('access_token', token);")


setup = """const v = pm.collectionVariables;
const tag = Date.now().toString(36) + Math.random().toString(36).slice(2, 5);
const now = new Date();
const day = n => { const d = new Date(now); d.setUTCDate(d.getUTCDate()+n); return d.toISOString().slice(0,10); };
v.set('runTag', tag); v.set('today', day(0)); v.set('contractEnd', day(90)); v.set('dueDate', day(15));
v.set('studentEmail', 'quick.'+tag+'@example.com'); v.set('studentCode', 'Q'+tag.slice(-7).toUpperCase());
v.set('buildingCode', 'Q'+tag.toUpperCase()); v.set('roomCode', '101'); v.set('termCode', 'Q-'+tag); v.set('billKey', 'quick-'+tag);
['access_token','adminToken','staffToken','studentToken','buildingId','roomId','applicationId','contractId','electricityId','waterId','electricityMeterId','waterMeterId','billId'].forEach(k => v.unset(k));
// Local variables prevent a previously selected environment from overriding this run.
['baseUrl','adminEmail','adminPassword','staffEmail','staffPassword','studentPassword'].forEach(k => pm.variables.set(k,v.get(k)));
"""

items = [
    {"name": "00 - Khoi tao tu dong", "item": [req("Bat dau - tao ma va ngay tu dong", "GET", "/readyz", system=True, pre=setup)]},
    {"name": "01 - Tu dong lay access token", "item": [login("admin"), login("staff"),
        req("Dang ky sinh vien moi", "POST", "/auth/register", body={"email": "{{studentEmail}}", "full_name": "Quickrun {{runTag}}", "password": "{{studentPassword}}", "student_code": "{{studentCode}}", "age": 20}, code=201), login("student")]},
    {"name": "02 - Tao phong va hop dong", "item": [
        req("Tao toa nha", "POST", "/buildings", "admin", {"code": "{{buildingCode}}", "name": "Quickrun {{runTag}}", "address": "Demo", "floors": 2}, 201, save("buildingId")),
        req("Tao phong", "POST", "/rooms", "staff", {"building_id": "{{buildingId}}", "code": "{{roomCode}}", "floor": 1, "capacity": 2, "monthly_rate": 500000}, 201, save("roomId")),
        req("Sinh vien gui don", "POST", "/housing-applications", "student", {"term_code": "{{termCode}}", "room_id": "{{roomId}}"}, 201, save("applicationId")),
        req("Staff duyet don", "POST", "/housing-applications/{{applicationId}}/approve", "staff"),
        req("Staff lap hop dong", "POST", "/contracts/{{applicationId}}/assign-room", "staff", {"start_date": "{{today}}", "end_date": "{{contractEnd}}"}, 201, save("contractId")),
        req("Sinh vien xem hop dong", "GET", "/contracts/me", "student", tests="pm.expect(pm.response.json().id).to.eql(pm.collectionVariables.get('contractId'));")]},
    {"name": "03 - Lay ID tien ich va cong to", "item": [
        req("Lay ID dien va nuoc", "GET", "/utilities", "staff", tests="const rows=pm.response.json(); ['electricity','water'].forEach(k=>{ const x=rows.find(x=>x.code===k.toUpperCase()); pm.expect(x,k).to.exist; pm.collectionVariables.set(k+'Id',x.id); });"),
        req("Lay ID cong to cua phong", "GET", "/meters?room_id={{roomId}}", "staff", tests="const rows=pm.response.json(); ['electricity','water'].forEach(k=>{ const x=rows.find(x=>x.utility_code===k.toUpperCase()); pm.expect(x,k).to.exist; pm.collectionVariables.set(k+'MeterId',x.id); });")]},
]

for kind, price, consumption in (("electricity", 1000, 80), ("water", 15000, 10)):
    reading = "Ghi chi so " + kind
    items.append({"name": "04 - Dien" if kind == "electricity" else "05 - Nuoc", "item": [
        req("Tim bieu gia " + kind, "GET", "/utility-tariffs?utility_id={{" + kind + "Id}}", "staff", tests="const date=pm.collectionVariables.get('today'); const found=pm.response.json().find(x=>x.is_active && x.effective_from<=date && (!x.effective_to || x.effective_to>=date)); if(found) pm.execution.setNextRequest('" + reading + "');"),
        req("Tao bieu gia " + kind + " neu chua co", "POST", "/utility-tariffs", "staff", {"utility_id": "{{" + kind + "Id}}", "name": "Quickrun " + kind + " {{runTag}}", "effective_from": "{{today}}", "effective_to": "{{today}}", "calculation_type": "Flat", "tiers": [{"tier_order": 1, "from_quantity": 0, "to_quantity": None, "unit_price": price}]}, 201),
        req(reading, "POST", "/meter-readings", "staff", {"meter_id": "{{" + kind + "MeterId}}", "period_start": "{{today}}", "period_end": "{{today}}", "previous_reading": 0, "current_reading": consumption}, 201)]})

items.append({"name": "06 - Hoa don va thanh toan", "item": [
    req("Tao hoa don phong", "POST", "/bills/generate", "staff", {"room_id": "{{roomId}}", "period_start": "{{today}}", "period_end": "{{today}}", "issued_date": "{{today}}", "due_date": "{{dueDate}}", "idempotency_key": "{{billKey}}"}, 201, save("billId") + "\nconst b=pm.response.json(); pm.test('Hai dong dien nuoc',()=>pm.expect(b.items).to.have.length(2)); pm.test('Tong tien duong',()=>pm.expect(Number(b.total_amount)).to.be.above(0));"),
    req("Sinh vien xem hoa don", "GET", "/bills/{{billId}}", "student"),
    req("Staff xac nhan thanh toan", "POST", "/bills/{{billId}}/confirm-payment", "staff", {"method": "Cash", "reference": "QUICK-{{runTag}}"}, tests="const b=pm.response.json(); pm.test('Da thanh toan',()=>pm.expect(b.status).to.eql('Paid')); pm.test('Het no',()=>pm.expect(Number(b.balance_amount)).to.eql(0));"),
    req("Ket thuc - sinh vien xem ket qua", "GET", "/bills/{{billId}}", "student", tests="pm.test('Paid',()=>pm.expect(pm.response.json().status).to.eql('Paid')); pm.collectionVariables.set('access_token',pm.collectionVariables.get('studentToken')); console.log('DONE. IDs and tokens are saved in collection variables.');") ]})

defaults = {"baseUrl": "http://localhost:8081", "adminEmail": "admin@dormitory.local", "adminPassword": "Admin@123", "staffEmail": "staff@dormitory.local", "staffPassword": "Staff@123", "studentPassword": "Student@123"}
keys = "runTag today contractEnd dueDate studentEmail studentCode buildingCode roomCode termCode billKey access_token adminToken staffToken studentToken buildingId roomId applicationId contractId electricityId waterId electricityMeterId waterMeterId billId".split()
collection = {
    "info": {"name": "Dormitory - CHAY NHANH TU DONG", "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json", "description": "Import, select No Environment, then Run entire collection in order (1 iteration, 300 ms delay). Requires Docker Compose and seeded demo accounts. Automatically creates demo records and pays the generated room bill. Repeatable with unique codes. Tariff setup branches automatically in Runner. Period is one day for a quick demo. Stop on HTTP failure. Tokens and IDs stay in collection variables; access_token points to the new student at the end."},
    "variable": [{"key": k, "value": v, "type": "string"} for k, v in {**defaults, **dict.fromkeys(keys, "")}.items()],
    "event": [script("prerequest", "// Always resolve variables from this collection, even if another environment was selected.\npm.collectionVariables.toObject && Object.entries(pm.collectionVariables.toObject()).forEach(([k,v])=>pm.variables.set(k,v));")],
    "item": items,
}
target = ROOT / "postman" / "Dormitory_QuickRun.postman_collection.json"
target.write_text(json.dumps(collection, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
print("Created postman/Dormitory_QuickRun.postman_collection.json")
