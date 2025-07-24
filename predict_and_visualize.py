#!/usr/bin/env python3
import os
import glob
import argparse
from ultralytics import YOLO
from PIL import Image

def process_images(model_path, test_dir, output_dir):
    # Load the fine‑tuned model
    model = YOLO(model_path)

    # Prepare output folders
    overlay_dir = os.path.join(output_dir, 'overlays')
    comparison_dir = os.path.join(output_dir, 'comparisons')
    os.makedirs(overlay_dir, exist_ok=True)
    os.makedirs(comparison_dir, exist_ok=True)

    # Iterate over all image files in test directory
    for img_path in glob.glob(os.path.join(test_dir, '*.*')):
        ext = os.path.splitext(img_path)[1].lower()
        if ext not in ('.jpg', '.jpeg', '.png', '.bmp'):
            continue
        stem = os.path.splitext(os.path.basename(img_path))[0]
        print(f"Processing: {img_path}")

        # Run prediction, saving annotated image to overlay_dir via project/name
        results = model.predict(
            source=img_path,
            save=True,
            project=output_dir,
            name='overlays',
            save_txt=False,
            exist_ok=True
        )

        # Determine overlay file path
        overlay_path = os.path.join(overlay_dir, stem + ext)
        if not os.path.exists(overlay_path):
            # If extension changed (e.g. saved as .jpg), try .jpg
            overlay_jpg = os.path.join(overlay_dir, stem + '.jpg')
            overlay_path = overlay_jpg if os.path.exists(overlay_jpg) else None

        if not overlay_path:
            print(f"Warning: No overlay found for {img_path}")
            continue

        # Load original and overlay images
        orig_img = Image.open(img_path).convert('RGB')
        pred_img = Image.open(overlay_path).convert('RGB')

        # Create side-by-side comparison
        total_width = orig_img.width + pred_img.width
        max_height = max(orig_img.height, pred_img.height)
        composite = Image.new('RGB', (total_width, max_height))
        composite.paste(orig_img, (0, 0))
        composite.paste(pred_img, (orig_img.width, 0))

        # Save comparison
        comp_path = os.path.join(comparison_dir, stem + '_comparison' + ext)
        composite.save(comp_path)
        print(f"Saved comparison to: {comp_path}")

    print("Done processing all test images.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Run YOLO predictions on test images and generate side-by-side comparisons'
    )
    parser.add_argument(
        '--model', type=str,
        default=os.path.join('runs', 'detect', 'train', 'weights', 'best.pt'),
        help='Path to the trained YOLO .pt model'
    )
    parser.add_argument(
        '--test-dir', type=str,
        default=os.path.join('test', 'images'),
        help='Directory containing test images'
    )
    parser.add_argument(
        '--output-dir', type=str,
        default=os.path.join('test', 'predictions'),
        help='Directory to save overlays and comparisons'
    )
    args = parser.parse_args()

    process_images(args.model, args.test_dir, args.output_dir)

