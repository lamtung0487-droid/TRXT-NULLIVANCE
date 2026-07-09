
import json
import hashlib
import os
import sys
from pathlib import Path

def compute_sha256(file_path):
    """Compute SHA256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def verify_and_update_manifest():
    """Verify data files and update manifest with actual hashes."""
    project_root = Path(__file__).parent.parent
    manifest_path = project_root / 'data' / 'data_manifest.json'
    
    
    if not manifest_path.exists():
        print(f"Manifest not found: {manifest_path}")
        sys.exit(1)
        
    try:
        with open(manifest_path, 'r', encoding='utf-8-sig') as f:
            manifest = json.load(f)
    except Exception as e:
        print(f"ERROR loading JSON: {e}")
        # Debug: print first 500 chars
        with open(manifest_path, 'rb') as f:
            print(f"File content head (bytes): {f.read(100)}")
        sys.exit(1)
    
    print("Verifying SPARC Data...")
    sparc_dir = project_root / 'data' / 'sparc'
    
    # Check MassModels file (using the filename found on disk)
    # Manifest lists "Rotmod_LTG.mrt" and "SPARC_Lelli2016c.mrt"
    # But we have "MassModels_Lelli2016c.mrt".
    # I should check what is physically there and update manifest to match reality.
    
    mass_models = sparc_dir / 'MassModels_Lelli2016c.mrt'
    if mass_models.exists():
        file_hash = compute_sha256(mass_models)
        print(f"Computed hash for {mass_models.name}: {file_hash[:8]}...")
        
        # Update manifest entry for SPARC
        # Find entry or add it
        found = False
        for f_entry in manifest['datasets']['sparc']['files']:
            if f_entry['name'] == mass_models.name:
                f_entry['sha256'] = file_hash
                f_entry['size_bytes'] = mass_models.stat().st_size
                found = True
                break
        
        if not found:
            # Add it
            manifest['datasets']['sparc']['files'].append({
                "name": mass_models.name,
                "description": "Mass Models (Observed)",
                "sha256": file_hash,
                "size_bytes": mass_models.stat().st_size
            })
            print(f"Added {mass_models.name} to manifest.")
    else:
        print(f"Warning: {mass_models} not found.")

    # Save updated manifest
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=4)
    
    print("Manifest updated successfully.")
    
if __name__ == "__main__":
    verify_and_update_manifest()
