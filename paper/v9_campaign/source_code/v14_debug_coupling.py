#!/usr/bin/env python3
"""
v14_debug_coupling.py
Goal: Force-find any algebra element that maps e_R to ANY Left-handed state.
"""
import numpy as np

# ... (Standard Algebra Setup copypasta for speed) ...
def rep_C(x):
    if x == 1: return np.eye(2)
    if x == 'i': return np.array([[0, -1], [1, 0]])
    return np.zeros((2,2))

def rep_H(x):
    I = np.eye(4)
    i = np.array([[0, -1, 0, 0], [1, 0, 0, 0], [0, 0, 0, -1], [0, 0, 1, 0]])
    j = np.array([[0, 0, -1, 0], [0, 0, 0, 1], [1, 0, 0, 0], [0, -1, 0, 0]])
    k = np.array([[0, 0, 0, -1], [0, 0, -1, 0], [0, 1, 0, 0], [1, 0, 0, 0]])
    if x == 1: return I; 
    if x == 'i': return i; 
    if x == 'j': return j; 
    if x == 'k': return k
    return np.zeros((4,4))

FANO = [(1,2,4), (2,3,5), (3,4,6), (4,5,7), (5,6,1), (6,7,2), (7,1,3)]
mult = np.zeros((8,8,8))
for i in range(8): mult[0,i,i] = 1; mult[i,0,i] = 1
for i in range(1,8): mult[i,i,0] = -1
for (a,b,c) in FANO:
    mult[a,b,c] = 1; mult[b,c,a] = 1; mult[c,a,b] = 1
    mult[b,a,c] = -1; mult[c,b,a] = -1; mult[a,c,b] = -1
O_mats = {}
for a in range(8):
    M = np.zeros((8,8))
    for j in range(8): M[:, j] = mult[a, j, :]
    O_mats[a] = M
def kron3(A, B, C): return np.kron(A, np.kron(B, C))

I_64 = np.eye(64)
iC = kron3(rep_C('i'), rep_H(1), O_mats[0])
eL = {}
for i in range(1, 8): eL[i] = kron3(rep_C(1), rep_H(1), O_mats[i])

P = 0.5 * (I_64 + iC @ eL[7])
U, S_vals, Vt = np.linalg.svd(P)
rank = np.sum(S_vals > 1e-5)
basis_S = U[:, :rank] 
def get_S_op(Op): return basis_S.T @ Op @ basis_S

# Recalculate States
Gammas = []
for k in range(1, 7): Gammas.append(iC @ eL[k])
G_vol = Gammas[0]
for k in range(1, 6): G_vol = G_vol @ Gammas[k]
Gamma7_S = get_S_op(1j * G_vol)
Id_S = np.eye(32)
P_L = 0.5 * (Id_S + Gamma7_S)
P_R = 0.5 * (Id_S - Gamma7_S)

P_color_8 = np.zeros((8,8)); 
for k in range(1, 7): P_color_8[k,k] = 1.0
P_color_S = get_S_op(kron3(np.eye(2), np.eye(4), P_color_8))
iH_full = kron3(rep_C(1), rep_H('i'), O_mats[0])
I3_S = get_S_op(0.5 * iH_full)
I3_L = -1j * I3_S @ P_L
I3_R = -1j * I3_S @ P_R
B_minus_L = (4.0/3.0) * P_color_S - Id_S
Y_Op = B_minus_L + 2.0 * I3_R
Q_Op = I3_L + 0.5 * Y_Op

vals, vecs = np.linalg.eigh(Q_Op + 0.1 * P_L + 0.01 * P_color_S)
vec_eL = None
vec_eR = None
vec_nuL = None

for i in range(32):
    v = vecs[:, i]
    q = np.vdot(v, Q_Op @ v).real
    is_l = np.vdot(v, P_L @ v).real > 0.5
    is_color = np.vdot(v, P_color_S @ v).real > 0.5
    if abs(q + 1.0) < 0.1 and is_l and not is_color: vec_eL = v
    if abs(q + 1.0) < 0.1 and not is_l and not is_color: vec_eR = v
    if abs(q) < 0.1 and is_l and not is_color: vec_nuL = v

# VERIFICATION
print("\nState Properties:")
for name, vec in [("eL", vec_eL), ("eR", vec_eR), ("nuL", vec_nuL)]:
    if vec is None:
        print(f"  {name}: Not Found")
        continue
    norm = np.linalg.norm(vec)
    q = np.vdot(vec, Q_Op @ vec).real
    chir = np.vdot(vec, Gamma7_S @ vec).real
    print(f"  {name}: Norm={norm:.4f}, Q={q:.2f}, Chirality={chir:.2f}")

if vec_eL is None or vec_eR is None:
    exit()

print("\nRunning FULL BASIS coupling check (Max Coupling)...")
labels_C = ['1', 'i']
labels_H = ['1', 'i', 'j', 'k']
labels_O = ['e0', 'e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7']

max_global_coupling = 0.0
coupling_map = []

for ic, c_lab in enumerate(labels_C):
    for ih, h_lab in enumerate(labels_H):
        for io, o_lab in enumerate(labels_O):
            op_full = kron3(rep_C(c_lab if c_lab!='1' else 1), 
                       rep_H(h_lab if h_lab!='1' else 1), 
                       O_mats[io])
            op_S = get_S_op(op_full)
            
            val = abs(np.vdot(vec_eL, op_S @ vec_eR))
            if val > 1e-4:
                coupling_map.append( (f"C({c_lab})xH({h_lab})xO({o_lab})", val) )
                max_global_coupling = max(max_global_coupling, val)

print(f"Global Max Coupling <eL| Op |eR> found: {max_global_coupling:.4f}")
if len(coupling_map) > 0:
    print("Top 5 Coupling Elements:")
    coupling_map.sort(key=lambda x: x[1], reverse=True)
    for c in coupling_map[:5]:
        print(f"  {c[0]}: {c[1]:.4f}")
else:
    print("  STILL ZERO. This violates Isomorphism Theorems.")
    
# CHECK GAMMA MATRICES explicitly too
print("\nChecking Gamma Matrices:")
for k in range(6):
    G = Gammas[k]
    G_S = get_S_op(G)
    val = abs(np.vdot(vec_eL, G_S @ vec_eR))
    print(f"  Gamma[{k+1}]: {val:.4f}")
