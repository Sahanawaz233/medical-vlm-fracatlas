#!/usr/bin/env python3
"""
FracAtlas Med-VQA & Diagnostic Web Application
==============================================
Interactive multimodal clinical interface for:
  - Drag-and-drop X-ray upload
  - Fracture detection and anatomical localization
  - Med-VQA conversational clinical queries
  - Structured clinical radiology report generation and download
"""

import os
import sys
import json
import time
import argparse
from pathlib import Path

# Add src/ to python path
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SRC_DIR)
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from inference import MedicalVLMInferenceEngine
from report_generator import generate_clinical_report


def run_gradio_app(port=7860, share=False):
    """Launch Gradio Web Application."""
    import gradio as gr

    engine = MedicalVLMInferenceEngine()
    engine.load_model()

    def process_radiograph(image):
        if image is None:
            return "Please upload an X-ray radiograph.", "", ""

        # Save temporary image if needed
        temp_dir = os.path.join(PROJECT_DIR, "data", "temp_uploads")
        os.makedirs(temp_dir, exist_ok=True)
        temp_path = os.path.join(temp_dir, f"upload_{int(time.time())}.jpg")
        image.save(temp_path)

        diag = engine.diagnose_xray(temp_path)
        status = "🔴 POSITIVE: FRACTURE DETECTED" if diag["fracture_detected"] else "🟢 NEGATIVE: NO FRACTURE"
        findings = diag["findings"]
        impression = diag["impression"]
        coords = f"Coordinates: {diag.get('bounding_box', 'N/A')}" if diag.get("bounding_box") else "No focal defect"

        return f"**Status**: {status}\n**Confidence**: {diag['confidence']*100:.1f}%\n**Localization**: {coords}", findings, impression

    def handle_vqa(image, question, chat_history):
        if image is None:
            return chat_history, "Please upload an X-ray radiograph first."
        if not question or not question.strip():
            return chat_history, ""

        temp_dir = os.path.join(PROJECT_DIR, "data", "temp_uploads")
        os.makedirs(temp_dir, exist_ok=True)
        temp_path = os.path.join(temp_dir, f"vqa_{int(time.time())}.jpg")
        image.save(temp_path)

        answer = engine.answer_query(temp_path, question)
        chat_history = chat_history or []
        chat_history.append((question, answer))
        return chat_history, ""

    def make_report(image):
        if image is None:
            return "Please upload an X-ray radiograph first.", None
        temp_dir = os.path.join(PROJECT_DIR, "data", "temp_uploads")
        os.makedirs(temp_dir, exist_ok=True)
        temp_path = os.path.join(temp_dir, f"report_{int(time.time())}.jpg")
        image.save(temp_path)

        diag = engine.diagnose_xray(temp_path)
        res = generate_clinical_report(diag, output_dir=os.path.join(PROJECT_DIR, "reports"))
        download_file = res["pdf_path"] if res.get("pdf_path") and os.path.exists(res["pdf_path"]) else res["txt_path"]
        return res["report_text"], download_file

    with gr.Blocks(title="FracAtlas Med-VQA Diagnostic Platform", theme=gr.themes.Soft()) as demo:
        gr.Markdown(
            """
            # 🦴 FracAtlas Multimodal AI Diagnostic Platform
            ### Orthopedic Fracture Detection, Med-VQA Conversational Radiologist & Automated Reports
            """
        )

        with gr.Row():
            with gr.Column(scale=1):
                input_image = gr.Image(type="pil", label="Upload Musculoskeletal Radiograph (X-Ray)")
                analyze_btn = gr.Button("🔍 Run Diagnostic Analysis", variant="primary")
                report_btn = gr.Button("📄 Generate Clinical Radiology Report", variant="secondary")

            with gr.Column(scale=2):
                with gr.Tab("Diagnostic Evaluation"):
                    diag_status = gr.Markdown("Upload an image and click **Run Diagnostic Analysis**.")
                    diag_findings = gr.Textbox(label="Radiological Findings", lines=4)
                    diag_impression = gr.Textbox(label="Diagnostic Impression", lines=3)

                with gr.Tab("Med-VQA Clinical Chat"):
                    chatbot = gr.Chatbot(label="Consultation Feed", height=300)
                    user_msg = gr.Textbox(placeholder="Ask a question (e.g. 'Is there a fracture?', 'Where is the lesion?')...", label="Clinical Query")
                    send_btn = gr.Button("Send Question")

                with gr.Tab("Radiology Report"):
                    report_preview = gr.TextArea(label="Clinical Report Document", lines=12)
                    download_btn = gr.File(label="Download Official Report")

        analyze_btn.click(process_radiograph, inputs=[input_image], outputs=[diag_status, diag_findings, diag_impression])
        send_btn.click(handle_vqa, inputs=[input_image, user_msg, chatbot], outputs=[chatbot, user_msg])
        report_btn.click(make_report, inputs=[input_image], outputs=[report_preview, download_btn])

    print(f"\n[Med-VQA] Launching Gradio Web Server on port {port}...")
    demo.launch(server_port=port, share=share)


def run_standalone_fallback(port=7860):
    """Fallback zero-dependency clinical web server when Gradio is not installed."""
    import http.server
    import urllib.parse

    engine = MedicalVLMInferenceEngine()
    engine.load_model()

    class StandaloneAppHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            parsed = urllib.parse.urlparse(self.path)
            if parsed.path == "/api/sample":
                # Run sample diagnosis
                sample_img = os.path.join(PROJECT_DIR, "data/raw/FracAtlas/FracAtlas/images/Fractured/IMG0000019.jpg")
                diag = engine.diagnose_xray(sample_img)
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(diag).encode("utf-8"))
                return

            # Serve minimal embedded clinical dashboard
            html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>FracAtlas Med-VQA Platform</title>
    <style>
        body {{ font-family: -apple-system, sans-serif; background: #030308; color: #f1f5f9; padding: 40px; }}
        .card {{ background: rgba(14, 42, 54, 0.6); border: 1px solid #00ffc8; border-radius: 12px; padding: 24px; max-width: 800px; margin: 0 auto; }}
        h1 {{ color: #00ffc8; margin-top: 0; }}
        .badge {{ display: inline-block; padding: 4px 12px; border-radius: 20px; font-weight: bold; background: #00ffc8; color: #030308; }}
        pre {{ background: #080a14; padding: 16px; border-radius: 8px; border: 1px solid #334155; overflow-x: auto; color: #cbd5e1; }}
        button {{ background: #00ffc8; color: #030308; border: none; padding: 10px 20px; border-radius: 6px; font-weight: bold; cursor: pointer; }}
    </style>
</head>
<body>
    <div class="card">
        <h1>🦴 FracAtlas Med-VQA Clinical Platform</h1>
        <p><span class="badge">Standalone Core Engine Active</span></p>
        <p>The diagnostic core engine is online and fully functional.</p>
        <p>To enable the full Gradio GUI with real-time image upload, install Gradio:</p>
        <pre>pip install gradio</pre>
        <button onclick="testInference()">Run Sample Diagnostic Test</button>
        <div id="output" style="margin-top: 20px;"></div>
    </div>
    <script>
        async function testInference() {{
            document.getElementById('output').innerHTML = '<em>Running clinical evaluation...</em>';
            const res = await fetch('/api/sample');
            const data = await res.json();
            document.getElementById('output').innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
        }}
    </script>
</body>
</html>"""
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))

    print(f"\n[Med-VQA] Launching Standalone Web Interface at: http://localhost:{port}")
    server = http.server.HTTPServer(("", port), StandaloneAppHandler)
    server.serve_forever()


def main():
    parser = argparse.ArgumentParser(description="FracAtlas Med-VQA Web Platform")
    parser.add_argument("--port", type=int, default=7860, help="Port to run web app (default: 7860)")
    parser.add_argument("--share", action="store_true", help="Generate public shareable link")
    args = parser.parse_args()

    try:
        import gradio
        run_gradio_app(port=args.port, share=args.share)
    except ImportError:
        print("[Notice] Gradio is not installed. Launching Standalone Clinical Web Interface...")
        run_standalone_fallback(port=args.port)


if __name__ == "__main__":
    main()
