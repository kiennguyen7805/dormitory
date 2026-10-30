"""Generate the eight-week importable Postman collection; stdlib only, workbook read-only."""
import json
import uuid
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
NS = {"s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
TARGET = ROOT / "postman/Dormitory_MasterPlan_8Tuan.postman_collection.json"


def read_plan():
    with zipfile.ZipFile(ROOT / "Master_Plan_MVP_8Tuan.xlsx") as z:
        ss = ["".join(x.itertext()) for x in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("s:si", NS)] if "xl/sharedStrings.xml" in z.namelist() else []
        weeks, tasks = [], {}
        for row in ET.fromstring(z.read("xl/worksheets/sheet1.xml")).findall(".//s:sheetData/s:row", NS):
            cells = {}
            for c in row:
                val, inline = c.find("s:v", NS), c.find("s:is", NS)
                cells[c.get("r").rstrip("0123456789")] = ss[int(val.text)] if c.get("t") == "s" else "".join(inline.itertext()) if inline is not None else val.text if val is not None else ""
            key, title = cells.get("A", ""), cells.get("B", "")
            if key.startswith("Tuần "):
                weeks.append({"name": title.replace("TUẦN", "Tuần"), "item": []})
            elif key.isdigit() and title:
                tasks[int(key)] = {"title": title, "row": row.get("r"), "week": len(weeks)}
    if len(weeks) != 8 or set(tasks) != set(range(1, 33)):
        raise ValueError("Expected eight weeks and tasks 1–32 in sheet Plan")
    return weeks, tasks


def event(kind, code):
    return {"listen": kind, "script": {"type": "text/javascript", "exec": code.splitlines()}}


BUILDING = {"code": "{{buildingCode}}", "name": "Postman {{runTag}}", "address": "Demo", "floors": 2}
ROOM = {"building_id": "{{buildingId}}", "code": "101", "floor": 1, "capacity": 2, "monthly_rate": 500000}
REGISTER = {"email": "{{studentEmail}}", "full_name": "Postman {{runTag}}", "password": "{{studentPassword}}", "student_code": "{{studentCode}}", "age": 20}
APPLICATION = {"term_code": "{{termCode}}", "room_id": "{{roomId}}"}
ASSIGN = {"start_date": "{{today}}", "end_date": "{{contractEnd}}"}
BILL = {"room_id": "{{roomId}}", "period_start": "{{today}}", "period_end": "{{today}}", "issued_date": "{{today}}", "due_date": "{{dueDate}}", "idempotency_key": "{{billKey}}"}
PAYMENT = {"method": "Cash", "reference": "PM-{{runTag}}"}


def reading(kind, previous=0, current=None):
    return {"meter_id": "{{" + kind + "MeterId}}", "period_start": "{{today}}", "period_end": "{{today}}", "previous_reading": previous, "current_reading": current if current is not None else (80 if kind == "electricity" else 10)}


def tariff(kind):
    return {"utility_id": "{{" + kind + "Id}}", "name": "PM " + kind + " {{runTag}}", "effective_from": "{{tariffDate}}", "effective_to": "{{tariffDate}}", "calculation_type": "Flat", "tiers": [{"tier_order": 1, "from_quantity": 0, "to_quantity": None, "unit_price": 1000 if kind == "electricity" else 15000}]}


TOKEN_TEST = """const b=pm.response.json();
pm.test('Có access_token và refresh_token',()=>{pm.expect(b.access_token).to.be.a('string').and.not.empty;pm.expect(b.refresh_token).to.be.a('string').and.not.empty;});
pm.collectionVariables.set('access_token',b.access_token);
pm.collectionVariables.set('refresh_token',b.refresh_token);"""
BILL_TEST = """const bill=pm.response.json();
pm.test('Hóa đơn phòng, không gắn riêng sinh viên',()=>{pm.expect(bill.room_id).to.eql(pm.variables.get('roomId'));pm.expect(bill.student_id).to.eql(null);pm.expect(bill.contract_id).to.eql(null);});
pm.test('Hai dòng điện/nước; tổng khớp các dòng',()=>{pm.expect(bill.items).to.have.length(2);pm.expect(bill.items.map(x=>x.item_type).sort()).to.eql(['Electricity','Water']);pm.expect(Number(bill.total_amount)).to.eql(bill.items.reduce((s,x)=>s+Number(x.amount),0));});"""
PAID_TEST = """const paid=pm.response.json();
pm.test('Paid, trả đủ, dư nợ 0',()=>{pm.expect(paid.status).to.eql('Paid');pm.expect(Number(paid.paid_amount)).to.eql(Number(paid.total_amount));pm.expect(Number(paid.balance_amount)).to.eql(0);});
pm.test('Lưu phương thức, tham chiếu, thời điểm',()=>{pm.expect(paid.payment_method).to.eql('Cash');pm.expect(paid.payment_reference).to.eql('PM-'+pm.variables.get('runTag'));pm.expect(paid.paid_at).to.be.a('string').and.not.empty;});"""
READING_TEST = """const b=pm.response.json();
pm.test('Tiêu thụ đúng, có snapshot, tiền không âm',()=>{pm.expect(Number(b.consumption)).to.eql(Number(b.current_reading)-Number(b.previous_reading));pm.expect(b.tariff_snapshot).to.be.an('object').and.not.empty;pm.expect(b.tariff_id).to.be.a('string');pm.expect(Number(b.calculated_amount)).to.be.at.least(0);});"""


def build():
    weeks, tasks = read_plan()
    specs, counts = {}, {}

    def add(task, title, method, path, role=None, body=None, status=200, setup="none", tests="", error=None, **options):
        counts[task] = counts.get(task, 0) + 1
        title = title.replace("/", "-")
        name = f"{task:02d}.{counts[task]:02d} - {title}"
        specs[name] = {"role": role, "setup": setup, **options}
        request = {"method": method, "url": "{{baseUrl}}" + path, "header": [], "auth": {"type": "bearer", "bearer": [{"key": "token", "value": "{{access_token}}", "type": "string"}]} if role else {"type": "noauth"}}
        request["description"] = (
            f"**Kế hoạch:** Plan!B{tasks[task]['row']} — {tasks[task]['title']}\n\n"
            f"**{method} {path}** · HTTP dự kiến **{status}**" + (f" · errorCode **{error}**" if error else "")
            + f"\n\nVai trò: {role or 'Không cần token'}. Bấm **Send**. Script collection tự đăng nhập và chuẩn bị dữ liệu mẫu riêng ({setup}); không phải chạy tuần trước. URL, body và Authorization điền bằng biến."
            + "\n\nMỗi Send có thể tạo dữ liệu demo mới trong database. Xem Scripts → Pre-request của collection và Post-response của request; mở Postman Console để xem các request chuẩn bị. Kỳ demo là một ngày, dùng biểu giá hiện hành."
        )
        if body is not None:
            request["header"].append({"key": "Content-Type", "value": "application/json"})
            request["body"] = {"mode": "raw", "raw": json.dumps(body, ensure_ascii=False, indent=2), "options": {"raw": {"language": "json"}}}
        code = f"pm.test('HTTP {status}',()=>pm.response.to.have.status({status}));\n"
        if status >= 400:
            code += "pm.test('Problem JSON có status, traceId, instance',()=>{const b=pm.response.json();pm.expect(b.status).to.eql(pm.response.code);pm.expect(b.traceId).to.be.a('string').and.not.empty;pm.expect(b.instance).to.include('/api/v1/');pm.expect(pm.response.headers.get('Content-Type')).to.include('application/problem+json');});\n"
        if error:
            code += f"pm.test('errorCode {error}',()=>pm.expect(pm.response.json().errorCode).to.eql('{error}'));\n"
        code += f"if(pm.response.code==={status}){{\n{tests}\n}}"
        weeks[tasks[task]["week"] - 1]["item"].append({"id": str(uuid.uuid5(uuid.NAMESPACE_URL, name)), "name": name, "request": request, "event": [event("test", code)]})

    add(1,"API đang sống","GET","/healthz",tests="pm.test('API ok',()=>pm.expect(pm.response.json().status).to.eql('ok'));")
    add(1,"PostgreSQL và migration sẵn sàng","GET","/readyz",tests="pm.test('Database ok',()=>pm.expect(pm.response.json().database).to.eql('ok'));")
    add(2,"Sinh viên đăng ký tài khoản","POST","/api/v1/auth/register",body=REGISTER,status=201)
    for role in ("admin","staff","student"):
        add(2,"Đăng nhập "+role,"POST","/api/v1/auth/login",body={"email":"{{"+role+"Email}}","password":"{{"+role+"Password}}"},setup="student" if role=="student" else "none",tests=TOKEN_TEST+f"\npm.test('Đúng vai trò',()=>pm.expect(b.user.role).to.eql('{role.title()}'));")
        add(2,"Xem phiên "+role,"GET","/api/v1/auth/me",role,tests=f"pm.test('Đúng vai trò',()=>pm.expect(pm.response.json().role).to.eql('{role.title()}'));")
    add(2,"Làm mới token","POST","/api/v1/auth/refresh",body={"refresh_token":"{{refresh_token}}"},setup="refresh",tests=TOKEN_TEST)
    add(2,"Admin xem người dùng","GET","/api/v1/users","admin",tests="pm.test('Ba vai trò',()=>pm.response.json().forEach(x=>pm.expect(['Admin','Staff','Student']).to.include(x.role)));")
    add(2,"Admin tạo tài khoản Staff","POST","/api/v1/users","admin",{"email":"staff.{{runTag}}@example.com","full_name":"PM Staff","password":"Staff@123","role":"Staff"},201)
    add(2,"Admin cập nhật tài khoản mẫu","PUT","/api/v1/users/{{managedUserId}}","admin",{"full_name":"PM Staff Updated","role":"Staff","is_active":True},setup="managed-user")
    add(2,"Sinh viên xem hồ sơ","GET","/api/v1/student-profile/me","student")
    add(2,"Sinh viên cập nhật hồ sơ","PUT","/api/v1/student-profile/me","student",{"student_code":"{{studentCode}}","faculty":"CNTT","cohort":"K24","phone":"0901234567"})
    add(2,"Staff xem sinh viên có phân trang","GET","/api/v1/students?page=1&pageSize=10","staff",tests="pm.test('Có phân trang',()=>{const b=pm.response.json();pm.expect(b.items).to.be.an('array');pm.expect(b.pageSize).to.eql(10);});")
    add(3,"Admin thêm tòa","POST","/api/v1/buildings","admin",BUILDING,201)
    add(3,"Staff thêm phòng","POST","/api/v1/rooms","staff",ROOM,201,"building")
    add(4,"Sinh viên xem tòa","GET","/api/v1/buildings","student")
    add(4,"Sinh viên xem phòng theo tòa","GET","/api/v1/rooms?buildingId={{buildingId}}","student",setup="room",tests="pm.test('Phòng mẫu xuất hiện',()=>pm.expect(pm.response.json().some(x=>x.id===pm.variables.get('roomId'))).to.eql(true));")
    add(4,"Phòng tự sinh hai công tơ","GET","/api/v1/meters?room_id={{roomId}}","staff",setup="room",tests="pm.test('Đúng hai công tơ điện/nước',()=>{const b=pm.response.json();pm.expect(b).to.have.length(2);pm.expect(b.map(x=>x.utility_code).sort()).to.eql(['ELECTRICITY','WATER']);});")
    add(5,"Sinh viên gửi đăng ký chọn phòng","POST","/api/v1/housing-applications","student",APPLICATION,201,"room")
    add(5,"Sinh viên theo dõi đơn","GET","/api/v1/housing-applications","student",setup="application",tests="pm.test('Thấy đơn vừa tạo',()=>pm.expect(pm.response.json().some(x=>x.id===pm.variables.get('applicationId'))).to.eql(true));")
    add(6,"Staff duyệt đơn","POST","/api/v1/housing-applications/{{applicationId}}/approve","staff",setup="application",tests="pm.test('Approved',()=>pm.expect(pm.response.json().status).to.eql('Approved'));")
    add(6,"Staff từ chối có lý do","POST","/api/v1/housing-applications/{{applicationId}}/reject","staff",{"reason":"Hồ sơ chưa đầy đủ"},setup="application",tests="pm.test('Rejected',()=>pm.expect(pm.response.json().status).to.eql('Rejected'));")
    add(7,"Lập hợp đồng gắn phòng đăng ký","POST","/api/v1/contracts/{{applicationId}}/assign-room","staff",ASSIGN,201,"approved",tests="pm.test('Đúng phòng',()=>{const b=pm.response.json();pm.expect(b.application_id).to.eql(pm.variables.get('applicationId'));pm.expect(b.current_assignment.building_code).to.eql(pm.variables.get('buildingCode').toUpperCase());pm.expect(b.current_assignment.room_code).to.eql('101');});")
    add(8,"Sinh viên xem hợp đồng","GET","/api/v1/contracts/me","student",setup="contract",tests="pm.test('Đúng hợp đồng',()=>pm.expect(pm.response.json().id).to.eql(pm.variables.get('contractId')));")
    add(8,"Staff xem hợp đồng","GET","/api/v1/contracts","staff",setup="contract")
    add(8,"Staff chấm dứt hợp đồng mẫu","POST","/api/v1/contracts/{{contractId}}/terminate","staff",{"termination_date":"{{today}}"},setup="contract",tests="pm.test('Terminated',()=>pm.expect(pm.response.json().status).to.eql('Terminated'));")
    add(9,"Danh sách hai tiện ích","GET","/api/v1/utilities","staff",tests="pm.test('Có điện và nước',()=>pm.expect(pm.response.json().map(x=>x.code)).to.include.members(['ELECTRICITY','WATER']));")
    add(9,"Danh sách công tơ phòng","GET","/api/v1/meters?room_id={{roomId}}","staff",setup="room")
    for kind,label in (("electricity","điện"),("water","nước")):
        add(10,"Thiết lập biểu giá "+label,"POST","/api/v1/utility-tariffs","staff",tariff(kind),201,"tariff-slot",kind=kind)
        add(10,"Nhập chỉ số "+label,"POST","/api/v1/meter-readings","staff",reading(kind),201,"meters",tests=READING_TEST)
    add(11,"[400] Chặn chỉ số giảm","POST","/api/v1/meter-readings","staff",reading("electricity",10,9),400,"meters",error="VALIDATION_ERROR")
    add(11,"[409] Chặn chỉ số trùng kỳ","POST","/api/v1/meter-readings","staff",reading("electricity"),409,"electricity-reading",error="METER_READING_ALREADY_EXISTS")
    add(12,"Kiểm tra tiền và snapshot giá","GET","/api/v1/meter-readings?meter_id={{electricityMeterId}}","staff",setup="readings",tests="pm.test('Snapshot và tiền đúng',()=>{const b=pm.response.json()[0];pm.expect(b.tariff_snapshot).to.be.an('object').and.not.empty;pm.expect(Number(b.consumption)).to.eql(80);pm.expect(Number(b.calculated_amount)).to.eql(Number(pm.variables.get('electricityAmount')));});")
    add(13,"[422] Không phát hành khi thiếu chỉ số nước","POST","/api/v1/bills/generate","staff",BILL,422,"electricity-reading",error="READINGS_INCOMPLETE")
    add(14,"Phát hành hóa đơn phòng/kỳ","POST","/api/v1/bills/generate","staff",BILL,201,"readings",tests=BILL_TEST)
    add(15,"Sinh viên thứ nhất xem hóa đơn","GET","/api/v1/bills/{{billId}}","student",setup="bill",tests=BILL_TEST)
    add(15,"Sinh viên thứ hai xem cùng hóa đơn","GET","/api/v1/bills/{{billId}}","student2",setup="shared-bill",tests=BILL_TEST)
    add(16,"Gửi lại cùng key trả cùng hóa đơn","POST","/api/v1/bills/generate","staff",BILL,201,"bill",tests="pm.test('Cùng billId',()=>pm.expect(pm.response.json().id).to.eql(pm.variables.get('billId')));")
    add(16,"[409] Cùng phòng/kỳ, key mới","POST","/api/v1/bills/generate","staff",{**BILL,"idempotency_key":"other-{{runTag}}"},409,"bill",error="BILL_PERIOD_ALREADY_EXISTS")
    add(16,"[409] Cùng key, dữ liệu khác","POST","/api/v1/bills/generate","staff",{**BILL,"period_end":"{{contractEnd}}"},409,"bill",error="IDEMPOTENCY_KEY_REUSED")
    add(17,"Staff xác nhận trả đủ","POST","/api/v1/bills/{{billId}}/confirm-payment","staff",PAYMENT,setup="bill",tests=PAID_TEST)
    add(18,"Xem thông tin xác nhận thanh toán","GET","/api/v1/bills/{{billId}}","staff",setup="paid",tests=PAID_TEST)
    add(19,"[409] Chặn xác nhận lần hai","POST","/api/v1/bills/{{billId}}/confirm-payment","staff",PAYMENT,409,"paid",error="BILL_NOT_PAYABLE")
    add(19,"Sinh viên xem đã trả","GET","/api/v1/bills/{{billId}}","student",setup="paid",tests=PAID_TEST)
    add(20,"Đối chiếu tổng tiền và hai dòng điện nước","GET","/api/v1/bills/{{billId}}","staff",setup="bill",tests=BILL_TEST)
    add(21,"Hai sinh viên cùng phòng, một hóa đơn chung","GET","/api/v1/bills?room_id={{roomId}}","student2",setup="shared-bill",tests="pm.test('Cả hai thấy một hóa đơn chung',()=>{const b=pm.response.json();pm.expect(b.map(x=>x.id)).to.include(pm.variables.get('billId'));pm.expect(JSON.parse(pm.variables.get('firstStudentBillIds'))).to.include(pm.variables.get('billId'));pm.expect(b.filter(x=>x.room_id===pm.variables.get('roomId'))).to.have.length(1);});")
    add(22,"[409] Phòng đủ hai chỗ không nhận người thứ ba","POST","/api/v1/contracts/{{applicationId}}/assign-room","staff",ASSIGN,409,"full-room",error="ROOM_FULL")
    add(22,"[409] Đơn chưa duyệt không lập hợp đồng","POST","/api/v1/contracts/{{applicationId}}/assign-room","staff",ASSIGN,409,"application",error="APPLICATION_NOT_APPROVED")
    add(22,"[409] Không lập trùng hợp đồng","POST","/api/v1/contracts/{{applicationId}}/assign-room","staff",ASSIGN,409,"contract",error="CONTRACT_ALREADY_EXISTS")
    add(23,"Admin được xem người dùng","GET","/api/v1/users","admin")
    add(23,"Staff được xem công tơ","GET","/api/v1/meters","staff")
    add(23,"[403] Staff không được thêm tòa","POST","/api/v1/buildings","staff",BUILDING,403,error="AUTH_FORBIDDEN")
    add(23,"[403] Student không được thêm tòa","POST","/api/v1/buildings","student",BUILDING,403,error="AUTH_FORBIDDEN")
    add(23,"[403] Student không được phát hành hóa đơn","POST","/api/v1/bills/generate","student",BILL,403,"room",error="AUTH_FORBIDDEN")
    add(23,"[403] Student không được xem hóa đơn phòng khác","GET","/api/v1/bills/{{billId}}","outsider",setup="bill",status=403,error="OWN_DATA_ONLY")
    add(23,"[401] Không có token","GET","/api/v1/auth/me",status=401,error="AUTH_INVALID_TOKEN")
    add(24,"[400] Chỉ số giảm","POST","/api/v1/meter-readings","staff",reading("electricity",10,9),400,"meters",error="VALIDATION_ERROR")
    add(24,"[409] Chỉ số trùng","POST","/api/v1/meter-readings","staff",reading("electricity"),409,"electricity-reading",error="METER_READING_ALREADY_EXISTS")
    add(24,"[422] Thiếu chỉ số","POST","/api/v1/bills/generate","staff",BILL,422,"electricity-reading",error="READINGS_INCOMPLETE")
    add(24,"[409] Thanh toán lặp","POST","/api/v1/bills/{{billId}}/confirm-payment","staff",PAYMENT,409,"paid",error="BILL_NOT_PAYABLE")
    add(25,"OpenAPI đúng phạm vi MVP","GET","/openapi.json",tests="pm.test('Có MVP, không có giường/chuyển phòng công khai',()=>{const p=pm.response.json().paths;pm.expect(p).to.have.property('/api/v1/bills/generate');pm.expect(p).to.have.property('/api/v1/contracts/{application_id}/assign-room');Object.keys(p).forEach(x=>pm.expect(x).not.to.match(/beds|room-matrix|transfer/));});")
    add(25,"Trang Swagger","GET","/docs",tests="pm.test('Swagger UI',()=>pm.expect(pm.response.text()).to.include('swagger-ui'));")
    add(26,"Luồng đăng ký đến trả đủ bằng một Send","GET","/api/v1/bills/{{billId}}","student",setup="paid",tests=PAID_TEST+"\n"+BILL_TEST)
    add(27,"Ví dụ lỗi đăng nhập và Problem JSON","POST","/api/v1/auth/login",body={"email":"missing.{{runTag}}@example.com","password":"Incorrect@123"},status=401,error="AUTH_INVALID_CREDENTIALS")
    add(28,"Rà endpoint và ba vai trò","GET","/api/v1/users","admin",tests="pm.test('Đủ ba vai trò',()=>pm.expect([...new Set(pm.response.json().map(x=>x.role))].sort()).to.eql(['Admin','Staff','Student']));")
    add(29,"Gateway Docker đang sống","GET","/gateway/healthz",tests="pm.test('Gateway ok',()=>pm.expect(pm.response.json().service).to.eql('gateway'));")
    add(30,"API và PostgreSQL sẵn sàng","GET","/readyz",tests="pm.test('Ready',()=>pm.expect(pm.response.json()).to.eql({status:'ready',database:'ok'}));")
    add(30,"Swagger môi trường demo","GET","/docs",tests="pm.test('Swagger UI',()=>pm.expect(pm.response.text()).to.include('swagger-ui'));")
    add(31,"Kiểm thử đầu cuối trên dữ liệu demo mới","GET","/api/v1/bills/{{billId}}","student",setup="paid",tests=PAID_TEST+"\n"+BILL_TEST)
    add(32,"Demo trọn luồng và hai sinh viên xem đã trả","GET","/api/v1/bills/{{billId}}","student2",setup="shared-paid",tests=PAID_TEST+"\n"+BILL_TEST)

    if set(counts) != set(tasks):
        raise ValueError("Every Plan task must have runnable requests")
    shared = (ROOT / "scripts/postman/masterplan_prerequest.js").read_text(encoding="utf-8-sig")
    pre = "(async () => {\nconst scenarios = " + json.dumps(specs, ensure_ascii=False, indent=2) + ";\n" + shared + "\n})().catch(error=>{pm.test('Setup completed',()=>{throw error;});console.error(error.message);if(pm.execution && pm.execution.skipRequest)pm.execution.skipRequest();});"
    for i, week in enumerate(weeks, 1):
        week["description"] = "\n".join(f"{k}. {t['title']} (Plan!B{t['row']})" for k,t in tasks.items() if t["week"]==i) + "\n\nMở bất kỳ request → Send. Mỗi request độc lập, kể cả ca lỗi. Có thể Run folder hoặc toàn collection, 1 iteration."
    defaults = {"baseUrl":"http://localhost:8081","adminEmail":"admin@dormitory.local","adminPassword":"Admin@123","staffEmail":"staff@dormitory.local","staffPassword":"Staff@123","studentPassword":"Student@123","access_token":"","refresh_token":""}
    collection = {
        "info": {"_postman_id":"e6e71173-5a66-4dca-8a87-80481c156200","name":"Dormitory MVP - Master Plan 8 tuần","schema":"https://schema.getpostman.com/json/collection/v2.1.0/collection.json","description":"Đủ 8 tuần, 32 công việc từ sheet Plan. Chọn No Environment, mở bất kỳ request → Send. Tự lấy token, tạo dữ liệu phụ thuộc riêng mỗi lần. Có thể Run toàn collection, gồm ca lỗi dự kiến 4xx. Cần Docker/gateway và tài khoản demo đã seed. Mỗi Send có thể thêm dữ liệu demo. Tuần 7/8 kiểm tra HTTP phục vụ tài liệu/Docker, không build hoặc chỉnh tài liệu qua HTTP. Checklist Excel còn logout nhưng backend đã bỏ endpoint này. Người xác nhận thanh toán lưu nội bộ, BillRead chưa công khai trường này."},
        "variable":[{"key":k,"value":x,"type":"string"} for k,x in defaults.items()],
        "event":[event("prerequest",pre)],
        "item":weeks,
    }
    TARGET.write_text(json.dumps(collection,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

    # Native Git / Local View format. JSON is valid YAML; PyYAML is optional.
    def write_yaml(path, data):
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            import yaml
        except ImportError:
            text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
        else:
            class Dumper(yaml.SafeDumper):
                pass
            Dumper.add_representer(str, lambda dumper, value: dumper.represent_scalar("tag:yaml.org,2002:str", value, style="|" if "\n" in value else None))
            text = yaml.dump(data, Dumper=Dumper, allow_unicode=True, sort_keys=False, width=100)
        path.write_text(text, encoding="utf-8")

    native_root = ROOT / "postman/collections" / collection["info"]["name"]
    write_yaml(native_root / ".resources/definition.yaml", {
        "$kind": "collection", "description": collection["info"]["description"],
        "variables": defaults,
        "scripts": [{"type": "beforeRequest", "code": pre, "language": "text/javascript"}],
    })
    for week_index, week in enumerate(weeks, 1):
        folder = native_root / week["name"]
        write_yaml(folder / ".resources/definition.yaml", {"$kind": "collection", "order": week_index * 1000, "description": week["description"]})
        for index, item in enumerate(week["item"], 1):
            req = item["request"]
            auth = {"type": "bearer", "credentials": {"token": "{{access_token}}"}} if req["auth"]["type"] == "bearer" else {"type": "noauth"}
            data = {"$kind": "http-request", "description": req["description"], "url": req["url"], "method": req["method"], "auth": auth, "order": index * 1000}
            if req["header"]:
                data["headers"] = {h["key"]: h["value"] for h in req["header"]}
            if "body" in req:
                data["body"] = {"type": "json", "content": req["body"]["raw"]}
            data["scripts"] = [{"type": "afterResponse", "code": "\n".join(item["event"][0]["script"]["exec"]), "language": "text/javascript"}]
            write_yaml(folder / (item["name"] + ".request.yaml"), data)
    coverage = ["# Đối chiếu Master Plan và Postman", "", "Sinh tự động từ sheet Plan; không sửa workbook.", "", "| Tuần | STT | Công việc trong Plan | Ô nguồn | Số request |", "|---|---:|---|---|---:|"]
    coverage += [f"| {t['week']} | {k} | {t['title']} | Plan!B{t['row']} | {counts[k]} |" for k,t in tasks.items()]
    coverage += ["", "Các mục tài liệu/build Docker được kiểm tra bằng HTTP và luồng E2E; Postman không thực hiện build Docker hoặc sửa tài liệu.", "Checklist Excel còn POST /api/v1/auth/logout nhưng backend hiện tại đã bỏ API này; không tạo request giả.", "BillRead trả phương thức, tham chiếu và thời điểm thanh toán; người xác nhận lưu nội bộ, không có trường public để assert qua API.", ""]
    (ROOT / "postman/MASTER_PLAN_COVERAGE.md").write_text("\n".join(coverage), encoding="utf-8")

    print(f"Created {TARGET.name}: {len(weeks)} weeks, {len(tasks)} tasks, {len(specs)} requests")


if __name__ == "__main__":
    build()

