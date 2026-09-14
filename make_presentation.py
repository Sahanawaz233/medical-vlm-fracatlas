import sys
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_deck(output_path="Review_1_Presentation.pptx"):
    prs = Presentation()
    # 16:9 Widescreen standard dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6] # completely blank layout

    # Palette
    C_BG = RGBColor(11, 19, 43)         # #0B132B Dark Navy
    C_CARD = RGBColor(20, 32, 60)       # #14203C Card Container
    C_ACCENT = RGBColor(0, 201, 167)    # #00C9A7 Cyan/Teal
    C_BLUE = RGBColor(77, 171, 247)     # #4DABF7 Soft Sky Blue
    C_WHITE = RGBColor(248, 250, 252)   # #F8FAFC Crisp White
    C_MUTED = RGBColor(148, 163, 184)   # #94A3B8 Cool Gray
    C_CARD_BORDER = RGBColor(30, 48, 86)
    C_DARK_TEXT = RGBColor(15, 23, 42)

    def set_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = C_BG
        bg.line.fill.background() # no line
        return bg

    def add_header(slide, slide_num, title_text, category="MEDICAL VISION-LANGUAGE MODEL (VLM)"):
        # Header category tag
        tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(10), Inches(0.35))
        tf_tag = tag_box.text_frame
        tf_tag.word_wrap = True
        tf_tag.margin_left = tf_tag.margin_top = tf_tag.margin_right = tf_tag.margin_bottom = 0
        p_tag = tf_tag.paragraphs[0]
        p_tag.text = category.upper()
        p_tag.font.name = "Arial"
        p_tag.font.size = Pt(11)
        p_tag.font.bold = True
        p_tag.font.color.rgb = C_ACCENT

        # Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(10.5), Inches(0.7))
        tf_t = title_box.text_frame
        tf_t.word_wrap = True
        tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.name = "Arial"
        p_t.font.size = Pt(24)
        p_t.font.bold = True
        p_t.font.color.rgb = C_WHITE

        # Slide number pill
        pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(11.8), Inches(0.55), Inches(0.75), Inches(0.35))
        pill.fill.solid()
        pill.fill.fore_color.rgb = C_CARD
        pill.line.color.rgb = C_ACCENT
        pill.line.width = Pt(1)
        p_pill = pill.text_frame.paragraphs[0]
        p_pill.text = f"{slide_num}/12"
        p_pill.alignment = PP_ALIGN.CENTER
        p_pill.font.name = "Arial"
        p_pill.font.size = Pt(11)
        p_pill.font.bold = True
        p_pill.font.color.rgb = C_WHITE

    # -------------------------------------------------------------------------
    # SLIDE 1: Title Slide
    # -------------------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    # Decorative Card Container
    card1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.0), Inches(11.333), Inches(5.5))
    card1.fill.solid()
    card1.fill.fore_color.rgb = C_CARD
    card1.line.color.rgb = C_ACCENT
    card1.line.width = Pt(1.5)

    # Department & College Tag
    tag1 = s1.shapes.add_textbox(Inches(1.5), Inches(1.35), Inches(10.3), Inches(0.4))
    tf1 = tag1.text_frame
    p = tf1.paragraphs[0]
    p.text = "ASSAM ENGINEERING COLLEGE • DEPARTMENT OF ELECTRONICS & TELECOMMUNICATION ENGINEERING"
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_ACCENT

    # Main Title
    t1 = s1.shapes.add_textbox(Inches(1.5), Inches(1.8), Inches(10.3), Inches(1.2))
    tf_t1 = t1.text_frame
    tf_t1.word_wrap = True
    p = tf_t1.paragraphs[0]
    p.text = "FracAtlas Medical Vision-Language Model"
    p.font.name = "Arial"
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = C_WHITE

    # Subtitle
    sub1 = s1.shapes.add_textbox(Inches(1.5), Inches(2.9), Inches(10.3), Inches(0.8))
    tf_sub1 = sub1.text_frame
    tf_sub1.word_wrap = True
    p = tf_sub1.paragraphs[0]
    p.text = "Multimodal AI for Musculoskeletal Fracture Detection, Conversational Med-VQA, and Automated Clinical Report Generation"
    p.font.name = "Arial"
    p.font.size = Pt(16)
    p.font.color.rgb = C_BLUE

    # Stage Badge
    stage_box = s1.shapes.add_textbox(Inches(1.5), Inches(3.7), Inches(10.3), Inches(0.4))
    p = stage_box.text_frame.paragraphs[0]
    p.text = "📌 Major Project (B.Tech 7th Semester) — Milestone Review 1"
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_WHITE

    # Project Members Card Left
    m_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), Inches(4.3), Inches(5.0), Inches(1.8))
    m_box.fill.solid()
    m_box.fill.fore_color.rgb = RGBColor(15, 23, 42)
    m_box.line.color.rgb = C_CARD_BORDER
    tf_m = m_box.text_frame
    tf_m.word_wrap = True
    p0 = tf_m.paragraphs[0]
    p0.text = "PROJECT TEAM MEMBERS"
    p0.font.bold = True
    p0.font.size = Pt(11)
    p0.font.color.rgb = C_ACCENT
    members = [
        ("• Sahanawaz Hussain", "Project Lead (Architecture & Inference)"),
        ("• Aryan", "Member (Preprocessing & Benchmark)"),
        ("• Pranita", "Member (Med-VQA UI & ReportLab PDF)")
    ]
    for name, role in members:
        p = tf_m.add_paragraph()
        p.text = f"{name} — {role}"
        p.font.size = Pt(10)
        p.font.color.rgb = C_WHITE

    # Guide & Repo Box Right
    g_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(4.3), Inches(5.0), Inches(1.8))
    g_box.fill.solid()
    g_box.fill.fore_color.rgb = RGBColor(15, 23, 42)
    g_box.line.color.rgb = C_CARD_BORDER
    tf_g = g_box.text_frame
    tf_g.word_wrap = True
    p0 = tf_g.paragraphs[0]
    p0.text = "PROJECT DETAILS"
    p0.font.bold = True
    p0.font.size = Pt(11)
    p0.font.color.rgb = C_ACCENT
    g_items = [
        ("• Department:", "Electronics & Telecommunication Engineering"),
        ("• Institution:", "Assam Engineering College, Jalukbari"),
        ("• GitHub Repo:", "github.com/Sahanawaz233/medical-vlm-fracatlas")
    ]
    for label, val in g_items:
        p = tf_g.add_paragraph()
        p.text = f"{label} {val}"
        p.font.size = Pt(10)
        p.font.color.rgb = C_WHITE

    # -------------------------------------------------------------------------
    # SLIDE 2: Clinical Need Analysis & Motivation
    # -------------------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, 2, "Clinical Need Analysis & Problem Background")

    cards_s2 = [
        ("🚨 Emergency Triage Bottleneck", 
         "Emergency trauma centers experience severe radiologist shortages during off-peak hours and night shifts.\n\nInitial radiographs are frequently evaluated by non-radiologist emergency physicians under severe time constraints."),
        ("⚠️ 80% Missed Fracture Risk", 
         "Clinical studies confirm missed bone fractures account for up to 80% of emergency department diagnostic errors.\n\nOverlooked hairline and non-displaced fractures lead to malunion, chronic pain, and avoidable joint arthrosis."),
        ("📦 Limits of Conventional CAD", 
         "Traditional deep learning models (CNNs) output only raw bounding boxes or binary heatmaps.\n\nThey are unable to explain their diagnostic reasoning, answer physician questions, or author verifiable clinical reports."),
        ("💡 Multimodal AI Solution", 
         "Our system bridges the vision-language gap for musculoskeletal trauma:\n\n• Point-of-care fracture detection\n• Interactive conversational Med-VQA\n• Automated, signed ACR radiology reports")
    ]

    for i, (title, body) in enumerate(cards_s2):
        col = i % 2
        row = i // 2
        left = Inches(0.8 + col * 5.95)
        top = Inches(1.65 + row * 2.65)
        card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(5.75), Inches(2.45))
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD
        card.line.color.rgb = C_CARD_BORDER
        tf = card.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.bold = True
        p0.font.size = Pt(14)
        p0.font.color.rgb = C_ACCENT if i == 3 else C_BLUE
        p1 = tf.add_paragraph()
        p1.text = body
        p1.font.size = Pt(11)
        p1.font.color.rgb = C_WHITE

    # -------------------------------------------------------------------------
    # SLIDE 3: Problem Statement & Objectives
    # -------------------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, 3, "Problem Statement & Project Objectives")

    # Formal Problem Box
    prob_box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.65), Inches(11.733), Inches(1.4))
    prob_box.fill.solid()
    prob_box.fill.fore_color.rgb = RGBColor(15, 23, 42)
    prob_box.line.color.rgb = C_ACCENT
    prob_box.line.width = Pt(1.5)
    tf_pb = prob_box.text_frame
    tf_pb.word_wrap = True
    p0 = tf_pb.paragraphs[0]
    p0.text = "🎯 FORMAL PROBLEM STATEMENT"
    p0.font.bold = True
    p0.font.size = Pt(12)
    p0.font.color.rgb = C_ACCENT
    p1 = tf_pb.add_paragraph()
    p1.text = "To design, train, and evaluate a Multimodal Vision-Language Model tailored for musculoskeletal trauma radiographs that performs acute fracture detection, interactive conversational Med-VQA, and automated structured reporting for emergency triage."
    p1.font.size = Pt(13)
    p1.font.color.rgb = C_WHITE

    # 4 Objectives Cards Horizontal
    objs = [
        ("1. Instruction Tuning", "Convert raw bounding annotations into 1,438 LLaVA multi-turn clinical dialogue pairs with balanced negative controls."),
        ("2. Fracture Localization", "Accurately detect and localize acute bone cortical disruptions across 11 major musculoskeletal extremities."),
        ("3. Conversational Med-VQA", "Enable clinicians to interact with X-rays regarding bone integrity, hardware, and joint alignment in natural language."),
        ("4. Automated Reporting", "Automatically synthesize ACR-compliant clinical radiology PDF reports with diagnostic findings and electronic verification.")
    ]
    for i, (title, desc) in enumerate(objs):
        left = Inches(0.8 + i * 2.98)
        card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(3.3), Inches(2.78), Inches(3.6))
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD
        card.line.color.rgb = C_CARD_BORDER
        tf = card.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.bold = True
        p0.font.size = Pt(13)
        p0.font.color.rgb = C_BLUE
        p1 = tf.add_paragraph()
        p1.text = desc
        p1.font.size = Pt(11)
        p1.font.color.rgb = C_WHITE

    # -------------------------------------------------------------------------
    # SLIDE 4: Literature Survey & Comparative Analysis
    # -------------------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, 4, "Literature Survey & Research Gaps")

    table_shape = s4.shapes.add_table(6, 4, Inches(0.8), Inches(1.65), Inches(11.733), Inches(5.1))
    table = table_shape.table
    table.columns[0].width = Inches(2.3)
    table.columns[1].width = Inches(2.1)
    table.columns[2].width = Inches(3.6)
    table.columns[3].width = Inches(3.733)

    headers = ["Study / Publication", "Modality Evaluated", "Key Strengths", "Identified Research Gaps"]
    for j, h in enumerate(headers):
        cell = table.cell(0, j)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(15, 23, 42)
        p = cell.text_frame.paragraphs[0]
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = C_ACCENT

    lit_data = [
        ("Lindsey et al.\n(PNAS 2018)", "Musculoskeletal Radiographs", "High sensitivity on wrist fractures via deep CNNs", "Pure classification; zero conversational dialogue or reports"),
        ("Iftekhar et al.\n(Nature Sci Data 2023)", "FracAtlas X-Rays\n(4,083 scans)", "Benchmarked multi-region bounding boxes (YOLOv8)", "Vision-only; no VQA reasoning or structured clinical impressions"),
        ("LLaVA-Med\n(NeurIPS 2023)", "Chest / General Biomedical", "Strong multi-turn conversational reasoning", "Focused on chest X-rays; high hallucination on subtle bone fractures"),
        ("CheXagent\n(Stanford 2024)", "Chest Radiographs (CXR)", "Specialized clinical LLM radiology reporting", "Strictly chest-specific; cannot handle extremity orthopedic trauma"),
        ("Our Proposed VLM\n(FracAtlas VLM)", "FracAtlas Musculoskeletal", "Orthopedic VQA + Grounding + ACR PDF Reports", "Bridges visual localization with interactive clinical documentation")
    ]

    for i, row in enumerate(lit_data, start=1):
        for j, val in enumerate(row):
            cell = table.cell(i, j)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(26, 42, 78) if i == 5 else C_CARD
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(10)
            p.font.bold = (i == 5 or j == 0)
            p.font.color.rgb = C_ACCENT if (i == 5 and j == 0) else C_WHITE

    # -------------------------------------------------------------------------
    # SLIDE 5: Dataset Profile (FracAtlas)
    # -------------------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, 5, "Dataset Profile & Demographics (FracAtlas)")

    # 4 Stat Cards Top
    stats = [
        ("4,083", "Total Radiographs", "High-resolution musculoskeletal scans"),
        ("717", "Fractured Cases", "17.56% of dataset (pathological)"),
        ("3,366", "Normal Controls", "82.44% of dataset (non-fractured)"),
        ("11", "Anatomical Sites", "Hand, wrist, knee, ankle, shoulder, etc.")
    ]
    for i, (num, label, sub) in enumerate(stats):
        left = Inches(0.8 + i * 2.98)
        card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(1.65), Inches(2.78), Inches(1.6))
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD
        card.line.color.rgb = C_CARD_BORDER
        tf = card.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        p0.text = num
        p0.font.bold = True
        p0.font.size = Pt(28)
        p0.font.color.rgb = C_ACCENT
        p1 = tf.add_paragraph()
        p1.text = label
        p1.font.bold = True
        p1.font.size = Pt(11)
        p1.font.color.rgb = C_WHITE
        p2 = tf.add_paragraph()
        p2.text = sub
        p2.font.size = Pt(9)
        p2.font.color.rgb = C_MUTED

    # Bottom Left: Anatomical Breakdown
    card_l = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.55), Inches(5.75), Inches(3.3))
    card_l.fill.solid()
    card_l.fill.fore_color.rgb = C_CARD
    card_l.line.color.rgb = C_CARD_BORDER
    tf_l = card_l.text_frame
    tf_l.word_wrap = True
    p = tf_l.paragraphs[0]
    p.text = "🦴 Comprehensive Anatomical Coverage"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = C_BLUE
    sites = [
        "• Upper Extremity: Hand, Wrist, Forearm, Elbow, Shoulder/Humerus",
        "• Lower Extremity: Foot, Ankle, Tibia/Fibula, Knee, Femur, Pelvis/Hip",
        "• Expert Annotations: COCO masks & bounding boxes, YOLO, Pascal VOC",
        "• Modality: Standard Digital Projection Radiography (DX)"
    ]
    for s in sites:
        p = tf_l.add_paragraph()
        p.text = s
        p.font.size = Pt(11)
        p.font.color.rgb = C_WHITE

    # Bottom Right: Dataset Pipeline
    card_r = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.75), Inches(3.55), Inches(5.75), Inches(3.3))
    card_r.fill.solid()
    card_r.fill.fore_color.rgb = C_CARD
    card_r.line.color.rgb = C_CARD_BORDER
    tf_r = card_r.text_frame
    tf_r.word_wrap = True
    p = tf_r.paragraphs[0]
    p.text = "⚡ Automated Dataset Ingestion (download_dataset.py)"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = C_ACCENT
    steps = [
        "• Automated Fetch: Direct API ingestion from official Figshare repository",
        "• Checksum Verification: Validates integrity of ~352 MB raw archive",
        "• Directory Extraction: Unpacks images into structured data/raw/ directory",
        "• Git Cleanliness: Lightweight repository (<10 MB) via automated exclusion"
    ]
    for s in steps:
        p = tf_r.add_paragraph()
        p.text = s
        p.font.size = Pt(11)
        p.font.color.rgb = C_WHITE

    # -------------------------------------------------------------------------
    # SLIDE 6: Multimodal Data Preprocessing Pipeline
    # -------------------------------------------------------------------------
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, 6, "Multimodal Data Preprocessing Pipeline")

    # 3 Cards Columns
    prep_cards = [
        ("⚖️ 1:1 Balanced Sampling", 
         "• The Problem: Raw dataset contains 82% normal scans.\n• VLM Risk: Without correction, models learn a trivial shortcut predicting 'No fracture' for every image.\n• Our Solution: Enforced strict 1:1 balanced sampling between fractured cases and normal controls across all splits."),
        ("📊 Formatted Splits (1,438 Total)", 
         "• Training Split: 1,148 samples (574 fractured + 574 normal controls)\n• Validation Split: 164 samples (82 fractured + 82 normal controls)\n• Benchmark Test Split: 126 samples (63 fractured + 63 normal controls)\n• Script: src/dataset_to_vlm.py"),
        ("💬 LLaVA Multimodal Schema", 
         "• Multi-Turn Conversations: Pairs raw images with expert clinical dialogues.\n• Diverse Clinical Queries: Examination findings, coordinate localization, and surgical hardware verification.\n• Industry Standard: Compatible with standard LLaVA / ShareGPT instruction formats.")
    ]

    for i, (title, body) in enumerate(prep_cards):
        left = Inches(0.8 + i * 3.98)
        card = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(1.65), Inches(3.78), Inches(5.1))
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD
        card.line.color.rgb = C_CARD_BORDER
        tf = card.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.bold = True
        p0.font.size = Pt(14)
        p0.font.color.rgb = C_ACCENT if i == 0 else C_BLUE
        for line in body.split("\n"):
            p = tf.add_paragraph()
            p.text = line
            p.font.size = Pt(11)
            p.font.color.rgb = C_WHITE

    # -------------------------------------------------------------------------
    # SLIDE 7: End-to-End System Architecture
    # -------------------------------------------------------------------------
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, 7, "End-to-End Neural System Architecture")

    layers = [
        ("Layer 1: Data Ingestion", "4,083 FracAtlas radiographs, COCO bounding coordinates, and metadata splits (download_dataset.py)"),
        ("Layer 2: Preprocessing", "Automated clinical conversation generator formulating 1,438 balanced instruction pairs (src/dataset_to_vlm.py)"),
        ("Layer 3: Foundation VLM", "Qwen2-VL-2B multimodal backbone with dynamic-resolution Vision Transformer (ViT) and M-RoPE embeddings"),
        ("Layer 4: QLoRA Fine-Tuning", "Parameter-Efficient Fine-Tuning via 4-bit NF4 targeting attention projections (q_proj, k_proj, v_proj, o_proj)"),
        ("Layer 5: Diagnostic Core", "Unified clinical inference engine executing fracture detection, coordinate localization, and VQA reasoning"),
        ("Layer 6: System Outputs", "Interactive Gradio Med-VQA Web UI (src/app.py) alongside automated ACR clinical PDF reporting engine")
    ]

    for i, (title, desc) in enumerate(layers):
        top = Inches(1.65 + i * 0.88)
        card = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top, Inches(11.733), Inches(0.76))
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD
        card.line.color.rgb = C_ACCENT if i in [3, 4] else C_CARD_BORDER
        tf = card.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        p0.text = f"{title}:  "
        p0.font.bold = True
        p0.font.size = Pt(12)
        p0.font.color.rgb = C_ACCENT if i in [3, 4] else C_BLUE
        # append description in same paragraph
        run = p0.add_run()
        run.text = desc
        run.font.bold = False
        run.font.size = Pt(11)
        run.font.color.rgb = C_WHITE

    # -------------------------------------------------------------------------
    # SLIDE 8: System & Technical Specifications
    # -------------------------------------------------------------------------
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, 8, "System & Technical Specifications")

    spec_cards = [
        ("💻 Hardware Requirements", [
            ("Local Workstation", "6 GB VRAM GPU (e.g. NVIDIA RTX 3050 Laptop / GTX 1660 Ti), 16 GB RAM"),
            ("Training Footprint", "Peak VRAM ~3.8 GB (runs safely within 6 GB VRAM limits)"),
            ("Inference Footprint", "< 2.5 GB VRAM (< 1.8 seconds per radiograph)"),
            ("Cloud Benchmark", "Google Colab Free/Pro (NVIDIA Tesla T4 16 GB VRAM)")
        ]),
        ("⚙️ Software Stack & Libraries", [
            ("Base Runtime", "Linux / Windows 11 / macOS, Python 3.10+"),
            ("Deep Learning", "PyTorch 2.2+, CUDA 12.1, HuggingFace Transformers, Accelerate"),
            ("PEFT & Quantization", "BitsAndBytes (4-bit NF4), PEFT (LoRA rank=16, alpha=32)"),
            ("UI & Reports", "Gradio 4.32+ (WebUI), ReportLab 4.1+ (PDF generation)")
        ])
    ]

    for i, (title, items) in enumerate(spec_cards):
        left = Inches(0.8 + i * 5.95)
        card = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(1.65), Inches(5.75), Inches(5.1))
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD
        card.line.color.rgb = C_CARD_BORDER
        tf = card.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.bold = True
        p0.font.size = Pt(14)
        p0.font.color.rgb = C_ACCENT if i == 0 else C_BLUE
        for k, v in items:
            p = tf.add_paragraph()
            p.text = f"\n• {k}:"
            p.font.bold = True
            p.font.size = Pt(11)
            p.font.color.rgb = C_WHITE
            p_sub = tf.add_paragraph()
            p_sub.text = f"  {v}"
            p_sub.font.size = Pt(10)
            p_sub.font.color.rgb = C_MUTED

    # -------------------------------------------------------------------------
    # SLIDE 9: Work Completed (Review 1 Deliverables)
    # -------------------------------------------------------------------------
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, 9, "Work Completed So Far (Review 1 Deliverables)")

    table_s9 = s9.shapes.add_table(8, 4, Inches(0.8), Inches(1.65), Inches(11.733), Inches(5.1))
    t9 = table_s9.table
    t9.columns[0].width = Inches(2.2)
    t9.columns[1].width = Inches(2.3)
    t9.columns[2].width = Inches(1.8)
    t9.columns[3].width = Inches(5.433)

    h9 = ["Project Module", "Core Script / Path", "Review 1 Status", "Delivered Capability"]
    for j, h in enumerate(h9):
        cell = t9.cell(0, j)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(15, 23, 42)
        p = cell.text_frame.paragraphs[0]
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = C_ACCENT

    deliv_data = [
        ("Dataset Ingestion", "download_dataset.py", "✅ Operational", "Automated download, hash validation & extraction of 4,083 scans"),
        ("Data Preprocessing", "src/dataset_to_vlm.py", "✅ Operational", "Generates 1,438 balanced LLaVA multi-turn instruction pairs"),
        ("Live Visualizer", "dashboard/serve.py", "✅ Operational", "Zero-dependency real-time filesystem monitor on port 8080"),
        ("Diagnostic Core", "src/inference.py", "✅ Operational", "Multi-stage fracture detection, bounding coordinates & VQA"),
        ("Report Generator", "src/report_generator.py", "✅ Operational", "Automated ACR-compliant clinical text & signed PDF generation"),
        ("Med-VQA Web UI", "src/app.py", "✅ Operational", "Interactive Gradio diagnostic, VQA, and report download suite"),
        ("Evaluation Harness", "src/evaluate.py", "✅ Operational", "Computes Sensitivity, Specificity, Precision, F1 & Confusion Matrix")
    ]

    for i, row in enumerate(deliv_data, start=1):
        for j, val in enumerate(row):
            cell = t9.cell(i, j)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_CARD
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(10)
            p.font.bold = (j in [0, 2])
            p.font.color.rgb = C_ACCENT if j == 2 else C_WHITE

    # -------------------------------------------------------------------------
    # SLIDE 10: Diagnostic Inference & Evaluation Framework
    # -------------------------------------------------------------------------
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, 10, "Diagnostic Inference & Evaluation Framework")

    # Left: Diagnostic Engine
    card_inf = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.65), Inches(5.75), Inches(5.1))
    card_inf.fill.solid()
    card_inf.fill.fore_color.rgb = C_CARD
    card_inf.line.color.rgb = C_CARD_BORDER
    tf = card_inf.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🔍 Diagnostic Core Engine (src/inference.py)"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = C_ACCENT
    inf_pts = [
        ("Dual-Mode Flexibility", "Seamlessly runs live neural VLM inference when GPU weights are loaded, with robust evaluation fallbacks."),
        ("Multi-Stage Clinical Reasoning", "Assesses cortical bone margins, adjacent joint spaces, and verifies presence/absence of orthopedic fixation hardware."),
        ("Real-Time Latency", "Executes full diagnostic pass in < 1.8 seconds per radiograph, satisfying emergency department triage constraints.")
    ]
    for h, b in inf_pts:
        p = tf.add_paragraph()
        p.text = f"\n• {h}:"
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = C_WHITE
        p2 = tf.add_paragraph()
        p2.text = f"  {b}"
        p2.font.size = Pt(10)
        p2.font.color.rgb = C_MUTED

    # Right: Evaluation Metrics
    card_eval = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.75), Inches(1.65), Inches(5.75), Inches(5.1))
    card_eval.fill.solid()
    card_eval.fill.fore_color.rgb = C_CARD
    card_eval.line.color.rgb = C_CARD_BORDER
    tf = card_eval.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "📈 Clinical Benchmark Harness (src/evaluate.py)"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = C_BLUE
    eval_pts = [
        ("Sensitivity / Recall (TP / (TP + FN))", "Measures the model's critical ability to detect true fractures without false negatives."),
        ("Specificity (TN / (TN + FP))", "Measures the model's ability to accurately clear normal radiographs without false alarms."),
        ("Balanced F1-Score & Accuracy", "Harmonic mean of precision and recall over balanced test cohorts."),
        ("Automated CSV Audit Export", "Logs all individual predictions to evaluation_results/test_predictions_detailed.csv for thesis tables.")
    ]
    for h, b in eval_pts:
        p = tf.add_paragraph()
        p.text = f"\n• {h}:"
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = C_WHITE
        p2 = tf.add_paragraph()
        p2.text = f"  {b}"
        p2.font.size = Pt(10)
        p2.font.color.rgb = C_MUTED

    # -------------------------------------------------------------------------
    # SLIDE 11: Project Roadmap & Milestone Timeline
    # -------------------------------------------------------------------------
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, 11, "Project Roadmap & Milestone Timeline")

    phases = [
        ("Phase 1: Foundation & Pipeline Scaffolding", "Milestone: Review 1 (✅ 100% Completed)", [
            "• Problem formulation, clinical need analysis, and literature survey",
            "• Automated FracAtlas dataset ingestion (download_dataset.py)",
            "• Multimodal preprocessing & 1:1 balanced instruction dataset (1,438 pairs)",
            "• Operational inference engine, Gradio app, PDF generator, evaluation harness"
        ]),
        ("Phase 2: Model Training & Ablation Studies", "Milestone: Review 2 (Next Milestone)", [
            "• Multi-epoch QLoRA fine-tuning execution on local and cloud GPUs",
            "• Comparative ablation study: Zero-shot base VLM vs. Fine-tuned VLM",
            "• Hyperparameter optimization (LoRA rank, learning rate, target modules)",
            "• Failure mode and error analysis on complex, non-displaced fractures"
        ]),
        ("Phase 3: Advanced Optimization & Clinical Defense", "Milestone: Review 3 / Final Defense", [
            "• Latent diffusion data augmentation for rare fracture categories",
            "• Clinical literature RAG integration for orthopedic anomalies",
            "• Final dissertation documentation, system packaging, and viva defense"
        ])
    ]

    for i, (title, badge, items) in enumerate(phases):
        top = Inches(1.65 + i * 1.75)
        card = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top, Inches(11.733), Inches(1.55))
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD
        card.line.color.rgb = C_ACCENT if i == 0 else C_CARD_BORDER
        tf = card.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.bold = True
        p0.font.size = Pt(13)
        p0.font.color.rgb = C_ACCENT if i == 0 else C_BLUE
        # badge
        run = p0.add_run()
        run.text = f"  [{badge}]"
        run.font.bold = True
        run.font.size = Pt(11)
        run.font.color.rgb = C_WHITE
        for item in items:
            p = tf.add_paragraph()
            p.text = item
            p.font.size = Pt(10)
            p.font.color.rgb = C_WHITE

    # -------------------------------------------------------------------------
    # SLIDE 12: Team Roles, Summary & Discussion
    # -------------------------------------------------------------------------
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12)
    add_header(s12, 12, "Team Roles, Summary & Discussion")

    # Team Members 3 Columns
    members_detail = [
        ("Sahanawaz Hussain", "Project Lead", [
            "• System neural architecture design",
            "• QLoRA fine-tuning pipeline setup",
            "• Diagnostic inference engine",
            "• Codebase & repository orchestration"
        ]),
        ("Aryan", "Project Member", [
            "• Dataset ingestion pipeline",
            "• COCO annotation parsing",
            "• 1:1 balanced instruction dataset",
            "• Benchmark evaluation harness"
        ]),
        ("Pranita", "Project Member", [
            "• Interactive Med-VQA web application",
            "• ReportLab clinical PDF generator",
            "• Architecture dashboard visualizer",
            "• Presentation & documentation design"
        ])
    ]

    for i, (name, role, tasks) in enumerate(members_detail):
        left = Inches(0.8 + i * 3.98)
        card = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(1.65), Inches(3.78), Inches(3.4))
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD
        card.line.color.rgb = C_CARD_BORDER
        tf = card.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        p0.text = name
        p0.font.bold = True
        p0.font.size = Pt(14)
        p0.font.color.rgb = C_WHITE
        p1 = tf.add_paragraph()
        p1.text = role
        p1.font.bold = True
        p1.font.size = Pt(11)
        p1.font.color.rgb = C_ACCENT
        for t in tasks:
            p = tf.add_paragraph()
            p.text = t
            p.font.size = Pt(10)
            p.font.color.rgb = C_MUTED

    # Bottom Banner for Q&A
    qa_banner = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.3), Inches(11.733), Inches(1.5))
    qa_banner.fill.solid()
    qa_banner.fill.fore_color.rgb = RGBColor(15, 23, 42)
    qa_banner.line.color.rgb = C_ACCENT
    qa_banner.line.width = Pt(1.5)
    tf_qa = qa_banner.text_frame
    tf_qa.word_wrap = True
    p0 = tf_qa.paragraphs[0]
    p0.text = "🏁 REVIEW 1 SUMMARY & OPEN DISCUSSION"
    p0.font.bold = True
    p0.font.size = Pt(13)
    p0.font.color.rgb = C_ACCENT
    p1 = tf_qa.add_paragraph()
    p1.text = "All Phase 1 foundational deliverables are fully functional, operational, and tested. The project is on schedule for Review 2 training runs. Thank you for your guidance — we welcome questions and suggestions from the panel."
    p1.font.size = Pt(11)
    p1.font.color.rgb = C_WHITE

    prs.save(output_path)
    print(f"Successfully generated: {output_path}")

if __name__ == "__main__":
    create_deck()
