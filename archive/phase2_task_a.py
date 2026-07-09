import os
import urllib.request
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from TRXT_Analysis_Engine import TRXTAnalyzer

# --- CONFIGURATION ---
DATA_URL = "http://opendata.cern.ch/record/545/files/Dimuon_DoubleMu.csv"
LOCAL_FILE = "cms_dimuon.csv"
MASS_MIN = 40.0
MASS_MAX = 60.0
BINS = 40  # 0.5 GeV per bin width

def fetch_data():
    if not os.path.exists(LOCAL_FILE):
        print(f"[DATA] Downloading CMS Dimuon data from {DATA_URL}...")
        try:
            urllib.request.urlretrieve(DATA_URL, LOCAL_FILE)
            print("[DATA] Download complete.")
        except Exception as e:
            print(f"[ERROR] Failed to download data: {e}")
            return None
    else:
        print(f"[DATA] Found local file: {LOCAL_FILE}")
    
    return LOCAL_FILE

def load_and_filter(filepath):
    print("[DATA] Loading and filtering data (V14.1 Compliance Checks used)...")
    try:
        df = pd.read_csv(filepath)
        print(f" -> Total events: {len(df)}")
        
        # Check for required columns for cuts
        required = ['M', 'pt1', 'pt2', 'eta1', 'eta2']
        if not all(col in df.columns for col in required):
            print(f"[WARNING] Columns {required} not all found. Available: {df.columns.tolist()}")
            if 'M' in df.columns:
                 print(" -> Falling back to Mass-only cut (Degraded mode).")
                 df_filtered = df[(df['M'] >= MASS_MIN) & (df['M'] <= MASS_MAX)]
                 return df_filtered['M'].values
            return None

        # Apply Proper Cuts (Phase 2.2 strict)
        # 1. pT > 15 GeV for both muons
        if 'pt1' in df.columns and 'pt2' in df.columns:
            cut_pt = (df['pt1'] > 15.0) & (df['pt2'] > 15.0)
        else:
            print("[WARNING] pT columns missing! Cannot apply crucial pT>15 cut. Result irrelevant.")
            return None

        # 2. |eta| < 2.4 (CMS acceptance)
        if 'eta1' in df.columns and 'eta2' in df.columns:
            cut_eta = (df['eta1'].abs() < 2.4) & (df['eta2'].abs() < 2.4)
        else:
             cut_eta = True # Safe fallback if eta missing, but pT is mandatory
             
        # 3. Mass Window
        cut_mass = (df['M'] >= MASS_MIN) & (df['M'] <= MASS_MAX)
        
        df_filtered = df[cut_pt & cut_eta & cut_mass]
        print(f" -> Events after Strict Cuts (pT>15, |eta|<2.4): {len(df_filtered)}")
        
        return df_filtered['M'].values
    except Exception as e:
        print(f"[ERROR] Reading CSV failed: {e}")
        return None

def main():
    print("=== TRXT PROTOCOL: TASK A (GHOST HUNTER) ===")
    
    # 1. Initialize Engine
    engine = TRXTAnalyzer()
    
    # 2. Get Data
    filepath = fetch_data()
    if not filepath:
        return
        
    masses = load_and_filter(filepath)
    if masses is None or len(masses) == 0:
        print("[ERROR] No data to analyze.")
        return

    # 3. Binning (Histogramming)
    print(f"[ANALYSIS] Histogramming data into {BINS} bins...")
    if len(masses) < 1000:
        print(f"[WARNING] Low statistic count ({len(masses)}). Results may be unstable.")

    counts, bin_edges = np.histogram(masses, bins=BINS, range=(MASS_MIN, MASS_MAX))
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    
    # 4. Run TRXT Analysis (V14.1 Rigorous Test)
    # Target 45.66 GeV
    target = engine.predict_mass(16, 16)
    result = engine.perform_statistical_test(bin_centers, counts, target_mass=target)
    
    if result:
        x = result["mass"]
        y_data = result["data"]
        y_h0 = result["fit_h0"]
        y_h1 = result["fit_h1"]
        sig_sigma = result["significance"]
        
        # 5. Specialized Plotting (Upper: Fit, Lower: Residuals)
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), gridspec_kw={'height_ratios': [3, 1]}, sharex=True)
        
        # Top Panel
        ax1.errorbar(x, y_data, yerr=np.sqrt(y_data), fmt='ko', label='CMS Open Data (Dimuon)', alpha=0.7)
        ax1.plot(x, y_h0, 'b--', linewidth=2, label='H0: Null Background')
        ax1.plot(x, y_h1, 'r-', linewidth=2, label=f'H1: Signal+BG (Sig={sig_sigma:.1f}$\sigma$)')
        
        ax1.set_title(f"TRXT Validation: Task A - Ghost Hunter (Target {target:.2f} GeV)")
        ax1.set_ylabel(f"Events / {(MASS_MAX-MASS_MIN)/BINS:.1f} GeV")
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Bottom Panel: Pulls/Residuals (Data - H0) / Error
        residuals = (y_data - y_h0) / np.sqrt(y_data)
        ax2.bar(x, residuals, width=(MASS_MAX-MASS_MIN)/BINS, color='gray', alpha=0.5, label='Pull (Data-H0)')
        ax2.axhline(0, color='k', linestyle='-')
        ax2.axhline(2, color='r', linestyle='--', alpha=0.5)
        ax2.axhline(-2, color='r', linestyle='--', alpha=0.5)
        ax2.set_xlabel("Invariant Mass $M_{\mu\mu}$ [GeV]")
        ax2.set_ylabel("Pull ($\sigma$)")
        ax2.set_ylim(-4, 4)
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        output_plot = "trxt_task_a_result_v14_1.png"
        plt.tight_layout()
        plt.savefig(output_plot)
        print(f"[OUTPUT] Validation plot saved to: {output_plot}")

if __name__ == "__main__":
    main()
