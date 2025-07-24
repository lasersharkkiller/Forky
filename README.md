# Forky

Original repo building from: https://github.com/PUTvision/UAVVaste/blob/main/README.md

UAVVaste dataset
The UAVVaste dataset consists to date of 772 images and 3718 annotations. The main motivation for the creation of the dataset was the lack of domain-specific data. Therefore, this image set is recommended for object detection evaluation benchmarking but also for developing solutions related to UAVs, remote sensing, or even environmental cleaning. The dataset is made publicly available and will be expanded.

Download original UAVVaste dataset available also in the Zenodo repository: https://zenodo.org/record/8214061.

---

The general concept of operations is to finetune a YOLO model on the rubbish dataset, export it as a .tflite, and use it in an ATAK plugin.

1. Download the UAVVaste dataset, which is in a strange sort of COCO format.
2. Convert the UAVVaste dataset from COCO format to YOLO format (subfolders)
3. Create a dataset.yaml file
4. Fine tune a pretrained YOLOv8 model on the converted dataset.
5. Export the finetuned model as a .tflite

To get up and running:

- `pip install ultralytics`    # for yolo cli
- `convert_coco.py` for a first pass at conversion
- `arrange_files.py` to move to subfolders based on train/val/test
- `fix_mapped_classes.py` to fix segments being mapped to a nonexistant -1 class
  - https://github.com/ultralytics/ultralytics/blob/main/ultralytics/data/converter.py has the code for convert_from_coco(), which unfortunately doesn't support custom classes outside of the COCO classes. so since our dataset defines its own new "rubbish" class which isn't a subset of the original, this will map all class labels to -1. therefore each .txt label file will start with a -1.
- create `dataset.yaml`
- `train.sh` to launch the finetune.
- `predict_and_visualize.py` to sanity check the work.
- `export_to_tflite.py` to convert to tflite.
