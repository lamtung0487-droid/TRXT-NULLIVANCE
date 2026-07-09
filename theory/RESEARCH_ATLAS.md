# TRXT-Nullivance RESEARCH ATLAS
**The lab's master knowledge base — built from a sequential full read of `paper/TRXT_Research_Report.pdf` (191 pp., compiled 2026-02-27) on 2026-07-09.**
Page numbers = PDF pages. Cross-referenced against lab audits in `theory/reviews/`. This file is the lookup system: consult it before re-reading the report.

---

## 1. WHAT THE MODEL IS (one paragraph)

The physical vacuum is a **superfluid condensate of chiral Planck-scale fermions** (NJL-type pairing, analogous to BCS superconductivity). Spacetime geometry, gravity, gauge forces, matter, dark matter, and dark energy are all **collective phenomena of this one entity**: gravity = induced elasticity/entanglement response of the condensate (Sakharov/Jacobson); gauge groups = automorphism structure of the division algebra ℂ⊗ℍ⊗𝕆 the condensate lives in; particles = topological defects (vortex knots) with quantized windings; particle masses = breathing-mode gaps of those defects; dark matter = large-winding solitons ("Dark Tower"); dark energy = the settled ground-state energy of the condensate (w = −1), with the huge bare vacuum energy sequestered because static energy produces no entropy flux. Beneath it all (Layer 0), the condensate itself emerges from a discrete O(3) sigma-model "logic field" whose topological frustration ("the void cannot fully erase itself") makes matter mathematically unavoidable.

## 2. THE 4-LAYER ARCHITECTURE (pp. 17–21, 175–181)

| Layer | Content | Key math | Where |
|---|---|---|---|
| **L0 Logic** | Discrete O(3) NLSM on lattice; harmonic map heat flow ∂ₜn = ∇²n + \|∇n\|²n; matter = Structural Obstruction (residual topological charge I∞ ≈ 0.007 that cooling cannot remove) | Incompleteness Functional I[n] = ∫\|q\|d²x; Kibble-Zurek: 1.85% defect survival | App. AL/AM pp. 176–181; §3.1 |
| **L1 Condensate** | NJL: L = Ψ̄iγ∂Ψ + G(Ψ̄Ψ)²; pairing at G > G_crit → order parameter Φ = ρe^{iθ}; acoustic metric ds² woven from (Ξ, ∂θ) (Unruh/Volovik) | Logic tension ℰ ∝ Ξ\|∇θ\|², Ξ-quenching Ξ ∝ r² regularizes cores | §2.1, §3.1.2 pp. 17–19 |
| **L2 EFT** | k-essence P(X) = c₂X + c₄X² (both coefficients derived from NJL loops, App. B/C p. 81); induced Einstein-Hilbert + SM | c_s² = (c₂+2c₄X)/(c₂+6c₄X) ∈ (1/3, 1]; screening Λ_eff⁴ = c₂ρ₀²/c₄ | §9.3, 9.5; App. I, X |
| **L3 Data** | Gates 0–6: Bullet, P(k), SPARC, Cassini, BBN, CMB | see §6 below | §7–9 |

**Genesis narrative:** Big Bang → "Big Condensation" (SSB of logic field at ~10⁻³⁶ s); inflation = slow-roll relaxation of \|Φ\|; CMB heat = latent heat of condensation; second phase transition at T_c ~ 1 eV (z ≈ 4300) makes the condensate CDM-like before recombination ("Perfect Disguise", p. 72). Cosmic timeline table: p. 23. L0→L1 freeze-out at M_cond ≈ M_GUT, derived from G₂/SU(3) NLSM asymptotic freedom (p. 181, factor-4.2 gap at 1-loop).

## 3. HOW EACH PIECE OF THE UNIVERSE IS EXPLAINED

### 3.1 Gravity (induced, not fundamental)
- **Mechanism:** three redundant derivations offered: (a) Sakharov heat-kernel: integrating out fermions gives 1/16πG_ind = N_f Λ²/12π² (App. P p. 101 — with an honest convention "Warning"); (b) Jacobson entropic: Einstein eqs from δQ = TδS across horizons (App. N pp. 99–101); (c) TQFT: Chern-Simons on S³ boundary → BF theory on 4D cobordism → Plebanski constraints (B = e∧e) → Einstein-Cartan + Yang-Mills (§2.1 p. 17, declared the "deeper truth", heat kernel demoted to IR approximation).
- **WEP:** soliton center-of-mass follows geodesics exactly, mass cancels (p. 19). Newtonian limit: standard Poisson recovered (p. 67).
- **c_gw = c exactly** — tensor sector unmodified; photons claimed to ride background metric with zero coupling to phase mode (p. 66). ⚠ tension with §II of SYSTEM_OF_EQUATIONS ("light = phase fluctuations θ").

### 3.2 Gauge forces & the Standard Model (division algebras)
- **Uniqueness:** Hurwitz → only ℝ,ℂ,ℍ,𝕆; scan of all 8 tensor candidates → only ℂ⊗ℍ⊗𝕆 (dim 64) scores 5/5 (Cl(6) embedding, minimal left ideal dim 32, no ghost doubling) (p. 30).
- **SU(3):** Stab_G₂(e₁) ≅ SU(3), verified numerically to 1e-16 (p. 28). **SU(2)_L:** Stab_G₂(ℍ) ≅ SO(4) → chiral selection via S³ vacuum holonomy/linking (parity violation = topological asymmetry, p. 28). **U(1):** phase.
- **Fermion spectrum:** minimal left ideal = 16 states/generation with exactly SM quantum numbers (joint diagonalization of Γ₇, P_color; table p. 31); anomaly cancellation automatic, verified to 1e-10 (App. AB.2 p. 150).
- **3 generations:** Spin(8) triality (8_v, 8_s, 8_c permuted by ℤ₃) (p. 32); alternatively/complementarily the 3 Diophantine Seifert fibrations of 1/a+1/b+1/c = 1: (3,3,3), (2,4,4), (2,3,6) (App. AK p. 175).
- **Weinberg angle:** sin²θ_W = 3/8 at unification from trace normalizations k₃=32, k₂=4, k₁=20/3 → RGE → 0.2312 (p. 38).
- **No-Go theorem:** bare mass Ψ̄_LOΨ_R = 0 for ALL O in the algebra → mass MUST come from condensate bridge (Higgs = condensate excitation) (§6.6 p. 38).
- **Confinement:** 3-strand braid Br₃ on S³; single strand = branch cut with infinite logic tension (App. R.4 p. 107).

### 3.3 Particle masses (the mass law — the most contested pillar)
- **Formula:** E(p,q) = M\*(1/p + 1/q), (p,q) = torus winding numbers. Physical picture (App. Q p. 102): particles are **Hopfions** — closed vortex rings with toroidal winding p, poloidal winding q, stabilized by helicity (Faddeev-Niemi).
- **Derivation of 1/p (three inconsistent routes in the same document — LAB FLAG):**
  1. §8.4 (p. 44): worldvolume mode gap, cycles L_p = pL₀ → ω ∝ 1/p. Radius GROWS: R ∝ p.
  2. App. K.2 (p. 92): variational tension–curvature balance → R_opt ∝ p, mass = gap ℏc_s/R ∝ 1/p; **explicitly discards the static energy (∝ p) by fiat**.
  3. App. T.1 (p. 104): Ginzburg-Landau E ∝ p²ln(R/ξ) "appears to contradict 1/p", rescued by Ricci-flow contraction R_opt ∝ 1/p² — radius SHRINKS. Contradicts routes 1–2.
- **M\* chain (the "zero-free-parameter" claim, App. VF/J/AF):** Cl(6) chirality reduction → D_e = 5 independent generators → equipartition t = 1/5 → Abrikosov triangular lattice q = 6, k_F = 5/6 → v_F = (2/5)sin(π/6) = 1/5 → C = gL_F/(4π²)·(2/v_F) = 50/(3π) → g_eff = C/X (X = 3/(2α) ≈ 205.55) ≈ 0.0258 → BCS gap M\* = Λ_UV·exp(−1/g_eff) ≈ 365.24 GeV → m_τ = 2αM\*/3 = 1776.86 MeV "predicted". Error budget ±25 MeV on M\* (p. 146).
- **Assignments:** W = (5,50), Z = (8,8), H = (5,7), DT-1 = (128,128). Sector derivation attempt (App. AC.2 p. 156): G₂→SU(3)→SU(2)×U(1) branching, 8 → 3₀⊕2₊₁⊕2₋₁⊕1₀; p_EW = dim(3₀⊕2₁) = 5, p_Z = dim(adj SU(3)) = 8; also p_EW = 1/v_F. Report's own honest MC: even WITH derived sectors, significance = 2.2σ (p = 0.013); without, p = 0.57 (null).
- **Lepton masses (different mechanism!):** m_i = M\*·exp(−4X·S_i), S_i = 1/(abc) from the generation's Seifert fibration → m_τ/m_μ ≈ 16.8 vs obs 16.81 (App. AK.4 p. 176). Koide K = 2/3 from Clifford-torus projection with phase 2/9 = Chern-Simons topological spin (p. 50).
- **Number-type taxonomy (p. 52):** prime×prime → scalars; prime×composite → charged vectors; symmetric composite → neutral vectors; 2ⁿ → dark sector.

### 3.4 Dark matter (the Dark Tower)
- **DT-1 = (128,128), m = 2M\*/128 = 5.707 GeV** — the framework's flagship testable prediction (Tier 3; 128 = 2⁷ from Clifford doubling; lab note: endpoint justified by Bott periodicity, `derivation_pq_selection_20260709.md`).
- **Why invisible:** (a) macroscopic soliton R ~ 10³ fm → form factor e^{−(qR)²} ~ 10⁻¹⁸ kills direct detection of microscopic probes; (b) production volume penalty ~10⁻⁹ at colliders — can only be born in the cosmological phase transition (p. 53); (c) alternative estimate σ_DT ≈ σ_weak(1/p)⁴ ~ 10⁻⁴⁸ cm² < LZ floor (p. 56); (d) phonon-mediated derivative coupling → σ ∝ v⁴/c_s⁴ ~ 10⁻⁵² cm² (p. 55). ⚠ several distinct suppression stories coexist.
- **SIDM:** σ/m ≈ 0.24 cm²/g geometric; velocity-dependent via 30 MeV phonon Yukawa: 60.7 (dwarfs) → 0.22 (Bullet) cm²/g — solves cusp-core, safe at clusters (pp. 57–58).
- **Relic density saga (exemplary honesty trail):** initial Ωh² = 0.1241 → RETRACTED (normalization error; true value with those params 0.013) → coupling λ_χ then "derived" two ways: Clifford-tower overlap λ = α·2^{−7/2}·√3 = 1.117e-3 and spectral-action RG λ = 8.72e-4, bracketing the required 1.038e-3 within ±10–16% → Ωh² = 0.10–0.13 "zero free parameters" (App. AB.4, AC.1, AC.3 pp. 152–158).
- **JWST early galaxies:** soliton cores as early seeds (p. 24).

### 3.5 Dark energy (PI-corrected understanding, see erratum in `derivation_ecore_tension_20260709.md`)
- **What it is:** the condensate ground state settled at the minimum of V_NJL. m_σ ≈ 2031 GeV ≫ H₀ → ε_V ~ 10⁻⁸⁹ → **w₀ = −1.000 exactly** (0.88σ from Planck; Gate G "VERIFIED", p. 41). NOT a particle; the superfluid relaxing to equilibrium after condensation.
- **Why not 10⁷⁴ GeV⁴:** three-layer sequestering: (a) Volovik Gibbs-Duhem P_vac = 0 for self-sustained droplet (App. E p. 81); (b) entropic: static ρ_vac gives ΔQ = ∫T_μν l^μl^ν = 0 through null horizons → "thermally invisible" (App. N p. 100); (c) unimodular/Kaloper-Padilla 4-form: Λ = integration constant, trace drift ρ_DE ≈ ¼⟨T_m⟩ ≈ ρ_crit → coincidence problem addressed (§4.0.2-3 pp. 25–26, App. Y pp. 116–118).
- ⚠ A fourth story (§3.1.3 p. 20): dynamical quintessence w = f(Ξ(z)) for DESI. Report reconciles background w=−1 vs perturbation P(X) in App. AB.6 (p. 153).

### 3.6 Cosmological tensions
- **H₀:** early universe = percolating logic network at criticality → Hausdorff D ≈ 2.53 → P(X) ~ X^{5/2} → c_s² = 1/(2n−1) ≈ 0.246 → r_s ≈ 140.5 Mpc → H₀ ≈ 70.6 (tension 4σ → ~1.5σ, "60% reduced"; honest: does not reach SH0ES 73) (§8.1-8.2 pp. 42–44).
- **S8:** ~8% P(k) suppression at k ~ 1 h/Mpc from finite c_s (p. 148).
- **BAO:** anchored to r_s (V2-level check, shape r > 0.98; V3 prediction = future work, §10.6 p. 77).

### 3.7 Baryogenesis, BBN, CMB
- **η = 7.7e-10** vs obs 6.14e-10 (factor 1.25): NJL gives strongly-first-order EWPT v(T_c)/T_c = M\*/(1.764·T_c) = 1.76 > 1; θ_CP ≈ 1.35e-5 from Cl(6) torsion; bounce S₃/T ≈ 142.5 (§9.9 p. 69, App. AC.4).
- **BBN Gate 5:** tracking superfluid RULED OUT (ΔN_eff too big); rescue = Ground State Decoupling / Energy-Lock: transition energy locks into defect rest mass + radiation, condensate drops to w = −1; PRyMordial bound f_BBN < 0.61% (pp. 69–71). CONDITIONAL PASS (f_BBN from Lagrangian pending; energy-lock proof pending §10.5).
- **CMB Gate 6:** CAMB vs 83 Planck TT points: ΛCDM-identical PASS; ΔN_eff = 0.1 already fails; w ≠ −1 fails; Ω_cdm pinned ±0.005 (p. 72). MCMC distance priors: χ² = 0.019, needs z_c > 50,000. **"Perfect Disguise" = the model is deliberately indistinguishable from ΛCDM at linear order.** Full hi_class TT/TE/EE = future work.
- **GW:** eV-scale first-order transition would give Ω_GW ~ 7e-13 ≫ bounds → transition must be smooth crossover (p. 41). GW170817: safe (c_gw = c; P(X) ⊂ G₂(X) Creminelli-Vernizzi safe class).

### 3.8 Screening & galactic dynamics
- **Solar system:** endogenous k-mouflage from derived c₂, c₄; r_V ≈ 2.4e7 AU; ε_fifth(1 AU) ≈ 8.6e-12, beats Cassini by 7 orders (§9.3 p. 63).
- **Galaxies:** two-phase halo — superfluid soliton core (Lane-Emden, n = 1.37) + NFW envelope, transition at r_t = 2r_s. **B2 model: 96.5% pass on 171 real SPARC galaxies, median χ²_ν = 0.41, beats MOND** (82.5%/1.11); a₀ = 6.93e-11 = a₀^Milgrom/√3 (√3 offset "needs theoretical explanation"); RAR scatter 0.134 dex (§9.1 pp. 61–62, App. AJ). ⚠ B2 uses 3 params/galaxy vs MOND-comparison 1; three different Gate-3 result sets appear (96.5%/0.41 §9.1; 68.4%/1.93 AB.7 p. 153; median 0.54 AG p. 147).
- **Bullet Cluster Gate 1:** PM sim, separation 194.1 kpc (obs 150–240) — but App. AB (p. 135) honestly concedes: **kinematically identical to relabeled CDM N-body**; drag Γ calibrated in [0.06, 0.12] Myr⁻¹ window where separation spans 100–350 kpc. Distinction "ontological rather than dynamical".

### 3.9 Neutrinos
- MaVaN: m_ν = geometric elastic strain of S³; environment-dependent coupling β = 2/(n+1): 0.844 galactic → < 0.0018 solar-core, requiring stiff-limit polytropic n₀ > 1110 — open falsifiable target (§9.2, 9.9 pp. 62, 68; App. W).

## 4. EPISTEMIC SELF-ASSESSMENT (the report's own honesty, pp. 14–16)

Axioms A0–A7 with status table (p. 14); claims table (p. 16): acoustic metric/G_ind/SIDM = Derived; **W/Z/H masses = Anchored (not Derived)**; **topology→gauge mapping = Proposed**; **dark energy ρ_eff = Proposed**. Validation levels V0–V3 defined; BAO explicitly V2. Author's Declaration (p. 104): PI openly acknowledges limits of formal background and invites audit — the lab exists to answer this.
Code: `github.com/lamtung0487-droid/TRXT-NULLIVANCE`; contact Vietthuc@giugocviet.org.

## 5. INTERNAL INCONSISTENCY REGISTRY (found in the full read — for /derive follow-ups)

| # | Contradiction | Locations |
|---|---|---|
| I-1 | Soliton radius: R ∝ p (§8.4, K.2) vs R ∝ 1/p² (T.1 Ricci flow) — opposite geometries both "derive" E ∝ 1/p | pp. 44, 92, 104 |
| I-2 | Static soliton energy ∝ p acknowledged in K.2 then discarded by fiat ("mass = gap only") — the exact E_core issue proven fatal in `derivation_ecore_tension_20260709.md` (13.5 GeV vs 3.5e-6 GeV, 6.6 orders) | p. 92 |
| I-3 | Null-model statistics: K.5 claims p ≈ 10⁻³ for W match; App. U.8/W says without sectors p = 0.57; robustness report says random-match chance 144.93%; lab MC: 52.5% of random masses match at 0.1% | pp. 94, 106–107 |
| I-4 | Photons: "zero coupling to phase mode, ride background metric" (p. 66) vs "light = Goldstone phase fluctuations" (SYSTEM_OF_EQUATIONS §II) | — |
| I-5 | Three different Gate-3 SPARC scorecards coexist (96.5%/0.41; 68.4%/1.93; median 0.54) | pp. 61, 147, 153 |
| I-6 | Dark energy: four mechanisms (settled V_NJL w=−1; entropic sequester; KP 4-form; dynamical quintessence w(Ξ)) — AB.6 reconciles two of them | pp. 20, 41, 100, 116, 153 |
| I-7 | DT-1 invisibility: four distinct suppression mechanisms quoted with different scalings | pp. 53–56 |
| I-8 | Sector p: winding number (element of π₁ = ℤ²) equated to *dimension of a representation block* (AC.2) — category mismatch needing a mathematician audit | p. 156 |
| I-9 | Gate-1 monistic pass = relabeled CDM kinematics with calibrated drag (own admission) vs "Gate 1 PASS" headline | pp. 135–136, 148 |
| I-10 | Mapping Rule 4 "p,q < 5 unstable" (one line, no proof) vs Universal Stability Theorem "ALL modes stable" | pp. 47, 113 |

## 6. GATE SCORECARD (report's final audit, p. 149 + lab re-run 2026-07-09)

| Gate | Report status | Lab re-run (`results/logs/gate_ledger.md`) |
|---|---|---|
| G0 causality | PASS (analytic c_s ≤ 1; TQFT "ghost-free by construction") | Script tests foam ergodicity only — criterion mismatch; X<0 branch unproven (audit Item 5) |
| G1 Bullet | PASS 194 kpc | NOT RUN (FITS absent); admitted relabeled-CDM equivalence |
| G2 P(k)/S8 | PASS (r > 0.98, 8% suppression) | PASS* (qualitative criterion) |
| G3 SPARC | PASS (B2 96.5%) | v17 script: fitted a₀, χ² = 4.9986 marginal; NPL script: mock data (invalid) |
| G4 Cassini | PASS (1e-12) | v17 PASS; NPL 3D FAILS at Neptune/Pluto — unresolved solver contradiction |
| G5 BBN | CONDITIONAL PASS (f < 0.61%) | Local script hardcodes Yp (PRyMordial absent on Windows; real run was on WSL2) |
| G6 CMB | PASS (distance priors) | not re-run |

## 7. THE LAB'S STANDING VERDICTS (as of 2026-07-09)

1. **E_core incompatibility theorem (SIGNED-OFF):** pure 1/p+1/q mass law XOR stable vacuum — no σ₀ satisfies both (gap 6.6 orders). The report's K.2 contains the problem's seed (static energy ∝ p discarded). Escape routes: BPS cancellation (GAP-1), soliton-number superselection (GAP-2) — neither exists in the report.
2. **Sector assignments:** AC.2's G₂-branching derivation (p=5, 8 as rep dimensions) is the report's answer to GAP-3; needs mathematician audit of the winding=dimension identification (I-8); even accepted, report's own significance is only 2.2σ.
3. **Z at 58σ** (0.13%): unexplained; "EFT matching corrections" not computed.
4. **DT-1 5.707 GeV:** clean pre-registered number, but conditional on resolving (1).
5. Antiparticle/negative-winding channels: **absent from all 191 pages** (stability theorem restricted to p_i, q_i ≥ 1 in Eq. 182).

## 8. QUICK PAGE INDEX

Axioms/epistemics 13–16 · EFT action & TQFT circularity fix 17 · Layers/L0 18–20 · Big Condensation/inflation/CMB origin 20–24 · Sequestering theorems 25–26 · Division algebras 27–35 · SM Lagrangian/Weinberg/No-Go 36–39 · CMB shifts/GW/DE-EOS 40–41 · BAO/H₀ fractal 42–44 · **Mass law §8.4 44–48** · Koide/generations/number-types 49–52 · Dark Tower/invisibility/SIDM 53–58 · Relic Boltzmann 59–60 · SPARC 61–62 · Screening 63–64 · Lorentz/GW170817 65–66 · Limits (ℏ→0, SM) 67–68 · H₀/ν/baryogenesis 68–69 · BBN 70–71 · CMB Gate 6 71–73 · Constraint audit 73–74 · Honest limitations 75–77 · Synthesis 77–79 · Hierarchy/BCS 80–86 · Big Bang imaginary time 86–87 · Tight-binding C 87–91 · **App. K mode selection 92–95** · SPARC method 96–98 · Anomaly/DOF 98–99 · Entanglement gravity 99–101 · Induced gravity 101–102 · **Hopfions 102–103** · Author's declaration 104 · **Ricci flow mass 104–106** · Braid/TQFT/α decomposition 106–108(ff) · Mode selection W (dup) 113ff · Ghost X 118 · MaVaN 119–124 · Fractal D 124–126 · Unimodular N 126–128 · Validation protocols 129–135 · **Bullet monistic 135–137** · Source audit 137–144 · Params/errors/circularity 145–147 · Gates summary 147–149 · **AB resolutions 150–155** · **AC.1-2 λ_χ & sectors 155–158** · AC.4 baryogenesis 158–159 · AJ numerics 159+ · **AK Seifert 175–176** · **AL sigma model 176–181** · M_cond = M_GUT 180–181.
