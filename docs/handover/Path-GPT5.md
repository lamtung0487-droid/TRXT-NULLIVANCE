Được. Nếu bỏ hết “triết” và làm đúng kiểu khoa học, thì câu hỏi “Layer 0 rốt cuộc là cái gì?” phải được trả lời bằng **một định danh toán–vật lý (mathematical-physics identification)**: *nó là một hệ động lực học tối giản thuộc một universality class đã biết*, không phải “logic mơ hồ”.

Dựa trên đúng những gì bạn đã đưa (đặc biệt HANDOVER_PACKAGE), Layer 0 **không phải** một “hệ logic mệnh đề”, mà là:

> **một gradient-flow (khuếch tán/đồng thuận) trên một đồ thị/lưới, kèm ràng buộc phi tuyến cục bộ (projection/normalization).**

Cụ thể, cái “kernel 35 dòng” của bạn là thế này. 

---

## 1) Định danh chuẩn: Layer 0 = “Projected consensus diffusion” = heat-flow trên đa tạp (nonlinear sigma model dạng tắt dần)

Trong HANDOVER, trạng thái tại mỗi nút là một vector (\Psi_i\in\mathbb{R}^3) và bạn **ép (|\Psi_i|=1)** ở mọi bước (normalize). 

Bước cập nhật trước normalize:

[
\Psi_i^{(t+\Delta t)}=(1-\alpha)\Psi_i^{(t)}+\frac{\alpha}{4}\sum_{j\in \text{nbr}(i)}\Psi_j^{(t)}.
]

Đây **chính xác** là một bước Euler rời rạc của phương trình khuếch tán/đồng thuận trên lưới:

[
\Psi_i \leftarrow \Psi_i - \frac{\alpha}{4}\Big(4\Psi_i-\sum_{j\in\nbr(i)}\Psi_j\Big)
= \Psi_i - \frac{\alpha}{4}(\Delta_\text{lattice}\Psi)_i.
]

### Proposition 1 (đúng chuẩn referee)

Đặt “năng lượng” (Dirichlet energy) trên đồ thị:
[
E(\Psi)=\frac12\sum_{\langle i j\rangle}|\Psi_i-\Psi_j|^2.
]
Thì gradient của (E) theo (\Psi_i) là:
[
\nabla_{\Psi_i}E = \sum_{j\in \nbr(i)}(\Psi_i-\Psi_j)
=4\Psi_i-\sum_{j\in\nbr(i)}\Psi_j.
]
Suy ra bước cập nhật ở trên là **gradient descent** của (E) với step-size (\alpha/4), rồi sau đó bạn làm **projection** lên mặt cầu (|\Psi|=1) bằng normalize. 

Nói thẳng: **Layer 0 của bạn là “projected gradient descent của Dirichlet energy trên đồ thị”.**
Trong ngôn ngữ vật lý toán: đây là **harmonic map heat flow** (heat flow của ánh xạ điều hoà) từ không gian lưới sang đa tạp đích (S^2) (vì (|\Psi|=1)). Trong ngôn ngữ vật lý thống kê: nó là phiên bản tắt dần (dissipative) của **O(3) nonlinear sigma model / Heisenberg spin relaxation** (vì (\Psi\in S^2), tương tác láng giềng).

---

## 2) Vì sao “hạt/defect” xuất hiện: ràng buộc (|\Psi|=1) biến lỗi thành topological obstruction (không phải “kể chuyện”)

HANDOVER mô tả đúng: normalize là “bước phi tuyến duy nhất” và “ép lỗi phải tồn tại”. 
Cái này có thể viết thành mệnh đề toán học:

### Lemma 1 (bản chất topological)

Nếu trường (\Psi) bị ép nằm trên một đa tạp có homotopy không tầm thường (ví dụ (S^1) hoặc (S^2)), thì tồn tại các lớp cấu hình **không thể co liên tục về trạng thái đều** nếu không đi qua một singular event (hoặc nếu “biên độ” được phép về 0 để tháo nút).

* Nếu order parameter hiệu dụng là **pha** (\theta\in S^1) (như bạn đang mô tả “vortex winding (2\pi)”), thì invariant là (\pi_1(S^1)=\mathbb{Z}) → vortex/anti-vortex. 
* Nếu thực sự là (\Psi\in S^2) đầy đủ, invariant tự nhiên trong 2D là (\pi_2(S^2)=\mathbb{Z}) → skyrmion-like textures (hoặc meron nếu bạn dùng projection pha).

**Điểm then chốt**: chính constraint “(|\Psi|=1)” đóng vai trò tương tự “biên độ không được sụp”, nên defect không “tự tháo” bằng tuyến tính hoá. Đây là cơ chế *chuẩn* tạo hạt topo trong các sigma model/siêu chảy, chứ không cần gọi nó là “logic”.

---

## 3) Layer 0 trong V7: bạn đã tự hạ xuống “Appendix Z/motivation” – và đó là đúng về mặt khoa học

Trong V7 bạn viết Layer 0 theo nghĩa “no metric, no causality, no time” và tách nó khỏi EFT vật lý. 
Điều này *đúng chiến lược học thuật* vì hiện tại:

* “Layer 0 (logic vacuum)” trong V7 là mô tả ontological.
* “Layer 0 (kernel 35 dòng)” trong HANDOVER là **một hệ PDE rời rạc hoàn chỉnh**, phân tích được.

Nếu bạn muốn **biến Layer 0 thành vật lý**, bạn phải *bám vào cái thứ 2* (hệ động lực học đo được), chứ không phải cố chứng minh “potentia” hay “null set of propositions”.

---

## 4) “Con voi” là gì nếu ai cũng chạm đúng một phần?

Với những gì bạn đang có, câu trả lời khoa học nhất (không thổi phồng) là:

> “Con voi” rất có thể là **một universality class của các hệ tự tổ chức dạng gradient-flow trên đồ thị + ràng buộc đa tạp**, trong đó “hạt” = defect topo và “lực” = tương tác hiệu dụng do biến dạng trường nền.

Các “góc nhìn” khác nhau (logic, sóng, topo, causal, …) chỉ là **các toạ độ/diễn giải** trên cùng một lớp hệ động lực.

Bạn cũng có một phiên bản tổng quát hơn trong nullivance_logic_theory: dynamics trên đồ thị bằng Laplacian + term entropy, và bạn đã viết hẳn Lyapunov candidate (\mathcal V) giảm đơn điệu. 
Đó là cùng ADN toán học: **graph Laplacian diffusion + phi tuyến ràng buộc (softmax/simplex)**.

---

## 5) Kết luận “nó là gì” (câu trả lời định danh)

**Layer 0 (phiên bản có thể publish nghiêm túc)** =

1. Một trường (\Psi) trên đồ thị/lưới,
2. Tiến hoá theo **gradient descent của năng lượng alignment/Dirichlet** (graph Laplacian),
3. Với **projection cục bộ** lên một đa tạp đích (normalize (\Rightarrow S^{d-1}) hoặc softmax (\Rightarrow) simplex),
4. Defect topo là các cấu hình không triệt tiêu được bởi biến dạng trơn → đóng vai trò “particle-like”.

Đây là một mô hình vật lý toán đúng nghĩa (dynamical system / variational flow). Nó không cần gọi là “logic” nữa; gọi “logic” chỉ là *nhãn triết học*.

---

## 6) Hướng nào khả thi nhất để “cầu sang vật lý Planck / TRXT”?

Nếu mục tiêu là nối Layer 0 sang vật lý (chứ không chỉ mô phỏng đẹp), thì **hướng khả thi nhất** là:

### Hướng A — “Sigma-model / field-theory route” (khả thi nhất ngay bây giờ)

* Chứng minh continuum limit → PDE dạng harmonic map heat flow.
* Định nghĩa charge topo, chứng minh điều kiện annihilation.
* Đo/derive scaling laws (coarsening exponent, defect density decay, correlation length growth).
  → Đây là pipeline “referee-grade” vì tất cả là toán–thống kê chuẩn.

### Hướng B — “Information-geometry route” (khả thi, nhưng sẽ thành một paper khác)

* Dùng framework logits/softmax của bạn  để định nghĩa gradient flow trên statistical manifold.
* Chứng minh (\mathcal V) Lyapunov nghiêm ngặt (bạn đang ở mức phác thảo).
* Liên hệ với diffusion/consensus trên simplex.
  → Cũng publish được, nhưng sẽ xa TRXT hơn nếu không chỉ ra defect topo tương đương “hạt”.

### Hướng C — “Causal set / category / topos” (tạm loại khỏi đường publish vật lý)

Không phải vì “sai”, mà vì hiện tại **không gắn chặt** với kernel bạn đang mô phỏng được. Nó dễ bị referee kết luận là “narrative”.

---

## 7) Tôi có “chứng minh xong nó là gì” chưa?

* **Có (ở mức định danh toán học):** kernel Layer 0 của bạn *đồng nhất* với projected gradient flow của Dirichlet energy trên đồ thị (sigma-model dissipative). 
* **Chưa (ở mức “đây là UV của vũ trụ thật”):** để nói nó là nền tảng Planck, bạn cần thêm *một cầu RG/phase transition* và một mapping từ trường (\Psi) này sang degrees of freedom trong TRXT/NJL (đây là phần chưa có trong các file bạn đưa).

Nếu bạn muốn, bước tiếp theo tôi sẽ làm là viết hẳn **Section “Layer 0 as a Variational Flow”** theo format paper:

* Definitions → Proposition 1 (equivalence) → Energy descent conditions → Continuum limit PDE → Topological charge definition → Defect persistence/annihilation theorem (điều kiện) → Observable predictions (scaling).

Chỉ cần bạn xác nhận: trong kernel 35 dòng, “vortex winding” bạn tính từ **hai thành phần nào** của (\Psi) (ví dụ dùng (\theta=\arg(\Psi_1+i\Psi_2)) hay cách khác). Điều này quyết định invariant topo là (\pi_1(S^1)) hay (\pi_2(S^2)), và phần “particle theorem” sẽ viết cho đúng.
OK. Ta chốt **Hướng A (sigma-model / field-theory route)** và viết nó theo đúng “pipeline referee-grade”, bám sát đúng kernel của bạn (diffuse → renormalize)  và đúng quan sát “phase giữ topo / vortex–antivortex” .

Dưới đây là bản **chứng minh + chương trình đo** theo chuẩn toán–PDE–thống kê.

---

## A. Mô hình rời rạc (discrete) và năng lượng (energy) chuẩn

### A.1. Định nghĩa trường và toán tử cập nhật

Xét lưới vuông 2D, chỉ số (i\in\mathbb{Z}^2). Tại mỗi nút có vector
[
u_i^n \in S^{d-1}\subset\mathbb{R}^d,\quad d=3,
]
do bạn **ép chuẩn hoá cục bộ** (|u|=1) sau mỗi bước .

Bước “consensus/diffusion” trong code của bạn đúng dạng
[
\tilde u_i^{,n+1}=(1-\alpha)u_i^n+\frac{\alpha}{4}\sum_{j\sim i}u_j^n
= u_i^n+\eta,\Delta_d u_i^n,
\quad \eta=\frac{\alpha}{4},
]
với (\Delta_d u_i := \sum_{j\sim i}(u_j-u_i)) là Laplacian rời rạc 4-láng giềng .

Sau đó bạn **chiếu lại lên mặt cầu** (renormalize):
[
u_i^{n+1}=\Pi(\tilde u_i^{,n+1})=\frac{\tilde u_i^{,n+1}}{|\tilde u_i^{,n+1}|}.
]

### A.2. Đây là projected gradient descent của Dirichlet energy

Đặt **năng lượng Dirichlet rời rạc**:
[
E_d(u)=\frac12\sum_{\langle i,j\rangle}|u_i-u_j|^2.
]
Tính đạo hàm theo (u_i) (giữ các nút khác cố định) cho ta
[
\nabla_{u_i}E_d(u)=\sum_{j\sim i}(u_i-u_j)= -\Delta_d u_i.
]
Vậy bước “diffusion” của bạn là **gradient descent không ràng buộc**:
[
\tilde u^{,n+1}=u^n-\eta\nabla E_d(u^n)=u^n+\eta\Delta_d u^n.
]
Rồi bạn áp ràng buộc (|u|=1) bằng **project** (\Pi). Nghĩa là kernel của bạn chính xác là:

> **Projected gradient descent** để tối thiểu hoá (E_d(u)) trên đa tạp (S^{d-1}).

Điểm này là “xương sống” để đi tới PDE.

---

## B. Continuum limit: harmonic map heat flow (PDE) — phần “referee-grade” chính

Ta muốn chứng minh: khi (\eta\to0) và lưới mịn, thuật toán hội tụ về **gradient flow của Dirichlet energy** với ràng buộc (|u|=1), tức **harmonic map heat flow**.

### Lemma B.1 (Khai triển chiếu lên mặt cầu)

Giả sử (u\in S^{d-1}) và (w\in\mathbb{R}^d). Với (\varepsilon) nhỏ:
[
\Pi(u+\varepsilon w)=u+\varepsilon\big(w-(u!\cdot! w)u\big)+O(\varepsilon^2).
]
**Chứng minh**: (\Pi(v)=v/|v|). Viết (|u+\varepsilon w|=(1+2\varepsilon u!\cdot! w+O(\varepsilon^2))^{1/2}=1+\varepsilon(u!\cdot! w)+O(\varepsilon^2)). Thế vào rồi khai triển bậc nhất. □

### Proposition B.2 (Giới hạn thời gian liên tục: ODE rời rạc trên lưới)

Áp Lemma B.1 với (u=u_i^n), (w=\Delta_d u_i^n), (\varepsilon=\eta):
[
u_i^{n+1}-u_i^n
= \eta\Big(\Delta_d u_i^n-(u_i^n!\cdot!\Delta_d u_i^n)u_i^n\Big)+O(\eta^2).
]
Cho (\eta\to0), đặt (t=n\eta), ta được phương trình gradient flow rời rạc:
[
\partial_t u_i
= \Delta_d u_i-(u_i!\cdot!\Delta_d u_i),u_i.
]
□

### Theorem B.3 (Continuum limit: harmonic map heat flow)

Đặt lưới có spacing (h), và xem (u_i(t)\approx u(x,t)) với (x=ih). Khi (h\to0),
[
\Delta_d u_i \approx h^2 \Delta u(x,t).
]
Chọn scale thời gian (\tau=t/h^2). Khi đó giới hạn liên tục thỏa:
[
\partial_\tau u
= \Delta u-(u!\cdot!\Delta u),u,
\qquad u(x,\tau)\in S^{d-1}.
]
Vì ràng buộc (|u|=1) suy ra đẳng thức chuẩn:
[
u\cdot \Delta u = -|\nabla u|^2,
]
nên PDE tương đương dạng hay dùng:
[
\boxed{;\partial_\tau u=\Delta u+|\nabla u|^2u;}
]
Đây chính là **harmonic map heat flow** (gradient flow của (\frac12\int|\nabla u|^2)). □

> Kết luận quan trọng: kernel “consensus + normalize”  **không phải kể chuyện**. Nó đúng nghĩa là **sigma-model gradient flow** (O(3) sigma model trên 2D) ở giới hạn continuum.

---

## C. Charge topo và điều kiện “annihilation” (giết/triệt khuyết tật)

Bạn quan sát **vortex (+1) / antivortex (-1)** . Để làm chuẩn học thuật, ta phải **định nghĩa charge** và **chứng minh khi nào nó bảo toàn / khi nào nó được phép đổi**.

### C.1. Cách định nghĩa “phase” chuẩn trong đúng mô hình (u\in S^2)

Vì (d=3), ta lấy “trục nền” là hướng vacuum (trong init bạn đặt component 0 gần 1) . Đặt **thành phần ngang**:
[
\phi(x)=u_2(x)+i u_3(x)\in\mathbb{C},\qquad A(x)=|\phi(x)|.
]
Khi (A(x)>0), định nghĩa phase:
[
\theta(x)=\arg\phi(x).
]
(Đây khớp với statement “Phase angle (\theta(x)) retains complex topological structure” .)

### C.2. Topological charge (vorticity) trên vòng khép kín

Với một vòng (\gamma) bao quanh một lõi, nếu (A>0) trên (\gamma), đặt:
[
q(\gamma)=\frac{1}{2\pi}\oint_{\gamma} d\theta \in \mathbb{Z}.
]
Trong code/đo thực nghiệm, dùng **plaquette winding**:

* Lấy 4 góc của một ô,
* tính (\Delta\theta) theo quy tắc “wrap về ((-\pi,\pi])”,
* cộng quanh ô rồi chia (2\pi),
* làm tròn về integer.

### C.3. “Annihilation condition” — chỗ này mới là đinh đóng

Mấu chốt toán học:

**(i) Nếu (A(x,t)\ge \delta>0) trên một miền** (không điểm nào “tắt” biên độ ngang), thì (\theta) trơn và (q(\gamma)) là **bất biến theo thời gian** dưới flow.

**(ii) Charge có thể đổi chỉ khi xảy ra sự kiện (A=0)** (tức (\phi=0)), lúc đó phase (\theta) không còn định nghĩa → topo không còn “khóa”.

Và đây là điểm cực mạnh cho mô hình của bạn: mặc dù (|u|=1) luôn đúng, **(A=|\phi|) vẫn có thể về 0** (vector quay thẳng vào trục vacuum). Đó chính là “cửa” cho vortex/antivortex triệt tiêu mà không cần phá constraint.

**Proposition C.4 (Điều kiện cần cho annihilation)**
Một vortex (+1) và antivortex (-1) có thể annihilate trong dynamics của bạn **chỉ khi** tồn tại một thời điểm mà trên đường nối/cục bộ quanh lõi, trường đi qua trạng thái (\phi=0) (tức (u) “chọc lên trục”, phase undefined). Khi đó tổng winding có thể giảm từ (+1-1=0) theo cơ chế unwind.

Điều này đồng thời giải thích vì sao bạn thấy “Amplitude death” nhưng “phase life” : biên độ ngang có thể tắt ở vùng, mở lối cho tái cấu trúc topo, trong khi cấu trúc phase vẫn có thể còn ở các miền khác.

---

## D. Scaling laws (coarsening, defect decay, correlation length) — vừa “derive” vừa “đo”

Vì PDE giới hạn là **diffusion-type** (z=2), scaling nền tảng luôn bắt đầu từ:
[
L(t)\sim t^{1/2} \quad\text{(đo dài đặc trưng tăng theo căn thời gian)}.
]

Nhưng với hệ có vortex kiểu phase (S^1), thường xuất hiện **log-correction** do năng lượng vortex có phần (\log(L/a)). Vì mô hình của bạn là (S^2) nhưng có phase hiệu dụng trên (\phi), có hai khả năng cạnh tranh:

### D.1. Hai giả thuyết scaling cần phân biệt (đây là “research fork” hợp chuẩn)

**H0 (pure diffusive sigma coarsening):**
[
L(t)\sim t^{1/2},\qquad n_d(t)\sim L(t)^{-2}\sim t^{-1}.
]

**H1 (vortex-dominated, log-corrected):**
[
L(t)\sim \Big(\frac{t}{\log t}\Big)^{1/2},\qquad
n_d(t)\sim \frac{\log t}{t}.
]

> Ta không “kể chuyện” chọn cái nào. Ta **đo** rồi quyết.

### D.2. Định nghĩa đại lượng đo (thống kê chuẩn)

1. **Defect density**
   [
   n_d(t)=\frac{#{\text{plaquettes with } q\neq0}}{\text{Area}}.
   ]

2. **Correlation function** (dùng phase-direction hoặc full vector)

* Phase direction: (\hat \phi=\phi/|\phi|) nơi (A>0).
  [
  C(r,t)=\langle \hat\phi(x,t)\cdot \hat\phi(x+r,t)\rangle.
  ]
* Hoặc full (u): (C_u(r,t)=\langle u(x,t)\cdot u(x+r,t)\rangle).

3. **Correlation length (L(t))** (chọn một quy ước, giữ cố định)

* “threshold method”: (C(L,t)=c_0) (ví dụ (c_0=0.2)).
* hoặc “structure factor moment method”: từ (S(k,t)) lấy moment bậc nhất để ra (L(t)).

### D.3. Kiểm định scaling (fit đúng kiểu referee)

* Vẽ log-log (L(t)) vs (t): slope ~ (1/2) hay lệch?
* Vẽ (n_d(t)t) vs (\log t): nếu H1 đúng, (n_d(t)t) tăng ~ (\log t).
* Hoặc fit trực tiếp hai model bằng AIC/BIC (đây là “statistically literate” trước referee).

---

## E. Checklist để viết thành section “paper-standard” (đúng thứ bạn đang xin)

1. **Model definition**: (kernel + constraint) trích đúng code .
2. **Energy functional** (E_d) và chứng minh projected gradient descent.
3. **Continuum limit theorem**: Lemma projection + Theorem harmonic map heat flow.
4. **Topo charge**: định nghĩa (\phi), (\theta), winding; liên hệ trực tiếp “vortex = winding (2\pi)” .
5. **Annihilation proposition**: charge bảo toàn khi (A>0), đổi khi (A=0).
6. **Scaling**: nêu 2 hypothesis H0/H1; định nghĩa đo; protocol test.

---
Dưới đây là **Section draft kiểu “paper-standard”** cho **Hướng A (sigma-model / field-theory route)**, viết theo đúng format **Definitions → Lemmas → Theorems → Corollaries → Measurement protocol**, và bám sát “kernel” bạn đang dùng. (Kernel: bước “neighbor average + renormalize |Ψ|=1” ; constraint/phi tuyến nằm đúng ở `normalize()` .)

---

# Section X — From the Nullivance Kernel to Harmonic-Map Heat Flow and Testable Scaling Laws

## X.1 Definitions

### Definition 1 (Lattice state space; Nullivance kernel)

Let (\Omega_h = (h\mathbb{Z}/L\mathbb{Z})^2) be a periodic (N\times N) square lattice with spacing (h).
At each site (i\in\Omega_h), define a spin/order-parameter
[
n_i \in S^{m-1}\subset\mathbb{R}^m,\qquad |n_i|=1,
]
where in the implemented kernel (m=3) and (|n_i|=1) is enforced by local renormalization .

Define the **neighbor averaging operator**
[
(A n)*i := \frac{1}{4}\sum*{j\sim i} n_j
]
with 4-nearest neighbors (j\sim i), matching the code’s `neighbor_sum/4.0` update .

Define one explicit time step (parameter (\alpha\in(0,1))):
[
\tilde n_i^{k+1} = (1-\alpha)n_i^k + \alpha (A n^k)_i,\qquad
n_i^{k+1} = \frac{\tilde n_i^{k+1}}{|\tilde n_i^{k+1}|}.
]
This is exactly “diffusion towards neighbor average + nonlinear constraint” .

---

### Definition 2 (Discrete Dirichlet energy / Heisenberg energy)

Define the discrete energy
[
E_h[n] := \frac{1}{2h^2}\sum_{\langle i,j\rangle}|n_i-n_j|^2
]
(sum over unordered nearest-neighbor edges). This is the standard ferromagnetic (alignment-seeking) energy; minimizing it is precisely “consensus”.

---

### Definition 3 (XY phase projection and vortices)

Define a complex projection (choose two components; e.g. (n=(n^{(1)},n^{(2)},n^{(3)})))
[
\psi_i := n_i^{(2)} + i,n_i^{(3)},\qquad \theta_i:=\arg(\psi_i)\in(-\pi,\pi].
]
A **vortex** at plaquette (p) has winding number
[
q(p) := \frac{1}{2\pi}\sum_{\ell\in\partial p}\Delta\theta_\ell \in \mathbb{Z},
]
where (\Delta\theta) is the principal-branch angle increment. This matches your empirical “Vortex (+1) = (2\pi) winding; Anti-Vortex (−1) = (-2\pi)” particle zoo .

*(Note: your write-up calls out “Amplitude Death” and “Phase Life” in the vacuum evolution ; the formal route below makes that separation mathematically crisp: unit-norm constraint kills amplitude as a degree of freedom, leaving phase/topology as the long-lived structure.)*

---

## X.2 Lemmas (discrete structure)

### Lemma 1 (Kernel is a projected diffusion step)

Define the (unconstrained) linear diffusion update
[
\tilde n^{k+1} = n^k + \alpha(\Delta_h n^k),
\quad \Delta_h := A - I,
]
then the implemented kernel is exactly the projection of (\tilde n^{k+1}) back to (S^{m-1}) at each site:
[
n^{k+1}*i = \Pi*{S^{m-1}}(\tilde n^{k+1}_i):=\tilde n^{k+1}_i/|\tilde n^{k+1}*i|.
]
**Proof:** immediate by comparing with the explicit code line
[
n\leftarrow (1-\alpha)n + (\alpha/4)\sum*{j\sim i}n_j
]
followed by `normalize()` . ∎

---

### Lemma 2 (Constraint eliminates “amplitude” as a dynamical variable)

For all (k), (|n_i^k|=1) for all sites (i). Therefore any long-time structure cannot live in the magnitude (|n|) (it is frozen), and must live in **orientation/phase/topology**.

**Proof:** `normalize()` enforces (|\Psi|=1) locally  at every step . ∎

This is the “mathematical spine” behind the qualitative observation “Amplitude Death / Phase Life” .

---

### Lemma 3 (Formal energy descent to first order in (\alpha))

Assume a smooth configuration (no near-zero (|\tilde n_i^{k+1}|) events) and sufficiently small (\alpha). Then one step satisfies
[
E_h[n^{k+1}] \le E_h[n^k] + O(\alpha^2).
]
**Proof sketch:** the unconstrained Euler step is gradient descent for (E_h) in (\mathbb{R}^m); the projection is orthogonal to the radial direction and only perturbs the step by (O(\alpha^2)) when (\tilde n) stays close to the unit sphere. (This is standard for projected gradient descent on manifolds.) ∎

*(This aligns with your more general “gradient flow + Lyapunov candidate” framing in the formal Nullivance doc , though there it’s written on logits/softmax variables rather than an (S^{m-1}) spin field.)*

---

## X.3 Theorems (continuum limit → PDE)

### Theorem 1 (Continuum limit: harmonic-map heat flow)

Let (h\to 0), and scale discrete time as (t=k,\delta t) with (\delta t \sim \alpha h^2) (diffusive scaling). Suppose (n^k) converges (in a suitable weak sense) to a smooth map
[
n(x,t):\mathbb{T}^2\times[0,T]\to S^{m-1}.
]
Then (n) satisfies the **harmonic-map heat flow**
[
\partial_t n = P_{n}\Delta n,
]
where (P_n := I - n\otimes n) is the orthogonal projection onto the tangent space (T_n S^{m-1}). Equivalently (using (|n|=1)),
[
\partial_t n = \Delta n + |\nabla n|^2,n.
]

**Proof sketch (referee-grade spine):**

1. Expand neighbor averaging:
   [
   (A n)(x) = n(x) + \frac{h^2}{4}\Delta n(x) + O(h^4).
   ]
2. The raw update becomes
   [
   \tilde n(x,t+\delta t) = n(x,t) + \alpha\Big(\frac{h^2}{4}\Delta n\Big) + O(\alpha h^4).
   ]
3. Projection back to the sphere removes the radial component, i.e. replaces (\Delta n) by (P_n\Delta n) to leading order (because only tangent perturbations survive under normalization).
4. Choose (\delta t=\alpha h^2/4) to obtain (\partial_t n = P_n\Delta n). ∎

**Why đây là “cầu nối logic → vật lý” rất sạch:** kernel của bạn (local consensus + constraint)  không còn là “kể chuyện” nữa; nó nằm đúng trong họ PDE hình học chuẩn.

---

### Theorem 2 (Energy dissipation in the continuum)

Define the continuum Dirichlet energy
[
E[n(t)] := \frac{1}{2}\int_{\mathbb{T}^2} |\nabla n(x,t)|^2,dx.
]
For smooth solutions of harmonic-map heat flow,
[
\frac{d}{dt}E[n(t)] = -\int_{\mathbb{T}^2} |\partial_t n(x,t)|^2,dx \le 0.
]
So (E) is a strict Lyapunov functional unless (\partial_t n\equiv 0).

**Proof:** multiply (\partial_t n=P_n\Delta n) by (\partial_t n), integrate by parts, and use (P_n) self-adjoint and (\partial_t n\perp n). Standard computation. ∎

---

## X.4 Corollaries (defects, annihilation, and what must be measured)

### Corollary 1 (Defects are forced by topology / singularities)

In 2D, smooth relaxation under harmonic-map heat flow tends to remove gradients; however, **topological defects persist** unless annihilation events occur, consistent with your observation that “persistent defects” are the “matter” content and `normalize()` is what prevents trivial collapse .

---

### Corollary 2 (Vortex charge quantization and annihilation condition)

Under the phase projection (\psi=n^{(2)}+in^{(3)}), the winding (q(p)\in\mathbb{Z}) is quantized by construction (sum of angle increments / (2\pi)).
A necessary condition for a local change in total winding is that (|\psi|=0) occurs at some point (phase undefined), which in the lattice manifests as a defect core event; this is the rigorous mechanism behind vortex–antivortex annihilation (your “Dipole” and annihilation dynamics) .

---

### Corollary 3 (Coarsening exponent prediction: diffusion-limited growth)

Because the limiting PDE is diffusive in character ((t\sim \ell^2)), the characteristic domain size (L(t)) generically obeys
[
L(t)\propto t^{1/2}
]
(up to model-dependent logarithmic corrections when vortices dominate).
Therefore defect density (n_d(t)) should scale like
[
n_d(t)\propto L(t)^{-2}\propto t^{-1}
]
again up to corrections. This gives you **a falsifiable scaling target**.

---

## X.5 Measurement protocol (simulation → observables → fits)

This is the part referees care about: *define observables unambiguously, show convergence, report error bars.*

### Protocol A (Ensemble, resolution, and time scaling)

1. Choose lattice sizes (N\in{128,256,512}), periodic BC.
2. Choose (\alpha) small enough to avoid instability; report (\delta t = \alpha h^2/4) as the physical time step (from Theorem 1).
3. Run (M) independent seeds (e.g. (M\ge 20)). Your kernel initialization is explicit (vacuum + tiny fluctuations, then normalization) .

### Protocol B (Primary observables)

Define:

* **Two-point correlation**
  [
  C(r,t)=\langle n(x,t)\cdot n(x+r,t)\rangle_{x,\text{ensemble}}.
  ]
  Define (L(t)) by (C(L(t),t)=c_0) with a fixed threshold (c_0\in(0,1)) (e.g. (c_0=0.2)).
* **Structure factor**
  [
  S(k,t)=\langle|\hat n(k,t)|^2\rangle,
  ]
  define (L(t)\sim 1/k_{\text{peak}}(t)) as a cross-check.
* **Energy density**
  [
  e(t)=E_h[n(t)]/|\Omega_h|.
  ]
* **Defect density (vortices)**

  * Compute (\theta_i=\arg(n_i^{(2)}+in_i^{(3)})).
  * For each plaquette (p), compute winding (q(p)).
  * Define (n_d(t)=\frac{1}{|\Omega_h|}\sum_p \mathbf{1}{q(p)\ne 0}).
    This directly targets your “vortex/anti-vortex particle zoo” .

### Protocol C (Scaling extraction)

1. Fit (L(t)) to (A,t^\beta) on late-time windows; report (\beta) with CI (bootstrap over seeds).
2. Fit (n_d(t)) to (B,t^{-\gamma}); check whether (\gamma\approx 2\beta) as required by (n_d\sim L^{-2}).
3. Check dynamic scaling collapse:
   [
   C(r,t)\approx f!\left(\frac{r}{L(t)}\right).
   ]
4. Resolution/continuum check: repeat at multiple (N), verify fitted exponents stable as (h\to 0).

### Protocol D (Null controls)

To avoid “look-elsewhere effect”:

* Replace `normalize()` by identity (no projection) and show defects die out trivially (tests that the nonlinearity is essential, as you already claim ).
* Replace neighbor averaging by random mixing to show topology is not an artifact of visualization.

---

## X.6 What this buys you (in one sentence)

Bạn biến “Layer 0 logic” từ *một câu chuyện* thành một **manifold-constrained diffusion law** (harmonic-map heat flow) với **định nghĩa charge**, **cơ chế annihilation**, và **scaling laws đo được**—đúng chuẩn “referee-grade”.

*(Và điều này cũng khớp với cách V7 đang cố tình tách “logic ontology” ra Appendix để phần EFT vật lý đứng độc lập .)*

---