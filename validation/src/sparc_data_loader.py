"""
TRXT Validation - SPARC Data Loader
====================================
Loads actual SPARC rotation curve data from .mrt files.
Downloads data if not present.
"""

import numpy as np
import os
import urllib.request
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import logging
import json

logger = logging.getLogger(__name__)


SPARC_URL = "http://astroweb.cwru.edu/SPARC/"
SPARC_FILES = {
    "rotmod": "Rotmod_LTG.zip",
    "properties": "SPARC_Lelli2016c.mrt"
}


def read_file_safe(filepath: str) -> List[str]:
    """Read file trying multiple encodings."""
    encodings = ['utf-8', 'utf-16', 'latin-1', 'cp1252']
    for enc in encodings:
        try:
            with open(filepath, 'r', encoding=enc) as f:
                return f.readlines()
        except UnicodeError:
            continue
    raise ValueError(f"Could not read {filepath} with supported encodings")


@dataclass
class SPARCGalaxy:
    """Container for SPARC galaxy data."""
    name: str
    r_kpc: np.ndarray      # Radius in kpc
    v_obs: np.ndarray      # Observed rotation velocity (km/s)
    v_err: np.ndarray      # Velocity error (km/s)
    v_gas: np.ndarray      # Gas contribution (km/s)
    v_disk: np.ndarray     # Disk contribution (km/s)
    v_bul: np.ndarray      # Bulge contribution (km/s)
    distance_mpc: float    # Distance in Mpc
    inclination: float     # Inclination in degrees
    luminosity: float      # Luminosity in L_sun
    morphology: str        # Morphological type


def download_sparc_data(data_dir: str, force: bool = False) -> bool:
    """
    Download SPARC data files if not present.
    
    Parameters
    ----------
    data_dir : str
        Directory to store data
    force : bool
        Force re-download even if files exist
        
    Returns
    -------
    success : bool
        True if data is available
    """
    data_path = Path(data_dir) / "sparc"
    data_path.mkdir(parents=True, exist_ok=True)
    
    logger.info("Checking SPARC data files...")
    
    # Check if main data file exists
    rotmod_file = data_path / "Rotmod_LTG.mrt"
    
    if rotmod_file.exists() and not force:
        logger.info(f"SPARC data already exists: {rotmod_file}")
        return True
    
    # Download note: SPARC data requires manual download due to website structure
    logger.warning("=" * 60)
    logger.warning("SPARC DATA NOT FOUND - MANUAL DOWNLOAD REQUIRED")
    logger.warning("=" * 60)
    logger.warning(f"Please download SPARC data from: {SPARC_URL}")
    logger.warning(f"Place files in: {data_path}")
    logger.warning("Required files:")
    logger.warning("  1. Rotmod_LTG.mrt (rotation curves)")
    logger.warning("  2. SPARC_Lelli2016c.mrt (galaxy properties)")
    logger.warning("=" * 60)
    
    # Create placeholder instruction file
    readme_path = data_path / "DOWNLOAD_INSTRUCTIONS.txt"
    with open(readme_path, 'w') as f:
        f.write("SPARC Data Download Instructions\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"1. Go to: {SPARC_URL}\n")
        f.write("2. Download 'Rotmod_LTG.zip'\n")
        f.write("3. Extract to this directory\n")
        f.write("4. Also download 'SPARC_Lelli2016c.mrt'\n\n")
        f.write("Citation:\n")
        f.write("Lelli, McGaugh, & Schombert (2016), AJ, 152, 157\n")
        f.write("DOI: 10.3847/0004-6256/152/6/157\n")
    
    return False


def parse_rotmod_mrt(filepath: str) -> Dict[str, SPARCGalaxy]:
    """
    Parse SPARC Rotmod_LTG.mrt file.
    
    MRT (Machine-Readable Table) format from CDS.
    
    Parameters
    ----------
    filepath : str
        Path to .mrt file
        
    Returns
    -------
    galaxies : dict
        Dictionary of galaxy name -> SPARCGalaxy
    """
    galaxies = {}
    current_galaxy = None
    current_data = []
    
    try:
        lines = read_file_safe(filepath)
    except Exception as e:
        logger.error(f"Failed to read {filepath}: {e}")
        return {}
    
    # Find data section (after header)
    in_data = False
    
    for line in lines:
        line = line.strip()
        
        # Skip empty lines and comments
        if not line or line.startswith('#'):
            continue
        
        # Parse data lines
        # Format: Galaxy Rad Vobs errV Vgas Vdisk Vbul
        parts = line.split()
        
        if len(parts) >= 7:
            try:
                name = parts[0]
                r = float(parts[1])
                vobs = float(parts[2])
                verr = float(parts[3])
                vgas = float(parts[4])
                vdisk = float(parts[5])
                vbul = float(parts[6])
                
                if name not in galaxies:
                    galaxies[name] = {
                        'r': [], 'vobs': [], 'verr': [],
                        'vgas': [], 'vdisk': [], 'vbul': []
                    }
                
                galaxies[name]['r'].append(r)
                galaxies[name]['vobs'].append(vobs)
                galaxies[name]['verr'].append(verr)
                galaxies[name]['vgas'].append(vgas)
                galaxies[name]['vdisk'].append(vdisk)
                galaxies[name]['vbul'].append(vbul)
                
            except (ValueError, IndexError):
                continue
    
    # Convert to SPARCGalaxy objects
    result = {}
    for name, data in galaxies.items():
        if len(data['r']) < 5:  # Skip galaxies with too few points
            continue
            
        result[name] = SPARCGalaxy(
            name=name,
            r_kpc=np.array(data['r']),
            v_obs=np.array(data['vobs']),
            v_err=np.array(data['verr']),
            v_gas=np.array(data['vgas']),
            v_disk=np.array(data['vdisk']),
            v_bul=np.array(data['vbul']),
            distance_mpc=0.0,  # From properties file
            inclination=0.0,
            luminosity=0.0,
            morphology="Spiral"
        )
    
    return result


def parse_massmodels_mrt(filepath: str) -> Dict[str, SPARCGalaxy]:
    """
    Parse SPARC MassModels_Lelli2016c.mrt file.
    Columns: ID, D, R, Vobs, err, Vgas, Vdisk, Vbul
    """
    galaxies = {}
    
    try:
        lines = read_file_safe(filepath)
    except Exception as e:
        logger.error(f"Failed to read {filepath}: {e}")
        return {}
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#') or line.startswith('byte') or line.startswith('Byte') or line.startswith('='):
            continue
            
        parts = line.split()
        # MassModels has D at index 1, R at index 2
        # Check if line looks like data (starts with string, then numbers)
        if len(parts) >= 8:
            try:
                # Try to parse distance to check if it's a data line
                float(parts[1])
            except ValueError:
                continue
                
            try:
                name = parts[0]
                d_mpc = float(parts[1])
                r = float(parts[2])
                vobs = float(parts[3])
                verr = float(parts[4])
                vgas = float(parts[5])
                vdisk = float(parts[6])
                vbul = float(parts[7])
                
                if name not in galaxies:
                    galaxies[name] = {
                        'r': [], 'vobs': [], 'verr': [],
                        'vgas': [], 'vdisk': [], 'vbul': [], 'd': d_mpc
                    }
                
                galaxies[name]['r'].append(r)
                galaxies[name]['vobs'].append(vobs)
                galaxies[name]['verr'].append(verr)
                galaxies[name]['vgas'].append(vgas)
                galaxies[name]['vdisk'].append(vdisk)
                galaxies[name]['vbul'].append(vbul)
                
            except (ValueError, IndexError):
                continue

    # Convert to SPARCGalaxy objects
    result = {}
    for name, data in galaxies.items():
        if len(data['r']) < 3: 
            continue
            
        result[name] = SPARCGalaxy(
            name=name,
            r_kpc=np.array(data['r']),
            v_obs=np.array(data['vobs']),
            v_err=np.array(data['verr']),
            v_gas=np.array(data['vgas']),
            v_disk=np.array(data['vdisk']),
            v_bul=np.array(data['vbul']),
            distance_mpc=data['d'],
            inclination=0.0,
            luminosity=0.0,
            morphology="Spiral"
        )
    return result

def load_sparc_data(data_dir: str) -> Dict[str, SPARCGalaxy]:
    """
    Load SPARC data from directory.
    Checks for MassModels_Lelli2016c.mrt first, then Rotmod_LTG.mrt.
    """
    data_path = Path(data_dir) / "sparc"
    
    # Priority 1: MassModels file (manual download)
    massmodels_file = data_path / "MassModels_Lelli2016c.mrt"
    if massmodels_file.exists():
        logger.info(f"Loading SPARC data from MassModels: {massmodels_file}")
        return parse_massmodels_mrt(str(massmodels_file))
        
    # Priority 2: Rotmod file
    rotmod_file = data_path / "Rotmod_LTG.mrt"
    if rotmod_file.exists():
        logger.info(f"Loading SPARC data from Rotmod: {rotmod_file}")
        return parse_rotmod_mrt(str(rotmod_file))
        
    # Priority 3: Sample file
    sample_file = data_path / "sample_rotmod.mrt"
    if sample_file.exists():
        logger.warning(f"Using SAMPLE data: {sample_file}")
        return parse_rotmod_mrt(str(sample_file))

    logger.warning(f"SPARC data not found in {data_path}")
    download_sparc_data(data_dir)
    return {}


def compute_file_hash(filepath: str) -> str:
    """Compute SHA256 hash of file."""
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            sha256.update(chunk)
    return sha256.hexdigest()


def verify_data_integrity(data_dir: str, manifest_path: str) -> Dict[str, bool]:
    """
    Verify data files against manifest.
    
    Parameters
    ----------
    data_dir : str
        Path to data directory
    manifest_path : str
        Path to data_manifest.json
        
    Returns
    -------
    verification : dict
        Verification results per file
    """
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)
    
    results = {}
    
    for dataset_name, dataset_info in manifest.get('datasets', {}).items():
        if 'files' in dataset_info:
            for file_info in dataset_info['files']:
                file_path = Path(data_dir) / dataset_name / file_info['name']
                
                if not file_path.exists():
                    results[file_info['name']] = False
                    logger.warning(f"Missing: {file_path}")
                else:
                    # Check hash if provided
                    expected_hash = file_info.get('sha256', '')
                    if expected_hash and not expected_hash.startswith('<'):
                        actual_hash = compute_file_hash(str(file_path))
                        results[file_info['name']] = (actual_hash == expected_hash)
                    else:
                        results[file_info['name']] = True  # File exists, no hash to check
    
    return results


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    data_dir = Path(__file__).parent.parent / "data"
    
    print("=" * 60)
    print("SPARC DATA LOADER")
    print("=" * 60)
    
    # Try to load data
    galaxies = load_sparc_data(str(data_dir))
    
    if galaxies:
        print(f"\nLoaded {len(galaxies)} galaxies")
        print("\nSample galaxies:")
        for name in list(galaxies.keys())[:5]:
            g = galaxies[name]
            print(f"  {name}: {len(g.r_kpc)} points, r_max={g.r_kpc[-1]:.1f} kpc")
    else:
        print("\nNo data loaded. Please download SPARC data manually.")
        print(f"See: {data_dir / 'sparc' / 'DOWNLOAD_INSTRUCTIONS.txt'}")
