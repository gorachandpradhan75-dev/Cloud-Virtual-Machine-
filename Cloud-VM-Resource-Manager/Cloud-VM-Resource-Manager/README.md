# Cloud VM Resource Manager

A beginner-friendly, runnable academic project for the **Cloud Virtualization** subject. It demonstrates a cloud-style VM dashboard, VM inventory, lifecycle operations, simulated resource monitoring, and rule-based optimization suggestions.

## Important: simulation vs real virtualization

This project runs locally and simulates virtual machines and their CPU/RAM/disk telemetry. Start, stop, and restart actions update the demo inventory; they do **not** create or control real VMware, VirtualBox, KVM, AWS, or Azure instances. This keeps the project safe and runnable on a standard Windows/Linux laptop without a hypervisor account.

## Requirements

- Python 3.9 or newer
- A modern browser
- No third-party Python packages required

## Run on Windows

1. Extract the ZIP file.
2. Open the `Cloud-VM-Resource-Manager` folder.
3. Double-click `run.bat`.
4. Open **http://127.0.0.1:8000** in Chrome or Edge.
5. Keep the terminal window open while using the app. Press `Ctrl+C` in it to stop the server.

If the browser does not open automatically, enter the URL manually.

## Run on Linux/macOS

```bash
python3 app.py
```
Then open http://127.0.0.1:8000.

## Features

- Dashboard summary: total, running, stopped, average CPU.
- VM inventory with vCPU, RAM, disk, OS, and status.
- Create a demo VM.
- Start, stop, and restart VM lifecycle actions.
- Simulated CPU, RAM, and disk telemetry refreshes every 3.5 seconds.
- Rule-based optimization insights for low or high resource utilization.
- Local JSON persistence in `data/vms.json`.
- Responsive web UI.

## Project structure

```text
Cloud-VM-Resource-Manager/
├── app.py                 # Python HTTP server and JSON API
├── run.bat                # Windows one-click launcher
├── README.md              # Setup and project guide
├── data/
│   └── vms.json           # Demo VM inventory
└── web/
    ├── index.html         # Dashboard layout
    └── static/
        ├── style.css     # Dashboard styling
        └── app.js        # Frontend logic and API calls
```

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/health` | Server health |
| GET | `/api/vms` | List VMs and refresh simulated metrics |
| POST | `/api/vms` | Create a VM |
| POST | `/api/vms/{id}/action` | `start`, `stop`, or `restart` |

Example action body:

```json
{"action": "start"}
```

## Concepts demonstrated

- Cloud computing resource pooling (illustrative)
- Server virtualization and virtual machine abstraction
- VM provisioning and lifecycle management
- CPU, memory, and storage utilization
- Monitoring and threshold-based alerts
- Resource allocation and optimization
- Web client/API/data-layer architecture

## Troubleshooting

- **Python not found:** install Python 3.9+ from https://www.python.org/downloads/ and enable “Add Python to PATH”.
- **Port 8000 is busy:** close the other application using it, or change `8000` in the final line of `app.py` and the printed URL.
- **Page not loading:** confirm the terminal says the server is starting and use `http://127.0.0.1:8000`.
- **Metrics keep changing:** this is expected; values are generated for demonstration.

## Suggested viva explanation

“This project is a Cloud Virtual Machine Resource Manager prototype. It provides a web dashboard to provision demo VM records, manage their lifecycle, monitor resource utilization, and view optimization recommendations. The current build uses a simulation layer so it can run on a normal laptop without connecting to a hypervisor. The same API layer can later be integrated with a real virtualization platform such as KVM/libvirt or a cloud provider.”

## Future scope

- Integrate KVM/libvirt or VMware APIs for real VM provisioning.
- Add authentication, role-based access, and audit logs.
- Store historical metrics in PostgreSQL.
- Add real-time monitoring with Prometheus.
- Add cloud billing data and more advanced optimization models.
