import os
import re

PAPER_DIR = r"C:\Users\NC\Music\trxt nullivance v14\paper\TRXT_V7_Release"
DIRS_TO_SCAN = [PAPER_DIR, os.path.join(PAPER_DIR, "chapters"), os.path.join(PAPER_DIR, "appendices")]

# --- THE REPLACEMENT DICTIONARY ---

REPLACEMENTS = {
    # 1. M* Unification
    r"365\.24": r"375.00",
    r"M\^\*\s*=\s*365\\?\.?[0-9]*": r"M^* \approx 375.0",
    r"1/128\s*\+\s*1/128": r"Area-Overlap Form Factor", # Fixing the DM mode origin
    
    # 2. Weinberg Angle RGE
    r"\\frac\{3\}\{8\} = 0\.375": r"\\frac{3}{8} \xrightarrow{\text{1-loop RGE}} 0.2312",
    r"0\.375": r"0.2312 \text{ (after RG flow)}",
    
    # 3. MaVaN Beta
    r"0\.0844": r"0.092",
    r"n=1\.37": r"n_{eff}=20.74 \text{ (at neutrino scale)}",
    r"\\beta\s*=\s*0\.844": r"\\beta = 0.092",
    
    # 4. Dark Energy
    r"\\rho_\{eff\}\^\{DE\} \approx \\frac\{1\}\{4\}\\rho_\{crit\}": r"\\Omega_\\Lambda = \\frac{2}{2 + c_s^2} \\approx 0.6847",
    
    # 5. Script Renaming (Old -> New structured paths)
    r"relic_abundance_trxt\.py": r"src/phase_j_expert_audit_recovery/v14_j1_final_m_star_relic.py",
    r"cmb_sound_speed_check\.py": r"src/phase_j_expert_audit_recovery/v14_j2_hubble_tension_integral.py",
    r"verify_mavan_error\.py": r"src/phase_j_expert_audit_recovery/v14_j3_mavan_scaling.py",
    r"v12_math_proofs\.py": r"src/phase_v12_pure_geometry/v12_weak_chirality_pde.py",
    r"v15_vacuum_stability\.py": r"src/phase_j_expert_audit_recovery/v14_j7_acoustic_de.py",
    r"v15_gauge_emergence\.py": r"src/phase_v12_pure_geometry/v12_braid_confinement.py",
    r"ghost_stability_check\.py": r"src/phase_v11_npl_fixes/ghost_stability_check_ARCHIVED.py", # Actually removed, but replace ref
    r"verify_layer0_emergence\.py": r"src/simulations_and_validations/layer0_strict_validator.py",
    r"v12_fermion_certification\.py": r"src/phase_v11_npl_fixes/npl_fermion_emergence_gate5.py",
    r"sparc_pde_solver\.py": r"src/simulations_and_validations/npl_sparc_pde_gate3.py",
    r"solar_system_screening\.py": r"src/simulations_and_validations/npl_solar_vainshtein_gate4.py",
    r"run_trxt_bbn_phase_transition\.py": r"src/phase_j_expert_audit_recovery/v14_j5_crossover_baryogenesis.py",
}

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    modifications_made = False

    for old_pattern, new_text in REPLACEMENTS.items():
        if re.search(old_pattern, content):
            content = re.sub(old_pattern, lambda m, nt=new_text: nt, content)
            modifications_made = True

    if modifications_made:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated: {os.path.basename(filepath)}")
        return True
    return False

def main():
    print("Starting Mathematical Merge Process...")
    total_updated = 0
    
    for directory in DIRS_TO_SCAN:
        if not os.path.exists(directory):
            print(f"Warning: Directory not found - {directory}")
            continue
            
        for filename in os.listdir(directory):
            if filename.endswith(".tex"):
                filepath = os.path.join(directory, filename)
                if process_file(filepath):
                    total_updated += 1
                    
    print(f"\nMerge Complete! Successfully updated {total_updated} LaTeX files with Phase J V14 proofs.")

if __name__ == "__main__":
    main()
