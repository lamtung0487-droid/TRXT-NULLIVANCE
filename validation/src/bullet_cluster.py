"""
TRXT Validation - Bullet Cluster Simulation
=============================================
2D N-body simulation demonstrating separation of DM (collisionless) from Gas (collisional).
This is the G1 Gate test from the Master Protocol.
"""

import numpy as np
from typing import Tuple, Dict, List
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class Particle:
    """Single particle in simulation."""
    x: float
    y: float
    vx: float
    vy: float
    mass: float
    is_gas: bool  # True = gas (collisional), False = DM (collisionless)


@dataclass
class Cluster:
    """Galaxy cluster with gas and DM components."""
    name: str
    dm_particles: List[Particle]
    gas_particles: List[Particle]
    
    @property
    def dm_centroid(self) -> Tuple[float, float]:
        """Compute DM centroid."""
        if not self.dm_particles:
            return (0.0, 0.0)
        x = np.mean([p.x for p in self.dm_particles])
        y = np.mean([p.y for p in self.dm_particles])
        return (x, y)
    
    @property
    def gas_centroid(self) -> Tuple[float, float]:
        """Compute gas centroid."""
        if not self.gas_particles:
            return (0.0, 0.0)
        x = np.mean([p.x for p in self.gas_particles])
        y = np.mean([p.y for p in self.gas_particles])
        return (x, y)


class BulletClusterSimulation:
    """
    Simplified 2D simulation of Bullet Cluster collision.
    
    Key physics:
    - DM: Collisionless (passes through)
    - Gas: Collisional (experiences ram pressure, slows down)
    
    This demonstrates the key observational signature:
    DM centroid ≠ Gas centroid after collision.
    """
    
    def __init__(self, n_particles: int = 1000, sigma_m: float = 1.0, seed: int = 42):
        """
        Initialize simulation.
        
        Parameters
        ----------
        n_particles : int
            Number of particles per cluster per component
        sigma_m : float
            Self-interaction cross-section (cm²/g) - for SIDM mode
        seed : int
            Random seed
        """
        self.n_particles = n_particles
        self.sigma_m = sigma_m  # cm²/g
        self.seed = seed
        
        np.random.seed(seed)
        
        # Physical parameters (scaled units)
        self.G = 1.0  # Gravitational constant
        self.dt = 0.01  # Time step
        self.gas_friction = 0.5  # Friction coefficient for gas
        
        # Clusters
        self.main_cluster: Cluster = None
        self.bullet_cluster: Cluster = None
        
        # History for analysis
        self.history: List[Dict] = []
    
    def _create_spherical_cluster(self, center: Tuple[float, float],
                                   velocity: Tuple[float, float],
                                   radius: float = 1.0,
                                   mass_per_particle: float = 1.0,
                                   dm_fraction: float = 0.85) -> Cluster:
        """
        Create a spherical cluster with DM and gas.
        
        Parameters
        ----------
        center : tuple
            (x, y) center position
        velocity : tuple
            (vx, vy) bulk velocity
        radius : float
            Cluster radius
        mass_per_particle : float
            Mass of each particle
        dm_fraction : float
            Fraction of particles that are DM
            
        Returns
        -------
        cluster : Cluster
            Initialized cluster
        """
        dm_particles = []
        gas_particles = []
        
        n_dm = int(self.n_particles * dm_fraction)
        n_gas = self.n_particles - n_dm
        
        # Create DM particles
        for _ in range(n_dm):
            # Random position in sphere
            r = radius * np.random.uniform(0, 1) ** 0.5
            theta = np.random.uniform(0, 2 * np.pi)
            x = center[0] + r * np.cos(theta)
            y = center[1] + r * np.sin(theta)
            
            # Velocity dispersion
            v_disp = 0.1 * radius
            vx = velocity[0] + np.random.normal(0, v_disp)
            vy = velocity[1] + np.random.normal(0, v_disp)
            
            dm_particles.append(Particle(x, y, vx, vy, mass_per_particle, is_gas=False))
        
        # Create gas particles (more concentrated)
        for _ in range(n_gas):
            r = radius * 0.5 * np.random.uniform(0, 1) ** 0.5
            theta = np.random.uniform(0, 2 * np.pi)
            x = center[0] + r * np.cos(theta)
            y = center[1] + r * np.sin(theta)
            
            v_disp = 0.05 * radius
            vx = velocity[0] + np.random.normal(0, v_disp)
            vy = velocity[1] + np.random.normal(0, v_disp)
            
            gas_particles.append(Particle(x, y, vx, vy, mass_per_particle, is_gas=True))
        
        return Cluster(name="cluster", dm_particles=dm_particles, gas_particles=gas_particles)
    
    def initialize_collision(self, separation: float = 4.0, 
                              collision_velocity: float = 1.0):
        """
        Set up the initial conditions for collision.
        
        Parameters
        ----------
        separation : float
            Initial separation between cluster centers
        collision_velocity : float
            Relative collision velocity
        """
        # Main cluster (larger, stationary)
        self.main_cluster = self._create_spherical_cluster(
            center=(separation / 2, 0),
            velocity=(-collision_velocity / 2, 0),
            radius=1.5,
            mass_per_particle=1.0
        )
        self.main_cluster.name = "Main"
        
        # Bullet cluster (smaller, faster)
        self.bullet_cluster = self._create_spherical_cluster(
            center=(-separation / 2, 0),
            velocity=(collision_velocity, 0),
            radius=0.8,
            mass_per_particle=0.5
        )
        self.bullet_cluster.name = "Bullet"
        
        logger.info(f"Initialized collision: separation={separation}, v={collision_velocity}")
    
    def _compute_gravity(self, particles: List[Particle]) -> List[Tuple[float, float]]:
        """
        Compute gravitational acceleration on each particle.
        Simplified: use mean-field approximation.
        """
        accelerations = []
        
        # Compute total mass centroid
        total_mass = sum(p.mass for p in particles)
        cx = sum(p.x * p.mass for p in particles) / total_mass
        cy = sum(p.y * p.mass for p in particles) / total_mass
        
        for p in particles:
            dx = cx - p.x
            dy = cy - p.y
            r = np.sqrt(dx**2 + dy**2) + 0.1  # Softening
            
            # Gravitational acceleration toward center
            a = self.G * total_mass / r**2
            ax = a * dx / r
            ay = a * dy / r
            
            accelerations.append((ax, ay))
        
        return accelerations
    
    def _apply_gas_friction(self, gas1: List[Particle], gas2: List[Particle]):
        """
        Apply ram pressure friction between gas components.
        Gas particles that overlap experience drag.
        """
        for p1 in gas1:
            for p2 in gas2:
                dx = p2.x - p1.x
                dy = p2.y - p1.y
                r = np.sqrt(dx**2 + dy**2)
                
                if r < 0.3:  # Interaction radius
                    # Relative velocity
                    dvx = p2.vx - p1.vx
                    dvy = p2.vy - p1.vy
                    
                    # Friction force proportional to relative velocity
                    friction = self.gas_friction * np.exp(-r / 0.1)
                    
                    p1.vx += friction * dvx * self.dt
                    p1.vy += friction * dvy * self.dt
                    p2.vx -= friction * dvx * self.dt
                    p2.vy -= friction * dvy * self.dt
    
    def step(self):
        """Advance simulation by one time step."""
        # All particles
        all_particles = (
            self.main_cluster.dm_particles + 
            self.main_cluster.gas_particles +
            self.bullet_cluster.dm_particles +
            self.bullet_cluster.gas_particles
        )
        
        # Gravity
        accels = self._compute_gravity(all_particles)
        
        # Update velocities and positions
        for p, (ax, ay) in zip(all_particles, accels):
            p.vx += ax * self.dt
            p.vy += ay * self.dt
            p.x += p.vx * self.dt
            p.y += p.vy * self.dt
        
        # Gas friction (collisional interaction)
        self._apply_gas_friction(
            self.main_cluster.gas_particles,
            self.bullet_cluster.gas_particles
        )
    
    def run(self, n_steps: int = 500) -> Dict:
        """
        Run the full simulation.
        
        Parameters
        ----------
        n_steps : int
            Number of time steps
            
        Returns
        -------
        results : dict
            Simulation results including DM-gas separation
        """
        logger.info(f"Running Bullet Cluster simulation: {n_steps} steps")
        
        # Record initial state
        self._record_state(0)
        
        # Run simulation
        for step in range(n_steps):
            self.step()
            
            if step % 50 == 0:
                self._record_state(step)
        
        # Record final state
        self._record_state(n_steps)
        
        # Compute final separation
        final = self._compute_separation()
        
        logger.info(f"Final DM-Gas separation: {final['bullet_separation']:.3f}")
        
        return final
    
    def _record_state(self, step: int):
        """Record current state to history."""
        self.history.append({
            'step': step,
            'main_dm': self.main_cluster.dm_centroid,
            'main_gas': self.main_cluster.gas_centroid,
            'bullet_dm': self.bullet_cluster.dm_centroid,
            'bullet_gas': self.bullet_cluster.gas_centroid
        })
    
    def _compute_separation(self) -> Dict:
        """Compute DM-gas separation for each cluster."""
        # Bullet cluster separation
        dm = self.bullet_cluster.dm_centroid
        gas = self.bullet_cluster.gas_centroid
        bullet_sep = np.sqrt((dm[0] - gas[0])**2 + (dm[1] - gas[1])**2)
        
        # Main cluster separation
        dm = self.main_cluster.dm_centroid
        gas = self.main_cluster.gas_centroid
        main_sep = np.sqrt((dm[0] - gas[0])**2 + (dm[1] - gas[1])**2)
        
        return {
            'bullet_separation': bullet_sep,
            'main_separation': main_sep,
            'bullet_dm_centroid': self.bullet_cluster.dm_centroid,
            'bullet_gas_centroid': self.bullet_cluster.gas_centroid,
            'main_dm_centroid': self.main_cluster.dm_centroid,
            'main_gas_centroid': self.main_cluster.gas_centroid,
            'history': self.history
        }
    
    def verify_g1_gate(self) -> Dict:
        """
        Verify G1 Gate: DM-Gas separation must be non-zero.
        
        Returns
        -------
        result : dict
            G1 Gate verification result
        """
        sep = self._compute_separation()
        
        # Threshold for significant separation (in simulation units)
        threshold = 0.1
        
        bullet_passes = sep['bullet_separation'] > threshold
        main_passes = sep['main_separation'] > threshold
        
        return {
            'g1_gate_pass': bullet_passes or main_passes,
            'bullet_separation': sep['bullet_separation'],
            'main_separation': sep['main_separation'],
            'threshold': threshold,
            'message': (
                "PASS: DM-Gas separation observed" if bullet_passes 
                else "FAIL: No significant DM-Gas separation"
            )
        }


def run_bullet_cluster_test(n_particles: int = 500, n_steps: int = 300) -> Dict:
    """
    Run Bullet Cluster simulation and verify G1 Gate.
    
    Parameters
    ----------
    n_particles : int
        Particles per cluster component
    n_steps : int
        Simulation steps
        
    Returns
    -------
    results : dict
        Complete test results
    """
    logging.basicConfig(level=logging.INFO)
    
    sim = BulletClusterSimulation(n_particles=n_particles, seed=42)
    sim.initialize_collision(separation=4.0, collision_velocity=2.0)
    
    results = sim.run(n_steps=n_steps)
    g1_result = sim.verify_g1_gate()
    
    return {
        'simulation': results,
        'g1_gate': g1_result
    }


if __name__ == "__main__":
    results = run_bullet_cluster_test(n_particles=500, n_steps=300)
    
    print("\n" + "=" * 60)
    print("BULLET CLUSTER SIMULATION RESULTS")
    print("=" * 60)
    print(f"Bullet DM-Gas separation: {results['simulation']['bullet_separation']:.4f}")
    print(f"Main DM-Gas separation: {results['simulation']['main_separation']:.4f}")
    print(f"\nG1 GATE: {results['g1_gate']['message']}")
    print(f"PASS: {results['g1_gate']['g1_gate_pass']}")
