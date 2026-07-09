# Master Audit (Merged) – *Trinh, “Induced Superfluid Cosmology”* (Preprint 08/01/2026)

Tài liệu này **hợp nhất** hai bản audit (bản của anh Tony Tùng + bản audit của tôi) thành một **danh sách toàn diện** gồm: (1) toàn bộ vấn đề kỹ thuật/lập luận/định lượng, (2) mức ưu tiên, (3) hướng vá/đầu ra chứng minh tối thiểu (“deliverables”) để nâng bản thảo từ “proposal/numerology” lên “derivation/EFT-consistent + falsifiable”.

> Ghi chú: nơi tham chiếu theo số phương trình/section trong PDF (các trang mà anh đã nêu: tr. 9, 14–15, 18, 21, 24, 27–30, 39–40) và các phần phụ lục liên quan.

---

## 0) Executive Summary

### Kết luận nhanh
- **Không có mâu thuẫn lõi** giữa hai bản audit; các “điểm gãy” trùng nhau.
- Các vấn đề trọng yếu tập trung ở: **(i) cầu nối analogue gravity**, **(ii) induced gravity/one-loop + heat-kernel + cutoff**, **(iii) sequestering (action + variation + vacuum shift invariance)**, **(iv) Eq. (36) dark energy sai thang**, **(v) direct detection sai scaling và sai số học**, và một loạt **mâu thuẫn nội bộ** (SIDM bound vs bảng, primitive gcd vs mode W, benchmark DM 5.7 vs 10 GeV, …).

### Mục tiêu của patch
- Biến các claim “assertion” thành **derivation có kiểm chứng**, có **quy ước đóng**, có **đơn vị nhất quán**, và phân loại rõ: **Derived vs Anchored vs Proposed**.

---

## 1) BLOCKERS – Lỗi “đập là gãy” (phải vá trước khi claim đóng)

### B1) Analogue gravity / Acoustic metric: thiếu bước covariantization (Eq. (5)–(6), tr. 9)
**Vấn đề:** Từ \(\partial_\mu(\rho\,\partial^\mu\phi)=0\) “identify” sang KG covariant trong nền cong và định nghĩa metric conformal \(g_{\mu\nu}=\Omega^2\eta_{\mu\nu}\) với \(\Omega^2\propto\rho\) nhưng **không chứng minh** \(\sqrt{-g}g^{\mu\nu}\propto \rho\eta^{\mu\nu}\) trong 3+1D.

**Patch tối thiểu:** Chèn derivation ngay sau Eq. (6):
1) đặt \(g_{\mu\nu}=\Omega^2\eta_{\mu\nu},\ \Omega^2=\rho/\rho_0\);
2) tính \(g^{\mu\nu}=\Omega^{-2}\eta^{\mu\nu}\), \(\sqrt{-g}=\Omega^4\sqrt{-\eta}\);
3) suy \(\sqrt{-g}g^{\mu\nu}=\Omega^2\sqrt{-\eta}\,\eta^{\mu\nu}=(\rho/\rho_0)\sqrt{-\eta}\,\eta^{\mu\nu}\);
4) kết luận phương trình covariant đúng **tới một hệ số khác 0**.

**Lưu ý giới hạn:** Đây mới là **kinematics** cho mode vô hướng; **chưa** chứng minh dynamics spin-2/Einstein equation.

---

### B2) Induced gravity / one-loop: sai/thiếu về \(\Delta\), quy ước Euclid–Lorentz, thiếu \(\Lambda^2\) (Eq. (11)–(15), tr. 14–15)
**Vấn đề lớp 1 (operator):** \(\Delta\) từ Dirac-squared dễ sai dấu/hệ số \(R/4\) nếu không khóa quy ước (Lorentzian vs Euclidean, định nghĩa \(R^\rho{}_{\sigma\mu\nu}\)).

**Vấn đề lớp 2 (regularization):** Nếu đã có \(\rho_{vac}\sim \Lambda^4\) thì trong cutoff EFT, \(1/G\) thường có **power divergence** \(\sim\Lambda^2\). Bản thảo hiện thiên về dạng \(M^2\ln(\Lambda^2/M^2)\) mà không nêu rõ scheme/renorm condition → **bất nhất nội tại**.

**Vấn đề lớp 3 (heat-kernel):** Không đóng rõ \(a_0,a_1\) cho đúng spin/dof và trace → Eq. (15) hiện là assertion.

**Patch bắt buộc (deliverable Note-2):** Viết lại khối Eq. (11)–(15) theo pipeline:
1) chốt signature + Wick rotation;
2) tính Laplace-type: \(\Delta=-\nabla^2+E\) (Dirac: \(E=R/4\) tùy quy ước);
3) heat-kernel: \(\mathrm{Tr}\,e^{-s\Delta}=\int\sqrt{g}(4\pi s)^{-2}\,\mathrm{tr}[a_0+s a_1+\dots]\);
4) proper-time cutoff \(s\ge 1/\Lambda^2\):
   \(I_1=\int_{1/\Lambda^2}^\infty ds\,s^{-2}e^{-sM^2}=\Lambda^2-M^2\ln(\Lambda^2/M^2)+\dots\);
5) suy ra dạng tổng quát:
   \[\frac{1}{16\pi G_{ind}}=A\,N_f\,\Lambda^2 + B\,N_f\,M^2\ln\frac{\Lambda^2}{M^2}+\dots\]
   với \(A,B\) **tính ra** từ \(\mathrm{tr}(a_1)\) và dof.

**Yêu cầu chốt:** Trình bày rõ scheme (cutoff cứng / PV / DR) và điều kiện khi \(\Lambda^2\) bị hấp thụ vào counterterm.

---

### B3) Sequestering / Vacuum shift invariance: thiếu action + biến phân dẫn tới Eq. (49) (Appendix D tr. 40)
**Vấn đề:** Nêu \(T^{eff}_{\mu\nu}=T_{\mu\nu}-\tfrac14 g_{\mu\nu}\langle T\rangle\) nhưng thiếu chuỗi **biến phân** từ action KP-type, nên dễ bị coi là “gắn cơ chế ngoài”.

**Patch bắt buộc (deliverable Note-3):**
1) ghi action sequestering (Kaloper–Padilla) với \(\Lambda,\lambda\) là biến toàn cục + \(\sigma(\Lambda/\mu^4)\);
2) \(\delta/\delta g^{\mu\nu}\) → Einstein eq với \(-\Lambda g_{\mu\nu}+T_{\mu\nu}\);
3) \(\delta/\delta\Lambda\) và \(\delta/\delta\lambda\) → ràng buộc toàn cục \(\Lambda=\tfrac14\langle T\rangle\) (hoặc dạng tương đương);
4) thế lại → Eq. (49);
5) chứng minh invariance dưới \(\mathcal{L}_m\to\mathcal{L}_m-\delta\rho_{vac}\).

---

### B4) Dark Energy: Eq. (36) sai thang đo nghiêm trọng (tr. 29)
**Vấn đề:** \(\rho_{DE}\approx (M_{Pl}M^*)^2\) có đơn vị đúng nhưng lệch quan sát \(\sim 10^{88-90}\) bậc → fatal nếu coi là dự đoán.

**Patch bắt buộc (deliverable Note-4):**
- Bỏ Eq. (36) hoặc gắn nhãn “bare scale (non-gravitating under sequestering)”.
- Thay bằng định nghĩa đại lượng gravitate: \(\rho^{eff}_{DE}=\tfrac14\langle T_m\rangle\) (theo kết quả sequestering).
- Nếu muốn **dự đoán trị số**: cần mô hình hóa cosmic history để tính \(\langle T_m\rangle\), hoặc cơ chế residual bổ sung.

---

### B5) Direct detection: sai scaling theo \(\Lambda_\chi\), sai đại số \(|q|/q^2\), sai số học bậc lớn (Eq. (31)–(33), tr. 27)
**Vấn đề:**
- Mơ hồ “contact operator” vs “mediator exchange”; thiếu nhất quán số vertex.
- Lỗi đại số trong scaling \(|q|/q^2\) (phải \(1/|q|\) nếu chỉ có 1 đạo hàm).
- Cross-section cần 2 vertex → \(\sigma\propto \Lambda_\chi^{-4}\) (không phải \(\Lambda_\chi^{-2}\)).
- Nếu derivative coupling: có suppression mạnh theo \(v\) và/hoặc \(q\).

**Patch bắt buộc (deliverable Note-5):**
1) định nghĩa rõ UV/EFT: vertex DM–phonon và N–phonon;
2) NR limit: \(\bar u\gamma^0u\approx 2m_N\), \(\omega\approx \mathbf{q}\cdot\mathbf{v}\);
3) propagator phonon: \(D\sim -1/(c_s^2\mathbf{q}^2)\) khi \(\omega\ll c_s|\mathbf{q}|\);
4) amplitude với **hai vertex**: \(\mathcal{M}\sim (c_N/\Lambda_\chi)^2(2m_N)^2\,\omega^2/(c_s^2\mathbf{q}^2)\sim (c_N m_N/\Lambda_\chi)^2(v^2/c_s^2)\);
5) \(\sigma\sim (\mu^2/\pi)|\mathcal{M}|^2\propto \Lambda_\chi^{-4}v^4c_s^{-4}\);
6) đổi đơn vị \(\mathrm{GeV}^{-2}\to\mathrm{cm}^2\) và tính lại benchmark.

---

### B6) Screening/PPN: nhánh cubic vs quartic không nhất quán, tham số \(\Lambda_{eff}\) không neo từ EFT (Main + Appendix C)
**Vấn đề:** Dùng suppression \((r/r_V)^2\) cho quartic nhưng khi kết luận Cassini lại dùng \((r/r_V)^{3/2}\) “nếu cubic sinh ra” mà chưa chứng minh cubic thực sự xuất hiện từ EFT của mô hình. \(\Lambda_{eff}\) được gán số (ví dụ 0.1 eV) nhưng thiếu bridge định nghĩa.

**Patch bắt buộc:**
- Chọn **một nhánh** làm mainline (cubic hoặc quartic). Nếu giữ cả hai, đưa nhánh còn lại thành “contingent appendix” và không dùng nó để kết luận chính.
- Định nghĩa \(\Lambda_{eff}\) từ hệ số EFT (ví dụ \(\Lambda_{eff}^4\equiv c_2\rho_0^2/c_4\) hoặc mapping tương đương) rồi suy \(r_V\) và \(|\gamma-1|\) bằng bài toán nghiệm tĩnh + PPN chuẩn.

---

## 2) MAJOR – Mâu thuẫn lớn / thiếu logic nhưng có thể vá sau Blockers

### M1) BAO units / notation: biểu thức đổi \(k\) sang \(h/\mathrm{Mpc}\) dễ gây hiểu nhầm (Eq. (20)–(21), tr. 18)
**Vấn đề:** Con số \(0.0634\,h/\mathrm{Mpc}\) đúng nếu chia cho \(h\), nhưng cách trình bày có thể bị đọc như nhân \(h\). Đây là lỗi trình bày đơn vị dễ bị reviewer bắt.

**Patch:** Viết rõ:
\[k_{BAO}[h/\mathrm{Mpc}] = \frac{2\pi}{r_s[\mathrm{Mpc}]}\cdot\frac{1}{h}.\]
Đổi ký hiệu \(\Delta k_h\to k_{BAO}\) nếu thực chất là wavenumber của acoustic scale.

---

### M2) BAO/CMB/BBN pipeline: đang “anchored”, chưa dự đoán độc lập
**Vấn đề:** Dùng \(r_s\) quan sát làm anchor là hợp lệ như “consistency check” nhưng phải phân loại rõ; muốn dự đoán cần chạy pipeline (CLASS/CAMB) với \(H(z),c_s(z),\Omega_b\) hiệu dụng của mô hình. BBN tương tự: cần chạy yields dưới \(H(t)\) mô hình.

**Patch:** Thêm bảng “Derived vs Anchored vs Proposed” ở Introduction; đẩy BAO/BBN vào Anchored/Proposed cho tới khi có pipeline.

---

### M3) Particle spectrum: thống kê & ngôn ngữ claim chưa đạt chuẩn HEP
**Vấn đề:** Dùng “robust match” trong khi chênh lệch so với uncertainty đo có thể rất lớn (ví dụ Z). Look-elsewhere test còn phụ thuộc null model và trial factors.

**Patch:**
- Hạ ngôn ngữ: “percent-level agreement (systematics not modeled)”.
- Tối thiểu 2 null models (uniform, log-uniform / density-of-states) + trial factor minh bạch.
- “Pre-registered protocol” cho mapping để tránh hậu nghiệm.

---

### M4) Quy tắc primitive/gcd: mâu thuẫn nội bộ với gán mode (W=(5,50) vs gcd=1 rule)
**Vấn đề:** Nếu SM sector đòi gcd(p,q)=1 (primitive), thì gán W=(5,50) vi phạm. Nếu cho phép ngoại lệ, phải nêu quy tắc ngoại lệ.

**Patch:**
- Chốt rule primitive và kiểm tra toàn bộ mapping.
- Nếu W là composite của primitive mode, viết decomposition rõ (ví dụ (1,10) với factor?), hoặc bỏ rule gcd=1.

---

### M5) DM benchmark mâu thuẫn (DT-1 5.7 GeV vs mχ=10 GeV)
**Vấn đề:** Bảng/numerics/indirect line energy đang trộn benchmark.

**Patch (deliverable Note-6):**
- Chốt 1 benchmark chính (khuyến nghị DT-1≈5.70 GeV nếu gắn với line 2.85 GeV), benchmark phụ tách riêng.
- Đồng bộ mọi tính toán/bảng theo benchmark.

---

### M6) SIDM: mâu thuẫn bound trích dẫn vs số trong bảng (dwarf ~60 cm²/g)
**Vấn đề:** Nếu trích bound \(\sigma/m<10\) cm²/g mà bảng cho 60 và ghi “consistent” là mâu thuẫn.

**Patch:**
- Chỉ rõ đại lượng: \(\sigma_T\) (transfer) hay \(\sigma\) total.
- Trích bound đúng theo velocity regime, hoặc điều chỉnh benchmark để nằm trong bound.
- Công bố thuật toán: regime check (Born/classical/resonant), partial-wave cutoff, Maxwellian averaging.

---

### M7) Neutrino “defect gas”: định lượng mật độ và tính “dilute” chưa thuyết phục
**Vấn đề:** Công thức suy ra \(n_d\) có thể đúng đại số, nhưng diễn giải “dilute” không rõ. Cần đổi sang \(\mathrm{cm}^{-3}\) và suy ra khoảng cách \(L\sim n_d^{-1/3}\) để đánh giá vật lý. Cần định nghĩa defect core size/energy và tương tác với SM.

**Patch:**
- Thêm conversion \(\mathrm{GeV}^3\to\mathrm{cm}^{-3}\), tính \(L\) và so với \(\xi\).
- Nêu rõ stability/energy budget, constraints (N_eff, Σmν, scattering).

---

### M8) Topology → spin/statistics: thiếu định lý topo–động lực (Table 3)
**Vấn đề:** Spin-statistics không thể suy ra từ phân loại số học nếu không có holonomy/covering/braid group dẫn tới pha \(-1\) khi hoán vị.

**Patch:**
- Định nghĩa cấu hình topo cụ thể (soliton/domain-tube) và configuration space.
- Tính nhóm braid/covering/homotopy liên quan và chỉ ra điều kiện fermionic sign.
- Nếu chưa làm được: hạ claim thành “phenomenological classification”.

---

### M9) Topology → gauge mapping (Table 6): nguy cơ lẫn homotopy với gauge group
**Vấn đề:** Gán SU(2), SU(3), U(1) từ “effective sphere / π_p” cần cơ chế emergent gauge (Berry connection, constraint redundancy, moduli-space isometry). Hiện có nguy cơ lẫn khái niệm.

**Patch:**
- Chọn một cơ chế emergent gauge rõ ràng và derive gauge fields as connections.
- Hoặc hạ claim thành heuristic và dời sang Discussion.

---

### M10) Screening/PPN: thiếu nghiệm tĩnh + mapping sang \(\gamma\) PPN
**Vấn đề:** Đưa rV và \(|\gamma-1|\) nhưng thiếu bài toán profile field + metric potentials (Φ,Ψ) và công thức \(\gamma=\Psi/\Phi\).

**Patch:**
- Viết bài toán tĩnh đối xứng cầu, nghiệm gần/xa, rồi suy Φ,Ψ và \(\gamma\).
- Kết nối coupling của θ tới matter (trace T hay baryon current?).

---

### M11) “Emergent gravity” mới dừng ở scalar analogue; thiếu dynamics spin-2
**Vấn đề:** Metric hiệu dụng cho scalar fluctuations không đủ để kết luận GR emerges fully (2 DOF gravitons, Einstein-Hilbert action, ghost-free).

**Patch:**
- Nêu rõ claim: “analogue scalar kinematics” thay vì “GR fully”.
- Nếu muốn GR: derive effective action cho metric + kiểm tra propagating tensor modes.

---

## 3) MAJOR/MINOR – Lỗi kỹ thuật toán/đơn vị/trình bày gây “hỏng khả kiểm”

### T1) Appendix BCS / dimensional reduction: lỗi giải tích trong integral tạo log (G.3.3 / Eq. (62) tương ứng)
**Vấn đề:** Integral dạng \(\int dk/(k^2+\Delta^2)\) không sinh log; log sinh từ \(\int d\xi/\sqrt{\xi^2+\Delta^2}\) (BCS chuẩn). Nếu bản thảo suy log từ integral sai, toàn bộ “transmutation/hierarchy” bị suy yếu.

**Patch:** Viết lại derivation BCS chuẩn: biến \(\xi\) quanh Fermi surface, kernel pairing, điều kiện gần hằng → ra \(\Delta\sim 2\Lambda e^{-1/(gN(0))}\).

---

### T2) Parameter dictionary thiếu (\(g_c,c_s,M^*,\Lambda_{eff},\Lambda_\chi\))
**Vấn đề:** Nhiều ký hiệu xuất hiện mà chưa neo định nghĩa/đơn vị/phạm vi; làm reviewer không tái lập được.

**Patch:** Thêm “Parameter Dictionary” 1 trang: định nghĩa, đơn vị, benchmark, nguồn (PDG/CODATA) và status (derived/fit/assumed).

---

### T3) Traceability của bảng số (PDG year, CODATA year, Planck year)
**Patch:** Mọi bảng nên có cột/caption chỉ rõ input set và làm tròn.

---

### T4) Appendix numbering lặp / cấu trúc phụ lục
**Patch:** Dọn lại numbering, thêm “Appendix map: appendix nào chứng minh claim nào”.

---

## 4) “Không được claim” nếu chưa có chứng minh bổ sung

- “GR emerges fully” nếu chỉ có analogue KG cho scalar.
- “Robust match” theo chuẩn sigma HEP nếu không mô hình hóa uncertainty/systematics.
- “Prime/composite predicts spin-statistics” nếu chưa có topo/braid derivation.
- “Predict \(\rho_{DE}\)” nếu mới chỉ có sequestering (ổn định nhưng chưa định lượng cosmic history).

---

## 5) Patch Plan hợp nhất (theo Phase)

### Phase 1 (Bắt buộc – EFT consistency)
1) **B1 Metric mapping** (Note-1).
2) **B2 Induced gravity**: \(\Delta\) đúng + heat-kernel + cutoff-consistent \(\Lambda^2\)+log (Note-2).
3) **B3 Sequestering**: action + variation → Eq. (49) + vacuum shift invariance (Note-3).
4) **B4 Dark Energy**: bỏ/đổi Eq. (36), định nghĩa \(\rho_{DE}^{eff}\) và giới hạn dự đoán (Note-4).
5) **B5 Direct detection**: \(\Lambda^{-4}v^4\) + numerics + conversion đơn vị (Note-5).
6) **B6 Screening branch**: chốt cubic/quartic + định nghĩa \(\Lambda_{eff}\) + PPN derivation tối thiểu.

### Phase 2 (Internal consistency & credibility)
7) Đồng bộ benchmark DM (DT-1 5.7 vs 10 GeV) (Note-6).
8) Sửa wording thống kê (Table spectrum) + null models.
9) Sửa mâu thuẫn primitive gcd vs W-mode.
10) SIDM: sửa bound vs bảng, công bố \(\sigma_T\) và regime check.
11) Parameter dictionary + traceability + dọn phụ lục.

### Phase 3 (Từ “numerology” → “derivation”)
12) Topo→spin/statistics: mô hình cấu hình + holonomy.
13) Topo→gauge: emergent gauge mechanism.
14) BAO/CMB/BBN: pipeline dự đoán (CLASS/CAMB + BBN yields).
15) BCS/vacuum micro-model: nếu muốn dùng làm nền hierarchy thì phải đúng toán + có Fermi surface cơ chế.

---

## 6) Deliverables tối thiểu (gói gửi lại để review nhanh)

1) **Note-1 (Metric mapping):** chứng minh Eq. (5)→covariant KG với \(g_{\mu\nu}=\Omega^2\eta\) trong 4D.
2) **Note-2 (Induced gravity):** Dirac-squared + \(a_0,a_1\) + proper-time cutoff → \(\rho_{vac}\sim\Lambda^4\), \(1/G\sim\Lambda^2\) (và log) với quy ước đóng.
3) **Note-3 (Sequestering):** action + biến phân → Eq. (49) + vacuum shift invariance.
4) **Note-4 (Dark energy):** bare vs effective; \(\rho_{DE}^{eff}=\tfrac14\langle T_m\rangle\); nêu rõ chưa dự đoán trị số nếu chưa có cosmic history.
5) **Note-5 (Direct detection):** amplitude/cross-section scaling \(\Lambda^{-4}v^4\) + đổi đơn vị ra cm² + benchmark.
6) **Note-6 (Consistency patch):** chốt benchmark \(m_\chi\), đồng bộ Table 4/indirect lines, sửa wording thống kê Table spectrum.

---

## 7) Checklist cuối trước khi gửi lại bản thảo

- [ ] Eq. (5)–(6): mapping covariant rõ ràng (4D) và ghi rõ giới hạn (scalar analogue).
- [ ] Induced gravity: \(\Delta\) đúng, \(a_1\) có trace+dof, \(\Lambda^2\) xuất hiện nhất quán với \(\Lambda^4\), scheme chốt.
- [ ] Sequestering: action + biến phân, chứng minh vacuum shift invariance, không chỉ statement.
- [ ] Dark energy: bỏ Eq. (36) sai thang; thay bằng \(\rho_{DE}^{eff}\) và giới hạn dự đoán.
- [ ] Direct detection: \(\Lambda^{-4}v^4\) + numerics + conversion đúng.
- [ ] Screening: cubic/quartic nhất quán; \(\Lambda_{eff}\) định nghĩa từ EFT; PPN derivation.
- [ ] SIDM: bound vs bảng nhất quán; \(\sigma_T\) và regime check minh bạch.
- [ ] Primitive rule vs W-mode: không còn mâu thuẫn.
- [ ] Benchmark DM đồng bộ.
- [ ] Parameter dictionary + traceability + phụ lục đánh số chuẩn.

---

## 8) Gợi ý “bố cục lại” để bản thảo qua phản biện dễ hơn (tùy chọn)

1) Introduction: bảng **Derived / Anchored / Proposed**.
2) Core theory: (i) analogue scalar kinematics (có Note-1), (ii) induced gravity (Note-2), (iii) sequestering (Note-3).
3) Phenomenology: spectrum (kèm thống kê đúng), BAO (anchored), SIDM (regime), direct detection (Note-5), screening (PPN derivation).
4) Discussion: topology→spin/gauge (đưa sang “program” nếu chưa chứng minh).

---

**Kết luận:** Với Phase 1 hoàn tất và Phase 2 dọn sạch mâu thuẫn nội bộ + chuẩn hóa thống kê/đơn vị, bản thảo sẽ đạt trạng thái **EFT-consistent, derivation-present, claims calibrated**. Phase 3 là để nâng các phần spectrum/topology/BBN/CMB từ “đề xuất” thành “chứng minh”.

