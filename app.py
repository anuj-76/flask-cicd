import socket, time
from datetime import datetime, timezone
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)
START = time.time()

PAGE = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>CI/CD Dashboard</title>
  <style>
    body { margin:0; font-family:Arial,sans-serif; background:#0f172a; color:#e2e8f0;
           display:flex; justify-content:center; padding:40px 16px; }
    .card { background:#1e293b; border-radius:16px; padding:28px; max-width:520px; width:100%; }
    h1 { margin:0 0 6px; font-size:26px; }
    .sub { color:#94a3b8; margin-bottom:20px; }
    .badge { display:inline-block; background:#64748b; color:#fff; padding:4px 12px;
             border-radius:999px; font-size:13px; margin-bottom:20px; }
    .badge.ok { background:#16a34a; }
    .badge.bad { background:#dc2626; }
    .row { display:flex; justify-content:space-between; padding:10px 0;
           border-bottom:1px solid #334155; }
    .row span:first-child { color:#94a3b8; }
    .stages { margin-top:20px; display:flex; flex-wrap:wrap; gap:8px; }
    .stage { background:#334155; padding:6px 12px; border-radius:8px; font-size:13px; }
  </style>
</head>
<body>
  <div class="card">
    <h1>CI/CD Dashboard</h1>
    <div class="sub">Flask on Docker + Kubernetes (k3s) on AWS EC2 - v2</div>
    <div class="badge" id="badge">Checking...</div>
    <div class="row"><span>Pod name</span><span>{{ pod }}</span></div>
    <div class="row"><span>Server time (UTC)</span><span>{{ now }}</span></div>
    <div class="row"><span>Deployed by</span><span>GitHub Actions</span></div>
    <div class="stages">
      <span class="stage">Test</span>
      <span class="stage">Build</span>
      <span class="stage">Push to ECR</span>
      <span class="stage">Deploy to k3s</span>
    </div>
  </div>
  <script>
    async function check() {
      var b = document.getElementById('badge');
      try {
        var r = await fetch('/health');
        if (!r.ok) throw new Error('bad status');
        var d = await r.json();
        b.textContent = 'Healthy - ' + d.pod + ' - up ' + d.uptime_seconds + 's';
        b.className = 'badge ok';
      } catch (e) {
        b.textContent = 'Down';
        b.className = 'badge bad';
      }
    }
    check();
    setInterval(check, 5000);
  </script>
</body>
</html>
"""

@app.route("/")
def home():
    now = datetime.now(timezone.utc).strftime("%d %b %Y, %H:%M:%S")
    return render_template_string(PAGE, pod=socket.gethostname(), now=now)

@app.route("/health")
def health():
    return jsonify(
        status="ok",
        pod=socket.gethostname(),
        uptime_seconds=int(time.time() - START),
    )