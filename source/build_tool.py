# -*- coding: utf-8 -*-
import json, os, copy
import pools as P
import testbank as T
import taxonomy as TX

DEST = os.environ.get("ASSESSMENT_OUT", os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

LEVELS = P.build()
DIST = P.rebalance(LEVELS)          # even out correct-answer positions in the stored bank


def candidate_data():
    """Answer key REMOVED — no 'a', 'why', 'tol' or 'guide' reaches this payload."""
    out = {}
    for k, lv in LEVELS.items():
        pools = {}
        for sec, qs in lv["pools"].items():
            pools[sec] = [{k2: q[k2] for k2 in ("id", "sec", "type", "q", "track")}
                          | ({"opts": q["opts"]} if q["type"] == "mcq" else {})
                          for q in qs]
        out[k] = {"label": lv["label"], "difficulty": lv["difficulty"], "minutes": lv["minutes"],
                  "slots": lv["slots"], "wslots": lv["wslots"], "pools": pools,
                  "written": [{k2: w[k2] for k2 in ("id", "q", "words", "track")} for w in lv["written"]]}
    return out


def grader_data():
    out = {}
    for k, lv in LEVELS.items():
        flat = {}
        for sec, qs in lv["pools"].items():
            for q in qs:
                flat[q["id"]] = q
        out[k] = {"label": lv["label"], "difficulty": lv["difficulty"], "minutes": lv["minutes"],
                  "slots": lv["slots"], "wslots": lv["wslots"],
                  "q": flat, "written": {w["id"]: w for w in lv["written"]}}
    return copy.deepcopy(out)


CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Arial,sans-serif;
background:#eef1f6;color:#16223a;line-height:1.55;-webkit-font-smoothing:antialiased}
.wrap{max-width:860px;margin:0 auto;padding:26px 20px 90px}
.card{background:#fff;border-radius:12px;box-shadow:0 1px 3px rgba(20,35,70,.10),0 8px 24px rgba(20,35,70,.06);
padding:32px;margin-bottom:18px}
h1{font-size:23px;font-weight:700;letter-spacing:-.3px;margin-bottom:6px}
h2{font-size:17px;font-weight:700;margin-bottom:14px}
h3{font-size:13px;font-weight:700;text-transform:uppercase;letter-spacing:.7px;color:#5a6c8c;margin-bottom:10px}
p{margin-bottom:12px}
.sub{color:#5a6c8c;font-size:14px}
.brandbar{background:#1f3864;color:#fff;padding:20px 28px;border-radius:12px 12px 0 0;margin:-32px -32px 26px}
.brandbar h1{color:#fff;margin:0}.brandbar .sub{color:#b9c7e0;margin-top:4px}
label{display:block;font-size:13px;font-weight:600;color:#41516f;margin:16px 0 6px}
input[type=text],input[type=email],input[type=number],select,textarea{width:100%;padding:11px 13px;
border:1.5px solid #d3dbe8;border-radius:8px;font-size:15px;font-family:inherit;background:#fff;color:#16223a}
input:focus,select:focus,textarea:focus{outline:none;border-color:#2e5c9a;box-shadow:0 0 0 3px rgba(46,92,154,.12)}
textarea{min-height:150px;resize:vertical;line-height:1.6}
button{font-family:inherit;font-size:15px;font-weight:600;padding:12px 26px;border-radius:8px;border:none;
background:#1f3864;color:#fff;cursor:pointer;transition:.15s}
button:hover{background:#2e5c9a}button:disabled{background:#b6c1d4;cursor:not-allowed}
button.ghost{background:#fff;color:#1f3864;border:1.5px solid #cfd8e6}
button.ghost:hover{background:#f2f6fb}
button.skip{background:#fff;color:#8a6100;border:1.5px solid #e6c165;font-size:14px;padding:10px 18px}
button.skip:hover{background:#fff8e6}
.rule{border-top:1px solid #e6ebf3;margin:22px 0}
ul{margin:0 0 12px 20px}li{margin-bottom:6px}
.note{background:#fff8e6;border-left:3px solid #e0a800;padding:13px 16px;border-radius:0 8px 8px 0;font-size:14px;margin-bottom:16px}
.warn{background:#fdeded;border-left:3px solid #c0392b;padding:13px 16px;border-radius:0 8px 8px 0;font-size:14px}
.ok{background:#eaf6ee;border-left:3px solid #2e7d4f;padding:13px 16px;border-radius:0 8px 8px 0;font-size:14px}
.hdr{position:sticky;top:0;z-index:30;background:#1f3864;color:#fff;padding:11px 20px;
display:flex;justify-content:space-between;align-items:center;font-size:14px;gap:12px}
.timer{font-variant-numeric:tabular-nums;font-weight:700;font-size:17px;background:rgba(255,255,255,.13);
padding:5px 13px;border-radius:6px}
.timer.low{background:#c0392b}
.calcbtn{background:rgba(255,255,255,.15);border:none;color:#fff;font-size:13px;font-weight:600;
padding:7px 14px;border-radius:6px;cursor:pointer}
.calcbtn:hover{background:rgba(255,255,255,.28)}
.bar{height:4px;background:#dbe2ec;position:sticky;top:46px;z-index:29}
.bar>div{height:100%;background:#2e5c9a;width:0;transition:width .25s}
.qmeta{font-size:12px;font-weight:700;letter-spacing:.7px;text-transform:uppercase;color:#7b8aa5;margin-bottom:12px}
.qtext{font-size:18px;font-weight:600;line-height:1.5;margin-bottom:20px}
.opt{display:flex;gap:12px;align-items:flex-start;padding:14px 16px;border:1.5px solid #dde4ee;border-radius:9px;
margin-bottom:9px;cursor:pointer;transition:.12s;font-size:15px}
.opt:hover{border-color:#9bb2d4;background:#f7faff}
.opt.sel{border-color:#1f3864;background:#eef3fb;box-shadow:0 0 0 2px rgba(31,56,100,.10)}
.opt .k{flex:none;width:24px;height:24px;border-radius:5px;background:#eef1f6;color:#5a6c8c;font-size:12px;
font-weight:700;display:flex;align-items:center;justify-content:center}
.opt.sel .k{background:#1f3864;color:#fff}
.toggle{display:flex;gap:0;margin-bottom:18px;border:1.5px solid #d3dbe8;border-radius:9px;overflow:hidden}
.toggle div{flex:1;padding:11px 14px;text-align:center;cursor:pointer;font-size:14px;font-weight:600;
color:#5a6c8c;background:#f7f9fc;transition:.12s;border-right:1.5px solid #d3dbe8}
.toggle div:last-child{border-right:none}
.toggle div:hover{background:#eef3fb}
.toggle div.on{background:#1f3864;color:#fff}
.toggle div .tag{display:block;font-size:11px;font-weight:600;opacity:.75;margin-top:1px}
.toggle div.answered::after{content:" ✓";color:#2e7d4f;font-weight:700}
.toggle div.on.answered::after{color:#8fe0ad}
.wc{font-size:12px;color:#7b8aa5;text-align:right;margin-top:5px}
.wc.over{color:#c0392b;font-weight:700}
.row{display:flex;gap:10px;align-items:center;flex-wrap:wrap}
#code{width:100%;height:130px;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;
word-break:break-all;background:#f7f9fc}
/* calculator */
#calc{position:fixed;right:22px;bottom:22px;width:252px;background:#fff;border-radius:12px;z-index:60;
box-shadow:0 6px 32px rgba(15,25,50,.28);border:1px solid #d3dbe8;overflow:hidden}
#calc .ch{background:#1f3864;color:#fff;padding:8px 12px;font-size:12px;font-weight:700;
display:flex;justify-content:space-between;align-items:center;cursor:move;user-select:none}
#calc .ch span{cursor:pointer;font-size:16px;line-height:1;opacity:.8}
#calcdisp{padding:12px;text-align:right;font-size:24px;font-variant-numeric:tabular-nums;
font-family:ui-monospace,Menlo,Consolas,monospace;min-height:50px;word-break:break-all;background:#f7f9fc;
border-bottom:1px solid #e6ebf3}
#calchist{font-size:11px;color:#8a97ad;text-align:right;padding:0 12px 6px;min-height:15px;background:#f7f9fc}
#calcpad{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:#e6ebf3}
#calcpad button{background:#fff;border:none;padding:13px 0;font-size:16px;font-weight:600;color:#16223a;
border-radius:0;cursor:pointer}
#calcpad button:hover{background:#eef3fb}
#calcpad button.op{background:#f5f8fc;color:#2e5c9a}
#calcpad button.eq{background:#1f3864;color:#fff}
#calcpad button.eq:hover{background:#2e5c9a}
#calcpad button.fn{background:#f5f8fc;color:#8a6100;font-size:14px}
.hide{display:none}
@media print{body{background:#fff}.card{box-shadow:none;border:1px solid #ddd;page-break-inside:avoid}
.noprint,#calc{display:none!important}}
"""

CALC = """
<div id="calc" class="hide">
  <div class="ch" id="calchdr">Calculator<span id="calcx">&times;</span></div>
  <div id="calchist"></div><div id="calcdisp">0</div>
  <div id="calcpad">
    <button class="fn" data-k="C">C</button><button class="fn" data-k="back">&#9003;</button>
    <button class="fn" data-k="%">%</button><button class="op" data-k="/">&divide;</button>
    <button data-k="7">7</button><button data-k="8">8</button><button data-k="9">9</button><button class="op" data-k="*">&times;</button>
    <button data-k="4">4</button><button data-k="5">5</button><button data-k="6">6</button><button class="op" data-k="-">&minus;</button>
    <button data-k="1">1</button><button data-k="2">2</button><button data-k="3">3</button><button class="op" data-k="+">+</button>
    <button data-k="0" style="grid-column:span 2">0</button><button data-k=".">.</button><button class="eq" data-k="=">=</button>
  </div>
</div>
<script>
(function(){
  const c=document.getElementById("calc"),d=document.getElementById("calcdisp"),h=document.getElementById("calchist");
  let cur="0",prev=null,op=null,fresh=true;
  function show(){d.textContent=cur;h.textContent=(prev!==null?prev+" "+(op||""):"");}
  function num(v){if(fresh){cur=(v==="."?"0.":v);fresh=false;}
    else{if(v==="."&&cur.includes("."))return;cur=(cur==="0"&&v!==".")?v:cur+v;}show();}
  function calc(){if(prev===null||op===null)return;const a=parseFloat(prev),b=parseFloat(cur);
    let r=op==="+"?a+b:op==="-"?a-b:op==="*"?a*b:op==="/"?(b===0?NaN:a/b):b;
    cur=isNaN(r)?"Error":String(Math.round(r*1e10)/1e10);prev=null;op=null;fresh=true;show();}
  function setop(o){if(op&&!fresh)calc();prev=cur;op=o;fresh=true;show();}
  window.calcKey=function(k){
    if(/^[0-9.]$/.test(k))num(k);
    else if("+-*/".includes(k))setop(k);
    else if(k==="="){calc();}
    else if(k==="C"){cur="0";prev=null;op=null;fresh=true;show();}
    else if(k==="back"){cur=cur.length>1?cur.slice(0,-1):"0";if(cur==="0")fresh=true;show();}
    else if(k==="%"){cur=String(parseFloat(cur)/100);fresh=true;show();}
  };
  document.querySelectorAll("#calcpad button").forEach(b=>b.onclick=()=>window.calcKey(b.dataset.k));
  document.getElementById("calcx").onclick=()=>c.classList.add("hide");
  document.addEventListener("keydown",e=>{
    if(c.classList.contains("hide"))return;
    const t=e.target.tagName;if(t==="TEXTAREA"||t==="INPUT")return;
    if(/^[0-9.]$/.test(e.key)||"+-*/".includes(e.key))window.calcKey(e.key);
    else if(e.key==="Enter"||e.key==="=")window.calcKey("=");
    else if(e.key==="Backspace")window.calcKey("back");
    else if(e.key.toLowerCase()==="c")window.calcKey("C");});
  // drag
  const hd=document.getElementById("calchdr");let dx=0,dy=0,drag=false;
  hd.onmousedown=e=>{if(e.target.id==="calcx")return;drag=true;
    dx=e.clientX-c.offsetLeft;dy=e.clientY-c.offsetTop;e.preventDefault();};
  document.onmousemove=e=>{if(!drag)return;c.style.left=(e.clientX-dx)+"px";c.style.top=(e.clientY-dy)+"px";
    c.style.right="auto";c.style.bottom="auto";};
  document.onmouseup=()=>drag=false;
  window.toggleCalc=()=>c.classList.toggle("hide");
})();
</script>
"""

CAND = """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Performance Marketing Assessment</title><script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script><style>__CSS__</style></head><body>

<div id="hdr" class="hdr hide">
  <div><b id="hLevel"></b> <span style="opacity:.55">&nbsp;|&nbsp;</span> <span id="hProg"></span></div>
  <div class="row" style="gap:8px">
    <button class="calcbtn" onclick="window.toggleCalc()">Calculator</button>
    <div class="timer" id="clock">--:--</div>
  </div>
</div>
<div id="barwrap" class="bar hide"><div id="bar"></div></div>

<div class="wrap">

<div id="setup" class="card">
  <div class="brandbar"><h1>Performance Marketing Assessment</h1>
  <div class="sub">Google Ads &amp; Meta Ads &nbsp;|&nbsp; Lead Generation &amp; Ecommerce</div></div>

  <p>This assessment shows us where your strengths are before we take up more of your time. It is not a memory test
  &mdash; several questions have no single obvious answer and are there to show us how you think.</p>

  <div class="note"><b>Please read before you start:</b>
  <ul>
    <li><b>Every question gives you a choice of two.</b> Answer whichever one you prefer, then move on. If you cannot
        answer either, you may skip &mdash; skipping is recorded but it is not held against you as dishonesty.</li>
    <li>There is a <b>calculator</b> in the top bar. Use it freely. We care that you know what to calculate, not that
        you can do it in your head.</li>
    <li>The timer <b>cannot be paused</b> and submits automatically when it runs out.</li>
    <li>You cannot return to a previous question, so answer before moving on.</li>
    <li>Answer honestly. We would rather see an accurate picture than a perfect score &mdash; the interview finds the
        gap anyway, and being straight about it counts in your favour.</li>
  </ul></div>

  <label>Full name</label><input type="text" id="cName" placeholder="As it appears on your application">
  <label>Email address</label><input type="email" id="cEmail" placeholder="you@example.com">
  <label>Level you are being considered for</label>
  <select id="cLevel"><option value="">Select…</option></select>
  <label>Which best describes your experience?</label>
  <select id="cTrack"><option value="">Select…</option>
    <option value="lg">Mostly lead generation</option>
    <option value="ec">Mostly ecommerce</option>
    <option value="both">Roughly equal / both</option></select>
  <label>Name of the person supervising this session <span style="font-weight:400;color:#7b8aa5">(to be filled by our team)</span></label>
  <input type="text" id="cInvig" placeholder="Invigilator name">
  <div id="dur" class="sub" style="margin-top:16px"></div>
  <div class="rule"></div>
  <button id="start" disabled>Start the assessment</button>
</div>

<div id="qcard" class="card hide">
  <div class="qmeta" id="qsec"></div>
  <div class="toggle" id="toggle"></div>
  <div class="qtext" id="qtext"></div>
  <div id="qbody"></div>
  <div class="rule"></div>
  <div class="row"><button id="next" disabled>Next</button>
  <button class="skip" id="skip">I cannot answer either &mdash; skip</button></div>
</div>

<div id="wcard" class="card hide">
  <div class="qmeta">Written response &mdash; choose one of the two</div>
  <div class="toggle" id="wtoggle"></div>
  <div class="qtext" id="wtext"></div>
  <textarea id="wans" placeholder="Type your answer here…"></textarea>
  <div class="wc" id="wcount"></div>
  <div class="rule"></div>
  <div class="row"><button id="wnext" disabled>Next</button>
  <span class="sub">Specific examples score far better than general statements.</span></div>
</div>

<div id="done" class="card hide">
  <div class="brandbar"><h1>Assessment complete</h1><div class="sub" id="dsub"></div></div>
  <p>Thank you. Please hand the laptop back to the person supervising the session, or complete these two steps:</p>
  <ol style="margin:0 0 18px 20px">
    <li style="margin-bottom:8px"><b>Download the result file</b> using the button below.</li>
    <li><b>Give or email it</b> to the person who set up this assessment.</li>
  </ol>
  <div class="row"><button id="dl">Download result file</button>
  <button class="ghost" id="cp">Copy result code instead</button></div>
  <div class="rule"></div>
  <h3>Backup — if the download does not work</h3>
  <p class="sub">Copy everything in the box below.</p>
  <textarea id="code" readonly></textarea>
  <div class="rule"></div>
  <div id="statusNotice" class="note">Submitting your assessment to the database...</div>
</div>
</div>
__CALC__
<script>
const DATA = __DATA__;
let S={};
const $=id=>document.getElementById(id);
const sel=$("cLevel");
Object.keys(DATA).forEach(k=>{const o=document.createElement("option");o.value=k;
  o.textContent=DATA[k].label+" — "+DATA[k].minutes+" minutes";sel.appendChild(o);});

function shuffle(a){a=a.slice();for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));
  [a[i],a[j]]=[a[j],a[i]];}return a;}

// Samples a fresh set of question PAIRS from the pool. Every candidate gets a different set.
function plan(level,track){
  if(!level||!track)return null;
  const d=DATA[level],slots=[];
  Object.keys(d.slots).forEach(sec=>{
    const need=d.slots[sec], pool=shuffle(d.pools[sec]);
    for(let i=0;i<need;i++){
      const a=pool[i*2],b=pool[i*2+1];
      if(a&&b)slots.push({sec:sec,qs:shuffle([a,b])});
    }
  });
  const keep=w=>w.track==="both"||track==="both"||w.track===track;
  const wpool=shuffle(d.written.filter(keep)),wslots=[];
  for(let i=0;i<d.wslots;i++){
    const a=wpool[i*2],b=wpool[i*2+1];
    if(a&&b)wslots.push({qs:[a,b]});
  }
  return {d:d,slots:shuffle(slots),wslots:wslots,minutes:d.minutes};
}

function check(){
  const ok=$("cName").value.trim()&&$("cEmail").value.trim().includes("@")&&sel.value&&$("cTrack").value;
  $("start").disabled=!ok;
  if(sel.value&&$("cTrack").value){const d=DATA[sel.value];
    const n=Object.values(d.slots).reduce((a,b)=>a+b,0);
    let rows=Object.keys(d.slots).map(c=>"<li>"+c+" — "+d.slots[c]+"</li>").join("");
    $("dur").innerHTML="<b>"+d.label+"</b> &middot; "+d.difficulty+" level &middot; <b>"+d.minutes+
      "-minute</b> limit.<br><b>"+n+" scored questions</b> (each offering a choice of two) plus <b>"+
      d.wslots+" written answers</b>, which are marked separately.<br>"+
      "<span style='font-size:13px'>The "+n+" scored questions break down as:</span><ul style='font-size:13px;margin-top:4px'>"+rows+"</ul>";}
}
["cName","cEmail","cTrack"].forEach(x=>{$(x).addEventListener("input",check);$(x).addEventListener("change",check);});
sel.addEventListener("change",check);

$("start").onclick=()=>{
  const p=plan(sel.value,$("cTrack").value);
  S={name:$("cName").value.trim(),email:$("cEmail").value.trim().toLowerCase(),invig:$("cInvig").value.trim(),
     level:sel.value,track:$("cTrack").value,slots:p.slots,wslots:p.wslots,
     i:0,wi:0,pick:0,wpick:0,ans:{},order:{},wtext:{},t0:Date.now(),left:p.minutes*60,tick:null};
  S.slots.forEach(s=>{s.chose=null;s.skipped=false;});
  S.wslots.forEach(s=>{s.chose=null;});
  $("setup").classList.add("hide");$("hdr").classList.remove("hide");$("barwrap").classList.remove("hide");
  $("hLevel").textContent=p.d.label;
  S.tick=setInterval(()=>{S.left--;paintClock();if(S.left<=0){clearInterval(S.tick);finish(true);}},1000);
  paintClock();render();
};

function paintClock(){const m=Math.max(0,Math.floor(S.left/60)),s=Math.max(0,S.left%60);
  $("clock").textContent=String(m).padStart(2,"0")+":"+String(s).padStart(2,"0");
  $("clock").className="timer"+(S.left<=120?" low":"");}

function render(){
  const total=S.slots.length+S.wslots.length,done=S.i+S.wi;
  $("bar").style.width=(done/total*100)+"%";
  // scored questions and written answers are numbered separately, because they are marked separately
  if(S.i<S.slots.length){
    $("hProg").textContent="Scored question "+(S.i+1)+" of "+S.slots.length;
    renderQ();
  }else{
    $("hProg").textContent="Written answer "+(S.wi+1)+" of "+S.wslots.length+
      "  (scored separately from the "+S.slots.length+" questions)";
    renderW();
  }
}

function renderQ(){
  $("wcard").classList.add("hide");$("qcard").classList.remove("hide");
  const slot=S.slots[S.i],q=slot.qs[S.pick];
  $("qsec").textContent=slot.sec;
  const tg=$("toggle");tg.innerHTML="";
  slot.qs.forEach((qq,ix)=>{
    const d=document.createElement("div");
    d.className=(ix===S.pick?"on ":"")+(S.ans[qq.id]!==undefined?"answered":"");
    d.innerHTML="Option "+(ix===0?"1":"2")+"<span class='tag'>"+
      (qq.type==="num"?"calculation":"multiple choice")+"</span>";
    d.onclick=()=>{S.pick=ix;renderQ();};
    tg.appendChild(d);});
  $("qtext").textContent=q.q;
  const b=$("qbody");b.innerHTML="";
  if(q.type==="mcq"){
    // options shuffled per candidate; original index recorded so grading is unaffected
    if(!S.order[q.id])S.order[q.id]=shuffle(q.opts.map((_,i)=>i));
    const ord=S.order[q.id];
    ord.forEach((orig,pos)=>{
      const d=document.createElement("div");d.className="opt";
      if(S.ans[q.id]===orig)d.classList.add("sel");
      d.innerHTML='<div class="k">'+String.fromCharCode(65+pos)+'</div><div>'+q.opts[orig]+'</div>';
      d.onclick=()=>{S.ans[q.id]=orig;renderQ();};
      b.appendChild(d);});
  }else{
    b.innerHTML='<label>Your answer — numbers only, no commas, currency symbols or % signs</label>'+
      '<input type="number" step="any" id="numin" placeholder="e.g. 1250">'+
      '<div class="sub" style="margin-top:8px">Use the Calculator button in the top bar if you need it.</div>';
    const n=$("numin");if(S.ans[q.id]!==undefined)n.value=S.ans[q.id];
    n.addEventListener("input",()=>{S.ans[q.id]=n.value===""?undefined:parseFloat(n.value);
      $("next").disabled=n.value==="";});
    setTimeout(()=>n.focus(),40);
  }
  const answered=slot.qs.some(qq=>S.ans[qq.id]!==undefined);
  $("next").disabled=!answered;
}

function renderW(){
  $("qcard").classList.add("hide");$("wcard").classList.remove("hide");
  const slot=S.wslots[S.wi],w=slot.qs[S.wpick];
  const tg=$("wtoggle");tg.innerHTML="";
  slot.qs.forEach((ww,ix)=>{
    const d=document.createElement("div");
    d.className=(ix===S.wpick?"on ":"")+((S.wtext[ww.id]||"").trim().split(/\\s+/).filter(Boolean).length>=25?"answered":"");
    d.innerHTML="Question "+(ix===0?"1":"2")+"<span class='tag'>"+ww.words+" words max</span>";
    d.onclick=()=>{S.wpick=ix;renderW();};
    tg.appendChild(d);});
  $("wtext").textContent=w.q;
  const ta=$("wans");ta.value=S.wtext[w.id]||"";
  const upd=()=>{const n=ta.value.trim()?ta.value.trim().split(/\\s+/).length:0;
    $("wcount").textContent=n+" / "+w.words+" words";
    $("wcount").className="wc"+(n>w.words?" over":"");
    S.wtext[w.id]=ta.value;
    const any=slot.qs.some(ww=>(S.wtext[ww.id]||"").trim().split(/\\s+/).filter(Boolean).length>=25);
    $("wnext").disabled=!any;};
  ta.oninput=upd;upd();
  $("wnext").textContent=(S.wi===S.wslots.length-1)?"Finish and submit":"Next";
  setTimeout(()=>ta.focus(),40);
}

$("next").onclick=()=>{
  const slot=S.slots[S.i];
  const chosen=slot.qs.find(qq=>S.ans[qq.id]!==undefined);
  slot.chose=chosen?chosen.id:null;slot.skipped=false;
  S.i++;S.pick=0;render();};

$("skip").onclick=()=>{
  const slot=S.slots[S.i];
  slot.qs.forEach(qq=>delete S.ans[qq.id]);
  slot.chose=null;slot.skipped=true;
  S.i++;S.pick=0;render();};

$("wnext").onclick=()=>{
  const slot=S.wslots[S.wi];
  let best=null,bn=-1;
  slot.qs.forEach(ww=>{const n=(S.wtext[ww.id]||"").trim().split(/\\s+/).filter(Boolean).length;
    if(n>bn){bn=n;best=ww.id;}});
  slot.chose=best;
  if(S.wi===S.wslots.length-1)finish(false); else {S.wi++;S.wpick=0;render();}};

function finish(timedOut){
  if(S.tick)clearInterval(S.tick);
  const mins=Math.round((Date.now()-S.t0)/60000);
  const payload={v:2,name:S.name,email:S.email,invigilator:S.invig,level:S.level,track:S.track,
    submitted:new Date().toISOString(),minutes:mins,timedOut:!!timedOut,
    slots:S.slots.map(s=>({sec:s.sec,pair:s.qs.map(q=>q.id),chose:s.chose,
      ans:s.chose?S.ans[s.chose]:null,skipped:!!s.skipped})),
    wslots:S.wslots.map(s=>({pair:s.qs.map(q=>q.id),chose:s.chose,
      text:s.chose?(S.wtext[s.chose]||""):""}))};
  const b64=btoa(unescape(encodeURIComponent(JSON.stringify(payload))));
  $("code").value=b64;
  $("hdr").classList.add("hide");$("barwrap").classList.add("hide");
  $("qcard").classList.add("hide");$("wcard").classList.add("hide");
  $("done").classList.remove("hide");
  const skipped=S.slots.filter(s=>s.skipped).length;
  $("dsub").textContent=(timedOut?"Time ran out — answers so far have been saved. ":"")+
    S.slots.length+" scored questions and "+S.wslots.length+" written answers, completed in "+mins+
    " minutes"+(skipped?", "+skipped+" question"+(skipped>1?"s":"")+" skipped.":".");
  const safe=(S.name||"candidate").replace(/[^a-z0-9]+/gi,"-").toLowerCase();
  $("dl").onclick=()=>{const blob=new Blob([b64],{type:"text/plain"});
    const a=document.createElement("a");a.href=URL.createObjectURL(blob);
    a.download="assessment-"+safe+"-"+S.level+".txt";a.click();};
  $("cp").onclick=()=>{$("code").select();document.execCommand("copy");
    $("cp").textContent="Copied";setTimeout(()=>$("cp").textContent="Copy result code instead",1800);};

  // Supabase Database Auto-Submit
  const SUPABASE_URL = "https://cjkztctwnviglmhsjnep.supabase.co";
  const SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNqa3p0Y3R3bnZpZ2xtaHNqbmVwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODYzNzU1OTIsImV4cCI6MjEwMTk1MTU5Mn0.7smuVkpYnA1N5_BZHaKX28CpyqehJ5aFWhb8jUQCfNs";
  const db = window.supabase ? window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY) : null;
  if (db) {
    db.from('candidate_assessments').insert([{
      candidate_name: S.name,
      candidate_email: S.email,
      invigilator_name: S.invig,
      role_applied: S.track === 'lg' ? 'Lead Generation' : S.track === 'ec' ? 'Ecommerce' : 'Both',
      assessment_level: S.level,
      submission_payload: payload,
      status: 'submitted',
      created_at: new Date().toISOString()
    }]).then(({ error }) => {
      const notice = $("statusNotice") || document.createElement("div");
      if (error) {
        console.error("Supabase Save Error:", error);
        notice.className = "warn";
        notice.style.marginTop = "16px";
        notice.innerHTML = "<b>Database save notice:</b> Could not save automatically (" + (error.message || "error") + "). Please download your backup result file above.";
      } else {
        console.log("Successfully saved submission to Supabase!");
        notice.className = "ok";
        notice.style.marginTop = "16px";
        notice.innerHTML = "<b>Submitted to HR!</b> Your assessment has been recorded in the database. You may now hand back the laptop.";
      }
      if (!notice.parentNode) $("done").appendChild(notice);
    });
  }
  window.onbeforeunload=null;
}
window.onbeforeunload=e=>{if(S.t0&&$("done").classList.contains("hide")){e.preventDefault();return"";}};
</script></body></html>"""

GRADER = """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Assessment Grader — Internal</title><script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script><style>__CSS__
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px;margin-bottom:6px}
.stat{background:#f5f8fc;border:1px solid #e2e9f3;border-radius:9px;padding:14px}
.stat .n{font-size:25px;font-weight:700;letter-spacing:-.5px}
.stat .l{font-size:11px;text-transform:uppercase;letter-spacing:.7px;color:#7b8aa5;font-weight:700;margin-top:2px}
.band{padding:16px 20px;border-radius:9px;font-size:19px;font-weight:700;text-align:center;margin:16px 0}
.b-go{background:#eaf6ee;color:#1d6b3f;border:1.5px solid #93cba9}
.b-mid{background:#fff6e0;color:#8a6100;border:1.5px solid #e6c165}
.b-no{background:#fdeded;color:#96271a;border:1.5px solid #e0a09a}
table{width:100%;border-collapse:collapse;font-size:13.5px}
th{text-align:left;font-size:11px;text-transform:uppercase;letter-spacing:.6px;color:#7b8aa5;
padding:8px 10px;border-bottom:2px solid #e2e9f3}
td{padding:10px;border-bottom:1px solid #eef1f6;vertical-align:top}
tr.wrong{background:#fdf4f3}tr.skip{background:#fffaf0}
.tick{font-weight:700;color:#2e7d4f}.cross{font-weight:700;color:#c0392b}.sk{font-weight:700;color:#c08a00}
.why{color:#5a6c8c;font-size:12.5px;margin-top:4px;font-style:italic}
.alt{color:#8a97ad;font-size:12px;margin-top:4px}
.sbar{height:8px;background:#e6ebf3;border-radius:4px;overflow:hidden;margin-top:6px}
.sbar>div{height:100%;border-radius:4px}
.wblock{border:1px solid #e2e9f3;border-radius:9px;padding:18px;margin-bottom:14px;background:#fafcff}
.wans{background:#fff;border:1px solid #e6ebf3;border-radius:7px;padding:14px;margin:10px 0;white-space:pre-wrap;font-size:14.5px}
.scorebtns{display:flex;gap:8px;flex-wrap:wrap}
.sb{padding:9px 18px;border:1.5px solid #cfd8e6;border-radius:7px;background:#fff;cursor:pointer;
font-weight:700;font-size:14px;color:#41516f}
.sb.on{background:#1f3864;color:#fff;border-color:#1f3864}
</style></head><body>
<div class="wrap">
<div id="in" class="card">
  <div class="brandbar"><h1>Assessment Grader</h1>
  <div class="sub">Internal use only — this file contains the answer key. Never send it to a candidate.</div></div>
  <div class="warn"><b>Do not forward this file.</b> Keep it where candidates cannot reach it.
  The candidate test file contains no answers; this one does.</div>
  <label>Upload the candidate's result file</label>
  <input type="file" id="file" accept=".txt,.json,text/plain" style="padding:9px">
  <div class="rule"></div>
  <label>…or paste the result code</label>
  <textarea id="paste" placeholder="Paste the long code here" style="min-height:110px;font-family:ui-monospace,monospace;font-size:11px"></textarea>
  <div class="rule"></div>
  <label>…or fetch live submissions from Supabase Database</label>
  <button type="button" class="ghost" id="fetchDbBtn" style="margin-top:6px">Fetch Submissions from Database</button>
  <div id="dbList" style="margin-top:14px"></div>
  <div class="rule"></div>
  <button id="go">Grade this assessment</button>
  <div id="err" style="margin-top:14px"></div>
</div>
<div id="out" class="hide"></div>
</div>
<script>
const KEY = __DATA__;
const PROBE = __PROBE__;
const BLURB = __BLURB__;
const CATORDER = __CATORDER__;
const $=id=>document.getElementById(id);
let R=null;

const SUPABASE_URL = "https://cjkztctwnviglmhsjnep.supabase.co";
const SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNqa3p0Y3R3bnZpZ2xtaHNqbmVwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODYzNzU1OTIsImV4cCI6MjEwMTk1MTU5Mn0.7smuVkpYnA1N5_BZHaKX28CpyqehJ5aFWhb8jUQCfNs";
const db = window.supabase ? window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY) : null;

if (db) {
  setTimeout(() => {
    const btn = $("fetchDbBtn");
    if (btn) {
      btn.onclick = async () => {
        btn.disabled = true;
        btn.textContent = "Fetching...";
        const { data, error } = await db.from('candidate_assessments').select('*').order('created_at', { ascending: false }).limit(20);
        btn.disabled = false;
        btn.textContent = "Fetch Submissions from Database";
        const list = $("dbList");
        if (error) {
          list.innerHTML = '<div class="warn">Error fetching from database: ' + esc(error.message) + '</div>';
          return;
        }
        if (!data || !data.length) {
          list.innerHTML = '<div class="note">No submissions found in Supabase database.</div>';
          return;
        }
        let h = '<table style="margin-top:10px"><tr><th>Candidate</th><th>Level</th><th>Status</th><th>Submitted</th><th>Action</th></tr>';
        data.forEach(item => {
          h += '<tr><td><b>' + esc(item.candidate_name) + '</b><br><span class="sub">' + esc(item.candidate_email) + '</span></td>' +
               '<td>' + esc(item.assessment_level) + '</td>' +
               '<td><span class="' + (item.status === 'graded' ? 'tick' : 'sk') + '">' + esc(item.status || 'submitted') + '</span></td>' +
               '<td>' + new Date(item.created_at).toLocaleString() + '</td>' +
               '<td><button type="button" class="ghost" style="padding:6px 12px;font-size:13px" onclick="loadFromDb(\'' + item.id + '\')">Grade</button></td></tr>';
        });
        h += '</table>';
        list.innerHTML = h;
        window._dbSubmissions = data;
      };
    }
  }, 100);
}

window.loadFromDb = function(id) {
  const item = (window._dbSubmissions || []).find(x => x.id === id);
  if (!item) return;
  R = item.submission_payload;
  R._db_id = item.id;
  R.written_scores = {};
  $("in").classList.add("hide");$("out").classList.remove("hide");render();
};

$("file").addEventListener("change",e=>{const f=e.target.files[0];if(!f)return;
  const r=new FileReader();r.onload=()=>{$("paste").value=String(r.result).trim();};r.readAsText(f);});

$("go").onclick=()=>{
  const raw=$("paste").value.trim();
  if(!raw){$("err").innerHTML='<div class="warn">Nothing to grade — upload a file or paste the code.</div>';return;}
  try{R=JSON.parse(decodeURIComponent(escape(atob(raw))));}
  catch(e){try{R=JSON.parse(raw);}catch(e2){
    $("err").innerHTML='<div class="warn">That code could not be read. Ask the candidate to resend the downloaded file unedited.</div>';return;}}
  if(!R||!R.level||!KEY[R.level]||!R.slots){
    $("err").innerHTML='<div class="warn">Unrecognised result format. This grader expects a file from the current version of the assessment.</div>';return;}
  R.written_scores={};
  $("in").classList.add("hide");$("out").classList.remove("hide");render();
};

function grade(){
  const lv=KEY[R.level],rows=[],secs={};
  let correct=0,wrong=0,skipped=0;
  R.slots.forEach(s=>{
    const sec=s.sec;secs[sec]=secs[sec]||{n:0,c:0,s:0};secs[sec].n++;
    if(s.skipped||!s.chose){skipped++;secs[sec].s++;
      rows.push({sec:sec,skipped:true,pair:s.pair.map(id=>lv.q[id])});return;}
    const q=lv.q[s.chose],other=lv.q[s.pair.find(id=>id!==s.chose)];
    let ok=false,shown="—";
    if(q.type==="mcq"){
      if(s.ans!==null&&s.ans!==undefined){shown=q.opts[s.ans];ok=(s.ans===q.a);}
    }else{
      if(s.ans!==null&&s.ans!==undefined&&s.ans!==""){shown=String(s.ans);
        const tol=Math.max(Math.abs(q.a)*(q.tol||0.02),0.005);ok=Math.abs(s.ans-q.a)<=tol;}
    }
    if(ok){correct++;secs[sec].c++;}else{wrong++;}
    rows.push({sec:sec,q:q,other:other,ok:ok,shown:shown,
      correct:q.type==="mcq"?q.opts[q.a]:String(q.a)});
  });
  const n=R.slots.length;
  const autoPct=n?correct/n*100:0;
  const ws=R.wslots||[];
  let wpts=0,wdone=0;
  ws.forEach(s=>{const v=R.written_scores[s.chose];if(v!==undefined&&v!==null){wpts+=v;wdone++;}});
  const wmax=ws.length*3;
  const writPct=(ws.length&&wdone===ws.length)?wpts/wmax*100:null;
  const combined=writPct===null?null:autoPct*0.7+writPct*0.3;
  return {rows,secs,n,correct,wrong,skipped,autoPct,ws,wpts,wmax,writPct,combined};
}

function band(p){if(p>=80)return["b-go","PROCEED — send the practical case study"];
  if(p>=65)return["b-mid","BORDERLINE — proceed only if the written answers are strong"];
  return["b-no","DO NOT PROCEED — below the bar for this level"];}

function render(){
  const g=grade(),lv=KEY[R.level];
  const tl={lg:"Lead generation",ec:"Ecommerce",both:"Both"}[R.track]||R.track;
  let h='<div class="card"><div class="brandbar"><h1>'+esc(R.name)+'</h1><div class="sub">'+
    lv.label+' &nbsp;|&nbsp; '+(lv.difficulty||'')+' &nbsp;|&nbsp; '+tl+' &nbsp;|&nbsp; '+esc(R.email)+
    (R.invigilator?' &nbsp;|&nbsp; supervised by '+esc(R.invigilator):'')+'</div></div>';
  h+='<div class="note"><b>This paper was '+g.n+' scored questions plus '+(R.wslots||[]).length+
     ' written answers — '+(g.n+(R.wslots||[]).length)+' items in total.</b> '+
     'The scored questions and the written answers are marked separately and then combined, '+
     'so the "'+g.correct+' of '+g.n+'" below counts only the scored questions.</div>';
  h+='<div class="grid">'+stat(g.correct+"/"+g.n,"Correct")+stat(g.wrong,"Wrong")+
     stat(g.skipped,"Skipped")+stat(Math.round(g.autoPct)+"%","Scored questions")+
     stat(g.writPct===null?"—":Math.round(g.writPct)+"%","Written")+
     stat(g.combined===null?"—":Math.round(g.combined)+"%","Combined")+
     stat(R.minutes+"m","Time")+'</div>';
  if(g.skipped>0)h+='<div class="note" style="margin-top:14px"><b>'+g.skipped+' skipped.</b> '+
     'Skips score as incorrect, but they are shown separately on purpose. A candidate who skips a few and is right on '+
     'the rest is telling you honestly where their gaps are — that is different from guessing wrong. '+
     (g.skipped>=Math.ceil(g.n*0.25)?'<b>More than a quarter skipped — check the question-by-question list below to see whether the skips cluster in one area.</b>':'')+
     '</div>';
  if(R.timedOut)h+='<div class="note" style="margin-top:10px"><b>Ran out of time.</b> Unanswered questions score as wrong.</div>';
  const p=g.combined===null?g.autoPct:g.combined,b=band(p);
  h+='<div class="band '+b[0]+'">'+b[1]+(g.combined===null?
    '<div style="font-size:13px;font-weight:600;margin-top:5px">Provisional — score the written answers below to finalise</div>':'')+'</div>';
  h+='<div class="sub">Combined = 70% knowledge + 30% written. Bands: 80%+ proceed · 65–79% borderline · under 65% stop.</div></div>';

  h+='<div class="card"><h2>Capability breakdown</h2>'+
     '<p class="sub">Every question belongs to one of four capabilities. Read the shape, not just the total — '+
     'a candidate strong on knowledge and weak on calculation is a very different hire from the reverse.</p>'+
     '<div class="rule"></div>';
  const weak=[];
  CATORDER.forEach(s=>{
    const o=g.secs[s];if(!o)return;
    const pc=Math.round(o.c/o.n*100);
    if(pc<65)weak.push(s);
    const col=pc>=80?"#2e7d4f":pc>=65?"#e0a800":"#c0392b";
    const verdict=pc>=80?"Strong":pc>=65?"Adequate":"Below bar";
    h+='<div style="margin-bottom:18px"><div class="row" style="justify-content:space-between">'+
      '<b>'+s+'</b><span class="sub">'+o.c+' of '+o.n+(o.s?' &nbsp;('+o.s+' skipped)':'')+
      ' &nbsp; <b style="color:'+col+'">'+pc+'% · '+verdict+'</b></span></div>'+
      '<div class="sbar"><div style="width:'+pc+'%;background:'+col+'"></div></div>'+
      '<div class="alt" style="margin-top:4px">'+esc(BLURB[s]||"")+'</div></div>';});
  h+='</div>';

  h+='<div class="card"><h2>What to probe in the interview</h2>';
  if(!weak.length)h+='<p class="sub">No section fell below 65%. Use the standard interviewer card and spend the time on ownership and attitude rather than technical depth.</p>';
  else weak.forEach(s=>{if(PROBE[s])h+='<div class="note">'+PROBE[s]+'</div>';});
  if(g.writPct!==null&&g.writPct<60)h+='<div class="note">'+PROBE["written"]+'</div>';
  h+='<p class="sub" style="margin-top:10px">Take this into the final interview. Knowing where to dig is the whole reason for running the assessment first.</p></div>';

  h+='<div class="card noprint"><h2>Score the written answers</h2>'+
    '<p class="sub">0 = no real answer · 1 = generic · 2 = solid and specific · 3 = clearly strong. '+
    'Each was chosen by the candidate from a pair — the alternative they turned down is shown too.</p><div class="rule"></div>';
  (R.wslots||[]).forEach(s=>{
    const w=lv.written[s.chose],other=lv.written[s.pair.find(id=>id!==s.chose)];
    const wc=(s.text||"").trim()?s.text.trim().split(/\\s+/).length:0;
    h+='<div class="wblock"><div class="qmeta">'+s.chose+' &nbsp;·&nbsp; '+wc+' words</div>'+
      '<div style="font-weight:600;margin-bottom:8px">'+esc(w.q)+'</div>'+
      (other?'<div class="alt">They chose this over: '+esc(other.q)+'</div>':'')+
      '<div class="wans">'+esc(s.text||"(no answer given)")+'</div>'+
      '<div class="note"><b>What a strong answer includes:</b> '+esc(w.guide)+'</div>'+
      '<div class="scorebtns" data-w="'+s.chose+'">'+
      [0,1,2,3].map(v=>'<div class="sb'+(R.written_scores[s.chose]===v?" on":"")+'" data-v="'+v+'">'+v+'</div>').join("")+
      '</div></div>';});
  h+='</div>';

  h+='<div class="card"><h2>Decision record</h2><table>'+
    row("Candidate",esc(R.name))+row("Level / track",lv.label+" — "+tl)+
    row("Supervised by",esc(R.invigilator||"—"))+
    row("Submitted",new Date(R.submitted).toLocaleString())+
    row("Knowledge",Math.round(g.autoPct)+"% ("+g.correct+" correct, "+g.wrong+" wrong, "+g.skipped+" skipped)")+
    row("Written",g.writPct===null?"not yet scored":Math.round(g.writPct)+"% ("+g.wpts+" of "+g.wmax+")")+
    row("Combined","<b>"+(g.combined===null?"—":Math.round(g.combined)+"%")+"</b>")+
    row("Outcome","<b>"+b[1]+"</b>")+
    row("Graded by / date",'<span style="color:#aab">________________________________</span>')+
    '</table><div class="rule"></div><div class="row noprint">'+
    '<button onclick="window.print()">Print / save as PDF</button>'+
    (R._db_id ? '<button id="syncDbBtn" style="background:#2e7d4f" onclick="syncScoreToDb()">Sync &amp; Save Score to Database</button>' : '')+
    '<button class="ghost" onclick="location.reload()">Grade another candidate</button></div>'+
    '<div id="syncStatus" style="margin-top:10px"></div></div>';

  h+='<div class="card"><h2>Question by question</h2>'+
    '<p class="sub">Each row is one slot. The candidate chose one question from a pair — the one they turned down is '+
    'shown in grey, because what someone avoids is itself informative.</p><div class="rule"></div>'+
    '<table><tr><th style="width:30px"></th><th>Question they answered</th><th style="width:175px">Their answer</th>'+
    '<th style="width:175px">Correct</th></tr>';
  g.rows.forEach(r=>{
    if(r.skipped){
      h+='<tr class="skip"><td class="sk">–</td><td colspan="3"><b>Skipped</b> ('+esc(r.sec)+') — '+
        'declined both: <span class="alt">'+r.pair.map(q=>esc(q.q)).join(' &nbsp;/&nbsp; ')+'</span></td></tr>';
      return;}
    h+='<tr class="'+(r.ok?"":"wrong")+'"><td class="'+(r.ok?"tick":"cross")+'">'+(r.ok?"✓":"✗")+'</td>'+
      '<td><b>'+r.q.id+'</b> '+esc(r.q.q)+'<div class="why">'+esc(r.q.why)+'</div>'+
      (r.other?'<div class="alt">Chose this over: '+esc(r.other.q)+'</div>':'')+'</td>'+
      '<td>'+esc(r.shown)+'</td><td>'+esc(r.correct)+'</td></tr>';});
  h+='</table></div>';

  $("out").innerHTML=h;
  document.querySelectorAll(".scorebtns").forEach(gb=>{
    gb.querySelectorAll(".sb").forEach(b2=>{b2.onclick=()=>{
      R.written_scores[gb.dataset.w]=parseInt(b2.dataset.v,10);
      const y=window.scrollY;render();window.scrollTo(0,y);};});});
}

window.syncScoreToDb = async function() {
  if (!R || !R._db_id || !db) return;
  const g = grade();
  const btn = $("syncDbBtn");
  const status = $("syncStatus");
  if (btn) { btn.disabled = true; btn.textContent = "Syncing..."; }
  try {
    const { error } = await db.from('candidate_assessments').update({
      mcq_score: Math.round(g.autoPct),
      written_score: g.writPct !== null ? Math.round(g.writPct) : null,
      total_score: g.combined !== null ? Math.round(g.combined) : Math.round(g.autoPct),
      status: 'graded',
      graded_at: new Date().toISOString()
    }).eq('id', R._db_id);
    if (error) {
      if (status) status.innerHTML = '<div class="warn">Error syncing score to database: ' + esc(error.message) + '</div>';
      if (btn) { btn.disabled = false; btn.textContent = "Sync & Save Score to Database"; }
    } else {
      if (status) status.innerHTML = '<div class="ok"><b>Score Synced!</b> Candidate result updated in Supabase database. The candidate can now view their final result on the Result Portal.</div>';
      if (btn) { btn.textContent = "Score Synced to Database ✓"; }
    }
  } catch (err) {
    console.error(err);
    if (status) status.innerHTML = '<div class="warn">An unexpected error occurred during sync.</div>';
    if (btn) { btn.disabled = false; btn.textContent = "Sync & Save Score to Database"; }
  }
};
function row(a,b){return '<tr><td style="width:230px"><b>'+a+'</b></td><td>'+b+'</td></tr>';}
function stat(n,l){return '<div class="stat"><div class="n">'+n+'</div><div class="l">'+l+'</div></div>';}
function esc(s){return String(s==null?"":s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");}
</script></body></html>"""

HR_DASHBOARD = """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>HR Candidate Dashboard — Performance Marketing Assessment</title>
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
<style>__CSS__
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:12px;margin-bottom:16px}
.stat{background:#f5f8fc;border:1px solid #e2e9f3;border-radius:9px;padding:12px 14px}
.stat .n{font-size:24px;font-weight:700;letter-spacing:-.5px}
.stat .l{font-size:11px;text-transform:uppercase;letter-spacing:.7px;color:#7b8aa5;font-weight:700;margin-top:2px}
.band{padding:14px 18px;border-radius:9px;font-size:17px;font-weight:700;text-align:center;margin:14px 0}
.b-go{background:#eaf6ee;color:#1d6b3f;border:1.5px solid #93cba9}
.b-mid{background:#fff6e0;color:#8a6100;border:1.5px solid #e6c165}
.b-no{background:#fdeded;color:#96271a;border:1.5px solid #e0a09a}
.b-pending{background:#eef3fb;color:#1f3864;border:1.5px solid #9bb2d4}
table{width:100%;border-collapse:collapse;font-size:13.5px}
th{text-align:left;font-size:11px;text-transform:uppercase;letter-spacing:.6px;color:#7b8aa5;padding:9px 10px;border-bottom:2px solid #e2e9f3}
td{padding:10px;border-bottom:1px solid #eef1f6;vertical-align:top}
tr.wrong{background:#fdf4f3}tr.skip{background:#fffaf0}
.tick{font-weight:700;color:#2e7d4f}.cross{font-weight:700;color:#c0392b}.sk{font-weight:700;color:#c08a00}
.why{color:#5a6c8c;font-size:12.5px;margin-top:4px;font-style:italic}
.alt{color:#8a97ad;font-size:12px;margin-top:4px}
.sbar{height:8px;background:#e6ebf3;border-radius:4px;overflow:hidden;margin-top:6px}
.sbar>div{height:100%;border-radius:4px}
.wblock{border:1px solid #e2e9f3;border-radius:9px;padding:16px;margin-bottom:12px;background:#fafcff}
.wans{background:#fff;border:1px solid #e6ebf3;border-radius:7px;padding:12px;margin:8px 0;white-space:pre-wrap;font-size:14px}
.scorebtns{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}
.sb{padding:8px 16px;border:1.5px solid #cfd8e6;border-radius:7px;background:#fff;cursor:pointer;font-weight:700;font-size:13.5px;color:#41516f}
.sb.on{background:#1f3864;color:#fff;border-color:#1f3864}
.badge{display:inline-block;padding:3px 9px;border-radius:12px;font-size:11px;font-weight:700;text-transform:uppercase}
.badge.submitted{background:#fff6e0;color:#8a6100;border:1px solid #e6c165}
.badge.graded{background:#eaf6ee;color:#1d6b3f;border:1px solid #93cba9}
.searchbar{display:flex;gap:10px;margin-bottom:16px;flex-wrap:wrap}
.searchbar input{flex:1;min-width:200px}
.searchbar select{width:160px}
tr.hoverable:hover{background:#f7faff;cursor:pointer}
@media print{.noprint,#loginCard,.searchbar{display:none!important}body{background:#fff}.card{box-shadow:none;border:1px solid #ddd}}
</style></head><body>

<div class="wrap">
  <!-- LOGIN CARD -->
  <div id="loginCard" class="card">
    <div class="brandbar">
      <h1>HR / Recruiter Dashboard</h1>
      <div class="sub">Performance Marketing Assessment — Private Candidate Management</div>
    </div>
    <p>Please enter the HR Passcode to access the master candidate list and assessment results.</p>
    <div id="loginMsg"></div>
    <form id="loginForm" onsubmit="event.preventDefault(); loginHR();">
      <label for="passInput">HR Passcode</label>
      <input type="password" id="passInput" placeholder="Enter HR Passcode" required autofocus>
      <div class="rule"></div>
      <button type="submit" id="loginBtn">Unlock HR Dashboard</button>
    </form>
  </div>

  <!-- MAIN DASHBOARD -->
  <div id="dashboard" class="hide">
    <div class="card">
      <div class="brandbar">
        <div class="row" style="justify-content:space-between">
          <div>
            <h1>Candidate Assessment Master List</h1>
            <div class="sub">View candidate test submissions, evaluate written answers, and sync results</div>
          </div>
          <button class="ghost" style="color:#fff;border-color:rgba(255,255,255,.4);background:rgba(255,255,255,.1)" onclick="logoutHR()">Lock Dashboard</button>
        </div>
      </div>

      <!-- STATS OVERVIEW -->
      <div class="grid">
        <div class="stat"><div class="n" id="stTotal">0</div><div class="l">Total Submissions</div></div>
        <div class="stat"><div class="n" id="stPending">0</div><div class="l">Pending Evaluation</div></div>
        <div class="stat"><div class="n" id="stGraded">0</div><div class="l">Graded</div></div>
        <div class="stat"><div class="n" id="stProceed">0</div><div class="l">Passed (Proceed)</div></div>
      </div>

      <!-- SEARCH & FILTER BAR -->
      <div class="searchbar">
        <input type="text" id="searchInput" placeholder="Search candidates by name or email..." oninput="filterCandidates()">
        <select id="levelFilter" onchange="filterCandidates()">
          <option value="all">All Levels</option>
          <option value="Intern">Intern</option>
          <option value="Associate">Associate</option>
          <option value="Manager">Manager</option>
          <option value="Sr. Manager">Sr. Manager</option>
        </select>
        <select id="statusFilter" onchange="filterCandidates()">
          <option value="all">All Statuses</option>
          <option value="submitted">Pending Evaluation</option>
          <option value="graded">Graded</option>
        </select>
        <button class="ghost" onclick="fetchCandidates()">Refresh List</button>
      </div>

      <div id="tableMsg"></div>

      <!-- CANDIDATE LIST TABLE -->
      <div style="overflow-x:auto">
        <table>
          <thead>
            <tr>
              <th>Candidate Name &amp; Email</th>
              <th>Level</th>
              <th>Track</th>
              <th>Submitted</th>
              <th>Status</th>
              <th>MCQ Score</th>
              <th>Total Score</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody id="candidateTbody">
            <tr><td colspan="8" style="text-align:center;padding:24px;color:#7b8aa5">Loading candidates...</td></tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- CANDIDATE REPORT CARD -->
  <div id="reportCard" class="card hide">
    <div class="row noprint" style="margin-bottom:14px;justify-content:space-between">
      <button class="ghost" onclick="closeReport()">&larr; Back to Candidate List</button>
      <div class="row">
        <button id="saveScoreBtn" style="background:#2e7d4f" onclick="syncScoreToDb()">Sync &amp; Save Score to Supabase</button>
        <button onclick="window.print()">Print / Save PDF</button>
      </div>
    </div>

    <div id="saveStatus"></div>
    <div id="reportContent"></div>
  </div>
</div>

<script>
const KEY = __DATA__;
const PROBE = __PROBE__;
const BLURB = __BLURB__;
const CATORDER = __CATORDER__;
const HR_PASSCODE = "admin123";

const SUPABASE_URL = "https://cjkztctwnviglmhsjnep.supabase.co";
const SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNqa3p0Y3R3bnZpZ2xtaHNqbmVwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODYzNzU1OTIsImV4cCI6MjEwMTk1MTU5Mn0.7smuVkpYnA1N5_BZHaKX28CpyqehJ5aFWhb8jUQCfNs";
const db = window.supabase ? window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY) : null;

let allCandidates = [];
let currentRecord = null;
let R = null;

const $=id=>document.getElementById(id);

function loginHR() {
  const entered = $("passInput").value.trim();
  const msg = $("loginMsg");
  if (entered === HR_PASSCODE) {
    sessionStorage.setItem("hr_authenticated", "true");
    $("loginCard").classList.add("hide");
    $("dashboard").classList.remove("hide");
    fetchCandidates();
  } else {
    msg.innerHTML = '<div class="warn">Incorrect HR Passcode. Please try again.</div>';
  }
}

function logoutHR() {
  sessionStorage.removeItem("hr_authenticated");
  $("dashboard").classList.add("hide");
  $("reportCard").classList.add("hide");
  $("loginCard").classList.remove("hide");
  $("passInput").value = "";
}

if (sessionStorage.getItem("hr_authenticated") === "true") {
  $("loginCard").classList.add("hide");
  $("dashboard").classList.remove("hide");
  fetchCandidates();
}

async function fetchCandidates() {
  const tbody = $("candidateTbody");
  const msg = $("tableMsg");
  if (!db) {
    msg.innerHTML = '<div class="warn">Unable to connect to Supabase database. Check API credentials.</div>';
    return;
  }
  msg.innerHTML = "";
  tbody.innerHTML = '<tr><td colspan="8" style="text-align:center;padding:24px;color:#7b8aa5">Fetching live candidate data...</td></tr>';

  try {
    const { data, error } = await db.from('candidate_assessments').select('*').order('created_at', { ascending: false });
    if (error) {
      msg.innerHTML = '<div class="warn">Error fetching records: ' + esc(error.message) + '</div>';
      return;
    }
    allCandidates = data || [];
    updateStats(allCandidates);
    filterCandidates();
  } catch (err) {
    console.error(err);
    msg.innerHTML = '<div class="warn">An unexpected error occurred while querying the database.</div>';
  }
}

function updateStats(list) {
  $("stTotal").textContent = list.length;
  $("stPending").textContent = list.filter(c => c.status !== 'graded').length;
  $("stGraded").textContent = list.filter(c => c.status === 'graded').length;
  $("stProceed").textContent = list.filter(c => c.total_score >= 80).length;
}

function filterCandidates() {
  const q = $("searchInput").value.trim().toLowerCase();
  const lvl = $("levelFilter").value;
  const st = $("statusFilter").value;

  const filtered = allCandidates.filter(c => {
    const matchQ = !q || (c.candidate_name || "").toLowerCase().includes(q) || (c.candidate_email || "").toLowerCase().includes(q);
    const matchLvl = lvl === "all" || (c.assessment_level || "").toLowerCase().includes(lvl.toLowerCase());
    const matchSt = st === "all" || (st === "submitted" ? c.status !== "graded" : c.status === "graded");
    return matchQ && matchLvl && matchSt;
  });
  renderTable(filtered);
}

function renderTable(list) {
  const tbody = $("candidateTbody");
  if (!list || list.length === 0) {
    tbody.innerHTML = '<tr><td colspan="8" style="text-align:center;padding:24px;color:#7b8aa5">No candidate submissions match your criteria.</td></tr>';
    return;
  }

  let h = "";
  list.forEach(c => {
    const created = c.created_at ? new Date(c.created_at).toLocaleString([], { dateStyle: 'short', timeStyle: 'short' }) : '—';
    const isGraded = c.status === 'graded';
    const statusBadge = isGraded ? '<span class="badge graded">Graded</span>' : '<span class="badge submitted">Pending</span>';
    
    let mcqVal = c.mcq_score;
    if (mcqVal === null || mcqVal === undefined) {
      if (c.submission_payload && KEY[c.assessment_level]) {
        const g = gradePayload(c.submission_payload);
        mcqVal = Math.round(g.autoPct);
      }
    }
    const mcq = mcqVal !== null && mcqVal !== undefined ? mcqVal + '%' : '—';
    const total = c.total_score !== null && c.total_score !== undefined ? c.total_score + '%' : '—';

    h += `
      <tr class="hoverable" onclick="openReport('${c.id}')">
        <td><b>${esc(c.candidate_name)}</b><br><span class="sub">${esc(c.candidate_email)}</span></td>
        <td>${esc(c.assessment_level || '—')}</td>
        <td>${esc(c.role_applied || '—')}</td>
        <td style="font-size:12.5px">${created}</td>
        <td>${statusBadge}</td>
        <td><b>${mcq}</b></td>
        <td><b style="color:${c.total_score >= 80 ? '#2e7d4f' : c.total_score >= 65 ? '#e0a800' : '#16223a'}">${total}</b></td>
        <td><button class="ghost" style="padding:6px 12px;font-size:12.5px" onclick="event.stopPropagation(); openReport('${c.id}')">${isGraded ? 'View Report' : 'Grade &amp; Review'}</button></td>
      </tr>
    `;
  });
  tbody.innerHTML = h;
}

function gradePayload(payload) {
  const lv = KEY[payload.level];
  if (!lv) return { rows: [], secs: {}, n: 0, correct: 0, wrong: 0, skipped: 0, autoPct: 0 };
  const rows = [], secs = {};
  let correct = 0, wrong = 0, skipped = 0;
  (payload.slots || []).forEach(s => {
    const sec = s.sec;
    secs[sec] = secs[sec] || { n: 0, c: 0, s: 0 };
    secs[sec].n++;
    if (s.skipped || !s.chose) {
      skipped++;
      secs[sec].s++;
      rows.push({ sec: sec, skipped: true, pair: s.pair.map(id => lv.q[id]) });
      return;
    }
    const q = lv.q[s.chose], other = lv.q[s.pair.find(id => id !== s.chose)];
    let ok = false, shown = "—";
    if (q.type === "mcq") {
      if (s.ans !== null && s.ans !== undefined) { shown = q.opts[s.ans]; ok = (s.ans === q.a); }
    } else {
      if (s.ans !== null && s.ans !== undefined && s.ans !== "") {
        shown = String(s.ans);
        const tol = Math.max(Math.abs(q.a) * (q.tol || 0.02), 0.005);
        ok = Math.abs(s.ans - q.a) <= tol;
      }
    }
    if (ok) { correct++; secs[sec].c++; } else { wrong++; }
    rows.push({ sec: sec, q: q, other: other, ok: ok, shown: shown, correct: q.type === "mcq" ? q.opts[q.a] : String(q.a) });
  });
  const n = (payload.slots || []).length;
  const autoPct = n ? (correct / n * 100) : 0;
  return { rows, secs, n, correct, wrong, skipped, autoPct };
}

function openReport(id) {
  const rec = allCandidates.find(x => x.id === id);
  if (!rec) return;

  currentRecord = rec;
  R = JSON.parse(JSON.stringify(rec.submission_payload || {}));
  R._db_id = rec.id;
  R.written_scores = R.written_scores || {};

  $("dashboard").classList.add("hide");
  $("reportCard").classList.remove("hide");
  $("saveStatus").innerHTML = "";

  renderReport();
}

function closeReport() {
  $("reportCard").classList.add("hide");
  $("dashboard").classList.remove("hide");
  fetchCandidates();
}

function band(p) {
  if (p >= 80) return ["b-go", "PROCEED — Send the practical case study"];
  if (p >= 65) return ["b-mid", "BORDERLINE — Proceed only if the written answers are strong"];
  return ["b-no", "DO NOT PROCEED — Below the bar for this level"];
}

function renderReport() {
  const lv = KEY[R.level];
  if (!lv) { $("reportContent").innerHTML = '<div class="warn">Level structure not found.</div>'; return; }

  const g = gradePayload(R);

  const ws = R.wslots || [];
  let wpts = 0, wdone = 0;
  ws.forEach(s => { const v = R.written_scores[s.chose]; if (v !== undefined && v !== null) { wpts += v; wdone++; } });
  const wmax = ws.length * 3;
  const writPct = (ws.length && wdone === ws.length) ? (wpts / wmax * 100) : (currentRecord.written_score !== null && currentRecord.written_score !== undefined ? Number(currentRecord.written_score) : null);
  const combined = writPct === null ? null : (g.autoPct * 0.7 + writPct * 0.3);

  const tl = { lg: "Lead generation", ec: "Ecommerce", both: "Both" }[R.track] || R.track;

  let h = '<div class="brandbar"><h1>' + esc(R.name) + '</h1><div class="sub">' +
    lv.label + ' &nbsp;|&nbsp; ' + (lv.difficulty || '') + ' &nbsp;|&nbsp; ' + tl + ' &nbsp;|&nbsp; ' + esc(R.email) +
    (R.invigilator ? ' &nbsp;|&nbsp; Supervised by ' + esc(R.invigilator) : '') + '</div></div>';

  h += '<div class="grid">' +
    stat(g.correct + "/" + g.n, "Correct") +
    stat(g.wrong, "Wrong") +
    stat(g.skipped, "Skipped") +
    stat(Math.round(g.autoPct) + "%", "Scored Knowledge (70%)") +
    stat(writPct === null ? "Pending" : Math.round(writPct) + "%", "Written Score (30%)") +
    stat(combined === null ? "—" : Math.round(combined) + "%", "Combined Score") +
    stat(R.minutes + "m", "Time") + '</div>';

  if (g.skipped > 0) {
    h += '<div class="note"><b>' + g.skipped + ' skipped.</b> Skips score as incorrect, but are shown separately to highlight candidate honesty.</div>';
  }

  const p = combined === null ? g.autoPct : combined;
  const b = band(p);
  h += '<div class="band ' + b[0] + '">' + b[1] + (combined === null ? '<div style="font-size:13px;font-weight:600;margin-top:5px">Provisional — score the written answers below to finalise</div>' : '') + '</div>';

  // Capability Breakdown
  h += '<div class="rule"></div><h2>Capability Breakdown</h2><div class="sub">Every question belongs to one of four capabilities. Green = >=80% (Strong), Yellow = 65-79% (Adequate), Red = <65% (Below Bar).</div><div class="rule"></div>';
  const weak = [];
  CATORDER.forEach(s => {
    const o = g.secs[s]; if (!o) return;
    const pc = Math.round(o.c / o.n * 100);
    if (pc < 65) weak.push(s);
    const col = pc >= 80 ? "#2e7d4f" : pc >= 65 ? "#e0a800" : "#c0392b";
    const verdict = pc >= 80 ? "Strong" : pc >= 65 ? "Adequate" : "Below Bar";
    h += '<div style="margin-bottom:18px"><div class="row" style="justify-content:space-between">' +
      '<b>' + s + '</b><span class="sub">' + o.c + ' of ' + o.n + (o.s ? ' &nbsp;(' + o.s + ' skipped)' : '') +
      ' &nbsp; <b style="color:' + col + '">' + pc + '% · ' + verdict + '</b></span></div>' +
      '<div class="sbar"><div style="width:' + pc + '%;background:' + col + '"></div></div>' +
      '<div class="alt" style="margin-top:4px">' + esc(BLURB[s] || "") + '</div></div>';
  });

  // What to probe in interview
  h += '<div class="rule"></div><h2>What to Probe in the Interview</h2>';
  if (!weak.length) {
    h += '<p class="sub">No capability section fell below 65%. Use standard interviewer card for technical depth.</p>';
  } else {
    weak.forEach(s => { if (PROBE[s]) h += '<div class="note">' + PROBE[s] + '</div>'; });
  }
  if (writPct !== null && writPct < 60) h += '<div class="note">' + PROBE["written"] + '</div>';

  // Score Written Answers
  h += '<div class="rule"></div><h2>Score Written Answers</h2>' +
    '<p class="sub">0 = no real answer · 1 = generic · 2 = solid and specific · 3 = clearly strong.</p><div class="rule"></div>';
  (R.wslots || []).forEach(s => {
    const w = lv.written[s.chose], other = lv.written[s.pair.find(id => id !== s.chose)];
    const wc = (s.text || "").trim() ? s.text.trim().split(/\\s+/).length : 0;
    h += '<div class="wblock"><div class="sub" style="font-weight:700">' + s.chose + ' &nbsp;·&nbsp; ' + wc + ' words</div>' +
      '<div style="font-weight:600;margin-top:4px;margin-bottom:8px">' + esc(w.q) + '</div>' +
      (other ? '<div class="alt">They chose this over: ' + esc(other.q) + '</div>' : '') +
      '<div class="wans">' + esc(s.text || "(no answer given)") + '</div>' +
      '<div class="note"><b>What a strong answer includes:</b> ' + esc(w.guide) + '</div>' +
      '<div class="scorebtns" data-w="' + s.chose + '">' +
      [0, 1, 2, 3].map(v => '<div class="sb' + (R.written_scores[s.chose] === v ? " on" : "") + '" data-v="' + v + '">' + v + '</div>').join("") +
      '</div></div>';
  });

  // Question by Question breakdown table
  h += '<div class="rule"></div><h2>Question by Question Breakdown</h2>' +
    '<table><tr><th style="width:30px"></th><th>Question answered</th><th style="width:175px">Candidate Choice</th>' +
    '<th style="width:175px">Correct Answer</th></tr>';
  g.rows.forEach(r => {
    if (r.skipped) {
      h += '<tr class="skip"><td class="sk">–</td><td colspan="3"><b>Skipped</b> (' + esc(r.sec) + ') — ' +
        'declined both: <span class="alt">' + r.pair.map(q => esc(q.q)).join(' &nbsp;/&nbsp; ') + '</span></td></tr>';
      return;
    }
    h += '<tr class="' + (r.ok ? "" : "wrong") + '"><td class="' + (r.ok ? "tick" : "cross") + '">' + (r.ok ? "✓" : "✗") + '</td>' +
      '<td><b>' + r.q.id + '</b> ' + esc(r.q.q) + '<div class="why">' + esc(r.q.why) + '</div>' +
      (r.other ? '<div class="alt">Chose this over: ' + esc(r.other.q) + '</div>' : '') + '</td>' +
      '<td>' + esc(r.shown) + '</td><td>' + esc(r.correct) + '</td></tr>';
  });
  h += '</table>';

  $("reportContent").innerHTML = h;

  document.querySelectorAll(".scorebtns").forEach(gb => {
    gb.querySelectorAll(".sb").forEach(b2 => {
      b2.onclick = () => {
        R.written_scores[gb.dataset.w] = parseInt(b2.dataset.v, 10);
        const y = window.scrollY; renderReport(); window.scrollTo(0, y);
      };
    });
  });
}

async function syncScoreToDb() {
  if (!currentRecord || !db || !R) return;
  const g = gradePayload(R);
  const saveBtn = $("saveScoreBtn");
  const statusDiv = $("saveStatus");

  saveBtn.disabled = true;
  saveBtn.textContent = "Syncing...";

  const ws = R.wslots || [];
  let wpts = 0, wdone = 0;
  ws.forEach(s => { const v = R.written_scores[s.chose]; if (v !== undefined && v !== null) { wpts += v; wdone++; } });
  const wmax = ws.length * 3;
  const writPct = (ws.length && wdone === ws.length) ? Math.round(wpts / wmax * 100) : null;
  const combined = writPct === null ? Math.round(g.autoPct) : Math.round(g.autoPct * 0.7 + writPct * 0.3);

  try {
    const { error } = await db.from('candidate_assessments').update({
      mcq_score: Math.round(g.autoPct),
      written_score: writPct,
      total_score: combined,
      status: 'graded',
      graded_at: new Date().toISOString()
    }).eq('id', currentRecord.id);

    if (error) {
      statusDiv.innerHTML = '<div class="warn">Error updating database: ' + esc(error.message) + '</div>';
      saveBtn.disabled = false; saveBtn.textContent = "Sync & Save Score to Supabase";
    } else {
      statusDiv.innerHTML = '<div class="ok"><b>Scores Synced!</b> Candidate score updated in Supabase database.</div>';
      saveBtn.disabled = false; saveBtn.textContent = "Score Synced ✓";
      currentRecord.status = 'graded';
      currentRecord.mcq_score = Math.round(g.autoPct);
      currentRecord.written_score = writPct;
      currentRecord.total_score = combined;
    }
  } catch (err) {
    console.error(err);
    statusDiv.innerHTML = '<div class="warn">An unexpected error occurred during database sync.</div>';
    saveBtn.disabled = false; saveBtn.textContent = "Sync & Save Score to Supabase";
  }
}

function stat(n, l) { return '<div class="stat"><div class="n">' + n + '</div><div class="l">' + l + '</div></div>'; }
function esc(s) { return String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;"); }
</script>
</body>
</html>"""


def write(path, html, data, probe=None, calc=False):
    html = html.replace("__CSS__", CSS)
    html = html.replace("__CALC__", CALC if calc else "")
    html = html.replace("__DATA__", json.dumps(data, ensure_ascii=False))
    if probe is not None:
        html = html.replace("__PROBE__", json.dumps(probe, ensure_ascii=False))
        html = html.replace("__BLURB__", json.dumps(TX.CATEGORY_BLURB, ensure_ascii=False))
        html = html.replace("__CATORDER__", json.dumps(TX.CATEGORIES, ensure_ascii=False))
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(html)
    return len(html)


FOLDER = DEST
os.makedirs(FOLDER, exist_ok=True)
a = write(os.path.join(FOLDER, "index.html"), CAND, candidate_data(), calc=True)
b = write(os.path.join(FOLDER, "grader.html"), GRADER, grader_data(), TX.PROBE_MAP)
c = write(os.path.join(FOLDER, "hr.html"), HR_DASHBOARD, grader_data(), TX.PROBE_MAP)

print("index.html:", a, "bytes | grader.html:", b, "bytes | hr.html:", c, "bytes")
print("answer positions in stored bank:", DIST)
