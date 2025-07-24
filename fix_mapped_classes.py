#!/usr/bin/env python3
"""
Recursively traverse a directory for all .txt files and remap any class label of -1 to 1.
Usage:
    python3 remap_labels.py [root_directory]
If no directory is provided, uses the current working directory.
"""
import os
import sys

def remap_file(path):
    """Read a label file, replace leading '-1' class IDs with '1', and overwrite."""
    updated = []
    changed = False
    with open(path, 'r') as f:
        for line in f:
            stripped = line.strip()
            if not stripped:
                # preserve blank lines (or skip, as desired)
                continue
            parts = stripped.split(maxsplit=1)
            cid = parts[0]
            rest = parts[1] if len(parts) > 1 else ''
            if cid == '-1':
                cid = '0'
                changed = True
            # Reconstruct line
            updated.append(cid + (" " + rest if rest else '') + '\n')
    if changed:
        with open(path, 'w') as f:
            f.writelines(updated)
    return changed

def main():
    # Determine root directory
    root = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    print(f"Scanning for .txt files under '{root}'...")
    count = 0
    for dirpath, _, filenames in os.walk(root):
        for fname in filenames:
            if not fname.lower().endswith('.txt'):
                continue
            file_path = os.path.join(dirpath, fname)
            if remap_file(file_path):
                print(f"Remapped labels in: {file_path}")
                count += 1
    print(f"Done. Updated {count} file(s).")

if __name__ == '__main__':
    main()

