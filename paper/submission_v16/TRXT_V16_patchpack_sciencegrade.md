
# TRXT-Nullivance V16 — Patch Pack (Science-Grade Upgrade)
Ngày: 2026-01-03  
Mục tiêu: “đóng chặt” theo chuẩn reviewer Q1: định nghĩa rõ, kiểm tra thứ nguyên, hạ giọng các claim, bổ sung dẫn xuất & tham chiếu thực nghiệm.

---

## 0) Kết luận ngắn về tình trạng bản thảo hiện tại
Bản thảo đã có một “khung ý tưởng” tương đối mạch lạc (chân không siêu lỏng + mode tập thể + topo), nhưng đang vướng 5 điểm mà reviewer sẽ đánh rất mạnh:

1) **Numerology**: công thức mode `(p,q)` khớp số đẹp nhưng chưa có cầu nối toán học từ Lagrangian → phổ số nguyên.  
2) **Direct detection**: phần 5.71 GeV cần một EFT tán xạ hạt nhân *tường minh* + đối chiếu LZ/XENONnT/PandaX.  
3) **Vainshtein**: có nhắc cơ chế nhưng thiếu dẫn xuất r_V đúng chuẩn (và hiện tại ký hiệu Λ/Λ3 không nhất quán).  
4) **W-mass**: trích CDF như “bằng chứng” là rủi ro lớn (ATLAS/CMS nghiêng về SM). Cần chuyển luận điểm thành “environment/early-universe shear”.  
5) **Emergent Lorentz**: hiện mô tả định tính; cần dispersion relation + bound δ≪1.

---

## 1) Audit lỗi/thiếu (và vì sao reviewer sẽ bắt)
### 1.1. W-mass: nguồn trích dẫn và luận điểm
Trong bản thảo bạn viết ATLAS 2023 cho $M_W=80.353$ GeV nhưng mục [5] lại là PDG 2022 → **mismatch reference**.  
Ngoài ra, nếu “Vacuum shear” được trình bày như *cần thiết* để giải thích CDF, reviewer sẽ phản đòn ngay vì kết quả CDF đang gây tranh cãi với ATLAS/CMS.

**Patch:** đổi lập luận thành “shear là tham số môi trường”; ở vũ trụ hiện tại shear≈0 (SM-alignment). CDF chỉ còn là “case study”.

### 1.2. Direct detection: từ “suppression” sang EFT + so sánh limit
Hiện bạn ghi biên độ $|\mathcal{M}|\sim q^2$ → $\sigma\sim q^4$ và đưa số $\sigma_\mathrm{eff}\sim10^{-56}\,\mathrm{cm}^2$ (với $\Lambda=1$ TeV). Reviewer sẽ hỏi:
- Operator nào sinh ra đúng scaling đó?
- $q$ bạn lấy bao nhiêu (typical recoil)?
- So sánh với limit LZ/XENONnT ra sao?
- Có phụ thuộc vào vận tốc $v\sim10^{-3}$ không?

**Patch:** viết rõ EFT tối thiểu + power counting + v-suppression và/hoặc q-suppression. Làm 1 figure overlay với limit.

### 1.3. Vainshtein: thiếu Λ3 và công thức r_V nhất quán
Phương trình Galileon cần hệ số $1/\Lambda_3^3$ (không phải $1/\Lambda_3$). Công thức bán kính:
\[
r_V=\left(\frac{M}{16\pi M_\mathrm{Pl}}\frac{1}{\Lambda_3^3}\right)^{1/3}
\]
hoặc dạng tương đương (tùy quy ước). Bạn đang dùng $\Lambda$ không định nghĩa rõ, và ra con số $10^4$ AU là **khả nghi**.

**Patch:** định nghĩa $\Lambda_3$ (từ sector hấp dẫn/cosmology), dẫn xuất nghiệm cầu tĩnh, rồi tính r_V cho Mặt Trời theo một lựa chọn $\Lambda_3$ phù hợp (ví dụ DGP-like: $r_V=(r_s r_c^2)^{1/3}$).

### 1.4. Emergent Lorentz: cần dispersion relation + bound
Reviewer sẽ đòi:
\[
\omega^2=c^2 k^2\left[1+\xi\left(\frac{k}{\Lambda_{\rm UV}}\right)^n+\cdots\right]
\]
và chỉ ra $\delta(k)\equiv\xi(k/\Lambda_{\rm UV})^n\ll 1$ cho dải năng lượng quan sát (Fermi-LAT/GRB; GW).

**Patch:** trình bày mô hình phonon/Goldstone tối thiểu, tích phân mode nặng để được hiệu chỉnh bậc cao.

---

## 2) “Gói vá” nội dung: các đoạn LaTeX-ready bạn có thể dán thẳng
### 2.1. Section 4.1 (W-mass) — phiên bản reviewer-safe
```latex
\subsection{Vacuum Shear as an Environmental Parameter (Not a Required W-Mass Shift)}
Precision measurements of $M_W$ are currently not fully settled across experiments. 
Therefore, we do \emph{not} treat the CDF-II shift as a mandatory datum that the framework must reproduce.
Instead, we parameterize a \emph{vacuum shear} deformation by a custodial-breaking stiffness parameter $\rho_{\rm vac}$,
\begin{equation}
M_W^2=\rho_{\rm vac}\, M_Z^2 \cos^2\theta_W,\qquad \rho_{\rm vac}=1+\Delta\rho .
\end{equation}
In the late-time vacuum (laboratory conditions) we impose $\Delta\rho\simeq 0$ to ensure SM-alignment.
Nonzero $\Delta\rho$ is interpreted as an \emph{environmental} deformation, potentially relevant in early-universe/high-density regimes.
If one \emph{hypothetically} fits the CDF-II central value, one finds $\Delta\rho\simeq 1.9\times10^{-3}$, 
which numerically correlates with the TRXT scale via $\Delta\rho\sim \mathcal{O}(1)/X$.
We emphasize that this correlation is a \emph{model-motivated} parametrization and not a claimed discovery.
```

### 2.2. Section 5.2.3 (Direct detection) — EFT & suppression chuẩn
```latex
\subsection{Direct Detection and Derivative (Phonon-Mediated) Suppression}
We assume the light dark mode $\chi$ couples to Standard Model nucleons dominantly through the superfluid Goldstone/phonon $\theta$ via a derivative operator,
\begin{equation}
\mathcal{L}_{\rm int}=\frac{c_N}{\Lambda_\chi^2}\,(\partial_\mu \theta)\, \bar{N}\gamma^\mu N + \cdots ,
\end{equation}
where $\Lambda_\chi$ is the EFT cutoff and $c_N$ is a dimensionless coupling.
The phonon propagator in the nonrelativistic regime is
\begin{equation}
D(\omega,\mathbf{q})=\frac{i}{\omega^2-c_s^2 \mathbf{q}^2+i\epsilon},
\end{equation}
and typical nuclear recoils satisfy $\omega \sim \mathbf{q}^2/(2m_N)$ and $|\mathbf{q}|\sim 10\text{--}100~{\rm MeV}$.
Power counting then yields an amplitude schematically
\begin{equation}
\mathcal{M}\propto \frac{\omega}{\Lambda_\chi^2}\, \frac{1}{c_s^2\mathbf{q}^2}\, \frac{\omega}{\Lambda_\chi^2}
\;\;\Rightarrow\;\; |\mathcal{M}|^2\propto \frac{\omega^4}{c_s^4\,\Lambda_\chi^8\,\mathbf{q}^4}.
\end{equation}
Since $\omega\sim v\,|\mathbf{q}|$ with $v\sim 10^{-3}$, this produces a strong \emph{velocity suppression} $|\mathcal{M}|^2\propto v^4$,
and depending on the UV completion may also induce additional $q$-suppression.
The resulting per-nucleon cross section scales as
\begin{equation}
\sigma_N \simeq \frac{\mu_N^2}{\pi}\,|\mathcal{M}|^2
\propto \frac{\mu_N^2}{\pi}\,\frac{v^4}{c_s^4}\,\frac{1}{\Lambda_\chi^8}\times(\text{mild }q\text{-dependence}),
\end{equation}
which can naturally evade current LZ/XENONnT/PandaX bounds even for $m_\chi\sim 5~{\rm GeV}$ provided $\Lambda_\chi$ is in the multi-TeV range
or $c_N\ll 1$.
We therefore present direct-detection constraints in terms of $(c_N,\Lambda_\chi,c_s)$ rather than a single fixed number.
```

**Lưu ý quan trọng:** đoạn này thay thế “claim số học” kiểu $\sigma\sim10^{-56}$ bằng biểu thức *có tham số* để bạn vẽ band so sánh với limit.

### 2.3. Appendix (Vainshtein) — dẫn xuất tối thiểu đúng chuẩn
```latex
\appendix
\section{Nonlinear Screening and the Vainshtein Radius}
We consider the cubic Galileon (decoupling limit) as the minimal nonlinear screening prototype,
\begin{equation}
\mathcal{L}_\pi=-\frac{1}{2}(\partial\pi)^2 - \frac{1}{\Lambda_3^3}(\partial\pi)^2\square\pi + \frac{\pi}{M_{\rm Pl}}T,
\end{equation}
which yields the equation of motion
\begin{equation}
\square\pi + \frac{1}{\Lambda_3^3}\left[(\square\pi)^2-(\partial_\mu\partial_\nu\pi)^2\right]=\frac{T}{M_{\rm Pl}}.
\end{equation}
For a static spherically symmetric source of mass $M$, one obtains an algebraic relation for $\pi'(r)$
whose crossover defines the Vainshtein radius
\begin{equation}
r_V=\left(\frac{M}{16\pi M_{\rm Pl}}\frac{1}{\Lambda_3^3}\right)^{1/3}.
\end{equation}
For a DGP-like choice $\Lambda_3^3\sim M_{\rm Pl}H_0^2$, equivalently $r_V=(r_s r_c^2)^{1/3}$ with $r_c\sim H_0^{-1}$,
the Sun yields $r_V\sim 10^{7}\,{\rm AU}\gg 100\,{\rm AU}$, ensuring Solar-System screening.
```

### 2.4. Section 6.3 (Emergent Lorentz) — dispersion relation & δ
```latex
\subsection{Emergent Lorentz Invariance and Dispersion}
At low energies the superfluid supports a Goldstone mode $\theta$ with linear dispersion $\omega=c_s k$.
Integrating out heavy UV modes at scale $\Lambda_{\rm UV}$ generates higher-derivative operators,
\begin{equation}
\mathcal{L}_{\rm eff}\supset \frac{\xi}{\Lambda_{\rm UV}^2}(\partial^2\theta)^2+\cdots ,
\end{equation}
leading to
\begin{equation}
\omega^2=c_s^2 k^2\left[1+\delta(k)\right],\qquad 
\delta(k)=\xi\left(\frac{k}{\Lambda_{\rm UV}}\right)^2+\mathcal{O}\!\left(\frac{k^4}{\Lambda_{\rm UV}^4}\right).
\end{equation}
Thus Lorentz symmetry (or relativistic linearity) is \emph{emergent} as $k/\Lambda_{\rm UV}\to 0$.
Taking $\Lambda_{\rm UV}\sim M_{\rm Pl}$ yields $\delta\ll 1$ for all laboratory/astrophysical $k$.
Constraints from time-of-flight measurements bound $\delta$ and hence $\xi/\Lambda_{\rm UV}^2$; the Planck-suppressed scenario is automatically safe.
```

---

## 3) Nâng cấp “Numerology → Topology”: cách viết để reviewer chấp nhận (chưa cần chứng minh hoàn hảo)
Bạn chưa thể “chứng minh hoàn toàn” $(p,q)$ từ NJL/BCS trong 1 bước. Nhưng bạn có thể *đóng chặt theo chuẩn học thuật* bằng cách:

1) **Tuyên bố rõ mức độ:** mode formula là *conjectured spectral law* của sector collective trên $T^2$ (không phải “fit tuỳ ý”).  
2) **Chứng minh nguồn gốc số nguyên:** $\pi_1(T^2)=\mathbb{Z}\oplus\mathbb{Z}$ → tồn tại hai winding độc lập. Do đó số lượng lượng tử hoá tối thiểu phải là cặp số nguyên.  
3) **Chỉ ra cơ chế phổ ∝ 1/p:** trong một mô hình vortex-line trên manifold compact, năng lượng cong tối thiểu/độ cong trung bình giảm khi đường khuyết tật “quấn nhiều vòng” (chiều dài hiệu dụng tăng ∝ p), do đó scale năng lượng hiệu dụng có thể mang dạng ∝ 1/p.  
4) **Đưa 1 mô hình toy** (tight-binding Dirac crossing trên BZ của $T^2$) để suy ra density of states và hệ số $\mathcal{C}\approx 5.3$ (phần bạn đã phát triển ở Appendix H.21).  

Điều quan trọng là: **viết đúng kiểu “derivation program”**: nêu định lý topo → mô hình toy → scaling → dự báo.

---

## 4) References: bản nâng cấp tối thiểu cần thêm (BibTeX-ready gợi ý)
Bạn cần bổ sung ít nhất các cụm nguồn sau (để tránh bị reviewer “bắn” vì thiếu literature):

- W mass precision (ATLAS measurement; CMS context; PDG mới).  
- Direct detection limits: LZ / XENONnT / PandaX-4T / CRESST-III.  
- Superfluid DM & phonon-mediated interactions: Berezhiani–Khoury; Khoury review.  
- Emergent Lorentz & LIV bounds: Liberati review; Fermi-LAT GRB time-of-flight.  
- Vainshtein/Galileon screening: Nicolis–Rattazzi–Trincherini; de Rham review.  

Tôi có thể xuất một file `references_v16.bib` đúng format theo style bạn dùng (APS/Elsevier) nếu bạn cho biết template LaTeX đang dùng (revtex/elsarticle).

---

## 5) Checklist hình ảnh/biểu đồ để “đủ chuẩn gửi”
1) Mỗi figure có caption ghi rõ:
   - Dataset (run, energy, selection cuts),  
   - bin width, error bars, thống kê test.  
2) Trục log/linear nhất quán; units đầy đủ.  
3) Nếu là overlay limit (DM), phải ghi rõ đó là **envelope schematic** hay **official curve**.
4) W-mass: phải có figure “compare experiments” (CDF vs ATLAS vs world avg) và **không kết luận** “validated”.

---

## 6) Các file phụ trợ đi kèm (có sẵn trong sandbox)
- `TRXT_Wmass_compare.png` (so sánh W-mass)  
- `TRXT_sigma_q4_vs_q.png` (minh hoạ suppression vs q)  

---

## 7) Việc cần làm ngay (để bạn dán vào bản thảo và gửi)
1) Thay Section W-mass bằng bản “environmental shear” (2.1).  
2) Thay Direct detection bằng EFT (2.2) + thêm figure overlay với LZ/XENONnT.  
3) Thay Appendix Vainshtein bằng bản có $\Lambda_3^3$ và r_V (2.3).  
4) Bổ sung dispersion relation & δ (2.4).  
5) Cập nhật References.

Nếu bạn muốn, bước kế tiếp tôi sẽ:
- (i) tạo hẳn một **“diff patch”** theo cấu trúc file `.tex` (đúng tên section/equation label),  
- (ii) viết `references_v16.bib`,  
- (iii) tạo figure overlay DM với **limit thật** (cần bạn xác nhận dataset curve bạn muốn dùng: LZ 2022/2024 hay XENONnT 2023…).
