
import os
import zipfile
import shutil
import subprocess
from datetime import datetime

def package_project():
    """Package the project into a zip file."""
    print("="*60)
    print("TRXT VALIDATION PROJECT PACKAGER")
    print("="*60)
    
    # Step 1: Verify Data
    print("\n[Step 1] Verifying Data Integrity...")
    try:
        subprocess.run(["python", "scripts/verify_data.py"], check=True)
    except subprocess.CalledProcessError:
        print("ERROR: Data verification failed. Aborting.")
        return

    # Step 2: Define Archive Name
    timestamp = datetime.now().strftime("%Y%m%d")
    archive_name = f"trxt_validation_v7.1_polished_{timestamp}.zip"
    
    # Step 3: Zip it
    print(f"\n[Step 2] Creating Archive: {archive_name}")
    
    base_dir = "."
    excluded_dirs = {
        '__pycache__', 
        '.pytest_cache', 
        '.git', 
        '.idea', 
        'venv', 
        'env',
        'node_modules'
    }
    
    excluded_files = {
        archive_name,
        'package_project.py' # Don't need to include self if outside? Keep it.
    }

    with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(base_dir):
            # Modify dirs in-place to skip excluded
            dirs[:] = [d for d in dirs if d not in excluded_dirs]
            
            for file in files:
                if file in excluded_files:
                    continue
                if file.endswith('.pyc') or file.endswith('.pyo'):
                    continue
                    
                file_path = os.path.join(root, file)
                # Add to zip with relative path
                arcname = os.path.relpath(file_path, base_dir)
                zipf.write(file_path, arcname)
                # print(f"  Added: {arcname}")
                
        # [NEW] Add the external Research Report
        report_path = os.path.join("..", "paper", "submission_v16", "TRXT_Research_Report_English.tex")
        if os.path.exists(report_path):
            print(f"Adding Research Report from {report_path}...")
            zipf.write(report_path, "TRXT_Research_Report_English.tex")
        else:
            print("WARNING: Research Report not found at expected path!")
    
    print(f"SUCCESS: Archive created at {os.path.abspath(archive_name)}")
    
    # Step 4: Verify Zip
    print(f"\n[Step 3] Verifying Archive...")
    try:
        with zipfile.ZipFile(archive_name, 'r') as zipf:
            ret = zipf.testzip()
            if ret is not None:
                print(f"First bad file in zip: {ret}")
            else:
                print("Archive integrity check passed.")
                print(f"Total files: {len(zipf.namelist())}")
    except Exception as e:
        print(f"Archive check failed: {e}")

if __name__ == "__main__":
    package_project()
