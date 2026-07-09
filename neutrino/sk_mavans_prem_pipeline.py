#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Super-K Day/Night pipeline with:
  - PREM continuous density profile (generated + interpolated)
  - 20 zenith bins cosZ ∈ [-1, 0]
  - 3-flavor PMNS evolution (NuFIT defaults; CLI override)
  - Hamiltonian: vacuum + V_CC (MSW) + MaVaN log-running implemented as Δm^2(ρ)
  - B-8 spectrum + Super-K ES cross-sections read from Bahcall T_table.dat
Outputs:
  - A_DN total (SK convention and its negative)
  - A_DN(E) and night zenith distribution (optional plots + CSV)

References used for defaults/data sources:
  - NuFIT 5.2 parameter table PDF (v52.tbl-parameters.pdf)
  - Bahcall solar neutrino data tables: Momentsspectra/T_table.dat
"""

from __future__ import annotations

import argparse
import dataclasses
import math
import os
import sys
from scipy.linalg import expm, expm_frechet
from scipy.integrate import solve_ivp
from scipy import linalg
from typing import Dict, Tuple, Optional, List

import numpy as np

# ----------------------------
# Constants / units
# ----------------------------

R_EARTH_KM = 6371.0
# 1 m = 5.0677307e6 eV^-1  =>  1 km = 5.0677307e9 eV^-1
KM_TO_EVINV = 5.0677307e9

# MSW matter potential constant:
# V_CC[eV] ≈ 7.632e-14 * Ye * rho[g/cm^3]
# (standard neutrino oscillation convention; you can override if desired)
VCC_COEFF_eV = 7.632e-14

# Default MaVaN reference density
DEFAULT_RHO_C = 3.0  # g/cm^3 (KamLAND effective)

# ----------------------------
# PREM: generate table -> interpolate
# (piecewise polynomials used widely as PREM approximation)
# density in g/cm^3; x = r/R_E
# ----------------------------

def prem_rho_piecewise_gcm3(r_km: float) -> float:
    """PREM density (g/cm^3) using standard piecewise polynomials in normalized radius x=r/R."""
    if r_km < 0 or r_km > R_EARTH_KM:
        return 0.0
    x = r_km / R_EARTH_KM

    # Boundaries (km)
    r_icb = 1221.5  # inner core boundary
    r_cmb = 3480.0  # core-mantle boundary
    r_lm  = 5701.0
    r_tz1 = 5771.0
    r_tz2 = 5971.0
    r_tz3 = 6151.0
    r_lvz = 6346.6
    r_lid = 6356.0
    # crust: 6356-6371

    if r_km <= r_icb:
        # inner core
        rho = 13.0885 - 8.8381 * x**2
    elif r_km <= r_cmb:
        # outer core
        rho = 12.5815 - 1.2638 * x - 3.6426 * x**2 - 5.5281 * x**3
    elif r_km <= r_lm:
        # lower mantle
        rho = 7.9565 - 6.4761 * x + 5.5283 * x**2 - 3.0807 * x**3
    elif r_km <= r_tz1:
        rho = 5.3197 - 1.4836 * x
    elif r_km <= r_tz2:
        rho = 11.2494 - 8.0298 * x
    elif r_km <= r_tz3:
        rho = 7.1089 - 3.8045 * x
    elif r_km <= r_lvz:
        rho = 2.6910 + 0.6924 * x
    elif r_km <= r_lid:
        rho = 2.9000
    else:
        rho = 2.6000

    return float(max(rho, 0.0))


def prem_Ye_step(r_km: float) -> float:
    """
    Electron fraction Ye = n_e / n_b (dimensionless).
    PREM gives density; Ye is composition-dependent. Super-K day/night is not ultra-sensitive to small Ye tweaks,
    but we keep a physically reasonable profile:
      - core:   ~0.467
      - mantle: ~0.495
      - crust:  ~0.500
    """
    if r_km < 0 or r_km > R_EARTH_KM:
        return 0.0
    if r_km <= 3480.0:  # core
        return 0.467
    if r_km >= 6356.0:  # crust
        return 0.500
    return 0.495


def build_prem_interp(n_points: int = 5000) -> Tuple[np.ndarray, np.ndarray]:
    """
    Build (r_km, rho_gcm3) table and return arrays for interpolation.
    """
    r = np.linspace(0.0, R_EARTH_KM, n_points)
    rho = np.array([prem_rho_piecewise_gcm3(ri) for ri in r], dtype=float)
    return r, rho


@dataclasses.dataclass
class PremModel:
    r_km: np.ndarray
    rho_gcm3: np.ndarray

    def rho(self, r_km: float) -> float:
        if r_km <= 0:
            return float(self.rho_gcm3[0])
        if r_km >= R_EARTH_KM:
            return float(self.rho_gcm3[-1])
        return float(np.interp(r_km, self.r_km, self.rho_gcm3))

    def Ye(self, r_km: float) -> float:
        return prem_Ye_step(r_km)


# ----------------------------
# Neutrino parameters & PMNS
# ----------------------------

@dataclasses.dataclass
class OscParams:
    # angles in radians
    th12: float
    th13: float
    th23: float
    dcp: float  # CP phase in radians

    # mass splittings in eV^2 (NO by default)
    dm21: float
    dm31: float

    # MaVaN log-running coefficients
    beta_solar: float
    beta_earth: float
    rho_c: float

    # Solar core params (for production as matter eigenstates)
    rho_sun_core: float
    Ye_sun_core: float

    @property
    def U(self) -> np.ndarray:
        return pmns_matrix(self.th12, self.th13, self.th23, self.dcp)


def pmns_matrix(th12: float, th13: float, th23: float, dcp: float) -> np.ndarray:
    """Standard PDG parameterization (no Majorana phases)."""
    s12, c12 = math.sin(th12), math.cos(th12)
    s13, c13 = math.sin(th13), math.cos(th13)
    s23, c23 = math.sin(th23), math.cos(th23)

    e_minus_id = complex(math.cos(-dcp), math.sin(-dcp))  # e^{-iδ}
    e_plus_id  = complex(math.cos(dcp), math.sin(dcp))    # e^{+iδ}

    U = np.zeros((3, 3), dtype=complex)

    U[0, 0] = c12 * c13
    U[0, 1] = s12 * c13
    U[0, 2] = s13 * e_minus_id

    U[1, 0] = -s12 * c23 - c12 * s23 * s13 * e_plus_id
    U[1, 1] =  c12 * c23 - s12 * s23 * s13 * e_plus_id
    U[1, 2] =  s23 * c13

    U[2, 0] =  s12 * s23 - c12 * c23 * s13 * e_plus_id
    U[2, 1] = -c12 * s23 - s12 * c23 * s13 * e_plus_id
    U[2, 2] =  c23 * c13

    return U


# ----------------------------
# Bahcall table loader (B-8 spectrum + ES cross sections)
# ----------------------------

@dataclasses.dataclass
class BahcallTable:
    E_MeV: np.ndarray     # neutrino energy grid
    lam: np.ndarray       # spectrum weight (lambda)
    sigma_nue: np.ndarray # ES cross section for nue (units per header; scale cancels in asymmetry)
    sigma_numu: np.ndarray# ES cross section for numu/tau

    def restrict(self, emin: float, emax: float) -> "BahcallTable":
        m = (self.E_MeV >= emin) & (self.E_MeV <= emax)
        return BahcallTable(
            E_MeV=self.E_MeV[m],
            lam=self.lam[m],
            sigma_nue=self.sigma_nue[m],
            sigma_numu=self.sigma_numu[m],
        )


def load_bahcall_T_table(path: str) -> BahcallTable:
    """
    Parse Bahcall Momentsspectra 'T_table.dat'.
    Columns (per header) are:
      Enu, lambda, S(NC), S(CC), Tave, S(nue), T(nue), S(numu), T(numu)
    We use: Enu, lambda, S(nue), S(numu).
    """
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Bahcall table not found: {path}\n"
            f"Download 'T_table.dat' from Bahcall solar neutrino data tables and place it here, "
            f"or pass --bahcall_table /path/to/T_table.dat."
        )

    # Skip comment lines starting with '#'
    rows = []
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) < 9:
                continue
            
            # Check if first part is a number
            try:
                float(parts[0])
            except ValueError:
                continue
                
            rows.append([float(x) for x in parts[:9]])

    arr = np.array(rows, dtype=float)
    if arr.shape[1] < 9 or arr.shape[0] < 10:
        raise ValueError("Parsed Bahcall table looks wrong (too few rows/cols).")

    E = arr[:, 0]
    lam = arr[:, 1]
    sigma_nue = arr[:, 5]
    sigma_numu = arr[:, 7]

    return BahcallTable(E_MeV=E, lam=lam, sigma_nue=sigma_nue, sigma_numu=sigma_numu)


# ----------------------------
# Hamiltonian construction
# ----------------------------

def dm_eff(dm_vac: float, rho_gcm3: float, beta: float, rho_c: float) -> float:
    """
    Log-running MaVaN correction applied ONLY to Δm^2 (per your technical decision).
    Δm^2(ρ) = Δm^2_vac * [1 - beta * ln( rho / rho_c )]
    """
    rho = max(rho_gcm3, 1e-12)
    return dm_vac * (1.0 - beta * math.log(rho / rho_c))


def V_cc_eV(rho_gcm3: float, Ye: float) -> float:
    return VCC_COEFF_eV * Ye * rho_gcm3


def H_flavor_eV(E_MeV: float, rho_gcm3: float, Ye: float, p: OscParams, beta: float) -> np.ndarray:
    """
    3-flavor neutrino Hamiltonian in flavor basis, in eV:
      H = (1/2E) U diag(0, Δm21^2(ρ), Δm31^2(ρ)) U† + diag(Vcc,0,0)
    """
    E_eV = E_MeV * 1e6

    dm21 = dm_eff(p.dm21, rho_gcm3, beta, p.rho_c)
    dm31 = dm_eff(p.dm31, rho_gcm3, beta, p.rho_c)

    # mass^2 diag (m1^2=0 reference)
    m2 = dm21
    m3 = dm31
    M2 = np.diag([0.0, m2, m3]).astype(complex)

    U = p.U
    H_vac = (U @ M2 @ U.conj().T) / (2.0 * E_eV)

    H_mat = np.diag([V_cc_eV(rho_gcm3, Ye), 0.0, 0.0]).astype(complex)
    H = H_vac + H_mat

    # Ensure hermiticity numerically
    H = 0.5 * (H + H.conj().T)
    return H


def expm_hermitian(H: np.ndarray, L_evinv: float) -> np.ndarray:
    """
    Compute exp(-i H L) for small 3x3 Hermitian H using eigen-decomposition.
    """
    w, v = np.linalg.eigh(H)
    phase = np.exp(-1j * w * L_evinv)
    return (v * phase) @ v.conj().T


# ----------------------------
# Geometry: chord through Earth for given cosZ
# ----------------------------

def chord_points_for_cosz(cosz: float, ds_km: float) -> Tuple[np.ndarray, np.ndarray]:
    """
    For night cosZ in [-1, 0], build positions along Earth chord from entry to detector.
    Returns:
      s_km : coordinate along chord (km), from -L/2 to +L/2
      r_km : radial distance from Earth's center at each point
    """
    if cosz >= 0:
        return np.array([], dtype=float), np.array([], dtype=float)

    cosz_abs = abs(cosz)
    L_km = 2.0 * R_EARTH_KM * cosz_abs
    if L_km <= 0:
        return np.array([], dtype=float), np.array([], dtype=float)

    # Impact parameter p = R * sqrt(1 - cos^2) = R * sin(nadir)
    p = R_EARTH_KM * math.sqrt(max(0.0, 1.0 - cosz_abs**2))

    n_steps = max(1, int(math.ceil(L_km / ds_km)))
    s = np.linspace(-0.5 * L_km, 0.5 * L_km, n_steps + 1)
    r = np.sqrt(p**2 + s**2)
    return s, r


# ----------------------------
# Solar production -> mass eigenstate probabilities (adiabatic + decoherence)
# ----------------------------

def solar_mass_probs(E_MeV: float, p: OscParams) -> np.ndarray:
    """
    Track eigenvectors continuously from solar core to vacuum to avoid label switching.
    Density ladder: rho_sun_core -> ... -> 0
    Returns P_mass[i] = probability of arriving as mass eigenstate i.
    """
    # 1. Create density ladder (log-spaced)
    rho_start = p.rho_sun_core
    rho_end = 1e-10
    n_steps = 100
    rhos = np.logspace(math.log10(rho_start), math.log10(rho_end), n_steps)

    # 2. Get initial eigenvectors at core
    H_start = H_flavor_eV(E_MeV, rho_start, p.Ye_sun_core, p, beta=p.beta_solar)
    w_curr, v_curr = np.linalg.eigh(H_start)
    
    # 3. Step down
    for k in range(1, n_steps):
        rho_next = rhos[k]
        # Assume Ye transitions to 0? Or keeps solar core? simple approx: constant Ye
        # (Ye doesn't matter much at vacuum, standard is Ye proportional to rho or just constant)
        # We keep using Ye_sun_core for the tracking since we track "what comes out".
        H_next = H_flavor_eV(E_MeV, rho_next, p.Ye_sun_core, p, beta=p.beta_solar) 
        w_next, v_next = np.linalg.eigh(H_next)

        # Match v_next columns to v_curr columns to maximize overlap
        # overlap matrix M_ij = |v_next[:,i]^H . v_curr[:,j]|
        overlap = np.abs(v_next.conj().T @ v_curr) # shape (3,3)
        
        # Greedy assignment is usually fine for small steps
        
        # We need mapping: which index in "next" corresponds to index j in "curr"
        # Since v_next are sorted by eigenvalue, we just need to reorder v_next
        # to align with v_curr.
        
        # Find permutation of rows of overlap matrix to maximize trace (roughly)
        perms = [(0,1,2),(0,2,1),(1,0,2),(1,2,0),(2,0,1),(2,1,0)]
        best_perm = None
        best_score = -1.0
        
        for perm in perms:
            # Score = sum of overlaps if we map curr_0 -> next_p0, curr_1 -> next_p1...
            # overlap[i, j] is match between next_i and curr_j
            # We want to match curr_0 with some next_i...
            # Wait, overlap[i,j] = |<next_i | curr_j>|
            # We want to select row r0 for col 0, row r1 for col 1...
            score = overlap[perm[0], 0] + overlap[perm[1], 1] + overlap[perm[2], 2]
            if score > best_score:
                best_score = score
                best_perm = perm
        
        # Reorder v_next to match v_curr order
        # v_curr column j maps to v_next column best_perm[j]
        v_next_reordered = np.zeros_like(v_next)
        for j in range(3):
            v_next_reordered[:, j] = v_next[:, best_perm[j]]
            
        v_curr = v_next_reordered

    # Now v_curr contains vacuum eigenvectors, but ORDERED according to their origin at core.
    # v_curr[:, 0] is the state that started as "lowest energy state at core".
    # v_curr[:, 1] is the state that started as "middle energy state at core".
    # v_curr[:, 2] is the state that started as "highest energy state at core".
    
    # However, "mass eigenstate i" usually refers to vacuum states sorted by mass (1,2,3).
    # We need to identify which column of v_curr corresponds to vacuum mass state 1, 2, 3.
    # We construct "Standard Vacuum Eigenvectors" v_vac_std sorted by eigenvalue.
    
    H_vac_std = H_flavor_eV(E_MeV, 1e-12, 0.0, p, beta=p.beta_solar)
    w_vac_std, v_vac_std = np.linalg.eigh(H_vac_std)
    
    # Identify mapping from "tracked states" (v_curr) to "standard vacuum states" (v_vac_std)
    overlap_final = np.abs(v_vac_std.conj().T @ v_curr)
    
    # Which tracked column j maps to vacuum state i?
    # P_mass[i] is probability of vacuum state i.
    # This comes from the amplitude of tracked column j at the core, IF tracked column j maps to vacuum state i.
    
    # Let's verify mapping:
    # v_curr[:, j] should look like one of v_vac_std[:, i] (up to phase)
    
    map_track_to_vac = {} # track_idx -> vac_idx
    for j in range(3): 
        # find best match in vacuum states
        vac_idx = np.argmax(overlap_final[:, j])
        map_track_to_vac[j] = vac_idx
        
    # Calculate initial composition at core
    # At core, nu_e is produced. 
    # State is |nu_e> = (1,0,0)^T.
    # The amplitude of "core eigenstate j" (which is tracked to v_curr[:,j]) is:
    # A_j = <core_eigenstate_j | nu_e>^* = v_start[0, j]^*  (Wait, v_start was the core basis)
    # Yes, we need v_start (or recalculate it).
    
    # Let's re-get v_start (ordered by energy at core)
    # Actually, we tracked it. v_curr is the "evolution" of the basis.
    # BUT the "probability" is determined at PRODUCTION (core).
    # Adiabaticity means: A_j (amplitude in j-th instantaneous eigenstate) is CONSTANT.
    # So we need A_j at core.
    
    # Restart to get A_j at core properly
    H_start = H_flavor_eV(E_MeV, rho_start, p.Ye_sun_core, p, beta=p.beta_solar)
    w_start, v_start = np.linalg.eigh(H_start)
    
    # We need to know which "start" index corresponds to which "tracked" index.
    # In our loop, we maintained `v_curr` such that `v_curr[:, k]` is the continuation of `v_start[:, k]`.
    # (Because we reordered v_next to match v_curr's columns).
    # So: Track-index k corresponds to Start-index k.
    
    P_mass = np.zeros(3, dtype=float)
    
    for k in range(3):
        # Amplitude at production
        # |amplitude|^2 = |<nu_e | v_start_k>|^2 = |v_start[0, k]|^2
        prob_k = abs(v_start[0, k])**2
        
        # Which vacuum state i does track-k correspond to?
        vac_idx = map_track_to_vac[k]
        
        P_mass[vac_idx] += prob_k # accumulating (though accurate mapping is 1-to-1)

    return P_mass


# ----------------------------
# Earth evolution operator S(E, cosZ)
# ----------------------------

def earth_evolution_operator(E_MeV: float, cosz: float, prem: PremModel, p: OscParams, ds_km: float) -> np.ndarray:
    """
    Compute S such that psi_out = S psi_in (flavor basis), for night trajectories.
    For day (cosz>=0), return identity.
    """
    if cosz >= 0:
        return np.eye(3, dtype=complex)

    s_km, r_km = chord_points_for_cosz(cosz, ds_km=ds_km)
    if r_km.size == 0:
        return np.eye(3, dtype=complex)

    S = np.eye(3, dtype=complex)

    # step length in eV^-1 (use segment lengths)
    for k in range(len(r_km) - 1):
        r_mid = 0.5 * (r_km[k] + r_km[k+1])
        rho = prem.rho(float(r_mid))
        Ye = prem.Ye(float(r_mid))

        ds_seg = float(abs(s_km[k+1] - s_km[k]))  # km
        L_evinv = ds_seg * KM_TO_EVINV

        H = H_flavor_eV(E_MeV, rho, Ye, p, beta=p.beta_earth)
        U_step = expm_hermitian(H, L_evinv)
        S = U_step @ S

    return S

def earth_evolution_rk4(
    E_MeV: float,
    cosz: float,
    prem: PremModel,
    p: OscParams
) -> np.ndarray:
    """
    Independent solver using Runge-Kutta (scipy.integrate.solve_ivp)
    Solves dS/dx = -i H(x) S(x).
    We solve for the 3 columns of S simultaneously (9 complex components).
    """
    R_earth = R_EARTH_KM * KM_TO_EVINV
    # Geometry
    cosz_abs = abs(cosz)
    L_km = 2.0 * R_EARTH_KM * cosz_abs
    L_evinv = L_km * KM_TO_EVINV
    
    # Impact parameter b
    b_km = R_EARTH_KM * math.sqrt(max(0.0, 1.0 - cosz_abs**2))
    
    # Hamiltonian function for solver
    # H depends on position x along chord (0 to L)
    # r(x) = sqrt(b^2 + (x - L/2)^2)
    def rhs(x_ev, y_flat):
        # x_ev is distance in eV^-1
        # Convert back to km for density lookup
        x_km = x_ev / KM_TO_EVINV
        
        # Center of chord is at x_km = L_km / 2
        s_from_center = x_km - L_km * 0.5
        r_km = math.sqrt(b_km**2 + s_from_center**2)
        
        rho = prem.rho(r_km)
        Ye = prem.Ye(r_km)
        
        H = H_flavor_eV(E_MeV, rho, Ye, p, beta=p.beta_earth)
        
        # y_flat is 9 complex numbers (row-major 3x3 S matrix)
        S_mat = y_flat.reshape(3,3)
        
        # dS/dx = -i H S
        dSdx = -1j * (H @ S_mat)
        return dSdx.flatten()

    # Initial condition: S(0) = Identity
    y0 = np.eye(3, dtype=complex).flatten()
    
    # Tolerance: tight for cross-check
    sol = solve_ivp(rhs, [0, L_evinv], y0, rtol=1e-5, atol=1e-8)
    
    S_final = sol.y[:,-1].reshape(3,3)
    return S_final

def run_solver_cross_check(args, prem, p):
    """
    Goal: Verify that 'Slab' method and 'RK4' method give same S matrix.
    We pick a core-crossing trajectory (cosz = -1) and a mantle trajectory (cosz = -0.5).
    """
    print("\n=== SOLVER CROSS-CHECK (Work Package A2) ===")
    print("Comparing 'Constant Density Slab' vs 'Runge-Kutta 4' evolution...")

    test_points = [
        # (E_MeV, cosz, name, description)
        (10.0, -1.0, "Core-crossing", "Deepest path (max density)"),
        (5.0, -0.4, "Mantle-only", "Shadow zone or crust/mantle"),
    ]
    
    passing = True
    
    for E, cz, name, desc in test_points:
        print(f"\n--- Case: {name} ({desc}) ---")
        print(f"E = {E} MeV, cosZ = {cz}")
        
        # 1. Slab
        S_slab = earth_evolution_operator(E, cz, prem, p, ds_km=args.ds_km) # uses ds from args
        
        # 2. RK4
        S_rk4 = earth_evolution_rk4(E, cz, prem, p)
        
        # Compare
        diff = np.abs(S_slab - S_rk4)
        max_diff = np.max(diff)
        
        print("S_slab (top-left 2x2):\n", S_slab[:2,:2])
        print("S_rk4  (top-left 2x2):\n", S_rk4[:2,:2])
        print(f"Max absolute element difference: {max_diff:.2e}")
        
        if max_diff < 5e-3: # relaxed tolerance for ds=30km vs adaptive RK
            print(">> CHECK PASS")
        else:
            print(">> CHECK WARN (Diff > 0.5%)")
            passing = False
            
    if passing:
        print("\n[SUCCESS] Independent solver check confirmed consistent physics.")
    else:
        print("\n[WARNING] Discrepancy detected between solvers.")


# ----------------------------
# Event rates and A_DN
# ----------------------------

@dataclasses.dataclass
class ADNResult:
    A_dn_SK: float     # (D - N)/avg
    A_dn_alt: float    # (N - D)/avg
    day_rate: float
    night_rate: float


def integrate_energy(table: BahcallTable, fE: np.ndarray) -> float:
    """
    Weighted energy integral using trapezoid on the table grid:
      integral dE [ lambda(E) * f(E) ]
    """
    return float(np.trapz(table.lam * fE, table.E_MeV))


def compute_day_night_rates(
    table: BahcallTable,
    prem: PremModel,
    p: OscParams,
    cosz_bins: np.ndarray,
    cosz_weights: np.ndarray,
    ds_km: float,
    cache_S: Optional[Dict[Tuple[float,float], np.ndarray]] = None,
) -> Tuple[float, float, np.ndarray, np.ndarray, np.ndarray]:
    """
    Returns:
      day_rate (scalar),
      night_rate (scalar),
      day_rate_E (array per energy point),
      night_rate_E (array per energy point),
      night_rate_per_bin (array of size n_cos_bins - integrated over Energy)
    """
    if cache_S is None:
        cache_S = {}

    U = p.U
    Ue2 = abs(U[0,1])**2

    # Energy-dependent: mass-eigenstate probabilities from solar core
    Pmass = np.array([solar_mass_probs(E, p) for E in table.E_MeV], dtype=float)  # shape (nE,3)

    # Day survival: incoherent average in vacuum
    Pee_day = (
        Pmass[:,0] * (abs(U[0,0])**2) +
        Pmass[:,1] * (abs(U[0,1])**2) +
        Pmass[:,2] * (abs(U[0,2])**2)
    )

    # Day event rate per energy (ES: nue vs numu/tau)
    day_rate_E = Pee_day * table.sigma_nue + (1.0 - Pee_day) * table.sigma_numu

    # Night: for each cosz bin, propagate 3 basis states once via S; then average with Pmass
    night_rate_E_accum = np.zeros_like(table.E_MeV, dtype=float)
    night_rate_per_bin = [] # store total rate for each bin

    for cz, wcz in zip(cosz_bins, cosz_weights):
        if cz >= 0:
            night_rate_per_bin.append(0.0) # Should not happen for night bins
            continue

        Pee_night = np.zeros_like(table.E_MeV, dtype=float)

        for iE, E in enumerate(table.E_MeV):
            key = (float(E), float(cz))
            if key in cache_S:
                S = cache_S[key]
            else:
                S = earth_evolution_operator(E, cz, prem, p, ds_km=ds_km)
                cache_S[key] = S

            # For each vacuum mass eigenstate i, initial flavor vector is U[:, i]
            # (since |nu_i> = sum_alpha U_{alpha i}^* |nu_alpha>, but state vector in flavor basis is U[:,i])
            # Here we use "column i" convention consistent with PMNS definition above.
            # Then psi_out = S @ psi_in, and Pee_i = |(psi_out)_e|^2
            Pee_i = np.empty(3, dtype=float)
            for i in range(3):
                psi_in = U[:, i]
                psi_out = S @ psi_in
                Pee_i[i] = float((psi_out[0].conj() * psi_out[0]).real)

            Pee_night[iE] = float(Pmass[iE,0]*Pee_i[0] + Pmass[iE,1]*Pee_i[1] + Pmass[iE,2]*Pee_i[2])

        night_rate_E_bin = Pee_night * table.sigma_nue + (1.0 - Pee_night) * table.sigma_numu
        
        # Integrate this bin over energy to get total rate
        rate_bin_tot = integrate_energy(table, night_rate_E_bin)
        night_rate_per_bin.append(rate_bin_tot)

        night_rate_E_accum += wcz * night_rate_E_bin

    night_rate_E = night_rate_E_accum

    day_rate = integrate_energy(table, day_rate_E)
    night_rate = integrate_energy(table, night_rate_E)

    return day_rate, night_rate, day_rate_E, night_rate_E, np.array(night_rate_per_bin)

def compute_unoscillated_rate(table: BahcallTable, sigma_nue: np.ndarray) -> float:
    """
    Compute total unoscillated rate (Pee=1, Pmm=0) for standard solar model comparison.
    Rate = Integral( Phi(E) * sigma_nue(E) )
    We assume table.lam is Phi(E) normalized or we use it as is?
    table.lam from Bahcall is dPhi/dE? Or just weights.
    Actually in compute_rate: rate = Integral(lam * (Pee*sig_e + PmV*sig_mu)).
    For unoscillated: Pee=1.
    """
    rate_E = table.sigma_nue  # since Pee=1 everywhere
    return integrate_energy(table, rate_E)

def load_sk_zenith_data(csv_path: str) -> Optional[List[Tuple[str, float, float]]]:
    """
    Load SK Zenith Data from CSV.
    Returns list of (bin_name, ratio, error).
    """
    if not os.path.exists(csv_path):
        return None
    data = []
    with open(csv_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split(',')
            if len(parts) >= 3:
                try:
                    name = parts[0].strip()
                    ratio = float(parts[1])
                    err = float(parts[2])
                    data.append((name, ratio, err))
                except ValueError:
                    continue
    return data

def compute_chi2_zenith(
    model_day_rate: float,
    model_night_bins_rates: np.ndarray,
    model_unosc_rate: float,
    sk_data: List[Tuple[str, float, float]]
) -> Tuple[float, int, float, float]:
    """
    Compute Chi2 for Zenith Shape.
    Model Ratio = Rate_Osc / Rate_Unosc
    Data Ratio = R_obs
    Chi2 = Sum_i ( (R_obs_i - alpha * R_mod_i)^2 / sigma_i^2 )
    Analytically minimize alpha (scaling factor) to handle flux normalization nuisance.
    
    Returns: (chi2_min, ndf, p_value, alpha_best)
    """
    # Map model bins to data bins
    # Data: Day, Night1..6.
    # Model: day_rate (scalar), night_rate_bins (array).
    # We assume night_rate_bins corresponds to Night1..NightN.
    
    # 1. Flatten arrays
    # Model Ratios
    R_mod = []
    R_mod.append(model_day_rate / model_unosc_rate) # Day
    for val in model_night_bins_rates:
        R_mod.append(val / model_unosc_rate)
    R_mod = np.array(R_mod)
    
    # Data Ratios & Errors
    R_dat = []
    Sig = []
    # Make sure we match length
    # SK Data usually: Day, N1, N2, N3, N4, N5, N6 (7 bins)
    # Our model usually has N bins. If model has 20 bins, we need to rebin?
    # Wait, the user manual instruction implies "Night1...Night6".
    # BUT our simulation runs with `--n_cos_bins 20` or similar?
    # CRITICAL: We need to re-bin the model to match SK binning if they differ.
    # OR, we should have run the simulation with SK binning.
    # SK SK-IV bins: Day (all), Night divided by cosZ.
    # Bins: D, N1(-0.? to ?)...
    # If our simulation uses generic 20 bins, we can't directly compare to 6 bins unless we verify boundaries.
    # SK Night bins are typically equal width in cosZ?
    # PRD 94 Table XII bins defined as:
    # N1: 0 to -0.16? Or -0.something.
    # Actually, SK bins are typically N1..N6 defined by cos(theta_z).
    # "The night bins are defined as..." - usually 6 bins of width ~0.166? 
    # Or 5 bins of 0.2?
    # Let's assume for this "Kill-shot" we map generic bins to SK bins by averaging?
    # Or simpler: The user provided data has 6 night bins. 
    # If we run model with 6 night bins in [-1, 0], we match exactly (if SK bins are equal width).
    # SK-IV Night bins: -1.0 to -0.84, etc? 
    # Let's assume equal width for now to proceed, but ideally we match exactly.
    # If the user input generic `n_cos_bins`, we might have mismatch.
    # We will assume for this run we set `--n_cos_bins 6` to match SK Night bins?
    # Day is Day.
    
    # Let's filter data for Day + 6 Night bins.
    if len(sk_data) != len(R_mod):
        # Mismatch in bin count. 
        # For this specific task, we'll try to use relevant data bins.
        # But if we can't match, we return error or high chi2.
        print(f"Warning: Bin count mismatch. Data: {len(sk_data)}, Model: {len(R_mod)}")
        return 9999.0, 0, 0.0, 1.0

    R_dat = np.array([d[1] for d in sk_data])
    Sig = np.array([d[2] for d in sk_data])
    
    # Minimize Chi2 w.r.t alpha:
    # Chi2 = Sum ( (D - a*M)^2 / S^2 )
    # dChi2/da = Sum ( 2(D - a*M) * (-M) / S^2 ) = 0
    # Sum ( (D*M - a*M^2) / S^2 ) = 0
    # Sum (D*M/S^2) = a * Sum (M^2/S^2)
    # a = Sum(D*M/S^2) / Sum(M^2/S^2)
    
    w = 1.0 / (Sig**2)
    num = np.sum(R_dat * R_mod * w)
    den = np.sum(R_mod**2 * w)
    alpha = num / den
    
    chi2 = np.sum(w * (R_dat - alpha * R_mod)**2)
    ndf = len(R_dat) - 1 # -1 for alpha
    
    # p-value
    from scipy import stats
    p_val = 1.0 - stats.chi2.cdf(chi2, ndf)
    if np.isnan(p_val): p_val = 0.0
    
    return chi2, ndf, p_val, alpha

def compute_ADN(day_rate: float, night_rate: float) -> ADNResult:
    # Super-K convention often reported as (D - N)/((D + N)/2)
    avg = 0.5 * (day_rate + night_rate)
    if avg == 0:
        return ADNResult(A_dn_SK=float("nan"), A_dn_alt=float("nan"), day_rate=day_rate, night_rate=night_rate)
    A_dn_SK = (day_rate - night_rate) / avg
    A_dn_alt = -A_dn_SK
    return ADNResult(A_dn_SK=A_dn_SK, A_dn_alt=A_dn_alt, day_rate=day_rate, night_rate=night_rate)


# ----------------------------
# CLI / main
# ----------------------------

def default_params_from_nufit52_with_skatm_NO(beta_solar: float, beta_earth: float, rho_c: float, rho_sun_core: float, Ye_sun_core: float) -> OscParams:
    """
    Defaults from NuFIT 5.2 (2022), with SK-atm, Normal Ordering best fit:
      sin^2 θ12 = 0.303
      sin^2 θ13 = 0.02225
      sin^2 θ23 = 0.451  (lower octant minimum; this is the global minimum in that table)
      δCP = 232°  (table gives 232 +36/-26)
      Δm21^2 = 7.41e-5 eV^2
      Δm3l^2 = +2.507e-3 eV^2
    Source: v52.tbl-parameters.pdf
    """
    sin2_th12 = 0.303
    sin2_th13 = 0.02225
    sin2_th23 = 0.451
    dcp_deg = 232.0
    dm21 = 7.41e-5
    dm31 = 2.507e-3

    th12 = math.asin(math.sqrt(sin2_th12))
    th13 = math.asin(math.sqrt(sin2_th13))
    th23 = math.asin(math.sqrt(sin2_th23))
    dcp = math.radians(dcp_deg)

    return OscParams(
        th12=th12, th13=th13, th23=th23, dcp=dcp,
        dm21=dm21, dm31=dm31,
        beta_solar=beta_solar, beta_earth=beta_earth,
        rho_c=rho_c,
        rho_sun_core=rho_sun_core, Ye_sun_core=Ye_sun_core,
    )


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(
        prog="sk_mavans_prem_pipeline",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    ap.add_argument("--bahcall_table", type=str, default="T_table.dat",
                    help="Path to Bahcall Momentsspectra T_table.dat")
    ap.add_argument("--try_download", action="store_true",
                    help="Try downloading T_table.dat if missing (requires internet in runtime environment).")

    ap.add_argument("--emin", type=float, default=5.0)
    ap.add_argument("--emax", type=float, default=15.0)

    ap.add_argument("--n_cos_bins", type=int, default=20,
                    help="Number of zenith bins in cosZ from -1 to 0 (night).")
    ap.add_argument("--ds_km", type=float, default=30.0,
                    help="Step length along chord (km). Smaller -> more accurate, slower.")

    ap.add_argument("--beta", type=float, default=None,
                    help="Global beta override (sets both solar and earth).")
    ap.add_argument("--beta_solar", type=float, default=0.0,
                    help="MaVaN beta for Sun.")
    ap.add_argument("--beta_earth", type=float, default=0.0,
                    help="MaVaN beta for Earth.")

    ap.add_argument("--rho_c", type=float, default=DEFAULT_RHO_C,
                    help="Reference density rho_c in g/cm^3 for log-running.")

    ap.add_argument("--rho_sun_core", type=float, default=150.0,
                    help="Effective solar core density (g/cm^3) for production MSW (adiabatic approx).")
    ap.add_argument("--Ye_sun_core", type=float, default=0.67,
                    help="Effective solar core Ye for production MSW (adiabatic approx).")

    # Optional manual override of oscillation params
    ap.add_argument("--sin2_th12", type=float, default=None)
    ap.add_argument("--sin2_th13", type=float, default=None)
    ap.add_argument("--sin2_th23", type=float, default=None)
    ap.add_argument("--dcp_deg", type=float, default=None)
    ap.add_argument("--dm21", type=float, default=None)
    ap.add_argument("--dm31", type=float, default=None)

    ap.add_argument("--plot", action="store_true", help="Make plots (requires matplotlib).")
    ap.add_argument("--out_prefix", type=str, default="out_mavans",
                    help="Prefix for output CSV/plots.")
    ap.add_argument("--dump_debug", action="store_true", help="Dump P_mass and Pee_day debug info.")

    ap.add_argument("--validate", action="store_true", help="Run Phase 4 validation against SK data.")
    ap.add_argument("--validate_energy", action="store_true", help="Run validation against SK Energy Spectrum.")
    ap.add_argument("--validate_low_e", action="store_true", help="Run Low-E Solar Neutrino consistency check.")
    ap.add_argument("--forecast", action="store_true", help="Run Hyper-K Forecasts.")

    ap.add_argument("--self_test", action="store_true",
                    help="Run quick numerical sanity checks (unitarity / hermiticity).")
    ap.add_argument("--check_solver", action="store_true",
                    help="Run solver cross-check (Work Package A2).")

    return ap.parse_args()


def try_download_file(url: str, dst_path: str) -> bool:
    try:
        import urllib.request
        urllib.request.urlretrieve(url, dst_path)
        return True
    except Exception:
        return False



def integrate_energy_bin(table: BahcallTable, fE: np.ndarray, E_min: float, E_max: float) -> float:
    """
    Integrate fE over [E_min, E_max] using the grid in table.
    """
    mask = (table.E_MeV >= E_min) & (table.E_MeV <= E_max)
    if not np.any(mask):
        return 0.0
    
    # Extract sub-arrays
    E_sub = table.E_MeV[mask]
    
    # Re-using the trapezoid logic from integrate_energy but for a slice
    y_sub = table.lam[mask] * fE[mask]
    return float(np.trapz(y_sub, E_sub))

def load_sk_energy_data(csv_path: str) -> Optional[List[Tuple[float, float, float, float]]]:
    """
    Load SK Energy Data from CSV.
    Format: E_min, E_max, A_DN_percent, Error_percent
    Returns list of (E_min, E_max, A_DN, Error).
    """
    if not os.path.exists(csv_path):
        return None
    data = []
    with open(csv_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("E_min"):
                continue
            parts = line.split(',')
            if len(parts) >= 4:
                try:
                    e_min = float(parts[0])
                    e_max = float(parts[1])
                    adn = float(parts[2])
                    err = float(parts[3])
                    data.append((e_min, e_max, adn, err))
                except ValueError:
                    continue
    return data

def compute_chi2_energy(
    res: ADNResult, 
    sk_data: List[Tuple[float, float, float, float]], 
    table: BahcallTable,
    day_rate_E: np.ndarray,
    night_rate_E: np.ndarray
) -> Tuple[float, int, List[float]]:
    """
    Compute Chi^2 for energy dependence.
    """
    chi2 = 0.0
    model_adn_values = []
    
    print("\n[Energy Spectrum Validation]")
    print(f"{'E_range (MeV)':<15} {'SK A_DN (%)':<15} {'Error (%)':<15} {'Model A_DN (%)':<15} {'Chi2 Contrib':<15}")
    print("-" * 80)

    for (e_min, e_max, sk_adn, sk_err) in sk_data:
        # Calculate Model A_DN for this bin
        day_bin = integrate_energy_bin(table, day_rate_E, e_min, e_max)
        night_bin = integrate_energy_bin(table, night_rate_E, e_min, e_max)
        
        if day_bin + night_bin > 0:
            avg_bin = 0.5 * (day_bin + night_bin)
            diff_bin = day_bin - night_bin
            model_adn = 100.0 * (diff_bin / avg_bin) 
        else:
            model_adn = 0.0
            
        model_adn_values.append(model_adn)
        
        # Chi2
        if sk_err > 0:
            delta = model_adn - sk_adn
            term = (delta / sk_err)**2
            chi2 += term
            print(f"{e_min:4.1f}-{e_max:4.1f}        {sk_adn:6.2f}          {sk_err:6.2f}          {model_adn:6.2f}          {term:6.2f}")
        else:
            print(f"{e_min:4.1f}-{e_max:4.1f}        {sk_adn:6.2f}          {sk_err:6.2f}          {model_adn:6.2f}          (no err)")

    print("-" * 80)
    print(f"Total Chi2_Energy: {chi2:.2f} / {len(sk_data)} dof")
    return chi2, len(sk_data), model_adn_values




def forecast_hyperk(table: BahcallTable, prem: PremModel, p: OscParams, day_rate: float) -> None:
    """
    Generate Hyper-Kamiokande Forecasts.
    Metrics:
    1. A_DN magnitude (Night - Day / Avg) approx.
    2. Core Enhancement Index: A_DN(Core) - A_DN(Mantle).
       Core region: cos(theta_z) > 0.84  (cosZ < -0.84)
       Mantle region: 0 < cos(theta_z) < 0.84 ( -0.84 < cosZ < 0)
    """
    print("\n=== HYPER-K FORECAST ===")
    
    # Define zones
    # Core: cosZ in [-1.0, -0.84]
    # Mantle: cosZ in [-0.84, 0.0]
    
    edges = np.array([-1.0, -0.84, 0.0])
    centers = 0.5 * (edges[:-1] + edges[1:])
    weights = np.diff(edges) 
    # Normalize weights so they represent fraction of night? 
    # Or keep as is -> compute_day_night_rates accumulates w*rate.
    # We only care about night_per_bin which is independent of weight.
    
    # Run
    # compute_day_night_rates(..., cosz_bins=centers, cosz_weights=weights, ...)
    _, _, _, _, night_per_bin = compute_day_night_rates(
        table, prem, p, centers, weights, ds_km=30.0
    )
    
    # night_per_bin contains the Rate evaluated at the center.
    # This represents the "Instantaneous Rate" at that Zenith angle.
    # To get the "Average Rate" over the bin, we assume the center value is representative.
    rate_core = night_per_bin[0]
    rate_mantle = night_per_bin[1]
    
    # Compare with Day Rate (Vacuum Rate)
    # Adn = (Day - Night) / Avg? 
    # We use Excess = (Night - Day) / Average
    # Usually A_DN is negative. Excess is positive.
    
    adn_core = 100.0 * (rate_core - day_rate) / (0.5*(rate_core + day_rate))
    adn_mantle = 100.0 * (rate_mantle - day_rate) / (0.5*(rate_mantle + day_rate)) 
    
    print(f"Day Rate (Ref): {day_rate:.4e}")
    print(f"Core   (cosZ ~ {centers[0]:.2f}): Rate={rate_core:.4e}, Excess={adn_core:+.3f}%")
    print(f"Mantle (cosZ ~ {centers[1]:.2f}): Rate={rate_mantle:.4e}, Excess={adn_mantle:+.3f}%")
    
    I_core = adn_core - adn_mantle
    print(f"Core Enhancement Index (I_core): {I_core:+.3f}%")
    print("--------------------------------")


def check_low_energy_consistency(p: OscParams) -> None:
    """
    Check Pee for low energy solar neutrinos (pp, Be7, pep) and CNO.
    Compare Standard MSW (beta=0) vs MaVaN.
    Reference Values (Borexino / Solar Standard Model approx):
      pp (0.267 MeV): Pee ~ 0.54 - 0.56
      Be7 (0.862 MeV): Pee ~ 0.51 - 0.53 (Transition region)
      pep (1.44 MeV): Pee ~ 0.50 (Vacuum-Matter transition)
    """
    print("\n[Low-E Solar Neutrino Partial Validation]")
    print(f"{'Source':<10} {'Energy (MeV)':<15} {'Pee (MaVaN)':<15} {'Pee (Std MSW)':<15} {'Diff (%)':<10}")
    print("-" * 70)
    
    # Characteristic energies
    sources = [
        ("pp", 0.267), # mean energy or peak? pp is continuous, peak ~0.26, max 0.42. 0.267 is typical for Pee eval.
        ("Be7", 0.384), # Branch 1 (10%)
        ("Be7", 0.862), # Branch 2 (90%)
        ("pep", 1.44),  # Line
        ("CNO", 1.0),   # Approx mean
        ("B8", 10.0),   # For comparison (High E)
    ]
    
    # Create a standard params object (beta=0) for comparison
    p_std = dataclasses.replace(p, beta_solar=0.0, beta_earth=0.0)
    # Ensure U matrix is re-inited if needed (but U depends on angles, which are same)
    # MaVaN affects Hamiltonian via dm_eff at production.
    
    for name, E in sources:
        # Calculate MaVaN Pee (averaged over production region approx? No, just @ core for check)
        # Using solar_mass_probs which computes P_mass at exit.
        # Then Pee = sum |Uei|^2 P_i (incoherent arrival at Earth).
        # Assuming no day/night effect for Low E (small anyway).
        
        # MaVaN
        pm_mavan = solar_mass_probs(E, p)
        pee_mavan = float(
            pm_mavan[0] * abs(p.U[0,0])**2 +
            pm_mavan[1] * abs(p.U[0,1])**2 +
            pm_mavan[2] * abs(p.U[0,2])**2
        )
        
        # Standard
        pm_std = solar_mass_probs(E, p_std)
        pee_std = float(
            pm_std[0] * abs(p.U[0,0])**2 +
            pm_std[1] * abs(p.U[0,1])**2 +
            pm_std[2] * abs(p.U[0,2])**2
        )
        
        diff_pct = 100.0 * (pee_mavan - pee_std) / pee_std
        print(f"{name:<10} {E:<15.3f} {pee_mavan:<15.4f} {pee_std:<15.4f} {diff_pct:<10.2f}")
    
    print("-" * 70)

def main() -> int:

    args = parse_args()

    # Ensure Bahcall table present
    if not os.path.exists(args.bahcall_table) and args.try_download:
        # Known stable landing page is a HTML; but the data file itself is usually accessible at:
        # https://www.sns.ias.edu/~jnb/SNdata/Export/Momentsspectra/T_table.dat
        url = "https://www.sns.ias.edu/~jnb/SNdata/Export/Momentsspectra/T_table.dat"
        ok = try_download_file(url, args.bahcall_table)
        if not ok:
            print("Download failed. Please download T_table.dat manually and retry.", file=sys.stderr)

    table = load_bahcall_T_table(args.bahcall_table).restrict(args.emin, args.emax)

    # Build PREM interpolation model
    r_tab, rho_tab = build_prem_interp(n_points=5000)
    prem = PremModel(r_km=r_tab, rho_gcm3=rho_tab)

    # Determine betas
    b_sol = args.beta_solar
    b_ear = args.beta_earth
    if args.beta is not None:
        b_sol = args.beta
        b_ear = args.beta

    # Default oscillation params from NuFIT 5.2 (NO, with SK-atm); override if provided
    p = default_params_from_nufit52_with_skatm_NO(
        beta_solar=b_sol,
        beta_earth=b_ear,
        rho_c=args.rho_c,
        rho_sun_core=args.rho_sun_core,
        Ye_sun_core=args.Ye_sun_core,
    )

    def override_if(x, default):
        return default if x is None else x

    # Apply overrides
    if args.sin2_th12 is not None:
        p.th12 = math.asin(math.sqrt(args.sin2_th12))
    if args.sin2_th13 is not None:
        p.th13 = math.asin(math.sqrt(args.sin2_th13))
    if args.sin2_th23 is not None:
        p.th23 = math.asin(math.sqrt(args.sin2_th23))
    if args.dcp_deg is not None:
        p.dcp = math.radians(args.dcp_deg)
    if args.dm21 is not None:
        p.dm21 = args.dm21
    if args.dm31 is not None:
        p.dm31 = args.dm31

    # Zenith bins in cosZ from -1 to 0 (night)
    cosz_edges = np.linspace(-1.0, 0.0, args.n_cos_bins + 1)
    cosz_bins = 0.5 * (cosz_edges[:-1] + cosz_edges[1:])

    # Default uniform weights (replace with SK exposure function if you have it)
    cosz_weights = np.ones_like(cosz_bins) / len(cosz_bins)

    # Compute rates
    cache_S: Dict[Tuple[float, float], np.ndarray] = {}
    day_rate, night_rate, day_rate_E, night_rate_E, night_rate_bins  = compute_day_night_rates(
        table=table,
        prem=prem,
        p=p,
        cosz_bins=cosz_bins,
        cosz_weights=cosz_weights,
        ds_km=args.ds_km,
        cache_S=cache_S
    )

    res = compute_ADN(day_rate, night_rate)
    
    # Energy Spectrum Validation
    if args.validate_energy:
        print(f"\n[Debug] Bahcall Table Energy Range: {table.E_MeV.min():.2f} - {table.E_MeV.max():.2f} MeV")
        try:
            sk_energy = load_sk_energy_data("sk_energy_data.csv")
            if sk_energy:
                print(f"[Debug] Loaded {len(sk_energy)} energy bins from sk_energy_data.csv")
                # Check bins against table range
                out_of_range = False
                for (em, ex, _, _) in sk_energy:
                    if ex > table.E_MeV.max() or em < table.E_MeV.min():
                        print(f"[Warning] Bin {em}-{ex} MeV is partially outside table limits!")
                        
                chi2_E, dof_E, vals_E = compute_chi2_energy(res, sk_energy, table, day_rate_E, night_rate_E)
                print(f"[Success] Energy validation complete.")
            else:
                print("Warning: sk_energy_data.csv not found or empty.")
        except Exception as e:
            print(f"Error during Energy Validation: {e}")
            import traceback
            traceback.print_exc()

    # Phase 4 Validation
    # Phase 4 Validation
    if args.validate:
        sk_data = load_sk_zenith_data("sk_zenith_data.csv")
        if sk_data:
            # Re-run simulation with correct bins for zenith validation if needed
            # SK bins: 1 Day + 6 Night.
            # Night bins are usually defined.
            # However, for now, let's assume the user wants check on current bins or we use standard 6 bins.
            # To do it properly:
            night_bins = np.linspace(0, 1, 7) # 6 bins
            res_val = compute_ADN(table, prem, p, n_cosz=None, custom_cosz=night_bins)
            
            # Unoscillated reference
            unosc_rate = compute_unoscillated_rate(table, table.sigma_nue)
            
            chi2, ndf, pval, alph = compute_chi2_zenith(res_val.day_rate, res_val.night_rate_per_bin, unosc_rate, sk_data)
            
            print(f"\n=== SK-IV VALIDATION (Zenith Shape) ===")
            print(f"Data Source: sk_zenith_data.csv ({len(sk_data)} bins)")
            print(f"Chi2 / ndf = {chi2:.2f} / {ndf} (p = {pval:.4f})")
            print(f"Norm factor (alpha) = {alph:.4f}")
            print(f"Sensitivity: {'PASS' if pval > 0.05 else 'FAIL (Shape Distortion)'}")
            
            # Save validation summary row
            val_out = f"validation_summary.csv"
            header_exists = os.path.exists(val_out)
            with open(val_out, 'a') as f:
                if not header_exists:
                    f.write("beta_solar,beta_earth,chi2,ndf,p_value,alpha,ADN_pct\n")
                f.write(f"{res_val.p.beta_solar},{res_val.p.beta_earth},{chi2:.4f},{ndf},{pval:.4e},{alph:.4f},{res_val.A_dn_SK*100:.4f}\n")
        else:
            print("Warning: sk_zenith_data.csv not found. Skipping validation.")
    

    
    # Calculate R(beta) metric
    # R = dm2_eff(rho_sun) / dm2_eff(rho_c)
    # Note: KamLAND sees rho ~ rho_c if rho_c=3 approx.
    dm2_sun = dm_eff(p.dm21, p.rho_sun_core, p.beta_solar, p.rho_c)
    dm2_kl  = dm_eff(p.dm21, p.rho_c, p.beta_earth, p.rho_c) # At rho_c, ln term is 0 regardless of beta if rho=rho_c
    # But if KamLAND avg density != rho_c, we should use that. For now assume rho_c is KL standard.
    R_beta = dm2_sun / dm2_kl if dm2_kl != 0 else 0

    print("=== CONFIG ===")
    print(f"E range: {args.emin:.2f}–{args.emax:.2f} MeV   (nE={len(table.E_MeV)})")
    print(f"cosZ bins: {args.n_cos_bins} in [-1,0], ds={args.ds_km:.1f} km")
    print(f"beta_solar={p.beta_solar:.6g}, beta_earth={p.beta_earth:.6g}")
    print(f"rho_c={p.rho_c:g} g/cm^3")
    print(f"R(beta) [Sun/KL] = {R_beta:.4f}")
    print(f"NuFIT-like params (rad): th12={p.th12:.6f}, th13={p.th13:.6f}, th23={p.th23:.6f}, dcp={p.dcp:.6f}")
    print(f"Δm21={p.dm21:.6g} eV^2, Δm31={p.dm31:.6g} eV^2")
    print(f"Solar core: rho={p.rho_sun_core:g} g/cm^3, Ye={p.Ye_sun_core:g}")

    print("\\n=== RESULTS ===")
    print(f"Day rate  (arb): {res.day_rate:.6e}")
    print(f"Night rate(arb): {res.night_rate:.6e}")
    print(f"A_DN (SK conv)   = (D-N)/avg = {res.A_dn_SK*100:+.3f}%")
    print(f"A_DN (alt conv)  = (N-D)/avg = {res.A_dn_alt*100:+.3f}%")

    if args.dump_debug:
        # Save P_mass debug
        # We need to re-compute P_mass for all E
        Pmass_debug = np.array([solar_mass_probs(E, p) for E in table.E_MeV], dtype=float)
        
        # Re-compute Pee_day for check
        U = p.U
        Pee_debug = (
            Pmass_debug[:,0] * (abs(U[0,0])**2) +
            Pmass_debug[:,1] * (abs(U[0,1])**2) +
            Pmass_debug[:,2] * (abs(U[0,2])**2)
        )
        
        debug_arr = np.column_stack([table.E_MeV, Pmass_debug, Pee_debug])
        np.savetxt(f"{args.out_prefix}_debug_Pmass.csv", debug_arr, delimiter=",", 
                   header="E_MeV,P1,P2,P3,Pee_day")
        print(f"Saved debug info: {args.out_prefix}_debug_Pmass.csv")

    # Solver Check (WP A2)
    if args.check_solver:
        run_solver_cross_check(args, prem, p)
        return 0

    # Save CSV outputs
    outE = np.column_stack([
        table.E_MeV,
        table.lam,
        day_rate_E,
        night_rate_E,
        (day_rate_E - night_rate_E) / (0.5 * (day_rate_E + night_rate_E)),
        (night_rate_E - day_rate_E) / (0.5 * (day_rate_E + night_rate_E)),
    ])
    out_csv = f"{args.out_prefix}_ADN_vs_E.csv"
    header = "E_MeV,lambda,rate_day_E,rate_night_E,ADN_SK(D-N)/avg,ADN_alt(N-D)/avg"
    np.savetxt(out_csv, outE, delimiter=",", header=header, comments="")
    print(f"\\nSaved: {out_csv}")
    
    # Save zenith bin outputs
    # Format: cosZ_center, night_rate_bin, day_rate_avg, A_DN_bin
    # day_rate_avg is just day_rate (scaled to per-bin if needed? No, rates are total).
    # Wait, A_DN per bin: (Day - NightBin) / Avg? Or (Day - NightBin) / Day?
    # Usually SK plots: (Night_i - Day)/Day_avg.
    # We will output raw rates so user can compute whatever.
    # Note: night_rate_bins contains the weighted sum contribution.
    # But for "per bin rate", we usually want the rate in that bin *multiplied by number of bins* or similar normalization
    # so that average matches total?
    # Actually, let's just save the raw computed value for that bin.
    # Our `night_rate_per_bin` is integrated over E.
    # But wait, in compute_DN, we did: `night_rate_E_accum += wcz * night_rate_E_bin`.
    # And `night_rate_per_bin` stored `rate_bin_tot`. `rate_bin_tot` is Integral(night_rate_E_bin).
    # It does NOT include wcz.
    # So the physics rate for that zenith angular bin is `rate_bin_tot`.
    
    outZ = np.column_stack([
         cosz_bins,
         night_rate_bins,
         np.full_like(cosz_bins, day_rate), # Day rate is constant
         (day_rate - night_rate_bins) / (0.5 * (day_rate + night_rate_bins)) # Local asymmetry
    ])
    out_z_csv = f"{args.out_prefix}_ADN_vs_cosZ.csv"
    np.savetxt(out_z_csv, outZ, delimiter=",", header="cosZ,rate_night,rate_day,ADN_local_SK", comments="")
    print(f"Saved: {out_z_csv}")

    # Optional plots
    if args.plot:
        try:
            import matplotlib.pyplot as plt
            plt.figure()
            plt.plot(table.E_MeV, 100.0 * (day_rate_E - night_rate_E) / (0.5 * (day_rate_E + night_rate_E)))
            plt.xlabel("Eν [MeV]")
            plt.ylabel("A_DN (SK conv) [%]")
            plt.title("Super-K Day/Night Asymmetry vs Energy")
            plt.grid(True, alpha=0.3)
            # png1 = f"{args.out_prefix}_ADN_vs_E.png"
            # plt.savefig(png1, dpi=160)
            # print(f"Saved: {png1}")
        except Exception as e:
            print(f"Plotting failed: {e}", file=sys.stderr)

    # Quick sanity checks
    if args.self_test:
        # Check hermiticity at representative point
        Ht = H_flavor_eV(10.0, 5.0, 0.495, p, beta=p.beta_earth)
        herm = np.max(np.abs(Ht - Ht.conj().T))
        print(f"\\n[SELF_TEST] max|H-H†| = {herm:.3e}")

        # Check (approx) unitarity of an evolution operator
        S = earth_evolution_operator(10.0, -1.0, prem, p, ds_km=args.ds_km)
        unit = np.max(np.abs(S.conj().T @ S - np.eye(3)))
        print(f"[SELF_TEST] max|S†S-I| = {unit:.3e}")


    # Low-E Validation
    if args.validate_low_e:
        check_low_energy_consistency(p)
    
    # Hyper-K Forecast
    if args.forecast:
       forecast_hyperk(table, prem, p, res.day_rate)

    return 0



if __name__ == "__main__":
    raise SystemExit(main())
