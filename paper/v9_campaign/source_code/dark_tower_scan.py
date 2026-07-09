#!/usr/bin/env python3
import numpy as np

M_star = 365.24 # GeV

print("DARK TOWER MODE SELECTION SCAN (Task B4)")
print("========================================")
print(f"Master Scale M* = {M_star} GeV")
print("We seek (p,q) pairs that yield a mass m_chi = M*(1/p + 1/q) ~ 5-10 GeV\n")

target_m = 5.778 # GeV
tol = 0.5 # GeV

valid_modes = []

for p in range(1, 1000):
    for q in range(p, 1000): # q >= p to avoid duplicates
        m_chi = M_star * (1.0/p + 1.0/q)
        if abs(m_chi - target_m) < tol:
            valid_modes.append((p, q, m_chi))

# Sort by mass
valid_modes.sort(key=lambda x: x[0])

print(f"Found {len(valid_modes)} unique (p,q) pairs yielding mass within {tol} GeV of {target_m} GeV.\n")

print(f"{'p':<6} {'q':<6} {'m_chi (GeV)':<10}")
print("-" * 25)
for p, q, m in valid_modes[:5]:
    print(f"{p:<6} {q:<6} {m:<10.3f}")
print("...")
if (17, 500, 5.778) not in [(x[0], x[1], round(x[2],3)) for x in valid_modes]:
    m_17_500 = M_star * (1/17 + 1/500)
    print(f"\nTarget mode: p=17, q=500 -> m_chi = {m_17_500:.3f} GeV")
