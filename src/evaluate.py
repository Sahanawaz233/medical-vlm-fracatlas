#!/usr/bin/env python3
"""
FracAtlas Model Evaluation & Academic Benchmark Harness
======================================================
Evaluates the fine-tuned VLM against test radiographs (data/processed/test.json)
and computes formal radiologist metrics for final year project defense:
  - Sensitivity / Recall (Fracture detection rate)
  - Specificity (True negative rate on normal radiographs)
  - Precision / Positive Predictive Value (PPV)
  - F1-Score & Overall Diagnostic Accuracy
  - Confusion Matrix (TP, FP, TN, FN)
  - CSV report export for project dissertation tables
"""

import os
import sys
import json
import csv
import time
import argparse
from pathlib import Path

# Add src/ to path
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SRC_DIR)
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from inference import MedicalVLMInferenceEngine


def evaluate_test_set(test_json_path, output_dir="evaluation_results", max_samples=None):
    """Run full benchmark evaluation on the test dataset."""
    os.makedirs(output_dir, exist_ok=True)

    if not os.path.exists(test_json_path):
        print(f"[Error] Test dataset not found at: {test_json_path}")
        print("Please run `python src/dataset_to_vlm.py` first.")
        return None

    with open(test_json_path, 'r', encoding='utf-8') as f:
        test_samples = json.load(f)

    if max_samples and max_samples > 0:
        test_samples = test_samples[:max_samples]

    print("=" * 65)
    print(f"  FracAtlas VLM Clinical Benchmark Evaluation")
    print(f"  Evaluating {len(test_samples)} test radiographs...")
    print("=" * 65)

    engine = MedicalVLMInferenceEngine()
    engine.load_model()

    tp, fp, tn, fn = 0, 0, 0, 0
    detailed_results = []
    start_time = time.time()

    for idx, sample in enumerate(test_samples, 1):
        image_rel = sample.get("image", "")
        full_img_path = os.path.join(PROJECT_DIR, image_rel)
        ground_truth_fracture = sample.get("is_fractured", False)

        try:
            diag = engine.diagnose_xray(full_img_path)
            pred_fracture = diag.get("fracture_detected", False)
            confidence = diag.get("confidence", 0.0)

            # Confusion Matrix Counters
            if ground_truth_fracture and pred_fracture:
                tp += 1
                result_type = "TP"
            elif not ground_truth_fracture and not pred_fracture:
                tn += 1
                result_type = "TN"
            elif not ground_truth_fracture and pred_fracture:
                fp += 1
                result_type = "FP"
            else:
                fn += 1
                result_type = "FN"

            detailed_results.append({
                "id": sample.get("id", f"sample_{idx}"),
                "image": image_rel,
                "ground_truth": "FRACTURED" if ground_truth_fracture else "NORMAL",
                "prediction": "FRACTURED" if pred_fracture else "NORMAL",
                "confidence": round(confidence, 3),
                "result": result_type
            })

            # Progress print
            if idx % 10 == 0 or idx == len(test_samples):
                print(f"[{idx}/{len(test_samples)}] Processed (Current TP: {tp}, TN: {tn}, FP: {fp}, FN: {fn})")

        except Exception as e:
            print(f"[Error] Failed evaluating sample {image_rel}: {e}")

    elapsed = time.time() - start_time
    total = tp + fp + tn + fn

    if total == 0:
        print("[Error] No samples were evaluated.")
        return None

    # Compute Statistical Diagnostic Metrics
    accuracy = (tp + tn) / total
    sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0.0  # Recall
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0.0
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    f1_score = 2 * (precision * sensitivity) / (precision + sensitivity) if (precision + sensitivity) > 0 else 0.0

    print("\n" + "=" * 65)
    print("                CLINICAL BENCHMARK RESULTS")
    print("=" * 65)
    print(f"Total Test Radiographs Evaluated : {total}")
    print(f"Time Elapsed                     : {elapsed:.2f} s ({elapsed/total:.2f} s/image)")
    print("-" * 65)
    print(f"Overall Diagnostic Accuracy       : {accuracy * 100:.2f}%")
    print(f"Sensitivity / Recall (Fracture)  : {sensitivity * 100:.2f}%")
    print(f"Specificity (Normal Control)     : {specificity * 100:.2f}%")
    print(f"Precision / PPV                  : {precision * 100:.2f}%")
    print(f"Balanced F1-Score                : {f1_score * 100:.2f}%")
    print("-" * 65)
    print("CONFUSION MATRIX:")
    print(f"  True Positives  (TP) : {tp:4d}  |  False Positives (FP) : {fp:4d}")
    print(f"  False Negatives (FN) : {fn:4d}  |  True Negatives  (TN) : {tn:4d}")
    print("=" * 65 + "\n")

    # Export to CSV for report / thesis tables
    csv_path = os.path.join(output_dir, "test_predictions_detailed.csv")
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["id", "image", "ground_truth", "prediction", "confidence", "result"])
        writer.writeheader()
        writer.writerows(detailed_results)

    # Export summary JSON
    summary_path = os.path.join(output_dir, "benchmark_metrics_summary.json")
    summary = {
        "evaluation_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_test_samples": total,
        "elapsed_seconds": round(elapsed, 2),
        "metrics": {
            "accuracy": round(accuracy, 4),
            "sensitivity_recall": round(sensitivity, 4),
            "specificity": round(specificity, 4),
            "precision": round(precision, 4),
            "f1_score": round(f1_score, 4)
        },
        "confusion_matrix": {
            "true_positives": tp,
            "false_positives": fp,
            "true_negatives": tn,
            "false_negatives": fn
        }
    }
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)

    print(f"[Export] Detailed CSV results saved to: {csv_path}")
    print(f"[Export] Summary metrics JSON saved to: {summary_path}\n")

    return summary


def main():
    parser = argparse.ArgumentParser(description="FracAtlas Benchmark Evaluation Harness")
    parser.add_argument("--test_data", type=str, default="data/processed/test.json",
                        help="Path to processed test JSON")
    parser.add_argument("--output_dir", type=str, default="evaluation_results",
                        help="Directory to save benchmark metrics and CSV")
    parser.add_argument("--max_samples", type=int, default=None,
                        help="Limit evaluation to first N samples (optional for quick testing)")
    args = parser.parse_args()

    evaluate_test_set(args.test_data, output_dir=args.output_dir, max_samples=args.max_samples)


if __name__ == "__main__":
    main()
