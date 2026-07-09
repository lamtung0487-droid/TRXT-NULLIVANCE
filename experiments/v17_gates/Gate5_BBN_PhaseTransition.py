"""
TRXT Gate 5 (V9 Upgrade): Phase Transition BBN
==============================================
Implements the "Perfect Disguise" mechanism where the superfluid
energy density turns OFF at high temperatures (T > Tc) via a 
smooth tanh phase transition switch.

Model:
  rho_sf(T) = rho_track(T) * 0.5 * [1 - tanh((T - Tc)/dT)]
  
This ensures the superfluid is absent during BBN (T ~ 1 MeV)
but recovers its full density at late times (T << Tc ~ 1 eV).
"""
import sys, os
import numpy as np

# Setup: Point to PRyMordial directory
# Adjust this path to match your environment
PRYM_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                        "../../paper/v7_release/source_code/bbn_prymordial/PRyMordial"))
if os.path.exists(PRYM_DIR):
    os.chdir(PRYM_DIR)
    sys.path.insert(0, PRYM_DIR)
else:
    print(f"WARNING: PRyMordial not found at {PRYM_DIR}")

# Configure PRyMordial
PRYM_AVAILABLE = False
try:
    import PRyM.PRyM_init as PRyMini
    PRyMini.working_dir = PRYM_DIR
    PRYM_AVAILABLE = True
except ImportError:
    print("PRyMordial module not found. Run this script from a valid environment.")

def make_trxt_phase_transition(f_BBN, w_sf=0.25, Tc_MeV=1e-6, dT_MeV=1e-7):
    """
    Creates rho_NP functions with a PHASE TRANSITION SWITCH.
    
    Parameters:
    -----------
    f_BBN : fraction of rho_rad at T_anchor (low T)
    Tc_MeV : Critical temperature (e.g. 1 eV = 1e-6 MeV)
    dT_MeV : Width of transition
    """
    # 1. Define Anchor at Low T (Late Universe)
    T_anchor = 1e-9 # 1 meV (CMB scale)
    g_star_anchor = 3.36 # Late time g*
    rho_rad_anchor = (np.pi**2 / 30.0) * g_star_anchor * T_anchor**4
    rho_sf_anchor = f_BBN * rho_rad_anchor
    
    # Scaling power law (Tracking behavior)
    n = 3.0 * (1.0 + w_sf)
    
    def switch(T):
        """
        Tanh Switch:
        - If T >> Tc: tanh -> 1  => switch -> 0 (OFF)
        - If T << Tc: tanh -> -1 => switch -> 1 (ON)
        """
        x = (T - Tc_MeV) / dT_MeV
        # Numerical safety for exp
        if x > 50: return 0.0
        if x < -50: return 1.0
        return 0.5 * (1.0 - np.tanh(x))
    
    def d_switch_dT(T):
        x = (T - Tc_MeV) / dT_MeV
        if abs(x) > 50: return 0.0
        # d/dT [0.5(1 - tanh(x))] = -0.5 * sech^2(x) * dx/dT
        sech2 = 1.0 / np.cosh(x)**2
        return -0.5 * sech2 * (1.0 / dT_MeV)

    def rho_NP(T_MeV):
        if T_MeV <= 0: return 0.0
        # Tracking Profile
        rho_track = rho_sf_anchor * (T_MeV / T_anchor)**n
        # Modulated by Switch
        return rho_track * switch(T_MeV)
    
    def p_NP(T_MeV):
        # Pressure follows density with EOS w
        return w_sf * rho_NP(T_MeV)
    
    def drho_NP_dT(T_MeV):
        if T_MeV <= 0: return 0.0
        # Product Rule: d(rho*S)/dT = rho'*S + rho*S'
        rho_track = rho_sf_anchor * (T_MeV / T_anchor)**n
        d_rho_track = n * rho_track / T_MeV
        
        S = switch(T_MeV)
        dS = d_switch_dT(T_MeV)
        
        return d_rho_track * S + rho_track * dS
        
    # No Coupling to SM
    def delta_rho_NP(Tg, Tnue, Tnumu, T_NP):
        return 0.0
        
    return rho_NP, p_NP, drho_NP_dT, delta_rho_NP

def run_v9_check():
    """Execute the Phase Transition BBN Check.

    Gate-integrity rule (lab, 2026-07-09): a gate may only report PASS/FAIL
    from an actual computation. Without PRyMordial there is nothing to
    compute, so the gate reports NOT RUN — never a hardcoded pass.
    """
    print("--- GATE 5 (V9): PHASE TRANSITION CHECK ---")
    print("Model: Superfluid Turns OFF at T > 1 eV")

    if not PRYM_AVAILABLE:
        print("  PRyMordial engine unavailable in this environment.")
        print("  The theoretical argument (rho_sf -> 0 at T_BBN) is NOT a substitute")
        print("  for the nuclear-network computation (see report App. AJ.3 for the")
        print("  WSL2 run that established f_BBN < 0.61%).")
        print(">>> GATE 5 STATUS: NOT RUN (PRyMordial unavailable - install per validation/MANUAL_DOWNLOAD_INSTRUCTIONS.md) <<<")
        return 2

    # Real computation path: SM baseline vs TRXT with the tanh switch.
    import PRyM.PRyM_main as PRyMmain
    print("Running SM Baseline...")
    sm = PRyMmain.PRyMclass()
    Yp_sm = sm.YPBBN()
    print(f"  Yp (SM) = {Yp_sm:.5f},  Neff = {sm.Neff():.3f},  D/H = {sm.DoH():.3e}")

    print("Running TRXT (Tc=1eV, f_BBN=0.5%)...")
    rho_NP, p_NP, drho_NP_dT, delta_rho_NP = make_trxt_phase_transition(f_BBN=0.005)
    PRyMini.NP_e_flag = True
    trxt = PRyMmain.PRyMclass(rho_NP, p_NP, drho_NP_dT, delta_rho_NP)
    Yp_trxt = trxt.YPBBN()
    dev = abs(Yp_trxt - Yp_sm) / Yp_sm
    print(f"  Yp (TRXT) = {Yp_trxt:.5f}  (deviation {dev*100:.3f}%)")
    # Pre-declared criterion: |dYp/Yp| < 0.4% (2-sigma observational band)
    if dev < 0.004:
        print(">>> GATE 5 STATUS: PASS (computed, criterion |dYp/Yp| < 0.4%) <<<")
        return 0
    print(">>> GATE 5 STATUS: FAIL (superfluid injection distorts Yp) <<<")
    return 1

if __name__ == "__main__":
    sys.exit(run_v9_check())
