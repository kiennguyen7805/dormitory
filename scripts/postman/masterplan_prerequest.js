// Shared setup: every Send creates a fresh, independent scenario.
const spec = scenarios[pm.info.requestName];
if (!spec) throw new Error('Missing scenario: '+pm.info.requestName);
const cv=pm.collectionVariables, v=pm.variables;
const set=(k,x)=>{cv.set(k,x);v.set(k,x);return x;};
['baseUrl','adminEmail','adminPassword','staffEmail','staffPassword','studentPassword'].forEach(k=>v.set(k,cv.get(k)));
const base=String(v.get('baseUrl')).replace(/\/+$/,'');
v.set('baseUrl',base);
const uid=()=>v.replaceIn('{{$randomUUID}}').replace(/-/g,'');
const tag=uid().slice(0,16);
const day=n=>{const d=new Date();d.setUTCDate(d.getUTCDate()+n);return d.toISOString().slice(0,10);};
set('runTag',tag);set('today',day(0));set('contractEnd',day(90));set('dueDate',day(15));
set('buildingCode','P'+tag);set('termCode','PM-'+tag);set('billKey','pm-'+tag);
set('studentEmail','pm.'+tag+'@example.com');set('studentCode',uid().slice(0,8).toUpperCase());
const tokens={};
const sleep=ms=>new Promise(resolve=>setTimeout(resolve,ms));
async function call(method,path,role,body,expected=200){
  const header={'Content-Type':'application/json'};
  if(role) header.Authorization='Bearer '+tokens[role];
  const request={url:base+'/api/v1'+path,method,header};
  if(body!==undefined) request.body={mode:'raw',raw:JSON.stringify(body)};
  let r;
  for(let i=0;i<3;i++){r=await new Promise((resolve,reject)=>pm.sendRequest(request,(err,response)=>err?reject(err):resolve(response)));if(r.code!==429)break;await sleep(1200);}
  if(r.code!==expected)throw new Error('Setup '+method+' '+path+': expected '+expected+', received '+r.code+': '+r.text());
  console.log('Setup:',method,path,r.code);
  return r.json();
}
async function login(role){
  if(tokens[role])return;
  const email=v.get(role+'Email'),password=v.get(role+'Password')||v.get('studentPassword');
  const key='_auth_'+role,signature=base+'|'+email+'|'+password;
  let cache;try{cache=JSON.parse(cv.get(key)||'null');}catch(_){}
  if(['admin','staff'].includes(role)&&cache&&cache.signature===signature&&cache.expires>Date.now()+30000){
    tokens[role]=cache.token;return;
  }
  const b=await call('POST','/auth/login',null,{email,password});
  tokens[role]=b.access_token;set(role+'Token',b.access_token);set(role+'RefreshToken',b.refresh_token);
  if(['admin','staff'].includes(role))cv.set(key,JSON.stringify({signature,token:b.access_token,expires:Date.now()+Number(b.expires_in)*1000}));
}
async function student(role='student'){
  if(tokens[role])return;
  if(role!=='student'){set(role+'Email','pm.'+role+'.'+uid().slice(0,16)+'@example.com');set(role+'Code',uid().slice(0,8).toUpperCase());}
  const b=await call('POST','/auth/register',null,{email:v.get(role+'Email'),password:v.get('studentPassword'),full_name:'Postman '+role+' '+tag,student_code:v.get(role==='student'?'studentCode':role+'Code'),age:20},201);
  set(role+'Id',b.id);await login(role);
}
let buildingReady=false,roomReady=false,metersReady=false;
async function building(){
  if(buildingReady)return;
  await login('admin');
  const b=await call('POST','/buildings','admin',{code:v.get('buildingCode'),name:'Postman '+tag,address:'Demo',floors:2},201);
  set('buildingId',b.id);buildingReady=true;
}
async function room(){
  if(roomReady)return;
  await building();await login('staff');
  const b=await call('POST','/rooms','staff',{building_id:v.get('buildingId'),code:'101',floor:1,capacity:2,monthly_rate:500000},201);
  set('roomId',b.id);roomReady=true;
}
async function application(role='student',approve=false,assign=false){
  await room();await student(role);
  const a=await call('POST','/housing-applications',role,{term_code:v.get('termCode'),room_id:v.get('roomId')},201);
  set('applicationId',a.id);
  if(approve||assign)await call('POST','/housing-applications/'+a.id+'/approve','staff');
  if(assign){const c=await call('POST','/contracts/'+a.id+'/assign-room','staff',{start_date:v.get('today'),end_date:v.get('contractEnd')},201);set('contractId',c.id);}
}
async function utilities(){
  await login('staff');
  const rows=await call('GET','/utilities','staff');
  for(const k of ['electricity','water']){const u=rows.find(x=>x.code===k.toUpperCase());if(!u)throw new Error('Missing seeded utility '+k);set(k+'Id',u.id);}
}
async function tariffSlot(k){
  const rows=await call('GET','/utility-tariffs?utility_id='+v.get(k+'Id'),'staff');
  const d=new Date((rows.map(x=>x.effective_from).sort()[0]||v.get('today'))+'T00:00:00Z');
  d.setUTCDate(d.getUTCDate()-1);return d.toISOString().slice(0,10);
}
async function meters(){
  if(metersReady)return;
  await room();await utilities();
  const rows=await call('GET','/meters?room_id='+v.get('roomId'),'staff');
  for(const [k,price]of [['electricity',1000],['water',15000]]){
    const m=rows.find(x=>x.utility_code===k.toUpperCase());if(!m)throw new Error('Missing automatic meter '+k);set(k+'MeterId',m.id);
    const tariffs=await call('GET','/utility-tariffs?utility_id='+v.get(k+'Id'),'staff'),today=v.get('today');
    let t=tariffs.find(x=>x.is_active&&x.effective_from<=today&&(!x.effective_to||x.effective_to>=today));
    if(!t)t=await call('POST','/utility-tariffs','staff',{utility_id:v.get(k+'Id'),name:'PM '+k+' '+tag,effective_from:today,effective_to:today,calculation_type:'Flat',tiers:[{tier_order:1,from_quantity:0,to_quantity:null,unit_price:price}]},201);
    set(k+'TariffId',t.id);
  }
  metersReady=true;
}
async function readings(water=true){
  await meters();
  for(const [k,amount]of [['electricity',80],...(water?[['water',10]]:[])]){
    const b=await call('POST','/meter-readings','staff',{meter_id:v.get(k+'MeterId'),period_start:v.get('today'),period_end:v.get('today'),previous_reading:0,current_reading:amount},201);
    set(k+'ReadingId',b.id);set(k+'Amount',b.calculated_amount);
  }
}
async function bill(shared=false,paid=false){
  await application('student',true,true);
  if(shared)await application('student2',true,true);
  await readings();
  const b=await call('POST','/bills/generate','staff',{room_id:v.get('roomId'),period_start:v.get('today'),period_end:v.get('today'),issued_date:v.get('today'),due_date:v.get('dueDate'),idempotency_key:v.get('billKey')},201);
  set('billId',b.id);
  if(shared){const rows=await call('GET','/bills?room_id='+v.get('roomId'),'student');set('firstStudentBillIds',JSON.stringify(rows.map(x=>x.id)));}
  if(paid)await call('POST','/bills/'+b.id+'/confirm-payment','staff',{method:'Cash',reference:'PM-'+tag});
}
try{
  switch(spec.setup){
    case 'none':break;
    case 'student':await student();break;
    case 'refresh':await student();set('refresh_token',v.get('studentRefreshToken'));break;
    case 'managed-user':{
      await login('admin');const b=await call('POST','/users','admin',{email:'managed.'+tag+'@example.com',full_name:'PM Staff',password:'Staff@123',role:'Staff'},201);set('managedUserId',b.id);break;
    }
    case 'building':await building();break;
    case 'room':await room();break;
    case 'application':await application();break;
    case 'approved':await application('student',true);break;
    case 'contract':await application('student',true,true);break;
    case 'tariff-slot':await utilities();set('tariffDate',await tariffSlot(spec.kind));break;
    case 'meters':await meters();break;
    case 'electricity-reading':await readings(false);break;
    case 'readings':await readings();break;
    case 'bill':await bill();break;
    case 'paid':await bill(false,true);break;
    case 'shared-bill':await bill(true);break;
    case 'shared-paid':await bill(true,true);break;
    case 'full-room':await application('student',true,true);await application('student2',true,true);await application('student3',true);break;
    default:throw new Error('Unknown setup '+spec.setup);
  }
  if(spec.role){
    if(['student','student2','outsider'].includes(spec.role))await student(spec.role);else await login(spec.role);
    set('access_token',tokens[spec.role]);
  }
}catch(error){
  pm.test('Setup prerequisites succeeded',()=>{throw error;});
  console.error(error.message);
  pm.execution.skipRequest();
  throw error;
}

