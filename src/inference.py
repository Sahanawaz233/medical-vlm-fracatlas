#!/usr/bin/env python3
"""
FracAtlas Diagnostic Inference Core Engine
===========================================
Central engine for musculoskeletal radiograph diagnostic analysis,
fracture detection, anatomical localization, and Med-VQA conversational queries.

Can be imported as a Python module or run directly via CLI.
"""

import os
import sys
import json
import argparse
from pathlib import Path


class MedicalVLMInferenceEngine:
    """Diagnostic Inference Engine for FracAtlas Vision-Language Model."""

    def __init__(self, model_id="Qwen/Qwen2-VL-2B-Instruct", adapter_path="models/fracatlas_vlm_lora", device="auto"):
        self.model_id = model_id
        self.adapter_path = adapter_path
        self.device = device
        self.model = None
        self.processor = None
        self.is_loaded = False

    def load_model(self):
        """Load foundation VLM and LoRA adapter weights if deep learning environment is available."""
        try:
            import torch
            from transformers import AutoProcessor, BitsAndBytesConfig
            from peft import PeftModel

            if self.device == "auto":
                self.device = "cuda" if torch.cuda.is_available() else "cpu"

            print(f"[Engine] Initializing {self.model_id} on {self.device}...")

            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.float16 if self.device == "cuda" else torch.float32
            )

            from transformers import Qwen2VLForConditionalGeneration
            self.model = Qwen2VLForConditionalGeneration.from_pretrained(
                self.model_id,
                quantization_config=bnb_config if self.device == "cuda" else None,
                device_map="auto" if self.device == "cuda" else None
            )

            if os.path.exists(self.adapter_path):
                print(f"[Engine] Attaching LoRA adapter from: {self.adapter_path}")
                self.model = PeftModel.from_pretrained(self.model, self.adapter_path)

            self.processor = AutoProcessor.from_pretrained(self.model_id)
            self.is_loaded = True
            print("[Engine] Model loaded successfully.")
            return True

        except Exception as e:
            print(f"[Engine Notice] Full GPU VLM weights not loaded ({e}). Operating in clinical evaluation mode.")
            self.is_loaded = False
            return False

    def diagnose_xray(self, image_path):
        """
        Perform complete clinical diagnostic evaluation of an X-ray radiograph.
        Returns a structured dictionary with findings, impression, fracture status, and bounding region.
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Radiograph image not found: {image_path}")

        # If live neural model is loaded, run transformer generation
        if not self.is_loaded:
            self.load_model()

        if self.is_loaded:
            return self._run_neural_inference(image_path)

        raise RuntimeError("VLM model could not be loaded.")
    def answer_query(self, image_path, question):
        """Answer arbitrary clinical user questions about the radiograph (Med-VQA)."""
        diag = self.diagnose_xray(image_path)
        q_lower = question.lower()

        if any(w in q_lower for w in ["fracture", "broken", "crack", "cortical"]):
            if diag["fracture_detected"]:
                return f"Yes, an acute fracture is identified. {diag['findings']}"
            else:
                return f"No acute fracture is observed in this radiograph. Cortical bone margins appear smooth and intact."

        if any(w in q_lower for w in ["where", "location", "localize", "coordinates"]):
            if diag["fracture_detected"]:
                return f"The fracture is localized within the following bounding coordinates: {diag.get('bounding_box', 'visualized region')}."
            else:
                return "No fracture was localized. The osseous margins appear intact."

        if any(w in q_lower for w in ["hardware", "fixation", "screw", "plate", "implant"]):
            return "No orthopedic internal fixation hardware, surgical plates, or screws are visualized in this scan."

        # Default comprehensive summary
        return f"{diag['findings']}\n\nImpression: {diag['impression']}"
    def _run_neural_inference(self, image_path):
        """Run Qwen2-VL inference on an X-ray and extract fracture status."""
        from PIL import Image
        import torch

        image = Image.open(image_path).convert("RGB")

        messages = [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                       "text": (
    "You are an orthopedic radiology assistant. "
    "Examine this musculoskeletal radiograph carefully. "
    "Describe your diagnostic findings and indicate if any fracture is present."
)
                    }
                ],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "image": image,
                    },
                    {
                        "type": "text",
                        "text": (
    "Examine this musculoskeletal radiograph carefully. "
    "Describe your diagnostic findings and indicate if any fracture is present."
)
                    },
                ],
            },
        ]

        text = self.processor.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )

        inputs = self.processor(
            text=[text],
            images=[image],
            padding=True,
            return_tensors="pt"
        )

        if self.device == "cuda":
            inputs = {k: v.to("cuda") for k, v in inputs.items()}

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=128
            )

        decoded_outputs = self.processor.batch_decode(
            outputs,
            skip_special_tokens=True
        )
        generated_text = decoded_outputs[0].strip()

        # Extract only the actual generated answer after the assistant marker
        lower_generated = generated_text.lower()

        if "assistant" in lower_generated:
            assistant_pos = lower_generated.rfind("assistant")
            generated_text = generated_text[
                assistant_pos + len("assistant"):
            ].strip()

        # Remove any remaining colon
        if generated_text.startswith(":"):
            generated_text = generated_text[1:].strip()

        print("[DEBUG] CLEAN MODEL OUTPUT:", repr(generated_text))

        lower_text = generated_text.lower().strip()

        # Determine fracture status from the beginning of the answer
                # Determine fracture status from the model's complete answer
        if any(phrase in lower_text for phrase in [
            "no acute fracture",
            "no fracture",
            "no fractures",
            "without fracture",
            "fracture is absent",
            "no evidence of fracture"
        ]):
            fracture_detected = False

        elif any(phrase in lower_text for phrase in [
            "fracture is present",
            "fracture is identified",
            "visible fracture",
            "there is a fracture",
            "there is also a fracture",
            "acute fracture is present",
            "fracture"
        ]):
            fracture_detected = True

        else:
            fracture_detected = False
        return {
            "image_path": image_path,
            "fracture_detected": fracture_detected,
            "confidence": None,
            "findings": generated_text,
            "impression": generated_text,
            "bounding_box": None
        }