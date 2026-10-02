# 🦴 FracAtlas Medical Vision-Language Model (VLM)

> Multimodal Vision-Language Model for Musculoskeletal Fracture Detection, Visual Question Answering (Med-VQA), and Automated Diagnostic Report Generation.

---

## 📌 Table of Contents
- [Overview](#overview)
- [Neural Architecture](#neural-architecture)
- [⚠️ Important: Dataset File Size & Git Exclusion Policy](#️-important-dataset-file-size--git-exclusion-policy)
- [🚀 Quickstart for Project Members](#-quickstart-for-project-members)
  - [1. Clone Repository](#1-clone-repository)
  - [2. View Architecture Dashboard Locally (Zero Dependencies!)](#2-view-architecture-dashboard-locally-zero-dependencies)
  - [3. Download FracAtlas Dataset Locally](#3-download-fracatlas-dataset-locally)
- [📂 Project Directory Layout](#-project-directory-layout)
- [👥 Contributors & Project Team](#-contributors--project-team)
- [📄 Documentation](#-documentation)

---

## Overview

This project builds an end-to-end medical AI diagnostic pipeline based on the **FracAtlas** musculoskeletal radiograph dataset. Using Parameter-Efficient Fine-Tuning (**QLoRA 4-bit**) on modern Vision-Language Models, the platform operates on a **Dual-Engine Architecture**:
* **Local Laptop Engine (Default)**: **`Qwen2-VL-2B-Instruct`** — optimized for consumer gaming laptops with 6 GB VRAM (e.g. Dell G15 with NVIDIA RTX 3050 6GB). Peak training VRAM is **~3.5 – 4.5 GB**, allowing 100% on-device training, offline inference, and local WebUI.
* **Cloud Benchmark Engine**: **`Qwen2-VL-7B-Instruct`** / **`LLaVA-1.5-7B`** — runs on Google Colab (16 GB T4 GPU) for comparative research and scaling evaluations.

The system enables:
1. **Accurate Fracture Detection & Localization** on raw musculoskeletal X-rays.
2. **Interactive Med-VQA Chat**: Natural-language clinical dialogue with radiographs.
3. **Automated Structured Report Generation**: Formatting diagnostic findings and impressions into downloadable clinical radiology PDF reports.

---

## Neural Architecture

The end-to-end system consists of 6 primary layers and an extensible future research module:

```mermaid
flowchart TD
    DS["1. FracAtlas Dataset<br/>(4,083 Radiographs)"] --> DP["2. Data Prep Pipeline<br/>(LLaVA Conversational JSON)"]
    DP --> FT["4. QLoRA 4-bit Fine-Tuning<br/>(Local RTX 3050 / Colab T4)"]
    PV["3. Pre-trained VLM<br/>(Qwen2-VL-2B [Local] / 7B [Cloud])"] --> FT
    FT --> DC["5. Diagnostic Inference Core<br/>(src/inference.py)"]
    DC --> VC["6a. Med-VQA Chat UI<br/>(src/app.py)"]
    DC --> RG["6b. PDF Report Generator<br/>(src/report_generator.py)"]
```

> 📖 For an in-depth architectural breakdown and hardware profiles, see [ARCHITECTURE.md](file:///Users/sahanawazhussain/PROJECT/ARCHITECTURE.md).

---

## ⚠️ Important: Dataset File Size & Git Exclusion Policy

> [!WARNING]
> ### 🛑 Why Raw Datasets and Model Weights Are NOT Tracked in Git
>
> 1. **GitHub File Size Limits**:
>    - GitHub rejects files larger than **100 MB** and issues warnings for files over **50 MB**.
>    - The total repository size is strongly recommended to stay under **1 GB** (ideally < 500 MB) for smooth cloning and syncing.
> 2. **FracAtlas Dataset Size**:
>    - The raw FracAtlas archive contains **4,083 high-resolution X-ray images** taking up approximately **352 MB** uncompressed.
> 3. **Model Binaries**:
>    - PyTorch and HuggingFace weights (`*.safetensors`, `*.pt`, `*.bin`, `*.gguf`) can easily exceed **4 GB to 14 GB**.
>
> **Best Practice Solution implemented in this repository**:
> - All heavy images (`data/raw/FracAtlas/`), processed caches, and model binary files are safely excluded in [.gitignore](file:///Users/sahanawazhussain/PROJECT/.gitignore).
> - Directory structures are preserved using `.gitkeep`.
> - **Every team member can download the dataset with a single command** using the automated script:
>   ```bash
>   python3 download_dataset.py
>   ```

---

## 🚀 Quickstart for Project Members

### 1. Clone Repository
```bash
git clone https://github.com/Sahanawaz233/medical-vlm-fracatlas.git
cd medical-vlm-fracatlas
```

### 2. View Architecture Dashboard Locally (Zero Dependencies!)
We built an interactive, dynamic neural architecture visualizer into the repository. It runs directly on Python's built-in standard library without needing to install any packages!

```bash
python3 dashboard/serve.py
```

Once running, open your web browser to:
```text
http://localhost:8080
```

#### What you will see:
* **Interactive Neural Diagram**: Visual representation of the data ingestion, preprocessing, training, inference core, and output layers.
* **Live Project Scanner**: The background server automatically checks your project folders every 10 seconds and dynamically updates the completion status of each module (Complete, In Progress, Pending).
* **Detailed Node Inspector**: Click on any node to view descriptions, upstream dependencies, and relevant file paths.

### 3. Download FracAtlas Dataset Locally
To retrieve the full dataset onto your local workstation:
```bash
python3 download_dataset.py
```
This script will:
* Fetch the official FracAtlas release from Figshare (approx. 322 MB zip).
* Extract all 4,083 musculoskeletal X-rays into `data/raw/FracAtlas/`.
* Automatically clean up the temporary zip file upon completion.

### 4. Install Dependencies
```bash
# For NVIDIA GPUs (Windows/Linux CUDA 12.1)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
pip install -r requirements.txt
```

### 5. Run Multimodal Data Preprocessing
Convert raw images and COCO bounding annotations into VLM instruction-tuning format:
```bash
python3 src/dataset_to_vlm.py
```
This generates `data/processed/train.json` and `data/processed/val.json` in standard LLaVA / ShareGPT multi-turn format. The dashboard will automatically update **Data Prep** to Complete!

### 6. Fine-Tune the Vision-Language Model
* **Local Laptop (Dell G15 / 6 GB RTX 3050)**:
  ```bash
  python3 src/train_vlm.py --model Qwen/Qwen2-VL-2B-Instruct --batch_size 1 --epochs 3
  ```
  *(Uses QLoRA 4-bit, peaks at ~3.8 GB VRAM, zero OOM risk)*.
* **Cloud Benchmark (Google Colab T4 16 GB)**:
  Open `notebooks/train_vlm.ipynb` in Colab, select T4 GPU, run cells, and save adapter to `models/`.

### 7. Run Diagnostic Inference & Web App
```bash
# Test single X-ray diagnosis
python3 src/inference.py --image data/raw/FracAtlas/FracAtlas/images/Fractured/IMG0000019.jpg

# Launch interactive Med-VQA Chat UI + PDF Report Generator
python3 src/app.py
```
Navigate to `http://localhost:7860` to upload any radiograph, chat with the diagnostic model, and generate official radiology PDF reports.

---

## 💻 Hardware Compatibility Matrix

| Hardware Setup | Target Model | Training Mode | VRAM Required | Status |
| :--- | :--- | :--- | :---: | :--- |
| **Consumer Gaming Laptop**<br>*(Dell G15 / RTX 3050 6GB)* | **`Qwen2-VL-2B-Instruct`** | 100% Local (QLoRA 4-bit) | ~3.8 GB |  **Recommended Local Setup** |
| **Cloud GPU**<br>*(Google Colab T4 16GB)* | **`Qwen2-VL-7B-Instruct`** | Cloud Colab (QLoRA 4-bit) | ~8.5 GB |  **Recommended Cloud Setup** |
| **Local CPU / Mac** | Dashboard & Data Prep | CPU Only | < 2 GB RAM |  **Zero GPU Needed** |

---

## 📂 Project Directory Layout

```text
medical-vlm-fracatlas/
├── ARCHITECTURE.md          # Detailed neural architecture & layer specs
├── README.md                # Project documentation & member guide
├── requirements.txt         # Complete Python dependencies specification
├── .gitignore               # Excludes large images, model checkpoints, OS files
├── download_dataset.py      # Automated dataset downloader & unpacker
├── dashboard/               # Interactive Neural Architecture Visualizer
│   ├── index.html           # Modern dark-mode architecture dashboard UI
│   ├── serve.py             # Zero-dependency Python server with live file scanner
│   └── status.json          # Live status state generated by scanner
├── data/
│   ├── raw/                 # Contains FracAtlas images (populated via download_dataset.py)
│   └── processed/           # Formatted LLaVA-style JSON training files (train.json, val.json)
├── models/                  # Trained LoRA adapter weights (adapter_config.json, etc.)
├── notebooks/               # Colab / Jupyter fine-tuning notebooks (train_vlm.ipynb)
└── src/                     # Core codebase
    ├── dataset_to_vlm.py    # Preprocessing script (dataset.csv -> train.json)
    ├── inference.py         # Diagnostic inference engine
    ├── app.py               # Med-VQA interactive chat application
    └── report_generator.py  # Structured medical PDF report generator
```

---

## 👥 Contributors & Project Team

* **Sahanawaz Hussain** ([@Sahanawaz233](https://github.com/Sahanawaz233)) - Project Lead
* **Aryan** ([@Aryaxnk](https://github.com/Aryaxnk)) - Project Member / Contributor
* **Pranita** ([@pranita157](https://github.com/pranita157)) - Project Member / Contributor
* **[@banesspidy-sketch](https://github.com/banesspidy-sketch)** - Project Member / Contributor

---

## 📄 Documentation

* [Architecture Specification](file:///Users/sahanawazhussain/PROJECT/ARCHITECTURE.md)
* [Interactive Visualizer Guide](file:///Users/sahanawazhussain/PROJECT/ARCHITECTURE.md#3-how-to-run-the-interactive-architecture-dashboard-locally)
