#!/usr/bin/env python3
import os
import json
import shutil

def main():
    # Base directory (assumes script is in yolo/ alongside images/, labels/, and the distribution JSON)
    base_dir = os.path.abspath(os.path.dirname(__file__))
    dist_file = os.path.join(base_dir, 'annotations/train_val_test_distribution_file.json')
    images_dir = os.path.join(base_dir, 'images')
    labels_dir = os.path.join(base_dir, 'labels/annotations')

    # Load the distribution mapping
    with open(dist_file, 'r') as f:
        dist = json.load(f)

    # For each split, create split/images and split/labels, then move files
    for split in ('train', 'val', 'test'):
        split_dir = os.path.join(base_dir, split)
        split_images_out = os.path.join(split_dir, 'images')
        split_labels_out = os.path.join(split_dir, 'labels')
        os.makedirs(split_images_out, exist_ok=True)
        os.makedirs(split_labels_out, exist_ok=True)

        file_list = dist.get(split, [])
        for img_name in file_list:
            # Move image
            src_img = os.path.join(images_dir, img_name)
            if os.path.exists(src_img):
                shutil.move(src_img, os.path.join(split_images_out, img_name))
            else:
                print(f"Warning: Image not found: {src_img}")

            # Move corresponding label
            base_name, _ = os.path.splitext(img_name)
            lbl_name = base_name + '.txt'
            src_lbl = os.path.join(labels_dir, lbl_name)
            if os.path.exists(src_lbl):
                shutil.move(src_lbl, os.path.join(split_labels_out, lbl_name))
            else:
                print(f"Warning: Label not found: {src_lbl}")

if __name__ == '__main__':
    main()

