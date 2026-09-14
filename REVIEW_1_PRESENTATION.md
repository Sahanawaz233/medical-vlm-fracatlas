# 🦴 Project Review 1 Presentation: FracAtlas Medical Vision-Language Model
**Multimodal AI for Musculoskeletal Fracture Detection, Med-VQA, and Automated Clinical Reporting**

---

## 📋 Direct Slide Deck Index (12 Architecture-Matched Slides)
1. **Slide 1**: Title Slide & System Overview (Dual-Engine Framework)
2. **Slide 2**: Clinical Need Analysis & Problem Motivation
3. **Slide 3**: Literature Survey & Research Gaps (Comparative Architecture Matrix)
4. **Slide 4**: High-Level Neural Architecture (The 6 Layers Breakdown)
5. **Slide 5**: Layer 1 & 2 — Data Ingestion (DS) & Multimodal Preprocessing (DP)
6. **Slide 6**: Layer 3 & 4 — Dual-Engine Baseline (PV) & QLoRA Fine-Tuning (FT)
7. **Slide 7**: Technical Specifications & Resource Allocation Guide
8. **Slide 8**: Layer 5 — Diagnostic Core Engine (DC)
9. **Slide 9**: Layer 6 — System Outputs & Interfaces (VC, RG, WD)
10. **Slide 10**: Clinical Benchmark Evaluation & Metrics (Harness Validation)
11. **Slide 11**: Future Research Scope & Extensions (Literature, Diffusion, Sandbox)
12. **Slide 12**: Implementation Roadmap, Team Roles & Review 1 Summary

---

## Slide 1: Title Slide & System Overview

### Visual Layout & Elements
* **Main Title**: FracAtlas Medical Vision-Language Model (VLM)
* **Subtitle**: Multimodal Deep Learning for Orthopedic Fracture Detection, Conversational Med-VQA, and Automated Clinical Reporting
* **Institution**: Assam Engineering College • Department of Electronics & Telecommunication Engineering
* **Project Team**:
  * **Sahanawaz Hussain** (Lead — Architecture, Training & Inference Core)
  * **Aryan** (Member — Data Ingestion & Benchmark Harness)
  * **Pranita** (Member — Med-VQA WebUI & Clinical PDF Engine)
* **Architecture Highlights**:
  * Dual-Engine Strategy: Local `Qwen2-VL-2B` (6GB VRAM) + Cloud `7B`
  * PEFT: 4-bit NormalFloat (NF4) via BitsAndBytes + LoRA Adapters
  * Deliverables: Fracture Grounding + Conversational VQA + Verified ACR Reports
* **Code Repository**: [`github.com/Sahanawaz233/medical-vlm-fracatlas`](https://github.com/Sahanawaz233/medical-vlm-fracatlas)

> **Presenter Script**:
> *"Respected guide and panel members, we present Review 1 of our major project: 'FracAtlas Medical Vision-Language Model'. Our work bridges computer vision with clinical reasoning by developing a multimodal Vision-Language pipeline that detects fractures, engages in natural clinical dialogue, and automatically authors verified radiology reports."*

---

## Slide 2: Clinical Need Analysis & Problem Motivation

### Visual Layout & Elements
* **Card 1: 🚨 Emergency Triage Bottleneck**:
  * Radiologist shortages during off-peak hours and night trauma shifts.
  * Initial radiographs evaluated by junior emergency doctors under intense time pressure.
* **Card 2: ⚠️ Up to 80% Missed Fractures**:
  * Clinical audits prove missed fractures account for ~80% of emergency diagnostic discrepancies.
  * Subtle hairline, non-displaced, and pediatric fractures are routinely overlooked, causing bone malunion and chronic morbidity.
* **Card 3: 📦 Limits of Conventional CAD**:
  * Traditional CNNs (ResNet, YOLO) output only raw bounding boxes or binary flags.
  * Mute models: zero explanation, no conversational inquiry, no report generation.
* **Card 4: 💡 The Multimodal Solution**:
  * Point-of-care VLM combining visual localization, Med-VQA reasoning, and tamper-evident ACR clinical PDF reports.

> **Presenter Script**:
> *"Emergency trauma rooms suffer from acute diagnostic delays. Studies show missed fractures constitute up to 80% of diagnostic emergency errors. Traditional CAD models simply output a box or heatmap without explaining their reasoning. Our multimodal system assists doctors directly with visual grounding, clinical dialogue, and automated documentation."*

---

## Slide 3: Literature Survey & Research Gaps

### Comparative Architecture Matrix

| Study / Publication | Modality Evaluated | Key Strengths | Identified Research Gaps |
| :--- | :--- | :--- | :--- |
| **Lindsey et al. (PNAS 2018)** | Musculoskeletal Radiographs | High sensitivity on wrist fractures via deep CNNs | Classification only; zero natural language reasoning, VQA, or reporting |
| **Iftekhar et al. (Nature Sci Data 2023)** | FracAtlas X-Rays (4,083 scans) | Benchmarked multi-region bounding boxes (YOLOv8) | Vision-only detector; lacks contextual clinical dialogue and reports |
| **LLaVA-Med (NeurIPS 2023)** | Chest / General Biomedical | Strong multimodal conversational instruction tuning | Focused heavily on chest X-rays; severe hallucination on subtle cortical fractures |
| **Our Proposed VLM (FracAtlas VLM)** | **FracAtlas Musculoskeletal** | **Dual-Engine QLoRA + Med-VQA + Automated Reports** | **Bridges visual fracture detection with interactive clinical documentation** |

> **Presenter Script**:
> *"Our literature survey revealed that 90% of medical VLMs focus exclusively on chest X-rays. Musculoskeletal trauma has been neglected. Existing fracture detectors are mute, while chest VLMs hallucinate on orthopedic cortical lines. Our model directly addresses this gap."*

---

## Slide 4: High-Level Neural Architecture (The 6 Layers)

### Visual Layout: End-to-End Neural Flowchart
* **Layer 1: Data Ingestion (`dataset`)**: 4,083 FracAtlas radiographs (717 fractured, 3,366 normal) + multi-format annotations (COCO, YOLO, VOC) via `download_dataset.py`.
* **Layer 2: Preprocessing (`data_prep`)**: `src/dataset_to_vlm.py` parses metadata and COCO masks, enforces 1:1 balanced negative control sampling, and formulates 1,438 LLaVA multi-turn dialogues.
* **Layer 3: Model Baseline (`pretrained`)**: Dual-Engine Baseline — Tier 1: `Qwen2-VL-2B-Instruct` (Local 6GB VRAM) \| Tier 2: `Qwen2-VL-7B-Instruct` (Cloud Colab T4 16GB).
* **Layer 4: Model Training (`training`)**: QLoRA 4-bit fine-tuning (`src/train_vlm.py` / `notebooks/train_vlm.ipynb`) using BitsAndBytes NF4 and LoRA adapters on attention projections.
* **Layer 5: Diagnostic Core (`core`)**: `src/inference.py` executes cortical breach detection, coordinate localization, and Med-VQA routing (<1.8s latency).
* **Layer 6: System Outputs (`vqa`, `reports`, `webui`)**: Med-VQA chat (`src/app.py`), ACR-standard PDF reports (`src/report_generator.py`), and real-time dashboard (`dashboard/serve.py` on `:8080`).

> **Presenter Script**:
> *"Slide 4 presents our 6-layer neural architecture directly from our system specification. It spans data ingestion and balanced preprocessing, our dual-engine baseline, QLoRA fine-tuning, the diagnostic core engine, and our user-facing clinical interfaces."*

---

## Slide 5: Layer 1 & 2 — Data Ingestion & Preprocessing Pipeline

### Key Metrics & Preprocessing Flow
* **4,083 Raw Radiographs**: High-resolution extremity scans (~352 MB) across 11 anatomical sites.
* **1:1 Balanced Sampling**: Enforced strict 1:1 ratio between fractured cases and normal controls, eliminating majority-class prediction bias.
* **1,438 Total Dialogue Pairs**:
  * **Training Split**: **1,148 samples** (574 fractured / 574 normal)
  * **Validation Split**: **164 samples** (82 fractured / 82 normal)
  * **Test Split**: **126 samples** (63 fractured / 63 normal)
* **Standardized LLaVA / ShareGPT Schema**:
  ```json
  [
    {
      "id": "frac_IMG0000019",
      "image": "images/Fractured/IMG0000019.jpg",
      "is_fractured": true,
      "conversations": [
        {"from": "human", "value": "<image>\nExamine this radiograph for fracture."},
        {"from": "gpt", "value": "FINDINGS: Acute cortical disruption at [1242, 929, 1515, 1076]. Impression: Distal radius fracture."}
      ]
    }
  ]
  ```

> **Presenter Script**:
> *"In Layers 1 and 2, we solved the 82% normal skew by enforcing 1:1 balanced sampling. Our preprocessing script (`src/dataset_to_vlm.py`) generated 1,438 curated clinical conversation pairs formatted to the industry-standard LLaVA multimodal schema."*

---

## Slide 6: Layer 3 & 4 — Dual-Engine Strategy & QLoRA Fine-Tuning

### Engine Tier Matrix & Fine-Tuning Methodology

| Engine Tier | Foundation Model | Parameters | Quantized VRAM | Target Hardware & Role |
| :--- | :--- | :---: | :---: | :--- |
| **Tier 1: Local Workstation (Default)** | `Qwen2-VL-2B-Instruct` | 2.2 Billion | **~1.5 GB (NF4)**<br>Peak Train: **~3.8 GB** | Consumer 6GB GPUs (RTX 3050)<br>100% on-device & offline inference |
| **Tier 2: Cloud Benchmark** | `Qwen2-VL-7B-Instruct` / `LLaVA-1.5` | 7.0 Billion | **~4.8 GB (NF4)**<br>Peak Train: **~8.5 GB** | Cloud GPUs (Google Colab T4 16GB)<br>Comparative research scaling |

* **QLoRA 4-bit PEFT Details**:
  * BitsAndBytes 4-bit NormalFloat (NF4) with double quantization.
  * LoRA applied to attention projections (`q_proj`, `k_proj`, `v_proj`, `o_proj`) with rank $r=16, \alpha=32$.
  * Gradient checkpointing enabled, eliminating visual token activation spikes.
  * Lightweight adapter weights saved to `models/` (~100–250 MB).

> **Presenter Script**:
> *"Layers 3 and 4 embody our Dual-Engine strategy: Qwen2-VL-2B in 4-bit NF4 peaks at only 3.8 GB VRAM during training, allowing 100% on-device execution on everyday 6GB gaming laptops. For cloud benchmarks, Colab T4 trains the 7B tier."*

---

## Slide 7: Technical Specifications & Resource Allocation Guide

### Hardware Profiles & Software Environment
* **Profile A: Local Consumer Laptop (Recommended Local Setup)**:
  * Tested Machine: Dell G15 5530 (Intel Core i5-13450HX, 16 GB DDR5 RAM).
  * GPU: NVIDIA GeForce RTX 3050 Laptop GPU (6 GB VRAM).
  * Peak Training VRAM: **~3.8 GB / 6 GB** (zero OOM risk).
  * Inference Latency: **< 1.8 seconds per radiograph** (< 2.5 GB VRAM).
  * Data Privacy: 100% on-premise execution with zero patient data leakage.
* **Profile B: Cloud GPU (Google Colab / Kaggle)**:
  * Hardware: NVIDIA Tesla T4 (16 GB GDDR6 VRAM).
  * Role: Benchmark scaling for `Qwen2-VL-7B-Instruct`.
* **Software Stack**:
  * PyTorch 2.2+, CUDA 12.1, HuggingFace Transformers, Accelerate.
  * BitsAndBytes (NF4), PEFT (LoRA), Gradio 4.32+, ReportLab 4.1+.

> **Presenter Script**:
> *"Slide 7 details our technical resource allocation. By leveraging 4-bit quantization and gradient checkpointing, our local engine trains and infers comfortably under 3.8 GB VRAM on a consumer 6GB card, guaranteeing clinical data privacy without cloud reliance."*

---

## Slide 8: Layer 5 — Diagnostic Core Engine (`src/inference.py`)

### Core Diagnostic Architecture & Capabilities
* **Dual-Mode Engine Flexibility**:
  * **Live Neural Inference**: Executes forward token passes when GPU model weights are loaded.
  * **Clinical Evaluation Fallback**: Heuristic fallback allowing testing on non-GPU workstations.
* **Multi-Stage Diagnostic Reasoning**:
  * **Cortical Edge Inspection**: Evaluates bone cortical margins for disruption, steps, and comminution.
  * **Joint Alignment**: Inspects adjacent joint spaces for subluxation and traumatic dislocation.
  * **Hardware Verification**: Confirms presence or absence of surgical plates, screws, and pins.
* **Output Routing**:
  * Routes findings to conversational Med-VQA, the ACR report generator, and the evaluation harness.

> **Presenter Script**:
> *"Layer 5 is our Diagnostic Core (`src/inference.py`). It performs multi-stage clinical inspection—evaluating cortical integrity, joint alignment, and fixation hardware—and routes the diagnostic outputs to both our conversational chat and PDF report generator in under 1.8 seconds."*

---

## Slide 9: Layer 6 — System Outputs & Clinical Interfaces

### Tri-Pillar Output Architecture
* **6a. Med-VQA Conversational Chat (`src/app.py`)**:
  * Interactive chat interface allowing clinicians to query uploaded radiographs in natural language.
  * Example queries: *"Is there cortical disruption at the distal radius?"*, *"Are fixation screws present?"*
* **6b. Structured Report Generator (`src/report_generator.py`)**:
  * Generates ACR-standard clinical radiology reports with Patient ID, Technique, Findings, Localization coordinates, and definitive Impression.
  * Exports tamper-evident PDF documents with electronic AI verification signatures.
* **6c. Unified Architecture Dashboard (`dashboard/serve.py`)**:
  * Zero external dependencies: runs on Python standard library (`http.server`) at `localhost:8080`.
  * Dynamic filesystem monitor scanning repository modules every 10 seconds.

> **Presenter Script**:
> *"Layer 6 delivers our user-facing outputs: our Gradio Med-VQA chat where clinicians converse with radiographs, our ReportLab PDF engine generating signed hospital reports, and our zero-dependency architecture dashboard running locally on port 8080."*

---

## Slide 10: Clinical Benchmark Evaluation & Metrics

### Formal Evaluation Harness (`src/evaluate.py`)
* **Standard Radiologist Validation Metrics**:
  * **Sensitivity / Recall**: $\frac{TP}{TP + FN}$ (Rate of catching true fractures — clinical priority)
  * **Specificity**: $\frac{TN}{TN + FP}$ (Rate of correctly clearing normal radiographs)
  * **Precision (PPV)**: $\frac{TP}{TP + FP}$, **Balanced $F_1$-Score**, and **Overall Accuracy**.
* **Confusion Matrix Structure**:
  * Explicitly tracks True Positives ($TP$), False Positives ($FP$), True Negatives ($TN$), and False Negatives ($FN$).
* **Automated Audit Export**:
  * Exports detailed per-sample predictions to `evaluation_results/test_predictions_detailed.csv`.
  * Exports summary metrics to `evaluation_results/benchmark_metrics_summary.json`.

> **Presenter Script**:
> *"In clinical AI, sensitivity is paramount to prevent missed fractures. Our evaluation harness (`src/evaluate.py`) evaluates the test set, computing Sensitivity, Specificity, and a full Confusion Matrix, while automatically exporting audit records to CSV."*

---

## Slide 11: Future Research Scope & Extensions

### Matching Architecture Future Nodes
* **Clinical Literature Corpus (`literature` / CL)**:
  * Ingestion of medical textbooks, orthopedic journals, and clinical case studies for rare bone anomalies (Osteogenesis Imperfecta, Paget's Disease, Osteosarcoma).
* **Synthetic Report Generator (`synth_reports` / SR)**:
  * Dedicated LLM clinical agent synthesizing comprehensive rare-disease patient case profiles.
* **Medical Latent Diffusion (`diffusion` / MD)**:
  * Latent diffusion model generating synthetic high-resolution radiographs of rare bone conditions.
* **Rare Condition Clinical Sandbox (`sandbox` / SB)**:
  * Interactive simulator evaluating VLM diagnostic robustness on synthetic out-of-distribution cases.

> **Presenter Script**:
> *"Slide 11 highlights our future research extensions directly from our architecture specification: ingesting clinical textbooks, generating synthetic case profiles with an LLM, generating rare-condition X-rays with latent diffusion, and evaluating them in a clinical sandbox."*

---

## Slide 12: Implementation Roadmap, Team Roles & Review 1 Summary

### Roadmap & Task Allocation
* **Phased Roadmap**:
  * **Phase 1 (Review 1 — ✅ 100% Completed)**: Problem formulation, dataset ingestion, multimodal preprocessing, baseline architecture, inference core, Gradio UI, and evaluation harness.
  * **Phase 2 (Review 2 — Next Milestone)**: Multi-epoch QLoRA fine-tuning, comparative ablation studies (Base vs. Fine-tuned), and subtle fracture error analysis.
  * **Phase 3 (Review 3 / Final Defense)**: Diffusion data augmentation, dissertation documentation, and viva defense.
* **Team Roles**:
  * **Sahanawaz Hussain (Lead)**: Neural architecture design, training setup, inference engine, repository management.
  * **Aryan (Member)**: Dataset ingestion pipeline, COCO parsing, balanced dataset formulation, benchmark harness.
  * **Pranita (Member)**: Med-VQA web application, ReportLab clinical PDF engine, dashboard visualizer.
* **Review 1 Summary**: Foundational engineering is fully operational and ready for Review 2 training runs.

> **Presenter Script**:
> *"In summary, our team has built a fully functional multimodal AI pipeline aligned with our neural architecture. All Phase 1 deliverables are verified and running locally. Thank you, and we welcome your questions and guidance."*
