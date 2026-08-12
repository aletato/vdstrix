#!/usr/bin/env python3
"""Standalone web UI for launching Strix scans."""

import json
import os
import subprocess
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

# Store active scan processes
active_scans = {}
scan_counter = 0
scan_counter_lock = threading.Lock()

STRIX_SCRIPT = Path(__file__).parent / "strix-scan.sh"

class ScanLauncherHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Suppress default logging

    def do_GET(self):
        if self.path == "/" or self.path.startswith("/?"):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode())
        elif self.path == "/api/scans":
            self.send_json(200, {
                "scans": [
                    {
                        "id": scan_id,
                        "target": info["target"],
                        "mode": info["mode"],
                        "status": "running" if info["process"].poll() is None else "finished",
                        "pid": info["process"].pid
                    }
                    for scan_id, info in active_scans.items()
                ]
            })
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/api/start-scan":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode())

            target = data.get("target", "").strip()
            mode = data.get("mode", "standard")

            if not target:
                self.send_json(400, {"error": "Target is required"})
                return

            # Start the scan
            try:
                global scan_counter
                with scan_counter_lock:
                    scan_counter += 1
                    scan_id = scan_counter

                cmd = [str(STRIX_SCRIPT), "-t", target, "-n"]
                if mode != "standard":
                    cmd.extend(["-m", mode])

                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    cwd=str(STRIX_SCRIPT.parent)
                )

                active_scans[scan_id] = {
                    "target": target,
                    "mode": mode,
                    "process": process
                }

                self.send_json(200, {
                    "success": True,
                    "scan_id": scan_id,
                    "message": f"Scan started for {target}"
                })
            except Exception as e:
                self.send_json(500, {"error": str(e)})
        else:
            self.send_response(404)
            self.end_headers()

    def send_json(self, code, data):
        self.send_response(code)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())


HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Strix Scan Launcher</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
        }
        .header {
            text-align: center;
            color: white;
            margin-bottom: 40px;
        }
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        .header p {
            opacity: 0.9;
        }
        .card {
            background: white;
            border-radius: 12px;
            padding: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            font-weight: 600;
            margin-bottom: 8px;
            color: #333;
        }
        input, select {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        input:focus, select:focus {
            outline: none;
            border-color: #667eea;
        }
        .btn {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
        }
        .btn:hover {
            transform: translateY(-2px);
        }
        .btn:active {
            transform: translateY(0);
        }
        .btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        .scans-list {
            margin-top: 20px;
        }
        .scan-item {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .scan-info {
            flex: 1;
        }
        .scan-target {
            font-weight: 600;
            color: #333;
            margin-bottom: 4px;
        }
        .scan-details {
            font-size: 14px;
            color: #666;
        }
        .status-badge {
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
        }
        .status-running {
            background: #4ade80;
            color: white;
        }
        .status-finished {
            background: #94a3b8;
            color: white;
        }
        .alert {
            padding: 12px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        .alert-success {
            background: #d1fae5;
            color: #065f46;
            border: 1px solid #6ee7b7;
        }
        .alert-error {
            background: #fee2e2;
            color: #991b1b;
            border: 1px solid #fca5a5;
        }
        .hidden {
            display: none;
        }
        .links {
            text-align: center;
            margin-top: 20px;
        }
        .links a {
            color: white;
            text-decoration: none;
            margin: 0 15px;
            opacity: 0.9;
            transition: opacity 0.3s;
        }
        .links a:hover {
            opacity: 1;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛡️ Strix Scan Launcher</h1>
            <p>Start security scans and monitor your targets</p>
        </div>

        <div class="card">
            <h2 style="margin-bottom: 20px;">Start New Scan</h2>

            <div id="alertBox" class="alert hidden"></div>

            <form id="scanForm">
                <div class="form-group">
                    <label for="target">Target (URL or IP)</label>
                    <input
                        type="text"
                        id="target"
                        placeholder="example.com or 192.168.1.1"
                        required
                    >
                </div>

                <div class="form-group">
                    <label for="mode">Scan Mode</label>
                    <select id="mode">
                        <option value="quick">Quick - Fast reconnaissance</option>
                        <option value="standard" selected>Standard - Balanced approach</option>
                        <option value="deep">Deep - Comprehensive testing</option>
                    </select>
                </div>

                <button type="submit" class="btn" id="submitBtn">
                    🚀 Launch Scan
                </button>
            </form>
        </div>

        <div class="card">
            <h2 style="margin-bottom: 20px;">Active Scans</h2>
            <div id="scansList" class="scans-list">
                <p style="text-align: center; color: #666;">No active scans</p>
            </div>
        </div>

        <div class="links">
            <a href="http://127.0.0.1:8080" target="_blank">📊 View Scan Results</a>
            <a href="#" onclick="location.reload()">🔄 Refresh</a>
        </div>
    </div>

    <script>
        const form = document.getElementById('scanForm');
        const alertBox = document.getElementById('alertBox');
        const submitBtn = document.getElementById('submitBtn');
        const scansList = document.getElementById('scansList');

        function showAlert(message, type) {
            alertBox.textContent = message;
            alertBox.className = `alert alert-${type}`;
            setTimeout(() => {
                alertBox.className = 'alert hidden';
            }, 5000);
        }

        async function loadScans() {
            try {
                const response = await fetch('/api/scans');
                const data = await response.json();

                if (data.scans.length === 0) {
                    scansList.innerHTML = '<p style="text-align: center; color: #666;">No active scans</p>';
                    return;
                }

                scansList.innerHTML = data.scans.map(scan => `
                    <div class="scan-item">
                        <div class="scan-info">
                            <div class="scan-target">${scan.target}</div>
                            <div class="scan-details">
                                Mode: ${scan.mode} • PID: ${scan.pid} • ID: ${scan.id}
                            </div>
                        </div>
                        <span class="status-badge status-${scan.status}">
                            ${scan.status}
                        </span>
                    </div>
                `).join('');
            } catch (error) {
                console.error('Failed to load scans:', error);
            }
        }

        form.addEventListener('submit', async (e) => {
            e.preventDefault();

            const target = document.getElementById('target').value.trim();
            const mode = document.getElementById('mode').value;

            if (!target) {
                showAlert('Please enter a target', 'error');
                return;
            }

            submitBtn.disabled = true;
            submitBtn.textContent = '⏳ Starting scan...';

            try {
                const response = await fetch('/api/start-scan', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ target, mode })
                });

                const data = await response.json();

                if (response.ok) {
                    showAlert(`✅ ${data.message}`, 'success');
                    form.reset();
                    loadScans();
                } else {
                    showAlert(`❌ Error: ${data.error}`, 'error');
                }
            } catch (error) {
                showAlert(`❌ Failed to start scan: ${error.message}`, 'error');
            } finally {
                submitBtn.disabled = false;
                submitBtn.textContent = '🚀 Launch Scan';
            }
        });

        // Load scans on page load and every 3 seconds
        loadScans();
        setInterval(loadScans, 3000);
    </script>
</body>
</html>
"""


def run_server(port=9000):
    server = HTTPServer(('127.0.0.1', port), ScanLauncherHandler)
    url = f"http://127.0.0.1:{port}"

    print(f"\n{'='*60}")
    print(f"🛡️  Strix Scan Launcher")
    print(f"{'='*60}")
    print(f"\n✅ Server running at: {url}")
    print(f"📊 Viewer running at: http://127.0.0.1:8080")
    print(f"\n Press Ctrl+C to stop\n")

    # Open browser
    threading.Timer(1.0, lambda: webbrowser.open(url)).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down...")
        server.shutdown()


if __name__ == "__main__":
    run_server()
