#!/usr/bin/env python3
"""
FracAtlas Multimodal Data Preprocessing Pipeline
=================================================
Converts raw musculoskeletal radiographs, fracture split CSVs, and COCO/VOC
annotations into standard Vision-Language Model (VLM) instruction-tuning datasets.

Outputs:
  - data/processed/train.json (LLaVA / ShareGPT format)
  - data/processed/val.json
  - data/processed/test.json
  - data/processed/dataset_summary.json
"""

import os
import sys
import json
import csv
import random
import argparse
from pathlib import Path


# Clinical prompt templates for diverse multi-turn training
CLINICAL_PROMPTS_FRACTURE = [
    {
        "question": "<image>\nExamine this musculoskeletal radiograph carefully. Describe your diagnostic findings and indicate if any fracture is present.",
        "findings_template": "FINDINGS: Discernible cortical bone disruption and acute fracture identified. {loc_desc}No signs of chronic healing or remodeling. Adjacent joint spaces are preserved without gross dislocation.\n\nIMPRESSION: Positive for acute musculoskeletal fracture. Orthopedic consultation and clinical correlation recommended."
    },
    {
        "question": "<image>\nIs there evidence of a bone fracture or acute structural injury in this radiograph?",
        "findings_template": "Yes. An acute cortical fracture is present. {loc_desc}Surrounding soft tissue swelling is consistent with an acute traumatic etiology."
    },
    {
        "question": "<image>\nPlease inspect this X-ray and localize any traumatic bone pathology.",
        "findings_template": "FRACTURE LOCALIZATION: Structural cortical disruption detected at bounding coordinates {boxes}. Diagnostic impression: Acute fracture."
    }
]

CLINICAL_PROMPTS_NORMAL = [
    {
        "question": "<image>\nExamine this musculoskeletal radiograph carefully. Describe your diagnostic findings and indicate if any fracture is present.",
        "findings_template": "FINDINGS: Cortical margins are smooth and intact throughout the visualized osseous structures. No evidence of acute fracture, dislocation, or joint effusion. Soft tissues are unremarkable.\n\nIMPRESSION: No acute fracture or dislocation. Normal musculoskeletal radiograph."
    },
    {
        "question": "<image>\nIs there evidence of a bone fracture or acute structural injury in this radiograph?",
        "findings_template": "No. There is no evidence of an acute fracture, dislocation, or bone cortical defect. Normal osseous architecture."
    },
    {
        "question": "<image>\nPlease inspect this X-ray and localize any traumatic bone pathology.",
        "findings_template": "FRACTURE LOCALIZATION: Negative for traumatic bone pathology. No fracture or cortical disruption identified in this radiograph."
    }
]


def load_coco_annotations(coco_path):
    """Load COCO format fracture bounding boxes and image metadata."""
    if not os.path.exists(coco_path):
        print(f"[Warning] COCO annotations not found at: {coco_path}")
        return {}

    with open(coco_path, 'r', encoding='utf-8') as f:
        coco = json.load(f)

    # Map image_id -> image info
    img_id_to_info = {img['id']: img for img in coco.get('images', [])}
    file_to_boxes = {}

    for ann in coco.get('annotations', []):
        img_id = ann.get('image_id')
        img_info = img_id_to_info.get(img_id)
        if not img_info:
            continue
        file_name = img_info['file_name']
        bbox = ann.get('bbox', [])  # [x, y, width, height]
        if bbox and len(bbox) == 4:
            x, y, w, h = bbox
            # Normalized or rounded coordinates
            box_coords = [round(x, 1), round(y, 1), round(x + w, 1), round(y + h, 1)]
            if file_name not in file_to_boxes:
                file_to_boxes[file_name] = []
            file_to_boxes[file_name].append(box_coords)

    return file_to_boxes


def load_split_csv(csv_path):
    """Load image filenames from fracture split CSV."""
    if not os.path.exists(csv_path):
        return []
    filenames = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for row in reader:
            if row:
                filenames.append(row[0].strip())
    return filenames


def generate_llava_sample(sample_id, rel_image_path, is_fractured, bboxes, rng):
    """Generate a LLaVA-style instruction-response pair."""
    if is_fractured:
        template = rng.choice(CLINICAL_PROMPTS_FRACTURE)
        if bboxes:
            boxes_str = ", ".join([f"[{b[0]}, {b[1]}, {b[2]}, {b[3]}]" for b in bboxes])
            loc_desc = f"The primary fracture site is localized at bounding coordinates {boxes_str}. "
        else:
            boxes_str = "visualized region"
            loc_desc = "Fracture is visualized along the cortical bone margin. "
        response_text = template["findings_template"].format(loc_desc=loc_desc, boxes=boxes_str)
    else:
        template = rng.choice(CLINICAL_PROMPTS_NORMAL)
        response_text = template["findings_template"]

    return {
        "id": sample_id,
        "image": rel_image_path,
        "is_fractured": is_fractured,
        "bboxes": bboxes if is_fractured else [],
        "conversations": [
            {
                "from": "human",
                "value": template["question"]
            },
            {
                "from": "gpt",
                "value": response_text
            }
        ]
    }


def main():
    parser = argparse.ArgumentParser(description="FracAtlas Multimodal VLM Preprocessor")
    parser.add_argument("--data_dir", type=str, default="data/raw/FracAtlas/FracAtlas",
                        help="Path to extracted FracAtlas dataset")
    parser.add_argument("--output_dir", type=str, default="data/processed",
                        help="Output directory for processed VLM JSON files")
    parser.add_argument("--negative_ratio", type=float, default=1.0,
                        help="Ratio of normal (non-fractured) samples per fractured sample (e.g. 1.0 for balanced 1:1)")
    parser.add_argument("--seed", type=int, default=42,
                        help="Random seed for deterministic split and prompt selection")
    args = parser.parse_args()

    rng = random.Random(args.seed)

    print("=" * 65)
    print("      FracAtlas Vision-Language Data Preprocessing Pipeline      ")
    print("=" * 65)

    base_dir = Path(args.data_dir)
    images_frac_dir = base_dir / "images" / "Fractured"
    images_norm_dir = base_dir / "images" / "Non_fractured"
    splits_dir = base_dir / "Utilities" / "Fracture Split"
    coco_path = base_dir / "Annotations" / "COCO JSON" / "COCO_fracture_masks.json"
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if not images_frac_dir.exists() or not images_norm_dir.exists():
        print(f"[Error] Images directory not found at {base_dir / 'images'}")
        print("Please ensure download_dataset.py has finished extracting.")
        sys.exit(1)

    print(f"[1/4] Loading fracture annotations from COCO...")
    coco_boxes = load_coco_annotations(str(coco_path))
    print(f"      Mapped bounding boxes for {len(coco_boxes)} fractured images.")

    print(f"[2/4] Loading official dataset splits...")
    train_frac_files = load_split_csv(str(splits_dir / "train.csv"))
    valid_frac_files = load_split_csv(str(splits_dir / "valid.csv"))
    test_frac_files = load_split_csv(str(splits_dir / "test.csv"))

    all_frac_files = sorted([f.name for f in images_frac_dir.iterdir() if f.suffix.lower() in ('.jpg', '.png', '.jpeg')])
    if not train_frac_files:
        print("      Split CSVs not found, generating deterministic 80/10/10 split...")
        shuffled_frac = all_frac_files.copy()
        rng.shuffle(shuffled_frac)
        n = len(shuffled_frac)
        train_frac_files = shuffled_frac[:int(0.8 * n)]
        valid_frac_files = shuffled_frac[int(0.8 * n):int(0.9 * n)]
        test_frac_files = shuffled_frac[int(0.9 * n):]

    print(f"      Fractured split: {len(train_frac_files)} train, {len(valid_frac_files)} val, {len(test_frac_files)} test")

    # Process Non-fractured images
    all_norm_files = sorted([f.name for f in images_norm_dir.iterdir() if f.suffix.lower() in ('.jpg', '.png', '.jpeg')])
    rng.shuffle(all_norm_files)
    print(f"      Found {len(all_norm_files)} normal (non-fractured) radiographs.")

    # Determine balanced negative subset according to negative_ratio
    total_frac = len(train_frac_files) + len(valid_frac_files) + len(test_frac_files)
    target_norm_count = int(total_frac * args.negative_ratio) if args.negative_ratio > 0 else len(all_norm_files)
    selected_norm_files = all_norm_files[:min(target_norm_count, len(all_norm_files))]

    # Distribute normal images into train/val/test using same proportions
    n_norm = len(selected_norm_files)
    r_train = len(train_frac_files) / total_frac
    r_val = len(valid_frac_files) / total_frac
    n_train_norm = int(n_norm * r_train)
    n_val_norm = int(n_norm * r_val)

    train_norm_files = selected_norm_files[:n_train_norm]
    valid_norm_files = selected_norm_files[n_train_norm:n_train_norm + n_val_norm]
    test_norm_files = selected_norm_files[n_train_norm + n_val_norm:]

    print(f"      Normal split (Ratio {args.negative_ratio}:1): {len(train_norm_files)} train, {len(valid_norm_files)} val, {len(test_norm_files)} test")

    print(f"[3/4] Synthesizing multi-turn clinical VLM conversations...")

    def build_split(frac_list, norm_list, split_name):
        dataset = []
        # Add fractured
        for fname in frac_list:
            img_rel = f"data/raw/FracAtlas/FracAtlas/images/Fractured/{fname}"
            sample_id = f"frac_{Path(fname).stem}"
            bboxes = coco_boxes.get(fname, [])
            sample = generate_llava_sample(sample_id, img_rel, is_fractured=True, bboxes=bboxes, rng=rng)
            dataset.append(sample)

        # Add normal
        for fname in norm_list:
            img_rel = f"data/raw/FracAtlas/FracAtlas/images/Non_fractured/{fname}"
            sample_id = f"norm_{Path(fname).stem}"
            sample = generate_llava_sample(sample_id, img_rel, is_fractured=False, bboxes=[], rng=rng)
            dataset.append(sample)

        rng.shuffle(dataset)
        return dataset

    train_data = build_split(train_frac_files, train_norm_files, "train")
    val_data = build_split(valid_frac_files, valid_norm_files, "val")
    test_data = build_split(test_frac_files, test_norm_files, "test")

    print(f"[4/4] Saving processed datasets to {output_dir}...")
    with open(output_dir / "train.json", 'w', encoding='utf-8') as f:
        json.dump(train_data, f, indent=2)

    with open(output_dir / "val.json", 'w', encoding='utf-8') as f:
        json.dump(val_data, f, indent=2)

    with open(output_dir / "test.json", 'w', encoding='utf-8') as f:
        json.dump(test_data, f, indent=2)

    # Save summary metadata
    summary = {
        "dataset_name": "FracAtlas VLM Instruction Dataset",
        "total_samples": len(train_data) + len(val_data) + len(test_data),
        "negative_ratio": args.negative_ratio,
        "splits": {
            "train": {
                "total": len(train_data),
                "fractured": len(train_frac_files),
                "normal": len(train_norm_files)
            },
            "validation": {
                "total": len(val_data),
                "fractured": len(valid_frac_files),
                "normal": len(valid_norm_files)
            },
            "test": {
                "total": len(test_data),
                "fractured": len(test_frac_files),
                "normal": len(test_norm_files)
            }
        },
        "format": "LLaVA / ShareGPT Multimodal Conversation",
        "sample_schema": {
            "id": "string",
            "image": "relative_path_to_radiograph",
            "is_fractured": "boolean",
            "bboxes": "list of [x1, y1, x2, y2]",
            "conversations": [
                {"from": "human", "value": "<image> + clinical question"},
                {"from": "gpt", "value": "findings and impression response"}
            ]
        }
    }

    with open(output_dir / "dataset_summary.json", 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)

    print("\n" + "=" * 65)
    print("SUCCESS: VLM Multimodal Dataset Ready!")
    print(f"  - Train Set : {output_dir / 'train.json'} ({len(train_data)} samples)")
    print(f"  - Val Set   : {output_dir / 'val.json'} ({len(val_data)} samples)")
    print(f"  - Test Set  : {output_dir / 'test.json'} ({len(test_data)} samples)")
    print(f"  - Summary   : {output_dir / 'dataset_summary.json'}")
    print("=" * 65 + "\n")


if __name__ == "__main__":
    main()
