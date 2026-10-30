import json
from pathlib import Path

BASE='{{baseUrl}}/api/v1'

def req(name, method, path, role=None, body=None, status=200, tests=None, pre=None):
    headers=[{'key':'Content-Type','value':'application/json'}]
    if role: headers.append({'key':'Authorization','value':f'Bearer {{{{{role}Token}}}}'})
    request={'method':method,'header':headers,'url':BASE+path}
    if body is not None:
        request['body']={'mode':'raw','raw':json.dumps(body,ensure_ascii=False,indent=2),'options':{'raw':{'language':'json'}}}
    ev=[]
    if pre: ev.append({'listen':'prerequest','script':{'type':'text/javascript','exec':pre.splitlines()}})
    code=[f"pm.test('HTTP {status}', () => pm.response.to.have.status({status}));"]+(tests or [])
    ev.append({'listen':'test','script':{'type':'text/javascript','exec':code}})
    return {'name':name,'request':request,'event':ev}

def login(name,email,password,token):
    return req(name,'POST','/auth/login',body={'email':email,'password':password},status=200,tests=[f"pm.collectionVariables.set('{token}', pm.response.json().access_token);"])

setup=[
"const d=new Date(); const iso=d.toISOString().slice(0,10); const end=new Date(d); end.setDate(end.getDate()+30); const due=new Date(d); due.setDate(due.getDate()+15);",
"const tag=Date.now().toString().slice(-8);",
"pm.collectionVariables.set('runTag',tag); pm.collectionVariables.set('today',iso); pm.collectionVariables.set('periodEnd',end.toISOString().slice(0,10)); pm.collectionVariables.set('dueDate',due.toISOString().slice(0,10));",
"pm.collectionVariables.set('studentEmail','pm.'+tag+'@example.com'); pm.collectionVariables.set('studentCode','PM'+tag); pm.collectionVariables.set('buildingCode','P'+tag); pm.collectionVariables.set('roomCode','R'+tag); pm.collectionVariables.set('billKey','pm-'+tag);",
"['adminToken','staffToken','studentToken','buildingId','roomId','applicationId','contractId','electricityId','waterId','electricityMeterId','waterMeterId','electricityTariffId','waterTariffId','billId'].forEach(k=>pm.collectionVariables.unset(k));"
]
find_tariff="const rows=pm.response.json(); const today=pm.collectionVariables.get('today'); const found=rows.find(x=>x.effective_from<=today && (!x.effective_to || x.effective_to>=today)); if(found) pm.collectionVariables.set(pm.variables.get('tariffVar'),found.id);"
items=[
{'name':'00 - Kiểm tra và khởi tạo','item':[
 req('Health check gateway','GET','/../gateway/healthz',status=200,tests=["pm.collectionVariables.set('ready','yes');"],pre='\n'.join(setup)),
]},
{'name':'01 - Đăng nhập và tạo sinh viên','item':[
 login('Đăng nhập quản trị','admin@dormitory.local','Admin@123','admin'),
 login('Đăng nhập nhân viên','staff@dormitory.local','Staff@123','staff'),
 req('Đăng ký sinh viên mới','POST','/auth/register',body={'email':'{{studentEmail}}','full_name':'Postman Student {{runTag}}','password':'Student@123','student_code':'{{studentCode}}','age':20},status=201),
 login('Đăng nhập sinh viên mới','{{studentEmail}}','Student@123','student'),
]},
{'name':'02 - Tòa nhà, phòng và đăng ký ở','item':[
 req('Tạo tòa nhà','POST','/buildings','admin',{'code':'{{buildingCode}}','name':'Postman {{runTag}}','address':'Postman test','floors':3},201,["pm.collectionVariables.set('buildingId',pm.response.json().id);"]),
 req('Tạo phòng (tự sinh đồng hồ điện/nước)','POST','/rooms','staff',{'building_id':'{{buildingId}}','code':'{{roomCode}}','floor':2,'capacity':2,'monthly_rate':500000},201,["pm.collectionVariables.set('roomId',pm.response.json().id);"]),
 req('Sinh viên xem danh sách phòng','GET','/rooms?buildingId={{buildingId}}','student'),
 req('Sinh viên tạo đơn đăng ký','POST','/housing-applications','student',{'term_code':'PM-{{runTag}}','room_id':'{{roomId}}'},201,["pm.collectionVariables.set('applicationId',pm.response.json().id);"]),
 req('Nhân viên duyệt đơn','POST','/housing-applications/{{applicationId}}/approve','staff',status=200),
 req('Nhân viên xếp phòng và tạo hợp đồng','POST','/contracts/{{applicationId}}/assign-room','staff',{'start_date':'{{today}}','end_date':'{{periodEnd}}'},201,["pm.collectionVariables.set('contractId',pm.response.json().id);"]),
 req('Sinh viên xem hợp đồng của mình','GET','/contracts/me','student'),
]},
{'name':'03 - Đồng hồ, biểu giá và chỉ số','item':[
 req('Lấy danh sách tiện ích','GET','/utilities','staff',tests=["const u=pm.response.json(); pm.collectionVariables.set('electricityId',u.find(x=>x.code==='ELECTRICITY').id); pm.collectionVariables.set('waterId',u.find(x=>x.code==='WATER').id);"]),
 req('Lấy đồng hồ của phòng','GET','/meters?room_id={{roomId}}','staff',tests=["const m=pm.response.json(); pm.collectionVariables.set('electricityMeterId',m.find(x=>x.utility_code==='ELECTRICITY').id); pm.collectionVariables.set('waterMeterId',m.find(x=>x.utility_code==='WATER').id);"]),
 req('Kiểm tra biểu giá điện đang hiệu lực','GET','/utility-tariffs?utility_id={{electricityId}}','staff',tests=[find_tariff.replace('tariffVar',"'electricityTariffId'")]),
 req('Tạo biểu giá điện nếu chưa có','POST','/utility-tariffs','staff',{'utility_id':'{{electricityId}}','name':'PM Electricity {{runTag}}','effective_from':'{{today}}','effective_to':None,'calculation_type':'Flat','tiers':[{'tier_order':1,'from_quantity':0,'to_quantity':None,'unit_price':1000}]},201,["pm.collectionVariables.set('electricityTariffId',pm.response.json().id);"],pre="if(pm.collectionVariables.get('electricityTariffId')) pm.execution.skipRequest();"),
 req('Kiểm tra biểu giá nước đang hiệu lực','GET','/utility-tariffs?utility_id={{waterId}}','staff',tests=[find_tariff.replace('tariffVar',"'waterTariffId'")]),
 req('Tạo biểu giá nước nếu chưa có','POST','/utility-tariffs','staff',{'utility_id':'{{waterId}}','name':'PM Water {{runTag}}','effective_from':'{{today}}','effective_to':None,'calculation_type':'Flat','tiers':[{'tier_order':1,'from_quantity':0,'to_quantity':None,'unit_price':15000}]},201,["pm.collectionVariables.set('waterTariffId',pm.response.json().id);"],pre="if(pm.collectionVariables.get('waterTariffId')) pm.execution.skipRequest();"),
 req('Ghi chỉ số điện','POST','/meter-readings','staff',{'meter_id':'{{electricityMeterId}}','period_start':'{{today}}','period_end':'{{periodEnd}}','previous_reading':0,'current_reading':80},201),
 req('Ghi chỉ số nước','POST','/meter-readings','staff',{'meter_id':'{{waterMeterId}}','period_start':'{{today}}','period_end':'{{periodEnd}}','previous_reading':0,'current_reading':10},201),
]},
{'name':'04 - Hóa đơn và thanh toán','item':[
 req('Tạo hóa đơn phòng','POST','/bills/generate','staff',{'room_id':'{{roomId}}','period_start':'{{today}}','period_end':'{{periodEnd}}','issued_date':'{{today}}','due_date':'{{dueDate}}','idempotency_key':'{{billKey}}'},201,["const b=pm.response.json(); pm.collectionVariables.set('billId',b.id); pm.test('Hóa đơn có hai khoản tiện ích',()=>pm.expect(b.items).to.have.length(2)); pm.test('Tổng tiền lớn hơn 0',()=>pm.expect(b.total_amount).to.be.above(0));"]),
 req('Sinh viên xem chi tiết hóa đơn','GET','/bills/{{billId}}','student'),
 req('Nhân viên xác nhận thanh toán','POST','/bills/{{billId}}/confirm-payment','staff',{'method':'Cash','reference':'PM-{{runTag}}'},200,["const b=pm.response.json(); pm.test('Hóa đơn đã thanh toán',()=>pm.expect(b.status).to.eql('Paid')); pm.test('Còn nợ bằng 0',()=>pm.expect(b.balance).to.eql(0));"]),
]}]
# Fix health URL explicitly because BASE prefix is /api/v1.
items[0]['item'][0]['request']['url']='{{baseUrl}}/gateway/healthz'
collection={'info':{'name':'Dormitory - Luồng E2E chạy một lần','description':'Chạy toàn bộ collection bằng Collection Runner theo đúng thứ tự. Cần bật Docker Compose và seed dữ liệu mặc định. Mỗi lần chạy tạo sinh viên, tòa nhà, phòng và mã hóa đơn mới. Biểu giá đang hiệu lực được tái sử dụng nếu có.','schema':'https://schema.getpostman.com/json/collection/v2.1.0/collection.json'},'variable':[{'key':'baseUrl','value':'http://localhost:8081'}],'item':items}
out=Path(__file__).resolve().parents[1]/'postman'/'Dormitory_MVP.postman_collection.json'
out.write_text(json.dumps(collection,ensure_ascii=False,indent=2),encoding='utf-8')
print(out)

