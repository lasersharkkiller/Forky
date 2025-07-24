#!/usr/bin/env python3
from ultralytics import YOLO

# 1. Load your fine‑tuned model
model = YOLO('runs/detect/train/weights/best.pt')

# 2. Export to float32 TFLite
model.export(format='tflite', imgsz=640)

# 3. (Optional) Export an INT8‑quantized TFLite
#model.export(format='tflite', imgsz=640, dynamic=True)

