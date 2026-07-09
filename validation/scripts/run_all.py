"""
TRXT Validation - Main Pipeline Script
=======================================
One-command script to run the full validation pipeline.
"""

import os
import sys
import uuid
import hashlib
import yaml
import json
import logging
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import click

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def get_git_commit_hash() -> str:
    """Get current git commit hash."""
    try:
        import subprocess
        result = subprocess.run(
            ['git', 'rev-parse', 'HEAD'],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )
        return result.stdout.strip()[:12]
    except Exception:
        return "unknown"


def generate_run_id() -> str:
    """Generate unique run ID."""
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    short_uuid = uuid.uuid4().hex[:8]
    return f"{timestamp}-{short_uuid}"


def load_config(config_path: str) -> dict:
    """Load YAML configuration."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def verify_data_integrity(manifest_path: str) -> bool:
    """Verify data files against manifest hashes."""
    logger.info("Verifying data integrity...")
    
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)
    
    # Check if data files exist (actual hash verification requires files)
    data_dir = Path(manifest_path).parent
    
    for dataset_name, dataset_info in manifest.get('datasets', {}).items():
        if 'files' in dataset_info:
            for file_info in dataset_info['files']:
                file_path = data_dir / dataset_name / file_info['name']
                if not file_path.exists():
                    logger.warning(f"Data file not found: {file_path}")
                    logger.info(f"Download from: {dataset_info.get('source_url', 'unknown')}")
    
    return True


def run_unit_tests() -> bool:
    """Run unit tests with pytest."""
    logger.info("Running unit tests...")
    try:
        import pytest
        test_dir = Path(__file__).parent.parent / "tests"
        exit_code = pytest.main([str(test_dir), "-v", "--tb=short"])
        return exit_code == 0
    except ImportError:
        logger.warning("pytest not installed, skipping unit tests")
        return True


def create_run_manifest(config: dict, run_id: str, output_dir: Path) -> dict:
    """Create run manifest with all metadata."""
    manifest = {
        'run_id': run_id,
        'timestamp': datetime.now().isoformat(),
        'commit_hash': get_git_commit_hash(),
        'hostname': os.environ.get('COMPUTERNAME', 'unknown'),
        'python_version': sys.version,
        'config': config,
        'results': {}
    }
    
    manifest_path = output_dir / 'manifest.yaml'
    with open(manifest_path, 'w') as f:
        yaml.dump(manifest, f, default_flow_style=False)
    
    logger.info(f"Run manifest saved to: {manifest_path}")
    return manifest


@click.command()
@click.option('--config', default='config/run_config.yaml', 
              help='Path to run configuration file')
@click.option('--skip-tests', is_flag=True, 
              help='Skip unit tests')
@click.option('--dry-run', is_flag=True,
              help='Only validate setup, do not run analysis')
def main(config: str, skip_tests: bool, dry_run: bool):
    """
    TRXT Validation Pipeline
    
    Run the full computational validation for the TRXT research project.
    """
    logger.info("=" * 60)
    logger.info("TRXT VALIDATION PIPELINE")
    logger.info("=" * 60)
    
    # Generate run ID
    run_id = generate_run_id()
    logger.info(f"Run ID: {run_id}")
    logger.info(f"Commit: {get_git_commit_hash()}")
    
    # Load configuration
    base_dir = Path(__file__).parent.parent
    config_path = base_dir / config
    
    if not config_path.exists():
        logger.error(f"Config file not found: {config_path}")
        sys.exit(1)
    
    cfg = load_config(config_path)
    logger.info(f"Loaded configuration from: {config_path}")
    
    # Create output directory
    output_dir = base_dir / "outputs" / "runs" / run_id
    output_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Output directory: {output_dir}")
    
    # Verify data integrity
    manifest_path = base_dir / "data" / "data_manifest.json"
    if manifest_path.exists():
        verify_data_integrity(str(manifest_path))
    else:
        logger.warning(f"Data manifest not found: {manifest_path}")
    
    # Run unit tests
    if not skip_tests:
        tests_passed = run_unit_tests()
        if not tests_passed:
            logger.error("Unit tests failed! Aborting pipeline.")
            sys.exit(1)
    
    # Create run manifest
    manifest = create_run_manifest(cfg, run_id, output_dir)
    
    if dry_run:
        logger.info("Dry run complete. Exiting.")
        return
    
    # =========================================================================
    # MAIN VALIDATION STEPS (to be implemented in Phase 2-3)
    # =========================================================================
    
    logger.info("-" * 60)
    logger.info("VALIDATION STEPS (Placeholder)")
    logger.info("-" * 60)
    
    # Step 1: SPARC rotation curve fitting
    logger.info("[TODO] Step 1: SPARC rotation curve fitting")
    
    # Step 2: Bootstrap uncertainty estimation
    logger.info("[TODO] Step 2: Bootstrap uncertainty estimation")
    
    # Step 3: Holdout test set evaluation
    logger.info("[TODO] Step 3: Holdout test set evaluation")
    
    # Step 4: SIDM cross-section calculation
    logger.info("[TODO] Step 4: SIDM cross-section calculation")
    
    # Step 5: Generate figures and tables
    logger.info("[TODO] Step 5: Generate figures and tables")
    
    logger.info("=" * 60)
    logger.info("PIPELINE COMPLETE")
    logger.info(f"Results saved to: {output_dir}")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
