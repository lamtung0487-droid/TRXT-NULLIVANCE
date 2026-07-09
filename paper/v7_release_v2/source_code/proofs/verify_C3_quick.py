"""Quick C3 verification — check the Test 3 anomaly and recompute p-values."""
import numpy as np

M_STAR = 365.24
M_W = 80.3692; M_Z = 91.1876; M_H = 125.20

def find_q(p, m_obs, m_star):
    denom = p * m_obs - m_star
    if denom <= 0: return None
    q = round(p * m_star / denom)
    return q if q >= 1 else None

def mass(p, q, m_star): return m_star * (1/p + 1/q)

rng = np.random.default_rng(42)
n = 50000
ms = rng.uniform(50, 1000, n)

# ====== Unconstrained test ======
thresholds = [0.01, 0.005, 0.002, 0.001, 0.0005]
worst_devs = []

for m_star in ms:
    worst = 0
    for m_obs in [M_W, M_Z, M_H]:
        best_dev = float('inf')
        for p in range(1, 21):
            q = find_q(p, m_obs, m_star)
            if q is None or q < 1 or q > 200: continue
            m_pred = mass(p, q, m_star)
            dev = abs(m_pred - m_obs) / m_obs
            best_dev = min(best_dev, dev)
        if best_dev == float('inf'):
            worst = float('inf')
            break
        worst = max(worst, best_dev)
    worst_devs.append(worst)

print('=== C3 Test 3 Recheck (Unconstrained, n=50000) ===')
for t in thresholds:
    count = sum(1 for w in worst_devs if w < t)
    print(f'  Within {t*100:.2f}%: {count}/{n} = {count/n:.4f}')

# TRXT actual deviation
worst_trxt = 0
for name, p, q, m_obs in [('W',5,50,M_W),('Z',8,8,M_Z),('H',5,7,M_H)]:
    m_pred = mass(p, q, M_STAR)
    dev = abs(m_pred - m_obs) / m_obs
    worst_trxt = max(worst_trxt, dev)
    print(f'  {name}: pred={m_pred:.4f} obs={m_obs:.4f} dev={dev*100:.4f}%')

n_better = sum(1 for w in worst_devs if w < worst_trxt)
print(f'\n  TRXT worst deviation: {worst_trxt*100:.4f}%')
print(f'  p-value (unconstrained): {n_better/n:.4f}')

# ====== Constrained test (fixed sectors) ======
print('\n=== C3 Test 4 Recheck (Constrained p=5,8,5, n=50000) ===')
worst_devs_c = []
for m_star in ms:
    worst = 0
    valid = True
    for p, m_obs in [(5, M_W), (8, M_Z), (5, M_H)]:
        q = find_q(p, m_obs, m_star)
        if q is None or q < 1:
            valid = False; break
        m_pred = mass(p, q, m_star)
        dev = abs(m_pred - m_obs) / m_obs
        worst = max(worst, dev)
    worst_devs_c.append(worst if valid else float('inf'))

for t in thresholds:
    count = sum(1 for w in worst_devs_c if w < t)
    print(f'  Within {t*100:.2f}%: {count}/{n} = {count/n:.6f}')

n_better_c = sum(1 for w in worst_devs_c if w < worst_trxt)
print(f'\n  p-value (constrained): {n_better_c/n:.6f}')
from scipy.stats import norm
if n_better_c > 0:
    print(f'  Equivalent sigma: {norm.ppf(1-n_better_c/n):.2f}')
else:
    print(f'  Equivalent sigma: > {norm.ppf(1-1/n):.1f}')

# ====== Check the original Test 3 bug ======
print('\n=== BUG CHECK: Original Test 3 threshold anomaly ===')
print('Original showed 0.1% having MORE passes than 0.2% — this is impossible')
print('in a correctly implemented test (tighter threshold cannot have more passes).')
for t in thresholds:
    count = sum(1 for w in worst_devs if w < t)
    print(f'  {t*100:.2f}%: {count}', end='')
    if t > thresholds[0]:
        count_prev = sum(1 for w in worst_devs if w < thresholds[thresholds.index(t)-1])
        ok = 'OK' if count <= count_prev else 'BUG!'
        print(f'  (should be <= {count_prev}: {ok})', end='')
    print()
