# TRXT-NULLIVANCE Research Changelog
## Nhật ký Nghiên cứu & Nâng cấp

---

## Version 8.0 (In Progress) - 2026-02-02

### Mục tiêu
Giải quyết triệt để 9 phản biện từ chuyên gia học thuật.

### Các Nâng cấp Hoàn thành
| WP | Nội dung | Trạng thái | Kết quả |
|----|----------|------------|---------|
| WP1 | NJL EFT Clarification | ✅ DONE | Appendix V: Λ_UV ~ 0.1 M_Pl |
| WP2 | CMB Sound Speed | ✅ DONE | TRXT modifies DM only, CMB unchanged |
| WP3 | SIDM Relic Abundance | ✅ DONE | ⟨σv⟩ = 2.3×10⁻²⁶ cm³/s DERIVED |
| WP4 | Mode Selection Rules | ✅ DONE | Appendix W: 4 rules (coprimality, energy, entropy, decay) |
| WP5 | Ghost/Stability Analysis | ✅ DONE | Ghost-free 50/50 ✅, Subluminal ✅ |
| WP6 | SPARC Robustness | 🔲 Pending | (Bootstrap error bars) |

### Files Created
- `Appendix_V_EFT.tex` - EFT interpretation with explicit cutoff
- `Appendix_W_ModeSelection.tex` - 4 first-principles selection rules
- `relic_abundance_trxt.py` - DT-1 mass = 5.778 GeV DERIVED
- `ghost_stability_check.py` - k-essence stability PROVEN
- `cmb_sound_speed_check.py` - CMB consistency VERIFIED
- `figures/fig_ghost_stability.png` - Ghost-free visualization

---

## Version 7.0 - 2026-02-02

### Mục tiêu
Tích hợp nhánh MaVaN và các appendix mới từ GPT review.

### Các Nâng cấp Hoàn thành
| Appendix | Nội dung | Đóng góp |
|----------|----------|----------|
| **Appendix N** | Endogenous A7 via Noether Charge | Chứng minh $\Lambda_{eff} = 0$ là định lý, không phải tiên đề |
| **Appendix T** | Topological Foundations (Ricci Flow) | Dẫn xuất $E \sim 1/p$ từ Perelman; Quark confinement proof |
| **Appendix U** | Mass-Varying Neutrino (MaVaN) | $\beta = 2/(n+1) \approx 0.084$ từ $n=1.37$ |
| **Appendix Z** | Ontological Foundations (Logic Layer) | Percolation → Spacetime emergence |

### Các Hình ảnh Mới
- `fig_noether_sequestering.png`
- `fig_ricci_flow_mass.png`
- `fig_mavan_beta_prediction.png`
- `fig_mavan_dm2_running.png`
- `fig_quark_confinement.png`

### Trích dẫn Mới (8 mục)
- Perelman 2002, 2003 (Ricci Flow)
- Hamilton 1982 (Original Ricci Flow)
- NJL 1961 (Nambu-Jona-Lasinio model)
- MaVaN 2004 (Fardon-Nelson-Weiner)
- Super-Kamiokande 2016
- Borexino 2018
- Noether 1918

### Thay đổi Bảng Trạng thái
| Assumption | V6 | V7 |
|------------|----|----|
| A5 (Mass Spectrum) | Conjectured | **Derived** (Ricci Flow) |
| A7 (Vacuum Sequestering) | Derived | **Derived** (Noether Charge - stronger) |

---

## Version 6.0 - 2026-01-14

### Mục tiêu
Phiên bản đầu tiên được tái cấu trúc với classification epistemic rõ ràng.

### Nội dung Chính
- Core Model: NJL Condensate → Induced Gravity
- Extensions: Vainshtein Screening, SIDM, Hubble Tension
- SPARC Validation: 91.4% pass rate với $n=1.37$
- Bullet Cluster compatibility

### Hạn chế Đã biết (V6)
1. A7 (Vacuum Sequestering) - Borrowed from Volovik, not derived
2. A5 (Mass Spectrum) - Conjectured without mechanism
3. Mode selection (p,q) - Arbitrary

---

## Archive Structure

```
paper/submission_v16/
├── TRXT_Research_Report_V7.tex (current)
├── TRXT_Research_Report_V8.tex (will be created)
├── archive/
│   ├── TRXT_Research_Report_V7_backup_20260202.tex
│   └── [future backups]
├── figures/
└── RESEARCH_CHANGELOG.md (this file)
```

---

## Quy tắc Nhật ký

1. **Trước mỗi nâng cấp lớn:** Backup file `.tex` vào `archive/`
2. **Ghi rõ:** Mục tiêu, nội dung thay đổi, trạng thái
3. **Đánh số:** Version X.Y (X = major, Y = minor)
4. **Không xóa:** Lịch sử cũ phải được giữ lại
