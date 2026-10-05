#!/usr/bin/env python3
"""
FracAtlas Simple Diagnostic Testing Workstation
===============================================
Clean, straightforward, minimalistic interface for testing:
  - Select test X-ray from presets or upload an image
  - Click "Diagnose" to see Fracture/Normal status, confidence, findings, impression
  - Ask clinical VQA questions
  - Generate clinical report
"""

import os
import sys
import json
import time
import base64
import argparse
import urllib.parse
from http.server import HTTPServer, SimpleHTTPRequestHandler

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SRC_DIR)
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from inference import MedicalVLMInferenceEngine
from report_generator import generate_clinical_report

engine = MedicalVLMInferenceEngine()
engine.load_model()


def get_sample_images():
    samples = []
    frac_dir = os.path.join(PROJECT_DIR, "data/raw/FracAtlas/FracAtlas/images/Fractured")
    norm_dir = os.path.join(PROJECT_DIR, "data/raw/FracAtlas/FracAtlas/images/Non_fractured")

    if os.path.exists(frac_dir):
        for f in sorted(os.listdir(frac_dir))[:6]:
            if f.lower().endswith(('.jpg', '.jpeg', '.png')):
                samples.append({
                    "id": f,
                    "label": f"[Fractured] {f}",
                    "path": os.path.join("data/raw/FracAtlas/FracAtlas/images/Fractured", f)
                })

    if os.path.exists(norm_dir):
        for f in sorted(os.listdir(norm_dir))[:6]:
            if f.lower().endswith(('.jpg', '.jpeg', '.png')):
                samples.append({
                    "id": f,
                    "label": f"[Normal] {f}",
                    "path": os.path.join("data/raw/FracAtlas/FracAtlas/images/Non_fractured", f)
                })
    return samples


class SimpleAppHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)

        if parsed.path == "/api/samples":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(get_sample_images()).encode("utf-8"))
            return

        if parsed.path.startswith("/image/"):
            rel_path = urllib.parse.unquote(parsed.path[7:])
            full_path = os.path.join(PROJECT_DIR, rel_path)
            if os.path.exists(full_path):
                self.send_response(200)
                content_type = "image/jpeg" if full_path.endswith((".jpg", ".jpeg")) else "image/png"
                self.send_header("Content-Type", content_type)
                self.end_headers()
                with open(full_path, "rb") as f:
                    self.wfile.write(f.read())
                return
            else:
                self.send_error(404, "Image not found")
                return

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(HTML_CONTENT.encode("utf-8"))

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)

        try:
            req = json.loads(post_data.decode("utf-8"))
        except Exception:
            req = {}

        if parsed.path == "/api/diagnose":
            image_path = req.get("image_path")
            image_base64 = req.get("image_base64")

            if image_base64:
                temp_dir = os.path.join(PROJECT_DIR, "data", "temp_uploads")
                os.makedirs(temp_dir, exist_ok=True)
                target_path = os.path.join(temp_dir, f"upload_{int(time.time()*1000)}.jpg")
                if "," in image_base64:
                    image_base64 = image_base64.split(",")[1]
                with open(target_path, "wb") as f:
                    f.write(base64.b64decode(image_base64))
            elif image_path:
                target_path = os.path.join(PROJECT_DIR, image_path) if not os.path.isabs(image_path) else image_path
            else:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "No image provided"}).encode("utf-8"))
                return

            try:
                diag = engine.diagnose_xray(target_path)
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(diag).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
            return

        if parsed.path == "/api/vqa":
            image_path = req.get("image_path")
            question = req.get("question", "")
            target_path = os.path.join(PROJECT_DIR, image_path) if not os.path.isabs(image_path) else image_path

            try:
                answer = engine.answer_query(target_path, question)
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"answer": answer}).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
            return

        if parsed.path == "/api/report":
            image_path = req.get("image_path")
            target_path = os.path.join(PROJECT_DIR, image_path) if not os.path.isabs(image_path) else image_path

            try:
                diag = engine.diagnose_xray(target_path)
                rep = generate_clinical_report(diag, output_dir=os.path.join(PROJECT_DIR, "reports"))
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({
                    "report_text": rep["report_text"]
                }).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
            return

        self.send_error(404, "Endpoint not found")


HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>FracAtlas VLM Diagnostic Test Interface</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 30px;
            background: #f8fafc;
            color: #0f172a;
        }
        .container {
            max-width: 1000px;
            margin: 0 auto;
            background: #ffffff;
            border: 1px solid #cbd5e1;
            border-radius: 8px;
            padding: 24px;
        }
        h1 { margin-top: 0; font-size: 22px; border-bottom: 2px solid #e2e8f0; padding-bottom: 10px; }
        .row { display: flex; gap: 20px; margin-top: 15px; }
        .col { flex: 1; }
        label { font-weight: bold; font-size: 14px; display: block; margin-bottom: 6px; }
        select, input[type="file"], input[type="text"], button {
            padding: 8px 12px;
            border: 1px solid #94a3b8;
            border-radius: 4px;
            font-size: 14px;
        }
        select { width: 100%; }
        button {
            background: #2563eb;
            color: #ffffff;
            font-weight: bold;
            cursor: pointer;
            border: none;
        }
        button:hover { background: #1d4ed8; }
        .btn-secondary { background: #475569; }
        .btn-secondary:hover { background: #334155; }
        .img-box {
            width: 100%;
            height: 320px;
            background: #000;
            border: 1px solid #94a3b8;
            border-radius: 4px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-top: 10px;
        }
        .img-box img { max-width: 100%; max-height: 100%; object-fit: contain; }
        .result-box {
            background: #f1f5f9;
            border: 1px solid #cbd5e1;
            border-radius: 4px;
            padding: 14px;
            margin-top: 15px;
            min-height: 160px;
            font-family: monospace;
            font-size: 13px;
            white-space: pre-wrap;
            line-height: 1.5;
        }
        .status-positive { color: #dc2626; font-weight: bold; font-size: 16px; }
        .status-negative { color: #16a34a; font-weight: bold; font-size: 16px; }
        .chat-row { display: flex; gap: 8px; margin-top: 10px; }
        .chat-row input { flex: 1; }
    </style>
</head>
<body>

<div class="container">
    <h1>🦴 FracAtlas VLM Diagnostic Test Interface</h1>

    <div class="row">
        <!-- LEFT: Controls & Image -->
        <div class="col">
            <label>1. Select Sample Radiograph:</label>
            <select id="sampleSelect" onchange="onSelectSample()">
                <option value="">-- Loading samples --</option>
            </select>

            <div style="margin-top: 12px;">
                <label>OR Upload Custom X-Ray:</label>
                <input type="file" id="uploadInput" accept="image/*" onchange="onUploadImage(event)">
            </div>

            <div class="img-box">
                <img id="previewImg" src="" alt="Selected Radiograph Preview" style="display:none;">
                <span id="noImgText" style="color: #94a3b8;">No radiograph selected</span>
            </div>

            <div style="margin-top: 15px; display: flex; gap: 10px;">
                <button onclick="runDiagnosis()">🔍 Run Diagnosis</button>
                <button class="btn-secondary" onclick="generateReport()">📄 Generate Report</button>
            </div>
        </div>

        <!-- RIGHT: Results & Med-VQA -->
        <div class="col">
            <label>Diagnostic Output:</label>
            <div id="resultBox" class="result-box">Select an X-ray image and click "Run Diagnosis".</div>

            <div style="margin-top: 20px;">
                <label>Med-VQA (Ask a question about this X-ray):</label>
                <div class="chat-row">
                    <input type="text" id="vqaInput" placeholder="e.g. Is there a fracture? Where is it?" onkeypress="if(event.key==='Enter') sendVQA()">
                    <button onclick="sendVQA()">Ask</button>
                </div>
                <div id="vqaResult" class="result-box" style="min-height: 80px; margin-top: 10px;">VQA response will appear here.</div>
            </div>
        </div>
    </div>
</div>

<script>
    let currentImagePath = "";
    let currentImageBase64 = null;

    async function loadSamples() {
        const res = await fetch('/api/samples');
        const samples = await res.json();
        const select = document.getElementById('sampleSelect');
        select.innerHTML = '<option value="">-- Choose a test radiograph --</option>';
        samples.forEach(s => {
            const opt = document.createElement('option');
            opt.value = s.path;
            opt.textContent = s.label;
            select.appendChild(opt);
        });

        if (samples.length > 0) {
            select.selectedIndex = 1;
            onSelectSample();
        }
    }

    function onSelectSample() {
        const select = document.getElementById('sampleSelect');
        const path = select.value;
        if (!path) return;

        currentImagePath = path;
        currentImageBase64 = null;
        document.getElementById('uploadInput').value = "";

        const img = document.getElementById('previewImg');
        img.src = '/image/' + encodeURIComponent(path);
        img.style.display = 'block';
        document.getElementById('noImgText').style.display = 'none';

        document.getElementById('resultBox').innerText = "Image loaded. Click 'Run Diagnosis'.";
        document.getElementById('vqaResult').innerText = "VQA response will appear here.";
    }

    function onUploadImage(e) {
        const file = e.target.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = function(evt) {
            currentImageBase64 = evt.target.result;
            currentImagePath = "";
            document.getElementById('sampleSelect').selectedIndex = 0;

            const img = document.getElementById('previewImg');
            img.src = evt.target.result;
            img.style.display = 'block';
            document.getElementById('noImgText').style.display = 'none';

            document.getElementById('resultBox').innerText = "Custom image uploaded. Click 'Run Diagnosis'.";
            document.getElementById('vqaResult').innerText = "VQA response will appear here.";
        };
        reader.readAsDataURL(file);
    }

    async function runDiagnosis() {
        if (!currentImagePath && !currentImageBase64) {
            alert("Please select or upload an X-ray image first.");
            return;
        }

        document.getElementById('resultBox').innerText = "Running diagnostic analysis...";

        const payload = currentImageBase64 ? { image_base64: currentImageBase64 } : { image_path: currentImagePath };
        const res = await fetch('/api/diagnose', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const data = await res.json();

        if (data.error) {
            document.getElementById('resultBox').innerText = "Error: " + data.error;
            return;
        }

        const statusTag = data.fracture_detected ? 
            "STATUS: 🔴 POSITIVE (FRACTURE DETECTED)" : 
            "STATUS: 🟢 NEGATIVE (NO FRACTURE)";

        const out = `========================================
${statusTag}
CONFIDENCE: ${(data.confidence * 100).toFixed(1)}%
COORDINATES: ${data.bounding_box || 'None'}
========================================

FINDINGS:
${data.findings}

IMPRESSION:
${data.impression}`;

        document.getElementById('resultBox').innerText = out;
    }

    async function sendVQA() {
        const q = document.getElementById('vqaInput').value.trim();
        if (!q) return;

        document.getElementById('vqaResult').innerText = "Processing question...";

        const payload = { image_path: currentImagePath, question: q };
        const res = await fetch('/api/vqa', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        document.getElementById('vqaResult').innerText = data.answer || data.error;
    }

    async function generateReport() {
        if (!currentImagePath && !currentImageBase64) {
            alert("Please select or upload an X-ray image first.");
            return;
        }

        document.getElementById('resultBox').innerText = "Generating formal clinical report...";

        const payload = { image_path: currentImagePath };
        const res = await fetch('/api/report', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        document.getElementById('resultBox').innerText = data.report_text || data.error;
    }

    window.onload = loadSamples;
</script>

</body>
</html>
"""


def main():
    parser = argparse.ArgumentParser(description="FracAtlas Simple Diagnostic Test Server")
    parser.add_argument("--port", type=int, default=7860, help="Port (default: 7860)")
    args = parser.parse_args()

    print(f"\n[Simple Test Studio] Running at: http://localhost:{args.port}\n")
    server = HTTPServer(("", args.port), SimpleAppHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
