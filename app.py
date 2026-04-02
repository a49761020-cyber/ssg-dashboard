from flask import Flask, request, jsonify, render_template_string
import requests
import json

app = Flask(__name__)

HTML = '''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SSG 대시보드</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box;margin:0;padding:0}
:root{--bg:#f5f6f8;--card:#fff;--border:#e2e5ea;--text:#1a1d23;--muted:#6b7280;--blue:#185FA5;--blue-light:#E6F1FB;--blue-dark:#0C447C;--green:#3B6D11;--green-light:#EAF3DE;--amber:#854F0B;--amber-light:#FAEEDA;--red:#A32D2D;--red-light:#FCEBEB;--radius:10px;--radius-sm:6px}
body{font-family:"Noto Sans KR",sans-serif;background:var(--bg);color:var(--text);min-height:100vh}
.header{background:var(--card);border-bottom:1px solid var(--border);padding:0 2rem;display:flex;align-items:center;justify-content:space-between;height:56px;position:sticky;top:0;z-index:100}
.logo{font-size:17px;font-weight:700}.logo span{color:var(--blue)}
.conn-badge{display:flex;align-items:center;gap:6px;font-size:12px;padding:4px 10px;border-radius:20px;border:1px solid var(--border);background:var(--bg)}
.conn-dot{width:7px;height:7px;border-radius:50%;background:#9ca3af}.conn-dot.on{background:#639922}
.clock{font-size:12px;color:var(--muted)}
.layout{display:flex;min-height:calc(100vh - 56px)}
.sidebar{width:200px;background:var(--card);border-right:1px solid var(--border);padding:1.5rem 0;flex-shrink:0}
.sidebar-section{padding:0 1rem;margin-bottom:1.5rem}
.sidebar-label{font-size:10px;font-weight:700;color:var(--muted);letter-spacing:.08em;text-transform:uppercase;padding:0 .75rem;margin-bottom:6px}
.nav-item{display:flex;align-items:center;gap:10px;padding:8px 12px;border-radius:var(--radius-sm);cursor:pointer;font-size:14px;color:var(--muted);transition:all .15s;margin-bottom:2px}
.nav-item:hover{background:var(--bg);color:var(--text)}
.nav-item.active{background:var(--blue-light);color:var(--blue);font-weight:500}
.main{flex:1;padding:2rem;overflow-y:auto}
.page{display:none}.page.active{display:block}
.page-title{font-size:20px;font-weight:700;margin-bottom:1.5rem;letter-spacing:-.3px}
.card{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:1.5rem;margin-bottom:1rem}
.card-title{font-size:11px;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;margin-bottom:1rem}
.field{margin-bottom:12px}
.field label{display:block;font-size:13px;font-weight:500;color:var(--muted);margin-bottom:5px}
.field input,.field select,.field textarea{width:100%;font-size:14px;font-family:"Noto Sans KR",sans-serif;border:1px solid var(--border);border-radius:var(--radius-sm);padding:9px 12px;background:#fff;color:var(--text);outline:none;transition:border .15s,box-shadow .15s}
.field input:focus,.field select:focus,.field textarea:focus{border-color:var(--blue);box-shadow:0 0 0 3px rgba(24,95,165,.1)}
.field textarea{resize:vertical;min-height:80px;line-height:1.5}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.grid3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px}
.required{color:var(--red)}
.btn-row{display:flex;gap:8px;justify-content:flex-end;align-items:center;margin-top:14px}
.btn{padding:9px 20px;font-size:14px;font-family:"Noto Sans KR",sans-serif;font-weight:500;border-radius:var(--radius-sm);cursor:pointer;border:1px solid var(--border);background:#fff;color:var(--text);transition:all .15s}
.btn:hover{background:var(--bg)}.btn:disabled{opacity:.4;cursor:not-allowed}
.btn.primary{background:var(--blue);color:#fff;border-color:var(--blue)}.btn.primary:hover:not(:disabled){background:var(--blue-dark)}
.badge{padding:3px 8px;border-radius:20px;font-size:11px;font-weight:500}
.badge.ok{background:var(--green-light);color:var(--green)}.badge.err{background:var(--red-light);color:var(--red)}.badge.info{background:var(--blue-light);color:var(--blue)}
.log-wrap{max-height:320px;overflow-y:auto}
.log-item{display:flex;align-items:flex-start;gap:8px;padding:10px 0;border-bottom:1px solid var(--border);font-size:13px}
.log-item:last-child{border-bottom:none}
.log-msg{flex:1;color:var(--text);word-break:break-all;line-height:1.5}
.log-time{color:var(--muted);font-size:11px;white-space:nowrap;margin-top:1px}
.empty{text-align:center;padding:2.5rem;color:var(--muted);font-size:14px}
.result-box{background:#f8f9fb;border:1px solid var(--border);border-radius:var(--radius-sm);padding:12px;font-size:12px;font-family:monospace;color:var(--muted);max-height:180px;overflow-y:auto;margin-top:10px;word-break:break-all;line-height:1.6;display:none;white-space:pre-wrap}
.info-box{background:var(--blue-light);border:1px solid #B5D4F4;border-radius:var(--radius-sm);padding:12px 14px;font-size:13px;color:#0C447C;line-height:1.6;margin-bottom:14px}
.info-box strong{font-weight:700}
.spinner{width:16px;height:16px;border:2px solid var(--border);border-top-color:var(--blue);border-radius:50%;animation:spin .7s linear infinite;display:none;flex-shrink:0}
@keyframes spin{to{transform:rotate(360deg)}}
.status-text{font-size:13px}.status-text.ok{color:var(--green)}.status-text.err{color:var(--red)}
.api-key-wrap{display:flex;gap:8px}.api-key-wrap input{flex:1}
.conn-row{display:flex;align-items:center;gap:10px;padding:12px 0;font-size:14px}
.conn-status-dot{width:10px;height:10px;border-radius:50%;background:#9ca3af;flex-shrink:0}.conn-status-dot.on{background:#639922}
.stat-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-bottom:1rem}
.stat-card{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:1.25rem}
.stat-label{font-size:12px;color:var(--muted);margin-bottom:6px}
.stat-val{font-size:26px;font-weight:700;letter-spacing:-.5px}
.stat-val.blue{color:var(--blue)}.stat-val.green{color:var(--green)}.stat-val.amber{color:var(--amber)}
.divider{height:1px;background:var(--border);margin:1rem 0}
.section-row{display:flex;align-items:center;justify-content:space-between;margin-bottom:1rem}
.section-row h3{font-size:15px;font-weight:700}
</style>
</head>
<body>
<div class="header">
  <div class="logo">SSG <span>파트너 대시보드</span></div>
  <div style="display:flex;align-items:center;gap:16px">
    <div class="conn-badge"><div class="conn-dot" id="header-dot"></div><span id="header-conn">미연결</span></div>
    <div class="clock" id="clock"></div>
  </div>
</div>
<div class="layout">
  <div class="sidebar">
    <div class="sidebar-section">
      <div class="sidebar-label">메뉴</div>
      <div class="nav-item active" onclick="showPage('overview')">📊 개요</div>
      <div class="nav-item" onclick="showPage('register')">➕ 상품 등록</div>
      <div class="nav-item" onclick="showPage('price')">💰 가격 수정</div>
      <div class="nav-item" onclick="showPage('log')">📋 작업 로그</div>
    </div>
    <div class="sidebar-section">
      <div class="sidebar-label">설정</div>
      <div class="nav-item" onclick="showPage('settings')">⚙️ API 설정</div>
    </div>
  </div>
  <div class="main">

    <!-- 개요 -->
    <div class="page active" id="page-overview">
      <div class="page-title">개요</div>
      <div class="stat-grid">
        <div class="stat-card"><div class="stat-label">오늘 등록한 상품</div><div class="stat-val blue" id="cnt-reg">0</div></div>
        <div class="stat-card"><div class="stat-label">오늘 가격 수정</div><div class="stat-val green" id="cnt-price">0</div></div>
        <div class="stat-card"><div class="stat-label">오류 건수</div><div class="stat-val amber" id="cnt-err">0</div></div>
      </div>
      <div class="card">
        <div class="section-row"><h3>최근 작업</h3></div>
        <div class="log-wrap" id="overview-log"><div class="empty">아직 작업 내역이 없습니다</div></div>
      </div>
    </div>

    <!-- 상품 등록 -->
    <div class="page" id="page-register">
      <div class="page-title">상품 등록</div>
      <div class="info-box"><strong>POST</strong> https://eapi.ssgadm.com/item/0.1/온라인<br>서버를 통해 SSG에 직접 요청합니다.</div>
      <div class="card">
        <div class="card-title">기본 정보</div>
        <div class="field"><label>상품명 (itemNm) <span class="required">*</span></label><input type="text" id="r-name" placeholder="예: 삼성 BESPOKE 냉장고 4도어"></div>
        <div class="grid2">
          <div class="field"><label>브랜드명</label><input type="text" id="r-brand" placeholder="예: 삼성"></div>
          <div class="field"><label>모델번호</label><input type="text" id="r-model" placeholder="예: RF85B91B1AP"></div>
        </div>
        <div class="grid2">
          <div class="field"><label>판매유형</label><select id="r-selltype"><option value="10">10 — 일반</option><option value="20">20 — 옵션</option></select></div>
          <div class="field"><label>재고 수량</label><input type="number" id="r-stock" placeholder="10" min="0"></div>
        </div>
      </div>
      <div class="card">
        <div class="card-title">가격 정보</div>
        <div class="grid2">
          <div class="field"><label>공급가 (splprc) <span class="required">*</span></label><input type="number" id="r-splprc" placeholder="1500000"></div>
          <div class="field"><label>판매가 (셀프른) <span class="required">*</span></label><input type="number" id="r-sellprc" placeholder="1990000"></div>
        </div>
        <div class="grid2">
          <div class="field"><label>마진율</label><input type="number" id="r-margin" placeholder="25.5" step="0.1"></div>
          <div class="field"><label>가격책정방식</label><select id="r-prctype"><option value="1">1 — 공급가 자동계산</option><option value="2">2 — 판매가 자동계산</option><option value="3">3 — 마진 자동계산</option></select></div>
        </div>
      </div>
      <div class="card">
        <div class="card-title">상품 설명</div>
        <div class="field"><label>상세설명</label><textarea id="r-desc" placeholder="상품 상세 설명을 입력하세요"></textarea></div>
      </div>
      <div class="btn-row">
        <div class="spinner" id="reg-spinner"></div>
        <span class="status-text" id="reg-status"></span>
        <button class="btn" onclick="resetRegister()">초기화</button>
        <button class="btn primary" id="reg-btn" onclick="doRegister()">SSG 등록 요청</button>
      </div>
      <div class="result-box" id="reg-result"></div>
    </div>

    <!-- 가격 수정 -->
    <div class="page" id="page-price">
      <div class="page-title">가격 수정</div>
      <div class="info-box"><strong>PUT</strong> https://eapi.ssgadm.com/item/0.1/online/{itemId}/가격<br>아이템ID는 상품 등록 후 SSG에서 발급되는 고유 번호입니다.</div>
      <div class="card">
        <div class="card-title">수정 정보</div>
        <div class="field"><label>아이템ID <span class="required">*</span></label><input type="text" id="p-itemid" placeholder="상품 등록 후 발급된 itemId 입력"></div>
        <div class="grid2">
          <div class="field"><label>공급가 (splprc) <span class="required">*</span></label><input type="number" id="p-splprc" placeholder="1500000"></div>
          <div class="field"><label>판매가 (셀프른) <span class="required">*</span></label><input type="number" id="p-sellprc" placeholder="1890000"></div>
        </div>
        <div class="grid2">
          <div class="field"><label>마진율</label><input type="number" id="p-margin" placeholder="25.5" step="0.1"></div>
          <div class="field"><label>가격책정방식</label><select id="p-prctype"><option value="1">1 — 공급가 자동계산</option><option value="2">2 — 판매가 자동계산</option><option value="3">3 — 마진 자동계산</option></select></div>
        </div>
        <div class="field"><label>적용 시작일 (선택)</label><input type="datetime-local" id="p-startdt"></div>
      </div>
      <div class="btn-row">
        <div class="spinner" id="price-spinner"></div>
        <span class="status-text" id="price-status"></span>
        <button class="btn" onclick="resetPrice()">초기화</button>
        <button class="btn primary" id="price-btn" onclick="doPrice()">SSG 가격 수정</button>
      </div>
      <div class="result-box" id="price-result"></div>
    </div>

    <!-- 로그 -->
    <div class="page" id="page-log">
      <div class="page-title">작업 로그</div>
      <div class="card">
        <div class="section-row"><h3>전체 내역</h3><button class="btn" onclick="clearLog()">로그 지우기</button></div>
        <div class="log-wrap" id="full-log"><div class="empty">작업 내역이 없습니다</div></div>
      </div>
    </div>

    <!-- API 설정 -->
    <div class="page" id="page-settings">
      <div class="page-title">API 설정</div>
      <div class="card">
        <div class="card-title">SSG EAPI 인증</div>
        <div class="field"><label>API 인증키</label>
          <div class="api-key-wrap">
            <input type="password" id="api-key" placeholder="예: 0123fb69-xxxx-xxxx-xxxx-xxxxxxxxxxxx">
            <button class="btn" onclick="toggleKey()">보기</button>
          </div>
        </div>
        <div class="field"><label>응답 형식</label><select id="api-accept"><option value="application/json">application/json (권장)</option><option value="application/xml">application/xml</option></select></div>
        <div class="btn-row">
          <span style="font-size:13px;color:var(--green);display:none" id="save-msg">저장되었습니다</span>
          <button class="btn primary" onclick="saveSettings()">저장</button>
        </div>
      </div>
      <div class="card">
        <div class="card-title">연결 상태</div>
        <div class="conn-row"><div class="conn-status-dot" id="conn-dot"></div><span id="conn-text">API 키를 입력하고 저장해주세요</span></div>
        <div class="divider"></div>
        <div style="font-size:13px;color:var(--muted);line-height:1.8">
          <div>기본 URL: <strong style="color:var(--text)">https://eapi.ssgadm.com</strong></div>
          <div>상품 등록: <strong style="color:var(--text)">POST /item/0.1/온라인</strong></div>
          <div>가격 수정: <strong style="color:var(--text)">PUT /item/0.1/online/{itemId}/가격</strong></div>
        </div>
      </div>
    </div>

  </div>
</div>

<script>
const S={apiKey:'',accept:'application/json',logs:[],cntReg:0,cntPrice:0,cntErr:0};

function showPage(p){
  document.querySelectorAll('.page').forEach(e=>e.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(e=>e.classList.remove('active'));
  document.getElementById('page-'+p).classList.add('active');
  ['overview','register','price','log','settings'].forEach((n,i)=>{if(n===p)document.querySelectorAll('.nav-item')[i].classList.add('active')});
}

function ts(){return new Date().toLocaleTimeString('ko-KR',{hour:'2-digit',minute:'2-digit',second:'2-digit'})}

function addLog(type,msg){
  S.logs.unshift({type,msg,time:ts()});
  if(type==='성공'&&msg.includes('등록'))S.cntReg++;
  if(type==='성공'&&msg.includes('가격'))S.cntPrice++;
  if(type==='오류')S.cntErr++;
  document.getElementById('cnt-reg').textContent=S.cntReg;
  document.getElementById('cnt-price').textContent=S.cntPrice;
  document.getElementById('cnt-err').textContent=S.cntErr;
  renderLog();
}

function renderLog(){
  const typeMap={성공:'ok',오류:'err',요청:'info'};
  const html=S.logs.map(l=>`<div class="log-item"><span class="badge ${typeMap[l.type]||'info'}">${l.type}</span><span class="log-msg">${l.msg}</span><span class="log-time">${l.time}</span></div>`).join('');
  document.getElementById('full-log').innerHTML=html||'<div class="empty">작업 내역이 없습니다</div>';
  document.getElementById('overview-log').innerHTML=(S.logs.slice(0,5).map(l=>`<div class="log-item"><span class="badge ${typeMap[l.type]||'info'}">${l.type}</span><span class="log-msg">${l.msg}</span><span class="log-time">${l.time}</span></div>`).join(''))||'<div class="empty">아직 작업 내역이 없습니다</div>';
}

function clearLog(){S.logs=[];S.cntReg=0;S.cntPrice=0;S.cntErr=0;['cnt-reg','cnt-price','cnt-err'].forEach(id=>document.getElementById(id).textContent='0');renderLog()}

function setLoading(p,on){document.getElementById(p+'-spinner').style.display=on?'block':'none';document.getElementById(p+'-btn').disabled=on}

function showResult(p,text,ok){
  const el=document.getElementById(p+'-result');el.textContent=text;el.style.display='block';
  const st=document.getElementById(p+'-status');st.textContent=ok?'성공!':'오류 발생';st.className='status-text '+(ok?'ok':'err');
}

async function doRegister(){
  if(!S.apiKey){alert('API 설정에서 인증키를 먼저 저장해주세요.');showPage('settings');return}
  const name=document.getElementById('r-name').value.trim();
  const sellprc=document.getElementById('r-sellprc').value;
  const splprc=document.getElementById('r-splprc').value;
  if(!name||!sellprc||!splprc){alert('상품명, 공급가, 판매가는 필수입니다.');return}
  setLoading('reg',true);addLog('요청',`상품 등록 요청 — ${name}`);
  const body={name,brand:document.getElementById('r-brand').value,model:document.getElementById('r-model').value,sellType:document.getElementById('r-selltype').value,stock:document.getElementById('r-stock').value,splprc:Number(splprc),sellprc:Number(sellprc),margin:document.getElementById('r-margin').value,prcType:document.getElementById('r-prctype').value,desc:document.getElementById('r-desc').value,apiKey:S.apiKey,accept:S.accept};
  try{
    const res=await fetch('/api/register',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
    const data=await res.json();
    const ok=data.success;
    addLog(ok?'성공':'오류',ok?`상품 등록 완료 — ${name}${data.itemId?' (itemId: '+data.itemId+')':''}`:`등록 실패: ${data.message}`);
    showResult('reg',JSON.stringify(data.raw||data,null,2),ok);
  }catch(e){addLog('오류','오류: '+e.message);showResult('reg',e.message,false)}
  setLoading('reg',false);
}

async function doPrice(){
  if(!S.apiKey){alert('API 설정에서 인증키를 먼저 저장해주세요.');showPage('settings');return}
  const itemId=document.getElementById('p-itemid').value.trim();
  const sellprc=document.getElementById('p-sellprc').value;
  const splprc=document.getElementById('p-splprc').value;
  if(!itemId||!sellprc||!splprc){alert('아이템ID, 공급가, 판매가는 필수입니다.');return}
  setLoading('price',true);addLog('요청',`가격 수정 요청 — itemId: ${itemId}`);
  const startDt=document.getElementById('p-startdt').value;
  const body={itemId,splprc:Number(splprc),sellprc:Number(sellprc),margin:document.getElementById('p-margin').value,prcType:document.getElementById('p-prctype').value,startDt,apiKey:S.apiKey,accept:S.accept};
  try{
    const res=await fetch('/api/price',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
    const data=await res.json();
    const ok=data.success;
    addLog(ok?'성공':'오류',ok?`가격 수정 완료 — itemId: ${itemId}, 판매가: ${Number(sellprc).toLocaleString()}원`:`가격 수정 실패: ${data.message}`);
    showResult('price',JSON.stringify(data.raw||data,null,2),ok);
  }catch(e){addLog('오류','오류: '+e.message);showResult('price',e.message,false)}
  setLoading('price',false);
}

function resetRegister(){['r-name','r-brand','r-model','r-stock','r-splprc','r-sellprc','r-margin','r-desc'].forEach(id=>{const el=document.getElementById(id);if(el)el.value=''});document.getElementById('reg-result').style.display='none';document.getElementById('reg-status').textContent=''}
function resetPrice(){['p-itemid','p-splprc','p-sellprc','p-margin','p-startdt'].forEach(id=>{const el=document.getElementById(id);if(el)el.value=''});document.getElementById('price-result').style.display='none';document.getElementById('price-status').textContent=''}
function toggleKey(){const el=document.getElementById('api-key');el.type=el.type==='password'?'text':'password'}

function saveSettings(){
  S.apiKey=document.getElementById('api-key').value.trim();
  S.accept=document.getElementById('api-accept').value;
  const on=!!S.apiKey;
  document.getElementById('conn-dot').className='conn-status-dot'+(on?' on':'');
  document.getElementById('conn-text').textContent=on?'API 키 설정 완료 — 요청 준비됨':'API 키를 입력하고 저장해주세요';
  document.getElementById('header-dot').className='conn-dot'+(on?' on':'');
  document.getElementById('header-conn').textContent=on?'연결됨':'미연결';
  const msg=document.getElementById('save-msg');msg.style.display='inline';setTimeout(()=>msg.style.display='none',2000);
}

setInterval(()=>{document.getElementById('clock').textContent=new Date().toLocaleString('ko-KR',{month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit'})},1000);
</script>
</body>
</html>'''

BASE_URL = 'https://eapi.ssgadm.com'

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    api_key = data.get('apiKey')
    accept = data.get('accept', 'application/json')

    body = {
        '온라인등록': {
            '아이템베이스': {
                'itemNm': data.get('name'),
                'brandNm': data.get('brand') or None,
                'mdlNm': data.get('model') or None,
                'itemSellTypeCd': data.get('sellType', '10'),
            },
            '가격': {
                '가격': {
                    'prcMngMthdCd': data.get('prcType', '1'),
                    '품목가격': {
                        'splprc': data.get('splprc'),
                        '셀프른': data.get('sellprc'),
                        'mrgrt': float(data['margin']) if data.get('margin') else None,
                    }
                }
            },
            '설명': {
                'itemDtlDesc': data.get('desc') or None,
            }
        }
    }

    try:
        res = requests.post(
            f'{BASE_URL}/item/0.1/온라인',
            headers={'Authorization': api_key, 'Accept': accept, 'Content-Type': 'application/json'},
            json=body,
            timeout=10
        )
        result = res.json()
        code = result.get('결과', {}).get('결과코드') or result.get('result', {}).get('resultCode')
        item_id = result.get('항목ID') or result.get('itemId', '')
        success = code == '00' or res.status_code == 200
        return jsonify({'success': success, 'itemId': item_id, 'message': str(result), 'raw': result})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/price', methods=['POST'])
def price():
    data = request.json
    api_key = data.get('apiKey')
    accept = data.get('accept', 'application/json')
    item_id = data.get('itemId')

    start_dt = data.get('startDt', '')
    if start_dt:
        start_dt = start_dt.replace('T', ' ').replace(':', '')[:14]

    body = {
        '가격': {
            'prcMngMthdCd': data.get('prcType', '1'),
            '품목가격': {
                'splprc': data.get('splprc'),
                '셀프른': data.get('sellprc'),
                'mrgrt': float(data['margin']) if data.get('margin') else None,
            },
            'aplStrtDt': start_dt or None,
        }
    }

    try:
        res = requests.put(
            f'{BASE_URL}/item/0.1/online/{item_id}/가격',
            headers={'Authorization': api_key, 'Accept': accept, 'Content-Type': 'application/json'},
            json=body,
            timeout=10
        )
        result = res.json()
        code = result.get('결과', {}).get('결과코드') or result.get('result', {}).get('resultCode')
        success = code == '00' or res.status_code == 200
        return jsonify({'success': success, 'message': str(result), 'raw': result})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

if __name__ == '__main__':
    print('=' * 50)
    print('  SSG 대시보드 서버 시작!')
    print('  브라우저에서 http://localhost:5000 접속하세요')
    print('=' * 50)
    import os
app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT',8080)))
