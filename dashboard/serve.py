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
        for root, _, files in os.walk(full_path):
            if any(f.endswith(exts) or f == 'adapter_config.json' for f in files):
                return True
        return False

    s = {}

    # Dataset
    s["dataset"] = "complete" if (exists("data/raw/FracAtlas/FracAtlas/images") or exists("data/raw/FracAtlas/FracAtlas/dataset.csv")) else "pending"

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
    has_weights = dir_has_model_files("models")
    if has_weights:
        s["training"] = "complete"
    elif exists("notebooks/train_vlm.ipynb") or exists("src/train_vlm.py"):
        s["training"] = "in_progress"
    else:
        s["training"] = "pending"

    # Diagnostic Core (Requires trained model weights to be complete)
    if has_weights and exists("src/inference.py"):
        s["core"] = "complete"
    elif exists("src/inference.py"):
        s["core"] = "in_progress"  # Code scaffolded, awaiting fine-tuned weights
    else:
        s["core"] = "pending"

    # VQA Chat (Requires trained model weights to be complete)
    if has_weights and exists("src/app.py"):
        s["vqa"] = "complete"
    elif exists("src/app.py"):
        s["vqa"] = "in_progress"  # UI ready, awaiting model weights
    else:
        s["vqa"] = "pending"

    # Report Generator
    if has_weights and exists("src/report_generator.py"):
        s["reports"] = "complete"
    elif exists("src/report_generator.py"):
        s["reports"] = "in_progress"  # Template generator ready, awaiting neural output
    else:
        s["reports"] = "pending"

    # Web Dashboard
    s["webui"] = s["vqa"]

    # Future Scope
    for mod in ["literature", "synth_reports", "diffusion", "sandbox"]:
        s[mod] = "future"

    return s


def get_project_metrics():
    """Gather live count metrics from the workspace."""
    def count_json_samples(rel_path):
        p = os.path.join(PROJECT_DIR, rel_path)
        if os.path.exists(p):
            try:
                with open(p, 'r', encoding='utf-8') as f:
                    d = json.load(f)
                    return len(d) if isinstance(d, list) else 0
            except:
                pass
        return 0

    reports_dir = os.path.join(PROJECT_DIR, "reports")
    rep_count = len([f for f in os.listdir(reports_dir) if f.endswith(('.txt', '.pdf'))]) if os.path.exists(reports_dir) else 0

    return {
        "raw_images": 4083 if os.path.exists(os.path.join(PROJECT_DIR, "data/raw/FracAtlas/FracAtlas/images")) else 0,
        "train_samples": count_json_samples("data/processed/train.json"),
        "val_samples": count_json_samples("data/processed/val.json"),
        "test_samples": count_json_samples("data/processed/test.json"),
        "total_conversations": count_json_samples("data/processed/train.json") + count_json_samples("data/processed/val.json") + count_json_samples("data/processed/test.json"),
        "reports_generated": rep_count
    }


def update_status_file():
    try:
        data = {
            "last_updated": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "modules": scan_project_status(),
            "metrics": get_project_metrics()
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
    def do_GET(self):
        # Route alias mapping
        if self.path in ('/docs', '/docs/'):
            self.path = '/docs.html'
        elif self.path in ('/architecture', '/arch', '/arch/'):
            self.path = '/index.html'
        return super().do_GET()

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
