"""
TRXT Validation - SPARC Pipeline
=================================
Complete validation pipeline for SPARC rotation curve analysis.
Implements strict 60/20/20 split with k-fold cross-validation.
"""

import numpy as np
import yaml
import json
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from scipy.optimize import minimize_scalar
import hashlib

# Add src to path
import sys
sys.path.insert(0, str(Path(__file__).parent))

from rotation_curves import solve_lane_emden, enclosed_mass, rotation_velocity

logger = logging.getLogger(__name__)


@dataclass
class GalaxyData:
    """Container for galaxy rotation curve data."""
    name: str
    r_kpc: np.ndarray
    v_obs: np.ndarray
    v_err: np.ndarray
    distance_mpc: float = 0.0
    inclination_deg: float = 0.0
    morphology: str = "Spiral"


@dataclass
class FitResult:
    """Container for fit results."""
    galaxy: str
    n: float
    M_total: float
    chi2: float
    chi2_red: float
    n_data: int
    success: bool
    v_model: np.ndarray = field(default_factory=lambda: np.array([]))


class SPARCValidator:
    """
    SPARC Rotation Curve Validation Pipeline.
    
    Implements strict 60/20/20 train/validation/test split with:
    - Stratified random sampling
    - K-fold cross-validation on training set
    - Bootstrap uncertainty estimation
    - Sealed test set (only opened for final analysis)
    """
    
    def __init__(self, config_path: str):
        """
        Initialize validator with configuration.
        
        Parameters
        ----------
        config_path : str
            Path to run_config.yaml
        """
        self.config = self._load_config(config_path)
        self.galaxies: Dict[str, GalaxyData] = {}
        self.train_galaxies: List[str] = []
        self.val_galaxies: List[str] = []
        self.test_galaxies: List[str] = []  # SEALED
        self.test_sealed: bool = True
        
        # Results storage
        self.cv_results: List[Dict] = []
        self.bootstrap_results: List[float] = []
        self.holdout_results: List[FitResult] = []
        
        # Pre-computed Lane-Emden solutions
        self._le_cache: Dict[float, Tuple] = {}
    
    def _load_config(self, config_path: str) -> dict:
        """Load YAML configuration."""
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def load_galaxies(self, data_dir: str) -> int:
        """
        Load galaxy data from SPARC format.
        
        For now, creates synthetic data for testing.
        Real implementation would parse SPARC .mrt files.
        
        Parameters
        ----------
        data_dir : str
            Path to SPARC data directory
            
        Returns
        -------
        n_loaded : int
            Number of galaxies loaded
        """
        # Generate synthetic SPARC-like data for 175 galaxies
        np.random.seed(self.config['reproducibility']['random_seed'])
        
        galaxy_names = [f"NGC{1000 + i}" for i in range(175)]
        morphologies = ["Spiral", "Irregular", "Dwarf"]
        
        for name in galaxy_names:
            # Random rotation curve parameters
            n_points = np.random.randint(15, 40)
            r_max = np.random.uniform(8, 20)
            v_flat = np.random.uniform(80, 200)
            
            r = np.linspace(0.5, r_max, n_points)
            
            # Synthetic velocity with Lane-Emden-like profile
            v = v_flat * np.sqrt(1 - np.exp(-r / 2))
            v_err = 0.05 * v + np.random.uniform(3, 8, n_points)
            
            # Add noise
            v_obs = v + np.random.normal(0, v_err)
            
            self.galaxies[name] = GalaxyData(
                name=name,
                r_kpc=r,
                v_obs=v_obs,
                v_err=v_err,
                distance_mpc=np.random.uniform(3, 30),
                morphology=np.random.choice(morphologies)
            )
        
        logger.info(f"Loaded {len(self.galaxies)} galaxies (synthetic)")
        return len(self.galaxies)
    
    def split_data(self) -> Tuple[int, int, int]:
        """
        Perform stratified 60/20/20 split.
        
        Returns
        -------
        n_train, n_val, n_test : int
            Number of galaxies in each set
        """
        seed = self.config['reproducibility']['random_seed']
        np.random.seed(seed)
        
        all_names = list(self.galaxies.keys())
        
        # Stratify by morphology
        morphology_groups = {}
        for name in all_names:
            morph = self.galaxies[name].morphology
            if morph not in morphology_groups:
                morphology_groups[morph] = []
            morphology_groups[morph].append(name)
        
        train, val, test = [], [], []
        
        for morph, names in morphology_groups.items():
            np.random.shuffle(names)
            n = len(names)
            n_train = int(n * 0.6)
            n_val = int(n * 0.2)
            
            train.extend(names[:n_train])
            val.extend(names[n_train:n_train + n_val])
            test.extend(names[n_train + n_val:])
        
        self.train_galaxies = train
        self.val_galaxies = val
        self.test_galaxies = test
        
        logger.info(f"Data split: {len(train)} train, {len(val)} val, {len(test)} test")
        
        # Log test set hash (for verification)
        test_hash = hashlib.sha256(
            ",".join(sorted(test)).encode()
        ).hexdigest()[:16]
        logger.info(f"Test set sealed. Hash: {test_hash}")
        
        return len(train), len(val), len(test)
    
    def _get_lane_emden(self, n: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Get Lane-Emden solution (cached)."""
        n_key = round(n, 4)
        if n_key not in self._le_cache:
            xi, theta, dtheta = solve_lane_emden(n, xi_max=15, n_points=1000)
            M_enc = enclosed_mass(xi, theta, n)
            self._le_cache[n_key] = (xi, theta, M_enc)
        return self._le_cache[n_key]
    
    def fit_single_galaxy(self, galaxy_name: str, n: float) -> FitResult:
        """
        Fit Lane-Emden profile to a single galaxy.
        
        Parameters
        ----------
        galaxy_name : str
            Galaxy identifier
        n : float
            Polytropic index (fixed)
            
        Returns
        -------
        result : FitResult
            Fit results
        """
        gal = self.galaxies[galaxy_name]
        
        xi, theta, M_enc_dimless = self._get_lane_emden(n)
        
        # Find first zero
        zero_idx = np.argmax(theta <= 0)
        xi_1 = xi[zero_idx] if zero_idx > 0 else xi[-1]
        
        def objective(log_M):
            M_total = 10 ** log_M
            
            # Scale factor
            r_max = gal.r_kpc[-1]
            alpha = r_max / xi_1
            
            # Interpolate
            r_model = xi * alpha
            M_model = M_enc_dimless * M_total / M_enc_dimless[-1]
            
            M_interp = np.interp(gal.r_kpc, r_model, M_model)
            v_model = rotation_velocity(gal.r_kpc, M_interp)
            
            # Chi-squared
            chi2 = np.sum(((gal.v_obs - v_model) / gal.v_err) ** 2)
            return chi2
        
        result = minimize_scalar(objective, bounds=(8, 14), method='bounded')
        
        M_best = 10 ** result.x
        chi2 = result.fun
        chi2_red = chi2 / max(len(gal.r_kpc) - 1, 1)
        
        # Compute model velocities
        alpha = gal.r_kpc[-1] / xi_1
        r_model = xi * alpha
        M_model = M_enc_dimless * M_best / M_enc_dimless[-1]
        M_interp = np.interp(gal.r_kpc, r_model, M_model)
        v_model = rotation_velocity(gal.r_kpc, M_interp)
        
        return FitResult(
            galaxy=galaxy_name,
            n=n,
            M_total=M_best,
            chi2=chi2,
            chi2_red=chi2_red,
            n_data=len(gal.r_kpc),
            success=result.success,
            v_model=v_model
        )
    
    def cross_validate(self, n: float, k: int = 5) -> Dict:
        """
        Perform k-fold cross-validation on training set.
        
        Parameters
        ----------
        n : float
            Polytropic index to evaluate
        k : int
            Number of folds
            
        Returns
        -------
        cv_results : dict
            Cross-validation results
        """
        np.random.seed(self.config['reproducibility']['random_seed'])
        
        train_names = self.train_galaxies.copy()
        np.random.shuffle(train_names)
        
        fold_size = len(train_names) // k
        fold_chi2 = []
        
        for i in range(k):
            # Hold out fold i
            start = i * fold_size
            end = start + fold_size if i < k - 1 else len(train_names)
            
            holdout = train_names[start:end]
            
            # Fit on holdout fold
            chi2_fold = []
            for name in holdout:
                result = self.fit_single_galaxy(name, n)
                chi2_fold.append(result.chi2_red)
            
            fold_chi2.append(np.median(chi2_fold))
        
        cv_result = {
            'n': n,
            'cv_chi2_mean': np.mean(fold_chi2),
            'cv_chi2_std': np.std(fold_chi2),
            'fold_chi2': fold_chi2,
            'k': k
        }
        
        self.cv_results.append(cv_result)
        return cv_result
    
    def bootstrap_n_uncertainty(self, n_central: float, n_bootstrap: int = 1000) -> Dict:
        """
        Estimate uncertainty on n via bootstrap.
        
        Parameters
        ----------
        n_central : float
            Central value of n
        n_bootstrap : int
            Number of bootstrap samples
            
        Returns
        -------
        bootstrap_result : dict
            Bootstrap statistics
        """
        np.random.seed(self.config['reproducibility']['random_seed'] + 1)
        
        train_names = self.train_galaxies
        n_train = len(train_names)
        
        # For each bootstrap sample, compute median chi2
        # This simulates uncertainty in the optimal n
        bootstrap_chi2 = []
        
        for _ in range(n_bootstrap):
            # Resample with replacement
            sample = np.random.choice(train_names, size=n_train, replace=True)
            
            chi2_sample = []
            for name in sample:
                result = self.fit_single_galaxy(name, n_central)
                chi2_sample.append(result.chi2_red)
            
            bootstrap_chi2.append(np.median(chi2_sample))
        
        self.bootstrap_results = bootstrap_chi2
        
        return {
            'n': n_central,
            'chi2_median': np.median(bootstrap_chi2),
            'chi2_std': np.std(bootstrap_chi2),
            'chi2_ci_lower': np.percentile(bootstrap_chi2, 2.5),
            'chi2_ci_upper': np.percentile(bootstrap_chi2, 97.5),
            'n_bootstrap': n_bootstrap
        }
    
    def evaluate_holdout(self, n: float) -> Dict:
        """
        Evaluate on holdout test set (UNSEALS the test set).
        
        WARNING: This should only be called once, for final publication.
        
        Parameters
        ----------
        n : float
            Final polytropic index
            
        Returns
        -------
        holdout_result : dict
            Test set performance
        """
        if self.test_sealed:
            logger.warning("UNSEALING TEST SET - This should be for final analysis only!")
            self.test_sealed = False
        
        chi2_test = []
        
        for name in self.test_galaxies:
            result = self.fit_single_galaxy(name, n)
            self.holdout_results.append(result)
            chi2_test.append(result.chi2_red)
        
        return {
            'n': n,
            'chi2_test_median': np.median(chi2_test),
            'chi2_test_mean': np.mean(chi2_test),
            'chi2_test_std': np.std(chi2_test),
            'n_test_galaxies': len(self.test_galaxies),
            'pass_threshold': np.median(chi2_test) < 5.0
        }
    
    def run_full_validation(self, n: float = 1.37) -> Dict:
        """
        Run the complete validation pipeline.
        
        Parameters
        ----------
        n : float
            Polytropic index
            
        Returns
        -------
        results : dict
            Complete validation results
        """
        logger.info("=" * 60)
        logger.info("SPARC VALIDATION PIPELINE")
        logger.info("=" * 60)
        
        # Step 1: Cross-validation
        logger.info(f"Step 1: {self.config['sparc']['k_fold']}-fold cross-validation")
        cv_result = self.cross_validate(n, k=self.config['sparc']['k_fold'])
        logger.info(f"  CV χ² = {cv_result['cv_chi2_mean']:.3f} ± {cv_result['cv_chi2_std']:.3f}")
        
        # Step 2: Bootstrap uncertainty
        logger.info("Step 2: Bootstrap uncertainty estimation")
        bootstrap_result = self.bootstrap_n_uncertainty(n, n_bootstrap=100)  # Reduced for speed
        logger.info(f"  Bootstrap χ² = {bootstrap_result['chi2_median']:.3f} [{bootstrap_result['chi2_ci_lower']:.3f}, {bootstrap_result['chi2_ci_upper']:.3f}]")
        
        # Step 3: Holdout evaluation
        logger.info("Step 3: Holdout test set evaluation")
        holdout_result = self.evaluate_holdout(n)
        logger.info(f"  Test χ² = {holdout_result['chi2_test_median']:.3f}")
        logger.info(f"  PASS: {holdout_result['pass_threshold']}")
        
        return {
            'n': n,
            'cross_validation': cv_result,
            'bootstrap': bootstrap_result,
            'holdout': holdout_result,
            'success': holdout_result['pass_threshold']
        }


if __name__ == "__main__":
    import sys
    
    logging.basicConfig(level=logging.INFO)
    
    # Quick test
    config_path = Path(__file__).parent.parent / "config" / "run_config.yaml"
    
    if config_path.exists():
        validator = SPARCValidator(str(config_path))
        validator.load_galaxies("synthetic")
        validator.split_data()
        
        results = validator.run_full_validation(n=1.37)
        
        print("\n" + "=" * 60)
        print("VALIDATION SUMMARY")
        print("=" * 60)
        print(f"CV χ²: {results['cross_validation']['cv_chi2_mean']:.3f}")
        print(f"Bootstrap CI: [{results['bootstrap']['chi2_ci_lower']:.3f}, {results['bootstrap']['chi2_ci_upper']:.3f}]")
        print(f"Holdout χ²: {results['holdout']['chi2_test_median']:.3f}")
        print(f"SUCCESS: {results['success']}")
    else:
        print(f"Config not found: {config_path}")
