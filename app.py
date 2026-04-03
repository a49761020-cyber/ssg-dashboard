import os
from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

BASE_URL = 'https://eapi.ssgadm.com'
CJ_API_URL = 'https://display.cjonstyle.com/c/rest/item/{}/buyInfo.json'

HTML = '''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>SSG 대시보드</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box;margin:0;padding:0}
:root{--bg:#f5f6f8;--card:#fff;--border:#e2e5ea;--text:#1a1d23;--muted:#6b7280;--blue:#185FA5;--blue-light:#E6F1FB;--blue-dark:#0C447C;--green:#3B6D11;--green-light:#EAF3DE;--red:#A32D2D;--red-light:#FCEBEB;--orange:#854F0B;--orange-light:#FEF3E2;--radius:10px;--radius-sm:6px}
body{font-family:"Noto Sans KR",sans-serif;background:var(--bg);color:var(--text);min-height:100vh}
.header{background:var(--card);border-bottom:1px solid var(--border);padding:0 2rem;display:flex;align-items:center;justify-content:space-between;height:56px;position:sticky;top:0;z-index:100}
.logo{font-size:17px;font-weight:700}.logo span{color:var(--blue)}
.layout{display:flex;min-height:calc(100vh - 56px)}
.sidebar{width:200px;background:var(--card);border-right:1px solid var(--border);padding:1.5rem 0;flex-shrink:0}
.sidebar-section{padding:0 1rem;margin-bottom:1.5rem}
.sidebar-label{font-size:10px;font-weight:700;color:var(--muted);letter-spacing:.08em;text-transform:uppercase;padding:0 .75rem;margin-bottom:6px}
.nav-item{display:flex;align-items:center;gap:10px;padding:8px 12px;border-radius:var(--radius-sm);cursor:pointer;font-size:14px;color:var(--muted);transition:all .15s;margin-bottom:2px}
.nav-item:hover{background:var(--bg);color:var(--text)}
.nav-item.active{background:var(--blue-light);color:var(--blue);font-weight:500}
.nav-item.cj-active{background:var(--orange-light);color:var(--orange);font-weight:500}
.nav-badge{margin-left:auto;background:var(--red);color:#fff;font-size:9px;font-weight:700;padding:1px 5px;border-radius:10px}
.main{flex:1;padding:2rem;overflow-y:auto}
.page{display:none}.page.active{display:block}
.page-title{font-size:20px;font-weight:700;margin-bottom:1.5rem}
.card{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:1.5rem;margin-bottom:1rem}
.card-title{font-size:11px;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;margin-bottom:1rem}
.field{margin-bottom:12px}
.field label{display:block;font-size:13px;font-weight:500;color:var(--muted);margin-bottom:5px}
.field input,.field select,.field textarea{width:100%;font-size:14px;font-family:"Noto Sans KR",sans-serif;border:1px solid var(--border);border-radius:var(--radius-sm);padding:9px 12px;background:#fff;color:var(--text);outline:none;transition:border .15s}
.field input:focus,.field select:focus,.field textarea:focus{border-color:var(--blue)}
.field textarea{resize:vertical;min-height:80px}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.required{color:var(--red)}
.btn-row{display:flex;gap:8px;justify-content:flex-end;align-items:center;margin-top:14px}
.btn{padding:9px 20px;font-size:14px;font-family:"Noto Sans KR",sans-serif;font-weight:500;border-radius:var(--radius-sm);cursor:pointer;border:1px solid var(--border);background:#fff;color:var(--text);transition:all .15s}
.btn:hover{background:var(--bg)}.btn:disabled{opacity:.4;cursor:not-allowed}
.btn.primary{background:var(--blue);color:#fff;border-color:var(--blue)}.btn.primary:hover:not(:disabled){background:var(--blue-dark)}
.btn.cj{background:#E8192C;color:#fff;border-color:#E8192C}.btn.cj:hover:not(:disabled){background:#c8141f}
.btn.success{background:var(--green);color:#fff;border-color:var(--green)}
.badge{padding:3px 8px;border-radius:20px;font-size:11px;font-weight:500}
.badge.ok{background:var(--green-light);color:var(--green)}.badge.err{background:var(--red-light);color:var(--red)}.badge.info{background:var(--blue-light);color:var(--blue)}.badge.warn{background:var(--orange-light);color:var(--orange)}
.log-wrap{max-height:320px;overflow-y:auto}
.log-item{display:flex;align-items:flex-start;gap:8px;padding:10px 0;border-bottom:1px solid var(--border);font-size:13px}
.log-item:last-child{border-bottom:none}
.log-msg{flex:1;color:var(--text);word-break:break-all;line-height:1.5}
.log-time{color:var(--muted);font-size:11px;white-space:nowrap}
.empty{text-align:center;padding:2.5rem;color:var(--muted);font-size:14px}
.result-box{background:#f8f9fb;border:1px solid var(--border);border-radius:var(--radius-sm);padding:12px;font-size:12px;font-family:monospace;color:var(--muted);max-height:180px;overflow-y:auto;margin-top:10px;word-break:break-all;line-height:1.6;display:none;white-space:pre-wrap}
.info-box{background:var(--blue-light);border:1px solid #B5D4F4;border-radius:var(--radius-sm);padding:12px 14px;font-size:13px;color:#0C447C;line-height:1.6;margin-bottom:14px}
.spinner{width:16px;height:16px;border:2px solid var(--border);border-top-color:var(--blue);border-radius:50%;animation:spin .7s linear infinite;display:none;flex-shrink:0}
@keyframes spin{to{transform:rotate(360deg)}}
.status-text{font-size:13px}.status-text.ok{color:var(--green)}.status-text.err{color:var(--red)}
.api-key-wrap{display:flex;gap:8px}.api-key-wrap input{flex:1}
.conn-row{display:flex;align-items:center;gap:10px;padding:12px 0;font-size:14px}
.conn-status-dot{width:10px;height:10px;border-radius:50%;background:#9ca3af;flex-shrink:0}.conn-status-dot.on{background:#639922}
.stat-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-bottom:1rem}
.stat-card{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:1.25rem}
.stat-label{font-size:12px;color:var(--muted);margin-bottom:6px}
.stat-val{font-size:26px;font-weight:700}
.stat-val.blue{color:var(--blue)}.stat-val.green{color:var(--green)}
.divider{height:1px;background:var(--border);margin:1rem 0}
.section-row{display:flex;align-items:center;justify-content:space-between;margin-bottom:1rem}
.section-row h3{font-size:15px;font-weight:700}

/* CJ 스타일 */
.cj-header{display:flex;align-items:center;gap:10px;margin-bottom:1.5rem}
.cj-badge{background:#E8192C;color:#fff;font-weight:700;font-size:12px;padding:4px 10px;border-radius:4px}
.ssg-badge{background:var(--blue);color:#fff;font-weight:700;font-size:12px;padding:4px 10px;border-radius:4px}
.cj-arrow{font-size:18px;color:var(--muted)}
.cj-item-wrap{display:flex;flex-direction:column;gap:8px;margin-top:12px}
.cj-item{background:#f8f9fb;border:1px solid var(--border);border-radius:var(--radius-sm);padding:12px 14px;display:flex;align-items:center;gap:12px}
.cj-item-num{font-size:12px;font-weight:700;color:var(--blue);min-width:90px;font-family:monospace}
.cj-item-info{flex:1}
.cj-item-name{font-size:13px;font-weight:500;margin-bottom:2px}
.cj-item-meta{font-size:11px;color:var(--muted)}
.cj-item-price{text-align:right;min-width:90px}
.cj-item-price-val{font-size:13px;font-weight:700}
.cj-item-price-label{font-size:10px;color:var(--muted)}
.cj-item-status{font-size:11px;font-weight:600;padding:2px 8px;border-radius:10px;white-space:nowrap}
.cj-item-status.fetched{background:var(--blue-light);color:var(--blue)}
.cj-item-status.registered{background:var(--green-light);color:var(--green)}
.cj-item-status.error{background:var(--red-light);color:var(--red)}
.cj-item-status.pending{background:var(--orange-light);color:var(--orange)}
.cj-item-actions{display:flex;gap:6px}
.btn.sm{padding:5px 10px;font-size:12px}
.progress-wrap{background:var(--border);border-radius:4px;height:6px;margin-top:10px;overflow:hidden;display:none}
.progress-fill{height:100%;background:linear-gradient(90deg,var(--blue),#4f8ef7);border-radius:4px;transition:width .3s}
.input-row{display:flex;gap:8px;align-items:flex-end}
.input-row .field{flex:1;margin-bottom:0}
</style>
</head>
<body>
<div class="header">
  <div class="logo">SSG <span>파트너 대시보드</span></div>
  <div style="font-size:12px;color:var(--muted)" id="clock"></div>
</div>
<div class="layout">
  <div class="sidebar">
    <div class="sidebar-section">
      <div class="sidebar-label">메뉴</div>
      <div class="nav-item active" onclick="showPage('overview')">개요</div>
      <div class="nav-item" onclick="showPage('cj')" id="nav-cj">CJ 연동 <span class="nav-badge">NEW</span></div>
      <div class="nav-item" onclick="showPage('register')">상품 등록</div>
      <div class="nav-item" onclick="showPage('price')">가격 수정</div>
      <div class="nav-item" onclick="showPage('log')">작업 로그</div>
    </div>
    <div class="sidebar-section">
      <div class="sidebar-label">설정</div>
      <div class="nav-item" onclick="showPage('settings')">API 설정</div>
    </div>
  </div>
  <div class="main">

    <!-- 개요 -->
    <div class="page active" id="page-overview">
      <div class="page-title">개요</div>
      <div class="stat-grid">
        <div class="stat-card"><div class="stat-label">오늘 등록한 상품</div><div class="stat-val blue" id="cnt-reg">0</div></div>
        <div class="stat-card"><div class="stat-label">오늘 가격 수정</div><div class="stat-val green" id="cnt-price">0</div></div>
        <div class="stat-card"><div class="stat-label">오류 건수</div><div class="stat-val" style="color:#854F0B" id="cnt-err">0</div></div>
      </div>
      <div class="card">
        <div class="section-row"><h3>최근 작업</h3></div>
        <div class="log-wrap" id="overview-log"><div class="empty">아직 작업 내역이 없습니다</div></div>
      </div>
    </div>

    <!-- CJ 연동 -->
    <div class="page" id="page-cj">
      <div class="cj-header">
        <span class="cj-badge">CJ온스타일</span>
        <span class="cj-arrow">→</span>
        <span class="ssg-badge">SSG.COM</span>
        <span style="font-size:13px;color:var(--muted);margin-left:4px">상품 자동 조회 및 등록</span>
      </div>

      <div class="card">
        <div class="card-title">CJ 상품번호 입력</div>
        <div class="input-row">
          <div class="field">
            <label>상품번호 (쉼표 또는 줄바꿈으로 여러 개 입력)</label>
            <input type="text" id="cj-ids" placeholder="예: 100000001, 100000002">
          </div>
          <button class="btn cj" id="cj-fetch-btn" onclick="fetchCJItems()">조회</button>
        </div>
        <div class="progress-wrap" id="cj-progress">
          <div class="progress-fill" id="cj-progress-bar" style="width:0%"></div>
        </div>
        <div style="font-size:11px;color:var(--muted);margin-top:8px">
          API: https://display.cjonstyle.com/c/rest/item/{상품번호}/buyInfo.json
        </div>
      </div>

      <div id="cj-item-list" class="cj-item-wrap" style="display:none"></div>

      <div id="cj-bulk-actions" style="display:none">
        <div class="card" style="margin-top:0">
          <div class="btn-row" style="justify-content:flex-start;margin-top:0">
            <button class="btn cj" onclick="bulkRegister()">전체 SSG 등록</button>
            <button class="btn" onclick="clearCJItems()">목록 지우기</button>
            <span class="status-text" id="cj-bulk-status"></span>
          </div>
        </div>
      </div>
    </div>

    <!-- 상품 등록 -->
    <div class="page" id="page-register">
      <div class="page-title">상품 등록</div>
      <div class="info-box"><strong>POST</strong> https://eapi.ssgadm.com/item/0.1/온라인</div>
      <div class="card">
        <div class="card-title">기본 정보</div>
        <div class="field"><label>상품명 <span class="required">*</span></label><input type="text" id="r-name" placeholder="예: 삼성 BESPOKE 냉장고 4도어"></div>
        <div class="grid2">
          <div class="field"><label>브랜드명</label><input type="text" id="r-brand" placeholder="예: 삼성"></div>
          <div class="field"><label>모델번호</label><input type="text" id="r-model" placeholder="예: RF85B91B1AP"></div>
        </div>
        <div class="grid2">
          <div class="field"><label>판매유형</label><select id="r-selltype"><option value="10">10 일반</option><option value="20">20 옵션</option></select></div>
          <div class="field"><label>재고 수량</label><input type="number" id="r-stock" placeholder="10" min="0"></div>
        </div>
      </div>
      <div class="card">
        <div class="card-title">가격 정보</div>
        <div class="grid2">
          <div class="field"><label>공급가 <span class="required">*</span></label><input type="number" id="r-splprc" placeholder="1500000"></div>
          <div class="field"><label>판매가 <span class="required">*</span></label><input type="number" id="r-sellprc" placeholder="1990000"></div>
        </div>
        <div class="grid2">
          <div class="field"><label>마진율</label><input type="number" id="r-margin" placeholder="25.5" step="0.1"></div>
          <div class="field"><label>가격책정방식</label><select id="r-prctype"><option value="1">1 공급가 자동계산</option><option value="2">2 판매가 자동계산</option><option value="3">3 마진 자동계산</option></select></div>
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
      <div class="info-box"><strong>PUT</strong> https://eapi.ssgadm.com/item/0.1/online/{itemId}/가격</div>
      <div class="card">
        <div class="card-title">수정 정보</div>
        <div class="field"><label>아이템ID <span class="required">*</span></label><input type="text" id="p-itemid" placeholder="상품 등록 후 발급된 itemId"></div>
        <div class="grid2">
          <div class="field"><label>공급가 <span class="required">*</span></label><input type="number" id="p-splprc" placeholder="1500000"></div>
          <div class="field"><label>판매가 <span class="required">*</span></label><input type="number" id="p-sellprc" placeholder="1890000"></div>
        </div>
        <div class="grid2">
          <div class="field"><label>마진율</label><input type="number" id="p-margin" placeholder="25.5" step="0.1"></div>
          <div class="field"><label>가격책정방식</label><select id="p-prctype"><option value="1">1 공급가 자동계산</option><option value="2">2 판매가 자동계산</option><option value="3">3 마진 자동계산</option></select></div>
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

    <!-- 설정 -->
    <div class="page" id="page-settings">
      <div class="page-title">API 설정</div>
      <div class="card">
        <div class="card-title">SSG EAPI 인증</div>
        <div class="field"><label>API 인증키</label>
          <div class="api-key-wrap">
            <input type="password" id="api-key" placeholder="0123fb69-xxxx-xxxx-xxxx-xxxxxxxxxxxx">
            <button class="btn" onclick="toggleKey()">보기</button>
          </div>
        </div>
        <div class="field"><label>응답 형식</label><select id="api-accept"><option value="application/json">application/json</option><option value="application/xml">application/xml</option></select></div>
        <div class="btn-row">
          <span style="font-size:13px;color:var(--green);display:none" id="save-msg">저장되었습니다</span>
          <button class="btn primary" onclick="saveSettings()">저장</button>
        </div>
      </div>
      <div class="card">
        <div class="card-title">연결 상태</div>
        <div class="conn-row"><div class="conn-status-dot" id="conn-dot"></div><span id="conn-text">API 키를 입력하고 저장해주세요</span></div>
      </div>
    </div>

  </div>
</div>
<script>
const S={apiKey:"",accept:"application/json",logs:[],cntReg:0,cntPrice:0,cntErr:0};
let cjItems=[];

const PAGES=["overview","cj","register","price","log","settings"];
function showPage(p){
  document.querySelectorAll(".page").forEach(e=>e.classList.remove("active"));
  document.querySelectorAll(".nav-item").forEach(e=>e.classList.remove("active","cj-active"));
  document.getElementById("page-"+p).classList.add("active");
  PAGES.forEach((n,i)=>{
    if(n===p){
      const el=document.querySelectorAll(".nav-item")[i];
      el.classList.add(p==="cj"?"cj-active":"active");
    }
  });
}
function ts(){return new Date().toLocaleTimeString("ko-KR",{hour:"2-digit",minute:"2-digit",second:"2-digit"})}
function addLog(type,msg){S.logs.unshift({type,msg,time:ts()});if(type==="성공"&&msg.includes("등록"))S.cntReg++;if(type==="성공"&&msg.includes("가격"))S.cntPrice++;if(type==="오류")S.cntErr++;document.getElementById("cnt-reg").textContent=S.cntReg;document.getElementById("cnt-price").textContent=S.cntPrice;document.getElementById("cnt-err").textContent=S.cntErr;renderLog()}
function renderLog(){const m={성공:"ok",오류:"err",요청:"info",CJ:"warn"};const h=S.logs.map(l=>`<div class="log-item"><span class="badge ${m[l.type]||"info"}">${l.type}</span><span class="log-msg">${l.msg}</span><span class="log-time">${l.time}</span></div>`).join("");document.getElementById("full-log").innerHTML=h||'<div class="empty">작업 내역이 없습니다</div>';document.getElementById("overview-log").innerHTML=S.logs.slice(0,5).map(l=>`<div class="log-item"><span class="badge ${m[l.type]||"info"}">${l.type}</span><span class="log-msg">${l.msg}</span><span class="log-time">${l.time}</span></div>`).join("")||'<div class="empty">아직 작업 내역이 없습니다</div>'}
function clearLog(){S.logs=[];S.cntReg=0;S.cntPrice=0;S.cntErr=0;["cnt-reg","cnt-price","cnt-err"].forEach(id=>document.getElementById(id).textContent="0");renderLog()}
function setLoading(p,on){document.getElementById(p+"-spinner").style.display=on?"block":"none";document.getElementById(p+"-btn").disabled=on}
function showResult(p,text,ok){const el=document.getElementById(p+"-result");el.textContent=text;el.style.display="block";const st=document.getElementById(p+"-status");st.textContent=ok?"성공!":"오류 발생";st.className="status-text "+(ok?"ok":"err")}

/* ===================== CJ 크롤링 ===================== */
async function fetchCJItems(){
  const raw=document.getElementById("cj-ids").value.trim();
  if(!raw){alert("상품번호를 입력하세요.");return}
  const ids=raw.split(/[,\\n]+/).map(s=>s.trim()).filter(Boolean);
  cjItems=ids.map(id=>({id,status:"pending",data:null,ssgItemId:null,error:null}));
  document.getElementById("cj-fetch-btn").disabled=true;
  document.getElementById("cj-progress").style.display="block";
  renderCJList();
  for(let i=0;i<ids.length;i++){
    document.getElementById("cj-progress-bar").style.width=Math.round((i/ids.length)*100)+"%";
    await fetchOneCJ(i);
    await sleep(300);
  }
  document.getElementById("cj-progress-bar").style.width="100%";
  document.getElementById("cj-fetch-btn").disabled=false;
  renderCJList();
  const ok=cjItems.filter(x=>x.status==="fetched").length;
  addLog("CJ",`상품 ${ids.length}개 조회 완료 (성공 ${ok}개)`);
  if(ok>0)document.getElementById("cj-bulk-actions").style.display="block";
}

async function fetchOneCJ(idx){
  const item=cjItems[idx];
  try{
    const res=await fetch("/api/cj/item/"+item.id);
    const data=await res.json();
    if(data.success){
      cjItems[idx].data=data.item;
      cjItems[idx].status="fetched";
    }else{
      cjItems[idx].status="error";
      cjItems[idx].error=data.message||"조회 실패";
    }
  }catch(e){
    cjItems[idx].status="error";
    cjItems[idx].error=e.message;
  }
  renderCJList();
}

function renderCJList(){
  const wrap=document.getElementById("cj-item-list");
  if(!cjItems.length){wrap.style.display="none";return}
  wrap.style.display="flex";
  wrap.innerHTML=cjItems.map((item,idx)=>{
    const d=item.data||{};
    const name=d.itemName||"-";
    const sellPrc=d.clpSlPrc||0;
    const brand=d.brandNm||"";
    const statusLabel={pending:"조회중",fetched:"조회완료",registered:"등록완료",error:"오류"}[item.status]||item.status;
    return `<div class="cj-item">
      <div class="cj-item-num">#${item.id}</div>
      <div class="cj-item-info">
        <div class="cj-item-name">${name}</div>
        <div class="cj-item-meta">${brand}${item.error?" · "+item.error:""}</div>
      </div>
      <div class="cj-item-price">
        <div class="cj-item-price-val">${sellPrc?Number(sellPrc).toLocaleString()+"원":"—"}</div>
        <div class="cj-item-price-label">판매가</div>
      </div>
      <span class="cj-item-status ${item.status}">${statusLabel}</span>
      <div class="cj-item-actions">
        ${item.status==="fetched"?`<button class="btn sm success" onclick="registerOneCJ(${idx})">SSG 등록</button>`:""}
        ${item.status==="registered"?`<span style="font-size:11px;color:var(--muted)">${item.ssgItemId||""}</span>`:""}
      </div>
    </div>`;
  }).join("");
}

async function registerOneCJ(idx){
  if(!S.apiKey){alert("API 설정에서 인증키를 먼저 저장해주세요.");showPage("settings");return}
  const item=cjItems[idx];
  if(!item.data)return;
  cjItems[idx].status="pending";
  renderCJList();
  try{
    const res=await fetch("/api/cj/register",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({item:item.data,apiKey:S.apiKey,accept:S.accept})});
    const data=await res.json();
    if(data.success){
      cjItems[idx].status="registered";
      cjItems[idx].ssgItemId=data.itemId||"";
      addLog("성공","CJ #"+item.id+" SSG 등록 완료"+(data.itemId?" itemId:"+data.itemId:""));
    }else{
      cjItems[idx].status="fetched";
      addLog("오류","CJ #"+item.id+" 등록 실패: "+data.message);
    }
  }catch(e){
    cjItems[idx].status="fetched";
    addLog("오류","CJ #"+item.id+" 오류: "+e.message);
  }
  renderCJList();
}

async function bulkRegister(){
  const targets=cjItems.filter(x=>x.status==="fetched");
  if(!targets.length){alert("조회 완료된 상품이 없습니다.");return}
  if(!S.apiKey){alert("API 설정에서 인증키를 먼저 저장해주세요.");showPage("settings");return}
  document.getElementById("cj-bulk-status").textContent="등록 중...";
  for(let i=0;i<cjItems.length;i++){
    if(cjItems[i].status==="fetched"){
      await registerOneCJ(i);
      await sleep(400);
    }
  }
  document.getElementById("cj-bulk-status").textContent="완료!";
}

function clearCJItems(){
  cjItems=[];
  renderCJList();
  document.getElementById("cj-bulk-actions").style.display="none";
  document.getElementById("cj-progress").style.display="none";
  document.getElementById("cj-ids").value="";
}

function sleep(ms){return new Promise(r=>setTimeout(r,ms))}
/* ===================================================== */

async function doRegister(){if(!S.apiKey){alert("API 설정에서 인증키를 먼저 저장해주세요.");showPage("settings");return}const name=document.getElementById("r-name").value.trim();const sellprc=document.getElementById("r-sellprc").value;const splprc=document.getElementById("r-splprc").value;if(!name||!sellprc||!splprc){alert("상품명, 공급가, 판매가는 필수입니다.");return}setLoading("reg",true);addLog("요청","상품 등록 요청 "+name);const body={name,brand:document.getElementById("r-brand").value,model:document.getElementById("r-model").value,sellType:document.getElementById("r-selltype").value,stock:document.getElementById("r-stock").value,splprc:Number(splprc),sellprc:Number(sellprc),margin:document.getElementById("r-margin").value,prcType:document.getElementById("r-prctype").value,desc:document.getElementById("r-desc").value,apiKey:S.apiKey,accept:S.accept};try{const res=await fetch("/api/register",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});const data=await res.json();const ok=data.success;addLog(ok?"성공":"오류",ok?"상품 등록 완료 "+name+(data.itemId?" itemId:"+data.itemId:""):"등록 실패: "+data.message);showResult("reg",JSON.stringify(data.raw||data,null,2),ok)}catch(e){addLog("오류","오류: "+e.message);showResult("reg",e.message,false)}setLoading("reg",false)}
async function doPrice(){if(!S.apiKey){alert("API 설정에서 인증키를 먼저 저장해주세요.");showPage("settings");return}const itemId=document.getElementById("p-itemid").value.trim();const sellprc=document.getElementById("p-sellprc").value;const splprc=document.getElementById("p-splprc").value;if(!itemId||!sellprc||!splprc){alert("아이템ID, 공급가, 판매가는 필수입니다.");return}setLoading("price",true);addLog("요청","가격 수정 요청 itemId:"+itemId);const startDt=document.getElementById("p-startdt").value;const body={itemId,splprc:Number(splprc),sellprc:Number(sellprc),margin:document.getElementById("p-margin").value,prcType:document.getElementById("p-prctype").value,startDt,apiKey:S.apiKey,accept:S.accept};try{const res=await fetch("/api/price",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});const data=await res.json();const ok=data.success;addLog(ok?"성공":"오류",ok?"가격 수정 완료 itemId:"+itemId+" 판매가:"+Number(sellprc).toLocaleString()+"원":"가격 수정 실패: "+data.message);showResult("price",JSON.stringify(data.raw||data,null,2),ok)}catch(e){addLog("오류","오류: "+e.message);showResult("price",e.message,false)}setLoading("price",false)}
function resetRegister(){["r-name","r-brand","r-model","r-stock","r-splprc","r-sellprc","r-margin","r-desc"].forEach(id=>{const el=document.getElementById(id);if(el)el.value=""});document.getElementById("reg-result").style.display="none";document.getElementById("reg-status").textContent=""}
function resetPrice(){["p-itemid","p-splprc","p-sellprc","p-margin","p-startdt"].forEach(id=>{const el=document.getElementById(id);if(el)el.value=""});document.getElementById("price-result").style.display="none";document.getElementById("price-status").textContent=""}
function toggleKey(){const el=document.getElementById("api-key");el.type=el.type==="password"?"text":"password"}
function saveSettings(){S.apiKey=document.getElementById("api-key").value.trim();S.accept=document.getElementById("api-accept").value;const on=!!S.apiKey;document.getElementById("conn-dot").className="conn-status-dot"+(on?" on":"");document.getElementById("conn-text").textContent=on?"API 키 설정 완료":"API 키를 입력하고 저장해주세요";const msg=document.getElementById("save-msg");msg.style.display="inline";setTimeout(()=>msg.style.display="none",2000)}
setInterval(()=>{document.getElementById("clock").textContent=new Date().toLocaleString("ko-KR",{month:"2-digit",day:"2-digit",hour:"2-digit",minute:"2-digit"})},1000);
</script>
</body>
</html>'''

@app.route('/')
def index():
    return render_template_string(HTML)

# ===================== CJ 크롤링 API =====================

@app.route('/api/cj/item/<item_id>')
def cj_item(item_id):
    """CJ온스타일 상품 정보 조회"""
    try:
        url = CJ_API_URL.format(item_id)
        res = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Referer': 'https://display.cjonstyle.com/'
        }, timeout=10)

        if res.status_code != 200:
            return jsonify({'success': False, 'message': f'HTTP {res.status_code}'})

        data = res.json()

        # 실제 CJ 응답 구조: { code, result: { itemSummaryInfo, returnChangeInfo, ... } }
        result = data.get('result', {})
        summary = result.get('itemSummaryInfo', {})
        return_info = result.get('returnChangeInfo', {})
        item_price = summary.get('itemPrice', {})

        # 필요한 필드만 추출해서 반환
        item = {
            'itemName': summary.get('itemName', ''),
            'clpSlPrc': summary.get('clpSlPrc', 0),   # 판매가
            'slPrc': return_info.get('slPrc', 0),       # 공급가(원가)
            'brandNm': return_info.get('mkrNm', ''),    # 브랜드
            'discountRate': item_price.get('discountRate', 0),
            'discountPrice': item_price.get('discountPrice', 0),
            'imgUrl': summary.get('imgUrl', ''),
            'couponText': summary.get('couponText', ''),
            'mainVenCd': summary.get('mainVenCd', ''),
        }

        return jsonify({'success': True, 'item': item, 'raw': data})

    except requests.Timeout:
        return jsonify({'success': False, 'message': '요청 시간 초과'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route('/api/cj/register', methods=['POST'])
def cj_register():
    """CJ 상품 데이터를 SSG에 등록"""
    data = request.json
    api_key = data.get('apiKey')
    accept = data.get('accept', 'application/json')
    item = data.get('item', {})

    # CJ 실제 필드 → SSG 필드 매핑
    item_nm = item.get('itemName', '')
    brand_nm = item.get('brandNm', '')
    sell_prc = int(item.get('clpSlPrc') or 0)   # CJ 판매가
    spl_prc = int(item.get('slPrc') or 0)         # CJ 원가/공급가

    # 공급가 없으면 판매가 기준 70%로 역산
    if not spl_prc and sell_prc:
        spl_prc = int(sell_prc * 0.7)

    body = {
        '온라인등록': {
            '아이템베이스': {
                'itemNm': item_nm,
                'brandNm': brand_nm or None,
                'mdlNm': mdl_nm or None,
                'itemSellTypeCd': '10',
            },
            '가격': {
                '가격': {
                    'prcMngMthdCd': '3',
                    '품목가격': {
                        'splprc': spl_prc,
                        '셀프른': sell_prc,
                        'mrgrt': None,
                    }
                }
            },
            '설명': {'itemDtlDesc': desc or None}
        }
    }

    try:
        res = requests.post(
            f'{BASE_URL}/item/0.1/온라인',
            headers={'Authorization': api_key, 'Accept': accept, 'Content-Type': 'application/json'},
            json=body, timeout=10
        )
        result = res.json()
        code = result.get('결과', {}).get('결과코드') or result.get('result', {}).get('resultCode')
        item_id = result.get('항목ID') or result.get('itemId', '')
        success = code == '00' or res.status_code == 200
        return jsonify({'success': success, 'itemId': item_id, 'message': str(result), 'raw': result})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

# =========================================================

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
            '설명': {'itemDtlDesc': data.get('desc') or None}
        }
    }
    try:
        res = requests.post(
            f'{BASE_URL}/item/0.1/온라인',
            headers={'Authorization': api_key, 'Accept': accept, 'Content-Type': 'application/json'},
            json=body, timeout=10
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
            json=body, timeout=10
        )
        result = res.json()
        code = result.get('결과', {}).get('결과코드') or result.get('result', {}).get('resultCode')
        success = code == '00' or res.status_code == 200
        return jsonify({'success': success, 'message': str(result), 'raw': result})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=False, host='0.0.0.0', port=port)
