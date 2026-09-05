#!/usr/bin/env python3
"""
Project Brain Dashboard Server
Auto-scans the project directory and serves the neural architecture visualization.
Status updates every 10 seconds automatically.
"""

import http.server
import threading
import time
import json
import os

DASHBOARD_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(DASHBOARD_DIR)
STATUS_FILE = os.path.join(DASHBOARD_DIR, "status.json")
PORT = 8080


def scan_project_status():
    """Scan the project directory and determine the status of each module."""
    def exists(rel_path):
        return os.path.exists(os.path.join(PROJECT_DIR, rel_path))

    def dir_has_model_files(rel_path):
        full_path = os.path.join(PROJECT_DIR, rel_path)
        if not os.path.isdir(full_path):
            return False
        exts = ('.pt', '.bin', '.safetensors', '.gguf')
        return any(f.endswith(exts) or f == 'adapter_config.json' for f in os.listdir(full_path))

    s = {}

    # Dataset
    s["dataset"] = "complete" if exists("data/raw/FracAtlas/FracAtlas/dataset.csv") else "pending"

    # Data Prep
    if exists("data/processed/train.json"):
        s["data_prep"] = "complete"
    elif exists("src/dataset_to_vlm.py"):
        s["data_prep"] = "in_progress"
    else:
        s["data_prep"] = "pending"

    # Pre-trained VLM
    s["pretrained"] = "complete"

    # Training
    if dir_has_model_files("models"):
        s["training"] = "complete"
    elif exists("notebooks/train_vlm.ipynb") or exists("src/train_vlm.py"):
        s["training"] = "in_progress"
    else:
        s["training"] = "pending"

    # Diagnostic Core
    s["core"] = "complete" if exists("src/inference.py") else "pending"

    # VQA Chat
    s["vqa"] = "complete" if exists("src/app.py") else "pending"

    # Report Generator
    s["reports"] = "complete" if exists("src/report_generator.py") else "pending"

    # Web Dashboard
    s["webui"] = s["vqa"]

    # Future Scope
    for mod in ["literature", "synth_reports", "diffusion", "sandbox"]:
        s[mod] = "future"

    return s


def update_status_file():
    try:
        data = {
            "last_updated": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "modules": scan_project_status()
        }
        with open(STATUS_FILE, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"[Error] Status scan failed: {e}")


def background_scanner():
    while True:
        update_status_file()
        time.sleep(10)


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass


def main():
    update_status_file()

    scanner = threading.Thread(target=background_scanner, daemon=True)
    scanner.start()

    os.chdir(DASHBOARD_DIR)
    server = http.server.HTTPServer(("", PORT), QuietHandler)

    print(f"\n{'='*50}")
    print(f"  🧠 Project Brain Dashboard")
    print(f"  URL: http://localhost:{PORT}")
    print(f"  Project: {PROJECT_DIR}")
    print(f"  Auto-refresh: every 10 seconds")
    print(f"{'='*50}\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nDashboard stopped.")
        server.server_close()


if __name__ == "__main__":
    main()
