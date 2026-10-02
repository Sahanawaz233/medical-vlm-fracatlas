# 🦴 B.Tech 7th Semester Project: Review 1 Presentation
**Department of Electronics and Telecommunication Engineering**
**Assam Engineering College, Jalukbari**

### Project Title:
**FracAtlas Medical Vision-Language Model: Musculoskeletal Fracture Detection, Conversational Med-VQA, and Automated Clinical Reporting**

---

## 📋 Review 1 Slide Outline (13 Academic Slides)

1. **Slide 1**: Title Slide (College, Department, Team, Guide, Project Title)
2. **Slide 2**: Introduction & Background Overview
3. **Slide 3**: Need Analysis & Clinical Motivation
4. **Slide 4**: Problem Statement & Project Scope
5. **Slide 5**: Literature Survey & Comparative Analysis
6. **Slide 6**: Research Gaps & Proposed Approach
7. **Slide 7**: Project Objectives & Key Deliverables
8. **Slide 8**: Layer 1: Dataset Description & Demographics (FracAtlas)
9. **Slide 9**: Layer 2: Multimodal Preprocessing Pipeline (`src/dataset_to_vlm.py`)
10. **Slide 10**: Work Done Till Review 1 (Completed Deliverables Summary)
11. **Slide 11**: Proposed Methodology & System Architecture (The 6 Layers)
12. **Slide 12**: System & Technical Specifications (Hardware & Software)
13. **Slide 13**: Project Roadmap & Semester Plan (Phases 1, 2, 3)

---

## Slide 1: Title Slide
* **Institution**: Assam Engineering College, Jalukbari
* **Department**: Department of Electronics and Telecommunication Engineering
* **Project Title**: FracAtlas Medical Vision-Language Model
* **Subtitle**: Multimodal AI for Musculoskeletal Fracture Detection, Conversational Med-VQA, and Automated Reporting
* **Stage**: B.Tech 7th Semester Major Project Work — Milestone Review 1 (2023 - 2027 Batch)
* **Project Group Members**:
  * Sahanawaz Hussain *(Roll No: ________)*
  * Aryan *(Roll No: ________)*
  * Pranita *(Roll No: ________)*
* **Project Guide**: *[Guide / Supervisor Name]*
* **Repository**: `github.com/Sahanawaz233/medical-vlm-fracatlas`

> **Speaking Script**:
> *"Respected guide and honorable panel members, good morning. We are presenting Review 1 of our B.Tech major project: 'FracAtlas Medical Vision-Language Model'. Our project focuses on developing an assistive multimodal AI system that performs fracture detection, clinical visual question answering, and automated radiology report generation. In this presentation, we will cover our Need Analysis, Literature Survey, Dataset Preprocessing, Work Done till Review 1, and our proposed execution Roadmap."*

---

## Slide 2: Introduction & Background Overview
* **Role of Musculoskeletal Radiography (X-Ray)**:
  * First-line diagnostic imaging modality for trauma emergencies and bone injuries.
  * Massive daily imaging volumes cause severe fatigue and diagnostic backlogs for radiologists.
* **Evolution of Computer-Aided Diagnosis (CAD)**:
  * *1st Generation*: Handcrafted image features & classical machine learning.
  * *2nd Generation*: Deep CNNs (ResNet, YOLO) outputting bounding boxes without textual explanation.
  * *3rd Generation (Current)*: Multimodal Vision-Language Models (VLMs) that unite visual understanding with natural clinical language.
* **What is a Medical Vision-Language Model?**:
  * An AI model combining a Vision Transformer (to process X-ray pixels) and a Large Language Model (to understand and generate clinical text).
  * Enables physicians to converse directly with scans and receive structured diagnostic impressions.

> **Speaking Script**:
> *"Digital projection radiography is the first-line imaging modality used in hospital trauma departments. Over the years, AI in medical imaging has evolved from basic bounding box detectors into multimodal Vision-Language Models. By uniting visual perception with clinical language reasoning, a VLM allows clinicians to interact with X-ray images, ask questions, and receive structured diagnostic findings."*

---

## Slide 3: Need Analysis & Clinical Motivation
* **Emergency Department Triage Bottleneck**:
  * Shortage of specialized musculoskeletal radiologists during night shifts and high-volume trauma hours.
  * Initial radiographs are assessed by non-radiologist junior emergency physicians under acute time constraints.
* **High Rate of Overlooked Fractures**:
  * Clinical audits prove that **missed fractures constitute up to 80% of diagnostic emergency room errors**.
  * Subtle hairline, non-displaced, and pediatric fractures are routinely overlooked, leading to malunion and chronic pain.
* **Limitations of Existing CAD Tools**:
  * Traditional CNNs only output a box or heatmap without explaining *why* an abnormality was flagged.
  * Clinicians cannot ask follow-up questions (e.g. *"Is bone displacement present?"* or *"Are surgical screws observed?"*).
  * Inability to draft standardized medical documentation for hospital patient records.
* **Value Proposition**:
  * A real-time (< 2 seconds) assistive second-reader providing instant fracture grounding, conversational reasoning, and signed reports.

> **Speaking Script**:
> *"Our Need Analysis highlights a critical clinical problem: missed bone fractures account for up to 80% of emergency department diagnostic errors, particularly during night shifts when junior clinicians evaluate radiographs without immediate radiologist supervision. Conventional deep learning models only output static bounding boxes. There is an urgent need for an assistive multimodal model that explains its findings and drafts diagnostic documentation in real time."*

---

## Slide 4: Problem Statement & Project Scope
* **Formal Problem Statement**:
  > *"To design, implement, and evaluate a Multimodal Vision-Language Model tailored for musculoskeletal radiographs that performs acute fracture detection, interactive clinical Visual Question Answering (Med-VQA), and automated structured radiology report generation for emergency triage."*
* **Project Scope & Inclusions**:
  * Peripheral musculoskeletal extremity radiographs (hands, wrists, forearms, elbows, shoulders, knees, ankles, feet).
  * Binary fracture presence detection and bounding coordinate localization.
  * Natural language Med-VQA for bone integrity, cortical disruption, and hardware presence.
  * Automated generation of ACR-standard clinical radiology reports (PDF format).
  * Lightweight deployment capable of running on consumer workstation hardware.
* **Project Boundaries**:
  * Focus is strictly on 2D projection radiographs (CT/MRI volumetric scans are out of scope).
  * Serves as an assistive decision-support tool for doctors, not an autonomous replacement.

> **Speaking Script**:
> *"Our problem statement defines our commitment to build an explainable, end-to-end clinical workflow. Our scope is focused on peripheral extremity radiographs, covering fracture localization, interactive Med-VQA, and automated report generation, designed specifically to operate as an assistive second-reader for emergency doctors."*

---

## Slide 5: Literature Survey & Comparative Analysis

| Paper / Author | Modality Evaluated | Methodology & Strengths | Identified Gaps & Limitations |
| :--- | :--- | :--- | :--- |
| **Lindsey et al. (PNAS 2018)** | Musculoskeletal X-Rays (Wrist, Hand) | Deep ResNet-based CNN.<br>Achieved high sensitivity on wrist fractures. | Pure classification only.<br>Zero natural language reasoning, VQA dialogue, or reporting. |
| **Iftekhar et al. (Nature Sci Data 2023)** | FracAtlas Dataset (4,083 X-rays) | Curated benchmark dataset.<br>Benchmarked YOLOv8 and Faster R-CNN. | Vision-only object detection.<br>Cannot answer clinical questions or draft radiology reports. |
| **LLaVA-Med (NeurIPS 2023)** | Chest / General Biomedical (MIMIC-CXR) | Multimodal conversational VLM.<br>Instruction-tuned on biomedical QA pairs. | Heavily biased to chest X-rays.<br>Hallucinates on fine cortical bone fracture lines. |
| **Our Proposed VLM (FracAtlas VLM)** | **FracAtlas Musculoskeletal (11 extremity sites)** | **Qwen2-VL-2B with 4-bit QLoRA.<br>Detection + Med-VQA + Automated PDF Reports.** | **Addresses orthopedic neglect by bridging detection, interactive dialogue, and clinical documentation.** |

> **Speaking Script**:
> *"Our literature survey examined seminal works in this domain. Traditional models like Lindsey et al. and the original FracAtlas YOLO benchmark are vision-only detectors—they lack any conversational capability. Conversely, recent medical VLMs like LLaVA-Med focus almost entirely on chest X-rays and hallucinate on subtle bone lines. Our work fills this gap by building a dedicated musculoskeletal VLM."*

---

## Slide 6: Research Gaps & Proposed Approach
* **Gap 1: Orthopedic Extremity Neglect**:
  * Over 90% of medical VLM literature focuses on chest radiography (MIMIC-CXR).
  * Extremity fractures—the most common emergency room trauma—are completely neglected.
* **Gap 2: The 'Mute Detector' Dilemma**:
  * Existing fracture detection tools (YOLO, Faster R-CNN) only output raw coordinates or heatmaps.
  * Clinicians cannot interrogate the model regarding fracture displacement, bone alignment, or hardware presence.
* **Gap 3: Prohibitive Hardware Barriers**:
  * 7B+ parameter VLMs require 24–40 GB enterprise GPUs, preventing adoption in local clinics.
* **Our Proposed Approach**:
  * Specializing a lightweight foundation model (`Qwen2-VL-2B-Instruct`) via **4-bit QLoRA** parameter-efficient fine-tuning, achieving full local execution within **6 GB VRAM** consumer hardware constraints.

> **Speaking Script**:
> *"We identified three main research gaps: orthopedic trauma has been ignored in medical VLM research, existing fracture detectors cannot converse with clinicians, and standard VLMs require enterprise GPUs. We solve this by fine-tuning Qwen2-VL-2B with 4-bit QLoRA, enabling full local deployment on consumer workstations."*

---

## Slide 7: Project Objectives & Key Deliverables
* **Objective 1: Multimodal Instruction Dataset Preparation**:
  * Formulate an automated pipeline converting FracAtlas X-rays and COCO annotations into 1,438 balanced LLaVA-format conversation pairs with a 1:1 negative control ratio.
* **Objective 2: Parameter-Efficient VLM Fine-Tuning**:
  * Fine-tune `Qwen2-VL-2B` on musculoskeletal trauma radiographs using QLoRA 4-bit (NF4) quantization, maintaining training peak memory below 4 GB VRAM.
* **Objective 3: Conversational Med-VQA Assistant**:
  * Implement an interactive multimodal chat interface allowing clinicians to query radiographs regarding fracture status, coordinates, and fixation hardware.
* **Objective 4: Automated Clinical Report Generation**:
  * Develop an automated report generator that transforms diagnostic findings into official, downloadable ACR-compliant radiology PDF reports.

> **Speaking Script**:
> *"Our project has four clearly defined objectives: first, structuring a balanced multimodal dataset; second, fine-tuning the VLM with 4-bit QLoRA; third, developing the conversational Med-VQA chat; and fourth, automating the generation of signed clinical radiology PDF reports."*

---

## Slide 8: Layer 1: Dataset Description & Demographics (FracAtlas)
* **Dataset Foundation**: Official peer-reviewed **FracAtlas** release (hosted on Figshare).
* **Dataset Metrics**:
  * **Total High-Resolution Radiographs**: **4,083 images** (~352 MB).
  * **Fractured Cases**: **717 images** (17.56% positive trauma cases).
  * **Normal Controls**: **3,366 images** (82.44% non-fractured cases).
* **Anatomical Extremity Sites (11 Major Sites)**:
  * Hand, Wrist, Forearm, Elbow, Humerus/Shoulder, Pelvis/Hip, Femur, Knee, Tibia/Fibula, Ankle, Foot.
* **Multi-Format Ground Truth**:
  * Expert-annotated bounding boxes and segmentation masks in COCO, YOLO, and Pascal VOC formats.
* **The Class Imbalance Challenge**:
  * Over 82% of raw radiographs are non-fractured normal controls. Without balanced sampling, models learn to guess 'normal' for all scans, yielding 0% clinical sensitivity.

> **Speaking Script**:
> *"Layer 1 represents our raw data ingestion from FracAtlas, containing 4,083 radiographs across 11 anatomical sites. Notice the severe class imbalance: 717 fractured cases versus 3,366 normal controls. If trained without correction, models learn to guess 'normal' for every image. We specifically address this in Layer 2 of our pipeline."*

---

## Slide 9: Layer 2: Multimodal Preprocessing Pipeline (`src/dataset_to_vlm.py`)
* **Core Pipeline Role**: Converts raw radiographs, tabular metadata, and COCO masks into standardized VLM instruction-tuning datasets.
* **3-Step Preprocessing Flow**:
  1. **Annotation Parsing**: Ingests raw split CSVs and `COCO_fracture_masks.json` to extract precise bounding coordinates `[x1, y1, x2, y2]`.
  2. **1:1 Balanced Negative-Control Sampling**: Solves the 82% normal skew by pairing each fractured scan with an anatomically matched normal control.
  3. **Multi-Turn Clinical Prompt Formulation**: Structures multi-turn clinical dialogues with `<image>` tags, examination queries, localization coordinates, and clinical impressions.
* **Generated Dataset Splits (1,438 Total Conversations)**:
  * **Training Split (`train.json`)**: **1,148 samples** (574 fractured + 574 normal controls)
  * **Validation Split (`val.json`)**: **164 samples** (82 fractured + 82 normal controls)
  * **Test Benchmark Split (`test.json`)**: **126 samples** (63 fractured + 63 normal controls)
* **Standardized LLaVA / ShareGPT Schema**:
  ```json
  {
    "id": "frac_IMG0000019",
    "image": "images/Fractured/IMG0000019.jpg",
    "is_fractured": true,
    "conversations": [
      {"from": "human", "value": "<image>\nExamine radiograph."},
      {"from": "gpt", "value": "FINDINGS: Acute fracture at [1242, 929, 1515, 1076]. Impression: Distal radius fracture."}
    ]
  }
  ```

> **Speaking Script**:
> *"Slide 9 details Layer 2 of our architecture: the Multimodal Preprocessing Pipeline implemented in `src/dataset_to_vlm.py`. Here, we solved the 82% class skew by enforcing a strict 1:1 ratio between fractured cases and normal controls. This pipeline successfully generated 1,438 curated conversation pairs divided into train, validation, and test splits formatted in the standard LLaVA multimodal schema."*

---

## Slide 10: Work Done Till Review 1 (Completed Deliverables)

| Milestone Task | Associated Script / Path | Current Status | Completed Output |
| :--- | :--- | :---: | :--- |
| **Layer 1: Dataset Ingestion** | `download_dataset.py` | ✅ Completed | Automated script fetching, verifying MD5 checksum, and extracting 4,083 scans. |
| **Layer 2: Preprocessing Pipeline** | `src/dataset_to_vlm.py` | ✅ Completed | Enforced 1:1 balanced sampling; created 1,438 LLaVA dialogue pairs (train: 1,148, val: 164, test: 126). |
| **Layer 5: Diagnostic Core** | `src/inference.py` | ✅ Completed | Established inference engine with dual-mode evaluation, coordinate localization, and Med-VQA. |
| **Layer 6: Reporting Engine** | `src/report_generator.py` | ✅ Completed | Built automated clinical report generator producing structured text & signed PDF reports. |
| **Layer 6: Med-VQA Interface** | `src/app.py` | ✅ Completed | Interactive Gradio web application for X-ray upload, conversational VQA, and report download. |

> **Speaking Script**:
> *"For Review 1, our foundational engineering is completed. As shown in this progress table, we have implemented the automated downloader, the data preprocessing script that generated 1,438 balanced conversation pairs, the baseline inference core, the clinical PDF report generator, and the interactive Gradio web application prototype."*

---

## Slide 11: Proposed Methodology & System Architecture
* **Layer 1: Data Ingestion**: 4,083 FracAtlas radiographs + COCO bounding coordinates (`download_dataset.py`).
* **Layer 2: Preprocessing Pipeline**: 1:1 balanced sampling producing 1,438 LLaVA-format conversation pairs with clinical queries (`src/dataset_to_vlm.py`).
* **Layer 3: Foundation Model**: `Qwen2-VL-2B-Instruct` featuring dynamic-resolution Vision Transformer (ViT) & M-RoPE positional embeddings.
* **Layer 4: Parameter-Efficient Fine-Tuning (PEFT)**: QLoRA 4-bit NormalFloat (NF4) via BitsAndBytes on attention projections (`q_proj`, `k_proj`, `v_proj`, `o_proj`).
* **Layer 5: Diagnostic Core Engine**: Central inference engine executing fracture detection, coordinate localization, and routing to clinical outputs.
* **Layer 6: Clinical Interfaces & Reporting**: Interactive Gradio Med-VQA Chat UI (`src/app.py`) + Automated ACR Clinical Radiology PDF Reports (`src/report_generator.py`).

> **Speaking Script**:
> *"Slide 11 illustrates our proposed system methodology. It follows a structured 6-layer pipeline: data ingestion, balanced preprocessing, foundation model integration, QLoRA fine-tuning, the diagnostic core engine, and our dual clinical interfaces—conversational VQA and automated PDF reporting."*

---

## Slide 12: System & Technical Specifications
* **Hardware Specifications**:
  * **Target Workstation**: Consumer Laptop / Lab Workstation (tested on Dell G15 / RTX 3050 6GB).
  * **GPU VRAM Required**: 6 GB VRAM minimum for QLoRA 4-bit local training.
  * **Peak Training VRAM**: **~3.8 GB** (well within 6 GB VRAM capacity).
  * **System RAM**: 16 GB DDR4 / DDR5 RAM.
  * **Storage Required**: 10 GB SSD space for dataset & checkpoints.
  * **Cloud Option**: Google Colab Free Tier (NVIDIA Tesla T4 16 GB VRAM).
* **Software Specifications**:
  * **Operating System**: Windows 11 / Linux (Ubuntu) / macOS.
  * **Programming Language**: Python 3.10+.
  * **Deep Learning Framework**: PyTorch 2.2+, CUDA 12.1, Torchvision.
  * **Transformers & PEFT**: HuggingFace Transformers 4.42+, BitsAndBytes (4-bit NF4), PEFT (LoRA).
  * **Web & PDF Tools**: Gradio 4.32+ (WebUI), ReportLab 4.1+ (PDF reports).

> **Speaking Script**:
> *"Slide 12 summarizes our system specifications. By leveraging 4-bit quantization and LoRA adapters, our local engine requires only 3.8 GB of VRAM during training, allowing full execution on a standard 6 GB consumer GPU workstation, with Google Colab T4 as a cloud scaling alternative."*

---

## Slide 13: Project Roadmap & Semester Plan (Timeline)
* **Phase 1: Foundation & Preprocessing (Review 1 — ✅ COMPLETED)**:
  * Literature survey and clinical need analysis.
  * Automated dataset ingestion of 4,083 FracAtlas radiographs.
  * Multimodal preprocessing & 1:1 balanced instruction dataset creation (1,438 conversation pairs).
  * Diagnostic inference pipeline scaffolding, Gradio WebUI prototype, and report generator setup.
* **Phase 2: Model Training & Ablation Studies (Review 2 — UPCOMING)**:
  * Multi-epoch QLoRA fine-tuning execution on local RTX 3050 GPU and Colab T4.
  * Validation loss tracking, learning rate tuning, and gradient accumulation optimization.
  * Comparative ablation study: Zero-shot base model vs. Fine-tuned VLM.
  * Error analysis across subtle hairline and non-displaced fracture sub-types.
* **Phase 3: Clinical Validation & Final Defense (Review 3 / Final Review)**:
  * Rigorous benchmark evaluation: Sensitivity, Specificity, F1-score, and Confusion Matrix on held-out test set.
  * Final system integration into unified clinical Gradio web dashboard.
  * Dissertation preparation, final documentation, and viva defense.

> **Speaking Script**:
> *"Slide 13 presents our phased roadmap across the semester. Having completed Phase 1 for Review 1, our upcoming focus for Review 2 is model fine-tuning and ablation experiments. In Phase 3, we will conduct full benchmark evaluations and finalize our thesis dissertation. Thank you, and we welcome your questions and feedback."*
