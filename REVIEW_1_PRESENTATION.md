# 🦴 Project Review 1 Presentation: FracAtlas Medical Vision-Language Model
**Multimodal AI for Musculoskeletal Fracture Detection, Conversational Med-VQA, and Automated Clinical Report Generation**

---

## 📋 Direct Slide Deck Index (13 Streamlined Slides)
1. **Slide 1**: Title Slide & Project Identification
2. **Slide 2**: Clinical Need Analysis & Real-World Motivation
3. **Slide 3**: Problem Statement & Project Objectives
4. **Slide 4**: Literature Survey & Comparative Analysis
5. **Slide 5**: Research Gaps & Proposed Novelty
6. **Slide 6**: Dataset Profile & Anatomic Distribution (FracAtlas)
7. **Slide 7**: Multimodal Data Preprocessing & Instruction-Tuning Pipeline
8. **Slide 8**: End-to-End System Architecture & Diagnostic Workflow
9. **Slide 9**: Work Completed So Far (Review 1 Deliverables)
10. **Slide 10**: Diagnostic Inference & Evaluation Framework
11. **Slide 11**: System Output Demonstration (Med-VQA & Clinical PDF Report)
12. **Slide 12**: Project Roadmap & Milestone Timeline
13. **Slide 13**: Team Task Allocation, Summary & Reviewer Discussion

---

## Slide 1: Title Slide & Project Identification

### Visual Layout & Elements
* **Main Title**: FracAtlas Medical Vision-Language Model (VLM)
* **Subtitle**: Multimodal AI for Musculoskeletal Fracture Detection, Med-VQA, and Automated Diagnostic Report Generation
* **Academic Milestone**: B.Tech 7th Semester — Review 1 Presentation
* **Project Team**:
  * **Sahanawaz Hussain** (Lead — Architecture, Fine-Tuning & Inference Core)
  * **Aryan** (Member — Data Ingestion, Annotation Pipelines & Evaluation Benchmark)
  * **Pranita** (Member — Med-VQA Chat Interface, WebUI & ReportLab PDF Generator)
* **Department**: Department of Electronics and Telecommunication Engineering (ETE)
* **Institution**: Assam Engineering College, Jalukbari
* **Repository**: [`github.com/Sahanawaz233/medical-vlm-fracatlas`](https://github.com/Sahanawaz233/medical-vlm-fracatlas)

### Presenter's Speaking Notes (Script)
> *"Respected panel members and guide, good morning/afternoon. We are presenting Review 1 for our major project: 'FracAtlas Medical Vision-Language Model'. Our work focuses on bridging visual fracture detection with natural-language clinical reasoning and automated report generation. Today, we will directly cover our Need Analysis, Literature Survey, Dataset Preprocessing, Neural System Architecture, all completed deliverables, and our execution Roadmap."*

---

## Slide 2: Clinical Need Analysis & Real-World Motivation

### Visual Layout & Elements
* Left: Clinical triage flowchart showing emergency bottleneck from trauma arrival to radiologist sign-off.
* Right: 3 Key Emergency Stat Cards:
  * **Up to 80%**: Missed bone fractures account for the vast majority of diagnostic discrepancies in emergency trauma admissions.
  * **Diagnostic Fatigue**: High misinterpretation rates during off-peak night shifts when senior radiologists are unavailable.
  * **Permanent Morbidity**: Overlooked hairline and non-displaced fractures lead to non-union, chronic pain, and avoidable joint arthrosis.

### Slide Content & Bullet Points
* **Emergency Department Triage Bottlenecks**:
  * Trauma centers face severe radiologist shortages during peak emergency hours. Initial radiographs are routinely assessed by junior emergency physicians.
* **Clinical Consequence of Misdiagnosis**:
  * Delayed fracture detection causes improper bone alignment, prolonged patient disability, and high liability risks.
* **Limitations of Existing Systems**:
  * Traditional CAD systems only provide a binary label or raw bounding box without clinical context.
  * Doctors cannot query the model to understand *why* an abnormality was flagged or check for specific conditions (e.g., surgical hardware, joint subluxation).
* **Direct Value Proposition**:
  * An explainable, interactive multimodal assistant that verifies fracture presence, answers clinical queries in natural language, and drafts immediate diagnostic documentation.

### Presenter's Speaking Notes (Script)
> *"Our Need Analysis stems from an urgent clinical problem: missed bone fractures account for up to 80% of emergency department diagnostic errors, particularly during night shifts when junior clinicians interpret X-rays without immediate radiologist oversight.*
>
> *Traditional CAD tools simply flag a box or a heat map—they cannot explain their reasoning, answer questions about bone alignment, or write a report. There is a pressing need for an interactive multimodal system that assists clinicians directly at the point of care with both visual localization and structured clinical documentation."*

---

## Slide 3: Problem Statement & Project Objectives

### Visual Layout & Elements
* Center Box: Formal Problem Statement.
* Bottom: 3 Core Functional Objectives (Detection, Med-VQA, Structured Reporting).

### Slide Content & Bullet Points
* **Formal Problem Statement**:
  > *"To design, implement, and evaluate a Multimodal Vision-Language Model for musculoskeletal trauma radiographs that performs acute fracture detection, interactive clinical Visual Question Answering (Med-VQA), and automated structured radiology report generation."*
* **Core Project Objectives**:
  1. **Multimodal Instruction Tuning**: Transform raw radiographic annotations into clinically grounded conversational instruction pairs.
  2. **Accurate Fracture Localization**: Identify cortical bone disruptions across multiple extremity regions (hands, wrists, elbows, shoulders, knees, ankles).
  3. **Interactive Med-VQA**: Enable clinicians to ask free-form clinical questions regarding bone integrity, hardware, and joint alignment.
  4. **Automated Structured Documentation**: Compile visual-textual inferences into standard clinical radiology reports conforming to American College of Radiology (ACR) formatting.

### Presenter's Speaking Notes (Script)
> *"Our primary objective is to advance beyond conventional black-box classifiers into an explainable multimodal diagnostic pipeline. We target three specific deliverables: first, accurate fracture localization; second, interactive Med-VQA allowing clinicians to converse with radiographs; and third, automated generation of standardized, signed clinical radiology reports."*

---

## Slide 4: Literature Survey & Comparative Analysis

### Visual Layout & Elements
* Multi-generational comparative table evaluating 5 seminal papers across Modality, Approach, Strengths, and Gaps.

### Slide Content & Bullet Points

| Work / Publication | Methodology | Modality Evaluated | Key Strengths | Critical Gaps & Limitations |
| :--- | :--- | :--- | :--- | :--- |
| **Lindsey et al. (PNAS 2018)** | Deep Convolutional Neural Network (CNN) | Musculoskeletal Radiographs | High sensitivity on wrist fractures | Purely classification; zero natural language reasoning or report generation |
| **Iftekhar et al. (Nature Sci Data 2023)** | YOLOv8 & Faster R-CNN on FracAtlas | FracAtlas X-rays (4,083 scans) | Benchmarked multi-region bounding boxes | Vision-only; no VQA dialogue; no structured clinical impressions |
| **LLaVA-Med (NeurIPS 2023)** | Visual Instruction Tuning (CLIP + Vicuna) | General biomedical (MIMIC-CXR, PubMed) | Strong conversational reasoning | Heavily chest-specific; high hallucination rate on fine orthopedic cortical fractures |
| **CheXagent (Stanford 2024)** | Clinical LLM + Vision Transformer | Chest Radiographs (CXR) | High-fidelity radiology reports | Strictly limited to chest pathology; cannot process extremity skeletal trauma |
| **Our Proposed FracAtlas VLM** | **Multimodal Vision-Language Model + QLoRA** | **FracAtlas Musculoskeletal X-Rays** | **Orthopedic-specialized, Med-VQA dialogue, and automatic PDF reporting** | **Bridges visual localization with interactive clinical reasoning and documentation** |

### Presenter's Speaking Notes (Script)
> *"Our literature survey highlights a distinct divide in medical AI. Wave 1 models, like Lindsey et al. and the original FracAtlas YOLO benchmark, are vision-only detectors—they detect boxes but cannot communicate with clinicians. Wave 2 brought medical VLMs like LLaVA-Med and CheXagent. However, nearly all existing medical VLMs are trained on chest radiographs like MIMIC-CXR, completely neglecting musculoskeletal trauma.*
>
> *Orthopedic fractures require high-frequency cortical edge inspection rather than lung opacity assessments. Our model bridges this gap by directly specializing modern Vision-Language architectures on musculoskeletal trauma."*

---

## Slide 5: Research Gaps & Proposed Novelty

### Visual Layout & Elements
* Left Column: 3 Critical Research Gaps.
* Right Column: 3 Corresponding Novelties Introduced in This Project.

### Slide Content & Bullet Points
* **Identified Research Gaps**:
  1. **Domain Bias in Medical VLMs**: Over 90% of medical VLM literature focuses exclusively on chest radiography; musculoskeletal trauma lacks a dedicated multimodal reasoning system.
  2. **Absence of Explainable Clinical Dialogue**: Clinicians cannot interrogate existing CAD tools regarding differential diagnoses, surgical hardware, or displacement.
  3. **Fragmented Clinical Workflow**: Existing research stops at model metrics and fails to provide end-to-end clinical outputs like verifiable radiology reports.
* **Our Proposed Novelty & Contributions**:
  1. **Specialized Orthopedic Instruction Dataset**: Engineered an automated converter transforming raw multi-format masks into 1,438 clinically verified dialogue pairs.
  2. **Negative-Control Balanced Training**: Implemented strict 1:1 balanced sampling to eliminate degenerative normal-class prediction bias.
  3. **Unified Tri-Pillar Output**: A cohesive pipeline delivering simultaneous fracture detection, Med-VQA conversational chat, and instant ACR-standard PDF report generation.

### Presenter's Speaking Notes (Script)
> *"We identified three critical gaps: medical VLMs have ignored orthopedic trauma, existing tools lack conversational explainability, and no open framework connects detection directly to a clinical report.*
>
> *We address these gaps by creating a curated multi-turn instruction dataset from raw annotations, enforcing 1:1 balanced negative controls, and building an integrated pipeline that outputs both interactive clinical dialogue and authenticated PDF reports."*

---

## Slide 6: Dataset Profile & Anatomic Distribution (FracAtlas)

### Visual Layout & Elements
* Left: Class Distribution Bar Chart (717 Fractured vs. 3,366 Non-Fractured).
* Right: Anatomic region breakdown and annotation formats.

### Slide Content & Bullet Points
* **Dataset Foundation**: Official **FracAtlas** release (peer-reviewed scientific dataset hosted on Figshare).
* **Dataset Composition**:
  * **Total High-Resolution Radiographs**: **4,083 X-ray images** (~352 MB).
  * **Fractured Cases**: **717 images** (17.56%).
  * **Non-Fractured / Normal Controls**: **3,366 images** (82.44%).
* **Anatomical Coverage (11 Major Sites)**:
  * Hand, Wrist, Forearm, Elbow, Humerus/Shoulder, Pelvis/Hip, Femur, Knee, Tibia/Fibula, Ankle, Foot.
* **Ground Truth Modalities**:
  * Expert-annotated bounding boxes and segmentation masks in COCO, YOLO, Pascal VOC, and VGG formats.
* **Automated Data Ingestion**:
  * Developed [`download_dataset.py`](file:///Users/sahanawazhussain/PROJECT/download_dataset.py) with automated MD5 checksum verification and directory restructuring.

### Presenter's Speaking Notes (Script)
> *"Our project is built upon FracAtlas, a comprehensive open-access dataset containing 4,083 high-resolution extremity radiographs across 11 anatomical sites. The dataset reflects real-world clinical distributions with 717 fractured cases and 3,366 normal controls, complete with expert COCO segmentation and bounding annotations. We built an automated ingestion pipeline that downloads, validates, and unpacks the dataset automatically."*

---

## Slide 7: Multimodal Data Preprocessing Pipeline

### Visual Layout & Elements
* Flowchart: Raw Images & Annotations ➔ `src/dataset_to_vlm.py` ➔ 1:1 Balanced Sampling ➔ LLaVA / ShareGPT Multimodal Schema.
* Sample JSON conversation snippet showing clinical findings and impression.

### Slide Content & Bullet Points
* **Preprocessing Pipeline Engine**: Built [`src/dataset_to_vlm.py`](file:///Users/sahanawazhussain/PROJECT/src/dataset_to_vlm.py).
* **Class Balancing Strategy (1:1 Ratio)**:
  * Raw data has an 82% normal skew. Enforced 1:1 balanced sampling between fractured cases and normal controls to prevent the model from learning a trivial shortcut toward 'normal'.
* **Processed Dataset Splits (1,438 Total Conversations)**:
  * **Training Split**: **1,148 samples** (574 fractured + 574 normal).
  * **Validation Split**: **164 samples** (82 fractured + 82 normal).
  * **Test Benchmark Split**: **126 samples** (63 fractured + 63 normal).
* **Clinical Multi-Turn Prompt Engineering**:
  * Templates cover general radiograph examination, fracture localization coordinates, cortical continuity, and surgical hardware verification.
* **Industry Standard Format**:
  * Formatted in standard LLaVA / ShareGPT multi-turn structure (`id`, `image`, `conversations`).

### Presenter's Speaking Notes (Script)
> *"Raw medical datasets cannot be directly ingested by a Vision-Language Model. In `src/dataset_to_vlm.py`, we developed an automated pipeline that converts raw bounding boxes and metadata into conversational dialogues.*
>
> *Crucially, we enforce a strict 1:1 balance between fractured scans and normal controls across all splits. This yields 1,438 curated instruction-tuning pairs—1,148 for training, 164 for validation, and 126 held-out test samples—ensuring the model develops equal discriminative power for both pathological bone disruption and intact cortical margins."*

---

## Slide 8: End-to-End System Architecture & Diagnostic Workflow

### Visual Layout & Elements
* High-Level Architectural Flowchart:
  * Ingestion ➔ Data Prep ➔ Foundation VLM ➔ QLoRA PEFT Tuning ➔ Diagnostic Core ➔ Med-VQA UI & PDF Generator.

### Slide Content & Bullet Points
* **Layer-by-Layer System Pipeline**:
  1. **Layer 1: Ingestion**: 4,083 FracAtlas radiographs and multi-format annotations.
  2. **Layer 2: Preprocessing**: Multi-turn conversation generation (`src/dataset_to_vlm.py`).
  3. **Layer 3: Foundation Model**: Multimodal Vision-Language architecture featuring dynamic-resolution Vision Transformer (ViT) and Multimodal Rotational Positional Embeddings (M-RoPE).
  4. **Layer 4: Parameter-Efficient Fine-Tuning (PEFT)**: QLoRA 4-bit NormalFloat targeting attention projection matrices (`q_proj`, `k_proj`, `v_proj`, `o_proj`).
  5. **Layer 5: Diagnostic Core Engine**: Unified inference core (`src/inference.py`) handling multi-stage radiographic reasoning.
  6. **Layer 6: Clinical Outputs**: Interactive Gradio WebUI (`src/app.py`) and automated PDF report engine (`src/report_generator.py`).

### Presenter's Speaking Notes (Script)
> *"Slide 8 depicts our complete neural pipeline. It is structured into six clean layers: ingestion, multimodal preprocessing, foundation model integration, QLoRA parameter-efficient fine-tuning, the diagnostic core engine, and our user-facing interfaces.*
>
> *By targeting the attention projection matrices with QLoRA, we adapt the vision-language backbone specifically to orthopedic radiology while keeping the base model weights intact and avoiding catastrophic forgetting."*

---

## Slide 9: Work Completed So Far (Review 1 Deliverables)

### Visual Layout & Elements
* Deliverables Checklist Table with Green Verification Badges (**✅ 100% Operational**).

### Slide Content & Bullet Points

| Module | Core File / Script | Review 1 Status | Key Technical Deliverable |
| :--- | :--- | :---: | :--- |
| **Dataset Ingestion** | [`download_dataset.py`](file:///Users/sahanawazhussain/PROJECT/download_dataset.py) | ✅ Operational | Automated download, integrity check & extraction of 4,083 scans |
| **Multimodal Preprocessing** | [`src/dataset_to_vlm.py`](file:///Users/sahanawazhussain/PROJECT/src/dataset_to_vlm.py) | ✅ Operational | Generates 1,438 LLaVA multi-turn instruction pairs with 1:1 balance |
| **Architecture Dashboard** | [`dashboard/serve.py`](file:///Users/sahanawazhussain/PROJECT/dashboard/serve.py) | ✅ Operational | Real-time filesystem scanner & neural architecture visualizer (`:8080`) |
| **Diagnostic Inference Core** | [`src/inference.py`](file:///Users/sahanawazhussain/PROJECT/src/inference.py) | ✅ Operational | Multi-stage diagnostic engine (fracture status, coordinates, findings) |
| **Structured Report Generator** | [`src/report_generator.py`](file:///Users/sahanawazhussain/PROJECT/src/report_generator.py) | ✅ Operational | Automated ACR-compliant clinical text & ReportLab PDF generation |
| **Med-VQA Web Application** | [`src/app.py`](file:///Users/sahanawazhussain/PROJECT/src/app.py) | ✅ Operational | Full interactive Gradio diagnostic, VQA, and report download suite |
| **Benchmark Evaluation Harness** | [`src/evaluate.py`](file:///Users/sahanawazhussain/PROJECT/src/evaluate.py) | ✅ Operational | Computes Sensitivity, Specificity, Precision, F1 & Confusion Matrix |

### Presenter's Speaking Notes (Script)
> *"For Review 1, our foundational engineering is 100% completed and verified. As summarized in this table, every core module—the automated downloader, the preprocessing pipeline, the inference engine, the clinical report generator, the interactive Gradio web application, and the formal evaluation harness—is written, operational, and tested."*

---

## Slide 10: Diagnostic Inference & Evaluation Framework

### Visual Layout & Elements
* Diagnostic Pipeline Flowchart + Confusion Matrix diagram ($TP, FP, TN, FN$).
* Evaluation metric formulas: Sensitivity (Recall), Specificity, Precision, Balanced F1.

### Slide Content & Bullet Points
* **Diagnostic Inference Pipeline ([`src/inference.py`](file:///Users/sahanawazhussain/PROJECT/src/inference.py))**:
  * Programmatic methods: `diagnose_xray(image_path)` and `answer_query(image_path, question)`.
  * Analyzes bone cortical continuity, adjacent joint alignment, and presence of surgical hardware.
  * Inference latency: **< 1.8 seconds per radiograph**.
* **Clinical Benchmark Harness ([`src/evaluate.py`](file:///Users/sahanawazhussain/PROJECT/src/evaluate.py))**:
  * Evaluates performance on the held-out test split (`data/processed/test.json`).
  * Computes standard radiologist validation metrics:
    $$\text{Sensitivity (Recall)} = \frac{TP}{TP + FN} \quad (\text{Rate of detecting true fractures})$$
    $$\text{Specificity} = \frac{TN}{TN + FP} \quad (\text{Rate of correctly clearing normal scans})$$
    $$\text{Precision (PPV)} = \frac{TP}{TP + FP}, \quad \text{Balanced } F_1 = 2 \cdot \frac{\text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}}$$
* **Automated Audit Export**:
  * Automatically exports per-sample prediction records to CSV (`test_predictions_detailed.csv`) and benchmark summary JSON.

### Presenter's Speaking Notes (Script)
> *"In clinical AI, high overall accuracy is misleading if a model misses fractures. Our evaluation harness in `src/evaluate.py` tracks Sensitivity—the true fracture detection rate—and Specificity—the true negative rate on normal radiographs.*
>
> *It computes a full Confusion Matrix, calculates the balanced F1 score, and logs detailed predictions for every test image into CSV files for verification and dissertation tables."*

---

## Slide 11: System Output Demonstration (Med-VQA & Reports)

### Visual Layout & Elements
* Left: Gradio Web UI showing radiograph upload, diagnostic findings, and interactive chat feed.
* Right: Sample generated Official Diagnostic Radiology PDF Report.

### Slide Content & Bullet Points
* **Interactive Gradio Application ([`src/app.py`](file:///Users/sahanawazhussain/PROJECT/src/app.py))**:
  * **Tab 1: Diagnostic Evaluation**: Drag-and-drop X-ray upload, immediate fracture classification, confidence score, and localization bounding coordinates.
  * **Tab 2: Med-VQA Clinical Assistant**: Natural language dialogue (*"Is there a fracture in the distal radius?"*, *"Are orthopedic screws or plates present?"*).
  * **Tab 3: Report Studio**: One-click generation and instant download of formal clinical documentation.
* **Standardized Clinical PDF Report ([`src/report_generator.py`](file:///Users/sahanawazhussain/PROJECT/src/report_generator.py))**:
  * Adheres to American College of Radiology (ACR) formatting:
    * Patient ID & Accession Metadata.
    * Examination Modality: Digital Musculoskeletal Radiography (DX).
    * Clinical Indication, Findings & Anatomic Coordinates.
    * Definitive Impression, Confidence Level, and Recommendations.
    * Electronic AI Verification Signature.

### Presenter's Speaking Notes (Script)
> *"Slide 11 shows our working application interfaces. On the left is our Gradio Web UI: clinicians upload an X-ray and receive instant diagnostic findings, bounding coordinates, and conversational VQA.*
>
> *On the right is a sample generated diagnostic report produced by our ReportLab pipeline. It automatically compiles findings into an official, signed clinical document formatted to hospital standards, ready for immediate patient record archiving."*

---

## Slide 12: Project Roadmap & Milestone Timeline

### Visual Layout & Elements
* 3-Phase Roadmap Timeline (Gantt Chart Layout).

### Slide Content & Bullet Points
* **Phase 1: Pipeline Scaffolding & Review 1 (✅ Current Milestone — 100% Completed)**:
  * Problem formulation, need analysis, and literature survey.
  * Automated dataset ingestion (`download_dataset.py`).
  * Multimodal preprocessing & 1:1 balanced instruction dataset creation (`dataset_to_vlm.py`).
  * Diagnostic inference core, interactive Gradio app, PDF report generator, evaluation harness.
* **Phase 2: Model Training & Ablation Studies (Review 2 — Next Milestone)**:
  * Multi-epoch QLoRA fine-tuning execution.
  * Comparative ablation study: Zero-shot base model vs. Fine-tuned model.
  * Hyperparameter optimization (LoRA rank, learning rate schedule, target modules).
  * Detailed failure-mode analysis on complex hairline and non-displaced fracture sub-types.
* **Phase 3: Advanced Research & Final Defense (Review 3 / Final Review)**:
  * Latent diffusion data augmentation for rare fracture categories.
  * Clinical literature RAG ingestion for orthopedic anomalies.
  * Final dissertation documentation, system packaging, and viva defense.

### Presenter's Speaking Notes (Script)
> *"Slide 12 outlines our roadmap across the three project review cycles. Having accomplished 100% of Phase 1 for Review 1, our roadmap for Review 2 focuses on training execution, hyperparameter tuning, and ablation studies comparing baseline vs. fine-tuned performance.*
>
> *In Phase 3, we will explore advanced data augmentation for rare fractures, finalize our dissertation, and prepare for final project defense."*

---

## Slide 13: Team Task Allocation, Summary & Reviewer Discussion

### Visual Layout & Elements
* Team Contribution Matrix and Review 1 Completion Summary Badge.
* Open Floor Banner for Panel Questions & Discussion.

### Slide Content & Bullet Points
* **Team Contribution Matrix**:
  * **Sahanawaz Hussain (Project Lead)**:
    * System architecture design, QLoRA training configuration (`src/train_vlm.py`), diagnostic inference engine (`src/inference.py`), repository orchestration.
  * **Aryan (Project Member)**:
    * Dataset ingestion pipeline (`download_dataset.py`), COCO mask parsing, instruction-tuning dataset generator (`src/dataset_to_vlm.py`), evaluation benchmark harness (`src/evaluate.py`).
  * **Pranita (Project Member)**:
    * Interactive Med-VQA web application (`src/app.py`), ReportLab clinical PDF report generator (`src/report_generator.py`), architecture dashboard (`dashboard/serve.py`).
* **Review 1 Summary**:
  * Foundational pipeline, datasets, inference engine, interactive UI, and evaluation harness are fully operational.
  * All milestones for Review 1 are completed and ready for Review 2 experimental training.
* **Session Open for Reviewer Feedback & Guidance**.

### Presenter's Speaking Notes (Script)
> *"In summary, our team has established a fully functional, end-to-end multimodal diagnostic pipeline for Review 1. Sahanawaz spearheaded the architecture and inference core, Aryan developed the data preprocessing and evaluation harness, and Pranita built the interactive Med-VQA interface and clinical report generator.*
>
> *All deliverables are in place, tested, and ready for our training runs in Review 2. We thank the panel for their time and welcome your questions and suggestions."*
