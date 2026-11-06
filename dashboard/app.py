from flask import Flask, jsonify, render_template_string
import socket
import time

app = Flask(__name__)

# Estimation indicative uniquement : a actualiser avec les donnees du reseau/pool.
NETWORK_HASHRATE = 500_000_000_000  # 500 GH/s, hypothese fixe
BLOCK_REWARD = 3.0                  # VRSC par bloc, hypothese fixe
VRSC_EUR = 0.146                    # cours indicatif fixe, pas un cours en direct


def miner_command(command):
    try:
        with socket.create_connection(("127.0.0.1", 4068), timeout=2) as s:
            s.settimeout(2)
            s.sendall((command + "\n").encode())
            return s.recv(8192).decode(errors="replace").strip()
    except OSError:
        return ""


def parse_fields(raw):
    result = {}
    for item in raw.replace("\n", ";").split(";"):
        if "=" in item:
            key, value = item.split("=", 1)
            result[key.strip()] = value.strip()
    return result


def get_stats():
    summary = parse_fields(miner_command("summary"))
    raw_threads = miner_command("threads")
    threads = []

    for block in raw_threads.split("|"):
        fields = parse_fields(block)
        if "GPU" in fields:
            try:
                thread_hashrate = float(fields.get("KHS", "0"))
            except ValueError:
                thread_hashrate = 0.0
            threads.append({
                "id": fields.get("GPU", "?"),
                "hashrate": thread_hashrate,
                "accepted": fields.get("ACC", "0"),
                "rejected": fields.get("REJ", "0"),
                "temperature": fields.get("TEMP", "0")
            })

    # La reponse summary ne fournit pas toujours KHS : dans ce cas,
    # on additionne les hashrates des threads retournes par l'API.
    try:
        hashrate = float(summary.get("KHS", summary.get("KH", "nan")))
        if hashrate != hashrate:  # NaN
            raise ValueError
    except (ValueError, TypeError):
        hashrate = sum(t["hashrate"] for t in threads)

    daily_vrsc = (hashrate * 1000 / NETWORK_HASHRATE) * 1440 * BLOCK_REWARD

    return {
        "connected": bool(summary),
        "name": summary.get("NAME", "Primo ARM Miner"),
        "version": summary.get("VER", "?"),
        "algorithm": summary.get("ALGO", "Verus"),
        "hashrate": hashrate,
        "accepted": summary.get("ACC", "0"),
        "rejected": summary.get("REJ", "0"),
        "uptime": summary.get("UPTIME", "0"),
        "threads": threads,
        "estimate_hour": daily_vrsc / 24,
        "estimate_day": daily_vrsc,
        "estimate_week": daily_vrsc * 7,
        "estimate_month": daily_vrsc * 30,
        "vrsc_eur": VRSC_EUR,
        "updated": time.strftime("%H:%M:%S")
    }


PAGE = """
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Miner-xmsrep</title>
<style>
*{box-sizing:border-box}
body{margin:0;background:#0b1020;color:#edf2ff;font-family:Arial,sans-serif;padding:22px}
main{max-width:850px;margin:auto}
header{display:flex;justify-content:space-between;align-items:center;margin-bottom:25px}
h1{font-size:25px;margin:0}
.sub{color:#8d9ab5;font-size:13px;margin-top:7px}
.status{background:#183b2c;color:#67e6a3;padding:9px 13px;border-radius:20px;font-size:12px}
.grid{display:grid;grid-template-columns:repeat(2,1fr);gap:14px}
.card{background:#151d32;border:1px solid #26324d;border-radius:16px;padding:20px}
.label{color:#92a1bd;font-size:13px}
.value{font-size:29px;font-weight:bold;margin-top:12px}
.unit{font-size:13px;color:#92a1bd}
.wide{grid-column:1/-1}
h2{font-size:17px;margin:0 0 16px}
.thread{display:flex;justify-content:space-between;gap:10px;padding:13px 0;border-top:1px solid #29344d}
.green{color:#65e6a0}
.red{color:#ff8585}
footer{text-align:center;color:#71809e;font-size:12px;margin-top:25px}
@media(max-width:480px){body{padding:15px}.value{font-size:24px}}
</style>
</head>
<body>
<main>
<header>
<div><h1>⛏ Miner-xmsrep</h1><div class="sub">VerusHash · Galaxy A21s</div></div>
<div class="status" id="status">Connexion...</div>
</header>
<div class="grid">
<div class="card">
<div class="label">Hashrate total</div>
<div class="value" id="hash">--</div>
<div class="unit">kH/s</div>
</div>
<div class="card">
<div class="label">Shares acceptées</div>
<div class="value green" id="accepted">--</div>
</div>
<div class="card">
<div class="label">Shares rejetées</div>
<div class="value red" id="rejected">--</div>
</div>
<div class="card">
<div class="label">Temps de fonctionnement</div>
<div class="value" id="uptime">--</div>
</div>
<div class="card wide">
<h2>Performances des threads CPU</h2>
<div id="threads">En attente des données...</div>
</div>
<div class="card wide">
<div class="label">Mineur</div>
<div class="value" style="font-size:19px" id="miner">Primo ARM Miner</div>
<div class="sub" id="updated">En attente...</div>
</div>
<div class="card wide">
<h2>Estimation des gains</h2>
<div class="sub">Estimation théorique brute · avant frais</div>
<div class="thread"><span>Par heure</span><b id="gain-hour">--</b></div>
<div class="thread"><span>Par jour</span><b id="gain-day">--</b></div>
<div class="thread"><span>Par semaine</span><b id="gain-week">--</b></div>
<div class="thread"><span>Par mois</span><b id="gain-month">--</b></div>
<div class="sub" id="gain-price">Cours VRSC : --</div>
</div>
</div>
<footer>Actualisation automatique · Données locales du mineur</footer>
</main>
<script>
function duration(s){
 s=Number(s)||0;
 return Math.floor(s/3600)+" h "+Math.floor(s%3600/60)+" min";
}
async function refresh(){
 try{
  const r=await fetch('/api/stats');
  const d=await r.json();
  document.getElementById('status').textContent=d.connected?'● Mineur connecté':'● Mineur hors ligne';
  document.getElementById('hash').textContent=Number(d.hashrate).toFixed(2);
  document.getElementById('accepted').textContent=d.accepted;
  document.getElementById('rejected').textContent=d.rejected;
  document.getElementById('uptime').textContent=duration(d.uptime);
  document.getElementById('miner').textContent=d.name+' · '+d.version;
  document.getElementById('updated').textContent='Dernière lecture : '+d.updated;
  const fmt=n=>Number(n).toFixed(6);
  ['hour','day','week','month'].forEach(period=>{
   const v=Number(d['estimate_'+period])||0;
   document.getElementById('gain-'+period).textContent=
    fmt(v)+' VRSC · '+(v*Number(d.vrsc_eur)).toFixed(6)+' €';
  });
  document.getElementById('gain-price').textContent=
   'Cours indicatif : '+Number(d.vrsc_eur).toFixed(3)+' € / VRSC';
  document.getElementById('threads').innerHTML=d.threads.length?
   d.threads.map(t=>'<div class="thread"><span>CPU '+t.id+
   '</span><b>'+Number(t.hashrate).toFixed(2)+' kH/s</b></div>').join(''):
   'Aucune donnée de thread disponible';
 }catch(e){
  document.getElementById('status').textContent='Connexion impossible';
 }
}
refresh();
setInterval(refresh,3000);
</script>
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(PAGE)


@app.route("/api/stats")
def api_stats():
    return jsonify(get_stats())


if __name__ == "__main__":
    # Ecoute locale uniquement : ne pas exposer ce tableau de bord sur Internet.
    app.run(host="127.0.0.1", port=5000, debug=False)
