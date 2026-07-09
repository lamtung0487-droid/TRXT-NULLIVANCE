import numpy as np
from TRXT_Analysis_Engine import TRXTAnalyzer

def main():
    print("=== TRXT PROTOCOL: V16 TASK 1 (VACUUM SHEAR) - SCIENCE GRADE ===")
    engine = TRXTAnalyzer()
    
    # ===== DUAL TRACK ANALYSIS =====
    # Track 1: CDF II Only (Controversial)
    MW_CDF = 80.433  # GeV (CDF II 2022)
    
    # Track 2: PDG Global Average (Excluding CDF)
    MW_PDG = 80.3692  # GeV (PDG 2024, CDF excluded)
    MW_PDG_ERR = 0.0133
    
    # Standard Model Prediction
    MW_SM = 80.357  # GeV
    
    print("[DATA SOURCES]")
    print(f"  MW (SM Prediction): {MW_SM} GeV")
    print(f"  MW (CDF II 2022): {MW_CDF} GeV [CONTROVERSIAL: 7sigma from world average]")
    print(f"  MW (PDG Global, CDF excluded): {MW_PDG} +/- {MW_PDG_ERR} GeV")
    
    print("\n===== TRACK 1: FIT TO CDF II =====")
    rho_cdf, delta_rho_cdf = engine.calculate_vacuum_shear(MW_SM, MW_CDF)
    print(f"  Required rho: {rho_cdf:.6f}")
    print(f"  Delta_rho: {delta_rho_cdf:.6f} ({delta_rho_cdf*100:.4f}%)")
    print(f"  Mass Shift: +{(MW_CDF - MW_SM)*1000:.1f} MeV")
    
    print("\n===== TRACK 2: FIT TO PDG GLOBAL AVERAGE =====")
    rho_pdg, delta_rho_pdg = engine.calculate_vacuum_shear(MW_SM, MW_PDG)
    print(f"  Required rho: {rho_pdg:.6f}")
    print(f"  Delta_rho: {delta_rho_pdg:.6f} ({delta_rho_pdg*100:.4f}%)")
    print(f"  Mass Shift: +{(MW_PDG - MW_SM)*1000:.1f} MeV")
    
    # Geometric Factor Check
    X_VAL = engine.X_FACTOR
    INV_X = 1.0 / X_VAL
    
    print("\n[GEOMETRY CORRELATION CHECK]")
    print(f"  TRXT 1/X: {INV_X:.6f}")
    print(f"  CDF Delta/X: {delta_rho_cdf / INV_X:.3f}")
    print(f"  PDG Delta/X: {delta_rho_pdg / INV_X:.3f}")
    
    print("\n[CONCLUSION]")
    if abs(delta_rho_pdg) < 0.0005:
        print("  PDG Track: Very small shift. Consistent with SM (no shear needed).")
    else:
        print("  PDG Track: Small positive shift. May indicate minor shear effect.")
        
    print("  CDF Track: Large shift ONLY if CDF is correct. Tension with all other experiments.")
    print("\n  STATUS: 'Consistent-with-CDF, TENSION-with-global-average'")
    print("  VERDICT: NOT VALIDATED (awaiting resolution of CDF anomaly)")

if __name__ == "__main__":
    main()
