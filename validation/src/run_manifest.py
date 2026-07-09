"""
TRXT Validation - Run Manifest Generator
=========================================
Generates and manages run manifests for reproducibility.
"""

import os
import sys
import uuid
import yaml
import json
import hashlib
import platform
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import subprocess


def get_git_info() -> Dict[str, str]:
    """Get git repository information."""
    try:
        # Get commit hash
        result = subprocess.run(
            ['git', 'rev-parse', 'HEAD'],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )
        commit_hash = result.stdout.strip()[:12] if result.returncode == 0 else "unknown"
        
        # Check for uncommitted changes
        result = subprocess.run(
            ['git', 'status', '--porcelain'],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )
        dirty = bool(result.stdout.strip()) if result.returncode == 0 else True
        
        return {
            'commit_hash': commit_hash,
            'dirty': dirty,
            'status': 'clean' if not dirty else 'modified'
        }
    except Exception as e:
        return {
            'commit_hash': 'unknown',
            'dirty': True,
            'status': f'error: {str(e)}'
        }


def get_environment_info() -> Dict[str, str]:
    """Get Python environment information."""
    import numpy as np
    import scipy
    
    return {
        'python_version': sys.version.split()[0],
        'python_path': sys.executable,
        'platform': platform.platform(),
        'hostname': platform.node(),
        'numpy_version': np.__version__,
        'scipy_version': scipy.__version__
    }


def generate_run_id() -> str:
    """Generate unique run ID."""
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    short_uuid = uuid.uuid4().hex[:8]
    return f"{timestamp}-{short_uuid}"


def compute_config_hash(config: Dict) -> str:
    """Compute hash of configuration for reproducibility check."""
    config_str = json.dumps(config, sort_keys=True)
    return hashlib.sha256(config_str.encode()).hexdigest()[:16]


class RunManifest:
    """
    Manages run manifests for reproducibility.
    
    A manifest captures all information needed to reproduce a run:
    - Configuration
    - Environment
    - Git state
    - Random seeds
    - Results
    """
    
    def __init__(self, config_path: str):
        """
        Initialize manifest from configuration.
        
        Parameters
        ----------
        config_path : str
            Path to run_config.yaml
        """
        self.run_id = generate_run_id()
        self.config_path = config_path
        self.start_time = datetime.now()
        self.end_time: Optional[datetime] = None
        
        # Load configuration
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        # Initialize manifest structure
        self.manifest = {
            'run_id': self.run_id,
            'timestamp': self.start_time.isoformat(),
            'config_path': str(config_path),
            'config_hash': compute_config_hash(self.config),
            'git': get_git_info(),
            'environment': get_environment_info(),
            'parameters': {
                'random_seed': self.config.get('reproducibility', {}).get('random_seed', 42),
                'physics': self.config.get('physics', {}),
                'sparc': self.config.get('sparc', {})
            },
            'results': {},
            'status': 'running'
        }
    
    def add_result(self, key: str, value: Any):
        """Add a result to the manifest."""
        self.manifest['results'][key] = value
    
    def add_metadata(self, key: str, value: Any):
        """Add metadata to the manifest."""
        self.manifest[key] = value
    
    def finalize(self, success: bool = True):
        """Finalize the manifest."""
        self.end_time = datetime.now()
        self.manifest['end_timestamp'] = self.end_time.isoformat()
        self.manifest['duration_seconds'] = (self.end_time - self.start_time).total_seconds()
        self.manifest['status'] = 'success' if success else 'failed'
    
    def save(self, output_dir: str) -> str:
        """
        Save manifest to file.
        
        Parameters
        ----------
        output_dir : str
            Directory to save manifest
            
        Returns
        -------
        manifest_path : str
            Path to saved manifest
        """
        run_dir = Path(output_dir) / self.run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        
        manifest_path = run_dir / 'manifest.yaml'
        with open(manifest_path, 'w') as f:
            yaml.dump(self.manifest, f, default_flow_style=False, sort_keys=False)
        
        # Also save as JSON for programmatic access
        json_path = run_dir / 'manifest.json'
        with open(json_path, 'w') as f:
            json.dump(self.manifest, f, indent=2)
        
        return str(manifest_path)
    
    def to_dict(self) -> Dict:
        """Return manifest as dictionary."""
        return self.manifest.copy()


def verify_manifest(manifest_path: str) -> Dict[str, bool]:
    """
    Verify a run can be reproduced from manifest.
    
    Parameters
    ----------
    manifest_path : str
        Path to manifest file
        
    Returns
    -------
    verification : dict
        Verification results
    """
    with open(manifest_path, 'r') as f:
        manifest = yaml.safe_load(f)
    
    current_git = get_git_info()
    current_env = get_environment_info()
    
    return {
        'git_match': current_git['commit_hash'] == manifest['git']['commit_hash'],
        'git_clean': not current_git['dirty'],
        'python_match': current_env['python_version'] == manifest['environment']['python_version'],
        'numpy_match': current_env['numpy_version'] == manifest['environment']['numpy_version'],
        'scipy_match': current_env['scipy_version'] == manifest['environment']['scipy_version'],
        'config_found': Path(manifest['config_path']).exists()
    }


if __name__ == "__main__":
    # Quick test
    config_path = Path(__file__).parent.parent / "config" / "run_config.yaml"
    
    if config_path.exists():
        manifest = RunManifest(str(config_path))
        
        # Add some test results
        manifest.add_result('test_chi2', 1.23)
        manifest.add_result('test_galaxies', 35)
        
        manifest.finalize(success=True)
        
        output_dir = Path(__file__).parent.parent / "outputs" / "runs"
        path = manifest.save(str(output_dir))
        
        print(f"Manifest saved to: {path}")
        print(f"Run ID: {manifest.run_id}")
    else:
        print(f"Config not found: {config_path}")
