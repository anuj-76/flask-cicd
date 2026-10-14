import socket, time
from flask import Flask, jsonify, Response

app = Flask(__name__)
START = time.time()
POD = socket.gethostname()

PAGE = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CI/CD Dashboard</title>
<style>
:root{--mut:#94a3b8;--line:rgba(255,255,255,.09)}
*{box-sizing:border-box}
body{margin:0;color:#e2e8f0;font-family:Inter,"Segoe UI",system-ui,sans-serif;background:#0b1020;
background-image:radial-gradient(900px 420px at 12% -10%,rgba(99,102,241,.28),transparent),radial-gradient(800px 400px at 95% 0,rgba(34,197,94,.14),transparent)}
.wrap{max-width:1000px;margin:0 auto;padding:36px 18px 48px}
header{display:flex;justify-content:space-between;align-items:flex-start;gap:16px;flex-wrap:wrap}
.eyebrow{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:#a5b4fc}
h1{margin:6px 0 8px;font-size:34px;letter-spacing:-.02em}
.sub{margin:0;max-width:560px;color:var(--mut);line-height:1.55}
h2{margin:34px 0 4px;font-size:18px}
.note{margin:0 0 14px;font-size:13px;color:var(--mut)}
.status{display:flex;align-items:center;gap:8px;padding:8px 16px;border-radius:999px;font-weight:600;font-size:14px;border:1px solid var(--line);background:rgba(255,255,255,.05)}
.status .dot{width:9px;height:9px;border-radius:50%;background:#64748b}
.status.ok{color:#4ade80}.status.ok .dot{background:#22c55e;box-shadow:0 0 10px #22c55e}
.status.bad{color:#f87171}.status.bad .dot{background:#ef4444;box-shadow:0 0 10px #ef4444}
.card{background:rgba(255,255,255,.045);border:1px solid var(--line);border-radius:16px;backdrop-filter:blur(10px)}
.pipeline{display:flex;align-items:stretch}
.step{flex:1;min-width:0;padding:16px 14px;border-radius:14px;background:rgba(255,255,255,.045);border:1px solid var(--line);animation:glow 7.2s infinite;animation-delay:calc(var(--i)*1.2s)}
.num{font:600 12px ui-monospace,Consolas,monospace;color:#93c5fd}
.step b{display:block;margin:6px 0 4px;font-size:15px}
.step span{font-size:12px;color:var(--mut);line-height:1.4}
.link{flex:0 0 34px;position:relative;align-self:center;height:2px;background:rgba(255,255,255,.12)}
.link::after{content:"";position:absolute;top:-3px;left:0;width:8px;height:8px;border-radius:50%;background:#60a5fa;box-shadow:0 0 10px #60a5fa;animation:travel 1.8s linear infinite}
@keyframes travel{from{left:0;opacity:0}20%{opacity:1}to{left:calc(100% - 8px);opacity:0}}
@keyframes travelv{from{top:0;opacity:0}20%{opacity:1}to{top:calc(100% - 8px);opacity:0}}
@keyframes glow{0%,16%{border-color:rgba(96,165,250,.85);box-shadow:0 0 26px rgba(96,165,250,.28)}17%,100%{border-color:rgba(255,255,255,.09);box-shadow:none}}
@keyframes flash{from{box-shadow:0 0 0 2px rgba(34,197,94,.8),0 0 28px rgba(34,197,94,.35)}to{box-shadow:none}}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px;margin-bottom:12px}
.stat{padding:14px 16px}.stat small{display:block;font-size:12px;color:var(--mut);margin-bottom:6px}
.stat b{font-size:22px;font-variant-numeric:tabular-nums}.stat b.sm{font-size:14px;font-family:ui-monospace,Consolas,monospace}
.pods{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:12px}
.pod{padding:16px}.pod.hit{animation:flash 1s ease-out}.pod.gone{opacity:.5}
.top{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px}
.pill{font-size:12px;font-weight:600;padding:3px 10px;border-radius:999px}
.pill.ok{background:rgba(34,197,94,.16);color:#4ade80}.pill.bad{background:rgba(239,68,68,.16);color:#f87171}
.mini{font-size:11px;color:#a5b4fc}
.pname{font:600 14px ui-monospace,Consolas,monospace;word-break:break-all;margin-bottom:10px}
.kv{display:flex;justify-content:space-between;padding:7px 0;border-top:1px solid var(--line);font-size:13px}
.kv span{color:var(--mut)}
ul{list-style:none;margin:0;padding:0}
#events li{padding:10px 14px;font-size:13px;border-bottom:1px solid var(--line)}
#events li:last-child{border:0}
time{display:inline-block;min-width:100px;color:var(--mut);font-family:ui-monospace,Consolas,monospace;font-size:12px}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:34px}
.chips span{font-size:12px;padding:5px 12px;border-radius:999px;border:1px solid var(--line);color:#cbd5e1;background:rgba(255,255,255,.04)}
footer{margin-top:16px;font-size:12px;color:var(--mut)}
@media(max-width:820px){.pipeline{flex-direction:column}.link{flex:0 0 26px;width:2px;height:26px;align-self:center}
.link::after{left:-3px;top:0;animation-name:travelv}h1{font-size:28px}}
</style></head>
<body><div class="wrap">
<header>
<div><div class="eyebrow">AWS &middot; Docker &middot; Kubernetes</div>
<h1>CI/CD Dashboard</h1>
<p class="sub">Every push to the main branch is tested, built and deployed automatically, with a health check confirming each release.</p></div>
<div class="status" id="status"><span class="dot"></span><span id="statusText">Checking</span></div>
</header>

<h2>Delivery pipeline</h2>
<p class="note">How a code change reaches the cluster (illustrative flow)</p>
<div class="pipeline">
<div class="step" style="--i:0"><div class="num">01</div><b>Push</b><span>Code is pushed to the main branch</span></div><div class="link"></div>
<div class="step" style="--i:1"><div class="num">02</div><b>Test</b><span>pytest validates the application</span></div><div class="link"></div>
<div class="step" style="--i:2"><div class="num">03</div><b>Build</b><span>A Docker image is built</span></div><div class="link"></div>
<div class="step" style="--i:3"><div class="num">04</div><b>Registry</b><span>Image is pushed to Amazon ECR</span></div><div class="link"></div>
<div class="step" style="--i:4"><div class="num">05</div><b>Deploy</b><span>Rolling update on Kubernetes (k3s)</span></div><div class="link"></div>
<div class="step" style="--i:5"><div class="num">06</div><b>Verify</b><span>Health check confirms the release</span></div>
</div>

<h2>Live cluster view</h2>
<p class="note">Pods are discovered from live health checks and refreshed every 2 seconds</p>
<div class="stats">
<div class="card stat"><small>Active pods</small><b id="active">0</b></div>
<div class="card stat"><small>Page served by</small><b class="sm">__POD__</b></div>
<div class="card stat"><small>Health checks</small><b id="checks">0</b></div>
<div class="card stat"><small>Time (UTC)</small><b id="clock">--:--:--</b></div>
</div>
<div class="pods" id="pods"></div>

<h2>Recent events</h2>
<div class="card"><ul id="events"><li>Waiting for activity</li></ul></div>

<div class="chips"><span>Flask</span><span>pytest</span><span>Docker</span><span>GitHub Actions</span><span>Amazon ECR</span><span>Amazon EC2</span><span>Kubernetes (k3s)</span></div>
<footer>Deployed automatically by GitHub Actions</footer>
</div>
<script>
var SELF="__POD__",pods={},events=[],checks=0,lastPod="";
function $(id){return document.getElementById(id);}
function fmt(s){var m=Math.floor(s/60);return m>0?m+"m "+(s%60)+"s":s+"s";}
function log(m){events.unshift({t:new Date().toISOString().substr(11,8),m:m});events=events.slice(0,6);}
function setStatus(ok){$("status").className="status "+(ok?"ok":"bad");$("statusText").textContent=ok?"Healthy":"Unreachable";}
function render(){
  var now=Date.now(),active=0,html="";
  Object.keys(pods).sort().forEach(function(n){
    var p=pods[n],age=now-p.last,live=age<15000;
    if(age>90000){delete pods[n];return;}
    if(live)active++;
    if(!live&&p.state!=="gone"){p.state="gone";log("Pod "+n+" stopped responding");}
    html+='<div class="card pod'+(live?"":" gone")+(n===lastPod&&live?" hit":"")+'">'+
      '<div class="top"><span class="pill '+(live?"ok":"bad")+'">'+(live?"Active":"Not responding")+'</span>'+
      (n===SELF?'<span class="mini">Served this page</span>':"")+'</div>'+
      '<div class="pname">'+n+'</div>'+
      '<div class="kv"><span>Health checks answered</span><b>'+p.hits+'</b></div>'+
      '<div class="kv"><span>Uptime</span><b>'+fmt(p.up)+'</b></div></div>';
  });
  $("pods").innerHTML=html;
  $("active").textContent=active;
  $("checks").textContent=checks;
  $("events").innerHTML=events.map(function(e){return "<li><time>"+e.t+" UTC</time>"+e.m+"</li>";}).join("")||"<li>Waiting for activity</li>";
}
async function poll(){
  try{
    var r=await fetch("/health",{cache:"no-store"});
    if(!r.ok)throw new Error("bad status");
    var d=await r.json();
    checks++;
    var p=pods[d.pod];
    if(!p){p=pods[d.pod]={hits:0,state:"live"};log("Pod "+d.pod+" detected");}
    if(p.state==="gone"){p.state="live";log("Pod "+d.pod+" is responding again");}
    p.hits++;p.last=Date.now();p.up=d.uptime_seconds;lastPod=d.pod;
    setStatus(true);
  }catch(e){setStatus(false);}
  render();
}
function tick(){$("clock").textContent=new Date().toISOString().substr(11,8);}
setInterval(poll,2000);setInterval(tick,1000);tick();poll();
</script></body></html>"""


@app.route("/")
def home():
    return Response(PAGE.replace("__POD__", POD), mimetype="text/html")


@app.route("/health")
def health():
    res = jsonify(status="ok", pod=POD, uptime_seconds=int(time.time() - START))
    res.headers["Cache-Control"] = "no-store"
    return res