
import numpy as np
import os

def calc_error_budget():
    """
    Calculate Error Budget for TRXT Model predictions.
    Propagates uncertainties from fundamental constants to M*.
    """
    print("Calculating V5 Error Budget...")
    
    # 1. Inputs (CODATA 2018 / PDG 2024)
    alpha_inv = 137.035999084
    d_alpha_inv = 0.000000021
    
    m_tau = 1776.86 # MeV
    d_m_tau = 0.12  # MeV
    
    G = 6.67430e-11
    d_G = 0.00015e-11
    
    # 2. Derived M* (Constituent Mass)
    # Formula: M* = m_tau * (3 / 2 * alpha_inv)?? 
    # Wait, Reference says: m_tau = (2 alpha / 3) M*  => M* = m_tau * 3 / (2 alpha) = m_tau * 1.5 * alpha_inv
    factor = 1.5 * alpha_inv
    
    M_star_MeV = m_tau * factor
    
    # Error Propagation (Quadrature)
    # y = a * x  => dy/y = dx/x
    # z = x * y  => (dz/z)^2 = (dx/x)^2 + (dy/y)^2
    
    rel_mtau = d_m_tau / m_tau
    rel_alpha = d_alpha_inv / alpha_inv # alpha_inv has error, alpha has same rel error
    
    rel_M_star = np.sqrt(rel_mtau**2 + rel_alpha**2)
    
    d_M_star_MeV = M_star_MeV * rel_M_star
    
    # Convert to GeV
    M_star_GeV = M_star_MeV / 1000.0
    d_M_star_GeV = d_M_star_MeV / 1000.0
    
    # 3. Output Table
    lines = []
    lines.append("# 📉 V5 Error Budget Analysis")
    lines.append(f"**Date:** {np.datetime64('today')}")
    lines.append("")
    lines.append("## 1. Input Uncertainties (PDG 2024)")
    lines.append("| Parameter | Value | Uncertainty (1σ) | Relative Error |")
    lines.append("|---|---|---|---|")
    lines.append(f"| $\\alpha^{{-1}}$ | {alpha_inv:.9f} | {d_alpha_inv:.9f} | {rel_alpha:.2e} |")
    lines.append(f"| $m_\\tau$ | {m_tau:.2f} MeV | {d_m_tau:.2f} MeV | {rel_mtau:.2e} |")
    lines.append(f"| $G$ | {G:.2e} | {d_G:.2e} | {d_G/G:.2e} |")
    lines.append("")
    lines.append("## 2. Propagated Prediction ($M^*$)")
    lines.append("Formula: $M^* = m_\\tau \\cdot \\frac{3}{2\\alpha}$")
    lines.append("")
    lines.append("| Quantity | Prediction | Propagated Error | Confidence |")
    lines.append("|---|---|---|---|")
    lines.append(f"| **$M^*$** | **{M_star_GeV:.4f} GeV** | **± {d_M_star_GeV:.4f} GeV** | **{rel_M_star*100:.4f}%** |")
    lines.append("")
    lines.append("## 3. Conclusion")
    lines.append(f"- The uncertainty in $M^*$ is dominated by the **Tau mass measurement** ({rel_mtau:.2e} vs {rel_alpha:.2e}).")
    lines.append("- Theoretical precision is currently limited by experimental inputs, not model intrinsics.")
    
    content = "\n".join(lines)
    
    with open("error_budget.md", "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"Propagated M* = {M_star_GeV:.4f} +/- {d_M_star_GeV:.4f} GeV")
    print("Report saved to error_budget.md")

if __name__ == "__main__":
    calc_error_budget()
