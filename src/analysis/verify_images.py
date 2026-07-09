import os
from PIL import Image
from pathlib import Path

# Path to figures
figures_dir = Path(r"c:\Users\NC\Music\trxt nullivance v14\results\FINAL_ACADEMIC_REPORT_V25\figures")

print(f"Checking images in: {figures_dir}")
print("-" * 50)

if not figures_dir.exists():
    print("ERROR: Directory does not exist!")
    exit(1)

files = list(figures_dir.glob("*.png"))
if not files:
    print("WARNING: No PNG files found!")
    exit(0)

errors = 0
for img_path in files:
    try:
        # Check size
        size = img_path.stat().st_size
        if size == 0:
            print(f"[FAIL] {img_path.name}: File is empty (0 bytes)")
            errors += 1
            continue
            
        # Verify integrity with PIL
        with Image.open(img_path) as img:
            img.verify() # Verify file integrity (checksums, headers)
            
        print(f"[OK] {img_path.name:<35} | Size: {size/1024:.1f} KB")
        
    except Exception as e:
        print(f"[FAIL] {img_path.name}: Corrupted - {str(e)}")
        errors += 1

print("-" * 50)
if errors == 0:
    print(f"SUCCESS: All {len(files)} images are valid.")
else:
    print(f"FAILURE: Found {errors} corrupted or empty images.")
