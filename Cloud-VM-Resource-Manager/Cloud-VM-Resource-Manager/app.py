from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
import json, random, time, threading

ROOT = Path(__file__).parent
DATA_FILE = ROOT / "data" / "vms.json"
lock = threading.Lock()

def load_vms():
    with lock:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))

def save_vms(vms):
    with lock:
        DATA_FILE.write_text(json.dumps(vms, indent=2), encoding="utf-8")

def metrics(vms):
    now = int(time.time())
    for vm in vms:
        if vm["status"] == "Running":
            # Demo telemetry: generated values, not readings from a real hypervisor.
            vm["cpu"] = max(2, min(98, round(vm["cpu"] + random.uniform(-8, 8), 1)))
            vm["ram"] = max(5, min(96, round(vm["ram"] + random.uniform(-4, 4), 1)))
            vm["disk"] = min(95, max(10, round(vm["disk"] + random.uniform(-0.2, 0.2), 1)))
            vm["updated_at"] = now
        else:
            vm["cpu"] = 0
    return vms

class Handler(BaseHTTPRequestHandler):
    def send_json(self, data, status=200):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/api/vms":
            self.send_json(metrics(load_vms()))
        elif path == "/api/health":
            self.send_json({"status": "ok", "mode": "simulation"})
        elif path == "/":
            page = (ROOT / "web" / "index.html").read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(page)))
            self.end_headers()
            self.wfile.write(page)
        elif path.startswith("/static/"):
            name = path.rsplit("/", 1)[-1]
            target = ROOT / "web" / "static" / name
            if not target.exists() or target.parent != (ROOT / "web" / "static"):
                self.send_error(404); return
            content_type = "text/css" if name.endswith(".css") else "application/javascript"
            data = target.read_bytes()
            self.send_response(200); self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(data))); self.end_headers(); self.wfile.write(data)
        else:
            self.send_error(404)

    def do_POST(self):
        path = urlparse(self.path).path
        try:
            payload = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0)) or 0) or b"{}")
        except Exception:
            self.send_json({"error": "Invalid JSON"}, 400); return
        vms = load_vms()
        if path.startswith("/api/vms/") and path.endswith("/action"):
            vm_id = path.split("/")[3]
            vm = next((x for x in vms if x["id"] == vm_id), None)
            if not vm:
                self.send_json({"error": "VM not found"}, 404); return
            action = payload.get("action")
            if action == "start": vm["status"] = "Running"
            elif action == "stop": vm["status"] = "Stopped"; vm["cpu"] = 0
            elif action == "restart": vm["status"] = "Running"; vm["cpu"] = 8
            else:
                self.send_json({"error": "Action must be start, stop, or restart"}, 400); return
            vm["updated_at"] = int(time.time()); save_vms(vms)
            self.send_json({"message": f"{vm['name']} {action} action completed in simulation", "vm": vm})
        elif path == "/api/vms":
            name = str(payload.get("name", "")).strip()
            if not name:
                self.send_json({"error": "VM name is required"}, 400); return
            vm_id = "vm-" + str(int(time.time() * 1000))[-6:]
            vm = {"id": vm_id, "name": name[:32], "os": payload.get("os", "Ubuntu Linux"),
                  "cpu_cores": int(payload.get("cpu_cores", 2)), "ram_gb": int(payload.get("ram_gb", 4)),
                  "disk_gb": int(payload.get("disk_gb", 40)), "status": "Stopped",
                  "cpu": 0, "ram": 8, "disk": 12, "updated_at": int(time.time())}
            vms.append(vm); save_vms(vms); self.send_json(vm, 201)
        else:
            self.send_error(404)

    def log_message(self, fmt, *args):
        print("%s - %s" % (self.address_string(), fmt % args))

if __name__ == "__main__":
    print("\\nCloud VM Resource Manager is starting...")
    print("Open http://127.0.0.1:8000 in your browser. Press Ctrl+C to stop.\\n")
    ThreadingHTTPServer(("127.0.0.1", 8000), Handler).serve_forever()
