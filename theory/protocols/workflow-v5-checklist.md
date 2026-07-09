---
description: workflow-v5-checklist
---


 0) Luật tổng quát (bắt buộc trước khi viết một dòng “lý thuyết”)

1. YÊU CÂU PHẢI tuyên bố rõ “đối tượng vật lý” của mô hình: hạt? trường? hình học? thông tin? hay một biến ẩn?
2. YÊU CÂU PHẢI chỉ ra “đại lượng đo được” (observables) và map chúng tới thực nghiệm: cross section, tần số, phổ, độ lệch pha, hệ số khuếch tán, phổ nhiễu, v.v.
3. YÊU CÂU PHẢI tách bạch ba tầng:

    Kinematical structure (không gian trạng thái, đối xứng, biến)
    Dynamical law (action/Lagrangian/Hamiltonian và EoM)
    Measurement/phenomenology (quan sát được, thống kê, sai số, dự đoán)
4. YÊU CÂU PHẢI ghi “điều kiện thất bại” của mô hình: khi nào mô hình không áp dụng (thang năng lượng, mật độ, độ cong, nhiệt độ, số hạt, mạnh/yếu tương tác).

---

 1) Nền tảng Tiên đề (Axiomatic Foundation)

 1.1. Chọn không gian toán học: bạn đang “chơi” trò nào?

YÊU CÂU PHẢI chọn chính xác một trong các khung sau (hoặc nêu rõ cách ghép và điều kiện tương thích):

 (A) Cơ học cổ điển (Hamilton/Lagrange)

 Cấu hình: đa tạp (Q), toạ độ (q^i).
 Động lực học: Lagrangian (L(q,\dot q,t)) hoặc Hamiltonian (H(q,p,t)).
 YÊU CÂU PHẢI xác định: cấu trúc symplectic (\omega) trên (T^Q), và Poisson bracket.

 (B) Trường cổ điển (Classical Field Theory)

 Trường: (\phi^a(x)) trên không-thời gian (M).
 Action: (S[\phi]=\int_M d^dx,\mathcal{L}(\phi,\partial\phi,\ldots)).
 YÊU CÂU PHẢI xác định: miền biến thiên, điều kiện biên, bậc đạo hàm cao nhất (để tránh bệnh Ostrogradsky trừ khi có cơ chế ràng buộc).

 (C) Lượng tử (QM)

 Không gian trạng thái: Hilbert space (\mathcal{H}).
 Observable: toán tử tự liên hợp (self-adjoint) trên miền xác định rõ.
 Động lực học: Hamiltonian tự liên hợp (H) sinh ra nhóm đơn vị (U(t)=e^{-iHt}).
 YÊU CÂU PHẢI chứng minh: tính tự liên hợp (không chỉ “Hermitian” hình thức) và tính unitarity.

 (D) Trường lượng tử (QFT)

 Kinematical: trường toán tử/đại số quan sát (algebraic QFT) hoặc đường tích phân (path integral).
 YÊU CÂU PHẢI tuyên bố: bạn dùng Minkowski hay Euclidean; nếu Wick rotation, phải chỉ điều kiện hợp lệ.
 YÊU CÂU PHẢI xác định: nội dung hạt (spectrum), không gian Fock (nếu thích hợp), và điều kiện vi mô (microcausality).

 1.2. Tiên đề tối thiểu (tùy khung, nhưng không được thiếu)

YÊU CÂU PHẢI viết ra như một danh sách hữu hạn. Không “ý tưởng chung chung”. Tối thiểu gồm:

1. Tập biến cơ bản (fields/coordinates/operators) và miền giá trị.
2. Nhóm đối xứng cơ bản (G) và cách nó tác động lên biến.
3. Nguyên lý động lực học: cực trị action / phương trình Schrödinger / phương trình Heisenberg.
4. Nguyên lý nhân quả / điều kiện lan truyền (cổ điển: hyperbolic PDE; lượng tử: microcausality; hoặc tuyên bố rõ bạn từ bỏ nhân quả chuẩn và trả giá gì).
5. Định nghĩa năng lượng và điều kiện ổn định (Hamiltonian bị chặn dưới).
6. Quy tắc ghép với nguồn/thiết bị đo: cách sinh ra correlators, cross sections, hoặc các đại lượng thực nghiệm.

---

 2) Checklist Nhất quán Nội tại (Internal Consistency Checklist)

Đây là những “bài kiểm tra chết người”. Không qua: mô hình bị loại trước khi chạm thực nghiệm.

 2.1. Phân tích thứ nguyên và thang (Dimensional analysis & scaling)

 YÊU CÂU PHẢI gán thứ nguyên cho mọi biến, hằng số, và tham số.
 YÊU CÂU PHẢI chứng minh: (\mathcal{L}) có thứ nguyên đúng (ví dụ trong (d=4): ([\mathcal{L}]=\text{energy}^4) trong (c=\hbar=1)).
 YÊU CÂU PHẢI liệt kê tất cả các thang: (M_), (\Lambda), (m), chiều dài đặc trưng, và regime hiệu lực.

 2.2. Tính xác định của bài toán (Well-posedness)

 YÊU CÂU PHẢI chứng minh: phương trình chuyển động có bài toán Cauchy đặt được (ít nhất trong miền quan tâm): hyperbolic/elliptic đúng chỗ; điều kiện biên hợp lệ.
 Nếu có đạo hàm bậc cao: YÊU CÂU PHẢI chứng minh không có bậc tự do ma (ghost) hoặc có ràng buộc loại bỏ.

 2.3. Unitarity / Positivity / Stability

 YÊU CÂU PHẢI chứng minh Hamiltonian bị chặn dưới (ổn định chân không).
 YÊU CÂU PHẢI kiểm tra dấu của kinetic term: không tachyon (khối lượng bình phương âm) trừ khi bạn chủ ý có phá vỡ đối xứng và vẫn kiểm soát được.
 QFT: YÊU CÂU PHẢI chứng minh ma trận tán xạ (S) đơn vị (hoặc ít nhất: Optical theorem ở bậc nhiễu loạn bạn xét).

 2.4. Đối xứng và bất biến (Symmetry & invariance)

 YÊU CÂU PHẢI viết rõ biến đổi đối xứng: toàn cục/địa phương, liên tục/rời rạc.
 YÊU CÂU PHẢI chứng minh action bất biến (hoặc biến đổi theo total derivative).
 YÊU CÂU PHẢI suy ra dòng Noether (J^\mu) và phương trình bảo toàn (\partial_\mu J^\mu=0) (trên-shell).
 Nếu đối xứng gauge: YÊU CÂU PHẢI chứng minh độc lập gauge của đại lượng quan sát (gauge-invariant observables).

 2.5. Ràng buộc và số bậc tự do (Constraints & DOF counting)

 YÊU CÂU PHẢI làm Dirac constraint analysis nếu có gauge/đẳng cấu.
 YÊU CÂU PHẢI đếm số bậc tự do vật lý (physical DOF) và chỉ ra chúng khớp với phổ bạn tuyên bố.

 2.6. Nhân quả và vận tốc truyền (Causality)

 Trường cổ điển: YÊU CÂU PHẢI kiểm tra đặc trưng (characteristics) không cho siêu quang tùy tiện (trừ khi có cơ chế và hệ quả rõ).
 QFT: YÊU CÂU PHẢI kiểm tra microcausality ([\phi(x),\phi(y)]=0) cho khoảng cách không-thời gian dạng spacelike (tùy formalism).

 2.7. Tính nhất quán lượng tử (nếu lượng tử hoá)

 YÊU CÂU PHẢI chỉ ra quy trình lượng tử hoá: canonical, path integral, hoặc algebraic—và chứng minh tương đương trong regime cần thiết.
 Nếu gauge: YÊU CÂU PHẢI đưa gauge-fixing, Faddeev–Popov/BRST, và kiểm tra nilpotency BRST (nếu dùng).

---

 3) Checklist Nhất quán Ngoại tại và Giới hạn (External Consistency & Limits)

Một lý thuyết mới không được “phủ định mọi thứ” bằng lời nói. Nó phải co lại đúng chỗ.

 3.1. Giới hạn cổ điển (Classical limit)

 YÊU CÂU PHẢI chứng minh: khi (\hbar\to 0) (hoặc hành động lớn so với (\hbar)), mô hình hồi về động lực học cổ điển tương ứng (stationary phase / WKB).
 Nếu mô hình sửa QM: YÊU CÂU PHẢI cho điều kiện để phục hồi phương trình Schrödinger chuẩn.

 3.2. Giới hạn Newton (weak-field, low-velocity)

Nếu mô hình liên quan hấp dẫn/hình học:

 YÊU CÂU PHẢI chứng minh trong (v\ll c), trường yếu, thế hấp dẫn nhỏ:

   phương trình chuyển động cho hạt thử → ( \ddot{\mathbf{x}}=-\nabla \Phi)
   và (\Phi) thỏa Poisson (\nabla^2\Phi = 4\pi G\rho) (hoặc dạng sửa đổi có giới hạn (G_{\rm eff}\to G)).

 3.3. Giới hạn tương đối tính (Lorentz invariance)

 Nếu bạn tuyên bố Lorentz bất biến: YÊU CÂU PHẢI chứng minh action hoặc đại lượng quan sát bất biến Lorentz.
 Nếu bạn phá vỡ Lorentz: YÊU CÂU PHẢI định lượng mức phá vỡ và so với cận thực nghiệm (không được nói “nhỏ” mà không có tham số và bound).

 3.4. Giới hạn QFT chuẩn / SM (nếu liên quan hạt)

 YÊU CÂU PHẢI chỉ ra regime năng lượng mà mô hình hiệu dụng hồi về Lagrangian chuẩn (ít nhất phần đã đo cực tốt).
 YÊU CÂU PHẢI chứng minh mọi hiệu chỉnh mới bị triệt theo ((E/\Lambda)^n) hoặc tham số nhỏ rõ ràng.

 3.5. Asymptotic limits bắt buộc

YÊU CÂU PHẢI tính tối thiểu các giới hạn:

1. IR limit (E\to 0): có singularity không? có hạt không khối lượng gây IR divergence không?
2. UV limit (E\to \infty): lý thuyết chạy về đâu (fixed point, Landau pole, hay breakdown ở (\Lambda))?
3. Decoupling: khi khối lượng một trường (M\to\infty), nó có rút khỏi động lực học thấp năng lượng không (Appelquist–Carazzone)?

---

 4) Khả năng Kiểm chứng và Bác bỏ (Falsifiability, Popper)

Không ai cần “một khung triết học đẹp”. Bạn cần các mệnh đề có thể bị đo sai.

YÊU CÂU PHẢI đưa ít nhất 3 dự đoán định lượng dạng:

 đại lượng (O)
 giá trị dự đoán (O_{\rm th}(\theta)) kèm tham số (\theta)
 độ chính xác cần thiết (\Delta O) để phân biệt với lý thuyết chuẩn
 thiết lập đo (thực nghiệm/quan sát) và nguồn sai số chính.

Dưới đây là ba “khuôn” dự đoán bắt buộc (bạn điền bằng mô hình của bạn; nếu không điền được, mô hình chưa phải lý thuyết vật lý):

 4.1. Dự đoán phổ (spectrum) hoặc dịch chuyển tần số

 YÊU CÂU PHẢI tính: hiệu chỉnh mức năng lượng/tần số (\delta \omega(\theta)) cho một hệ chuẩn (nguyên tử, dao động, cavity, interferometer).
 YÊU CÂU PHẢI chỉ ra: (\delta \omega/\omega) lớn nhất ở regime nào và có thể đo bằng kỹ thuật nào (đồng hồ nguyên tử, quang phổ chính xác, interferometry).

 4.2. Dự đoán tán xạ/cross section hoặc tỷ lệ phân rã

 YÊU CÂU PHẢI tính: hiệu chỉnh quan sát được (\delta\sigma(E,\theta)) hoặc (\delta\Gamma(\theta)).
 YÊU CÂU PHẢI đưa: chữ ký (signature) rõ ràng: góc tán xạ, phụ thuộc năng lượng, phân cực, bất đối xứng CP, v.v.

 4.3. Dự đoán về lan truyền/pha (propagation/phase)

 YÊU CÂU PHẢI tính: quan hệ tán sắc (\omega(k)) hoặc vận tốc nhóm (v_g) (nếu có sửa đổi).
 YÊU CÂU PHẢI đề xuất: phép đo time-of-flight, pha giao thoa, hoặc chuẩn đồng bộ thời gian; và mức cận cần đạt.

Quy tắc Popper:

 YÊU CÂU PHẢI viết ra “điều kiện loại bỏ”: nếu đo được (O) nằm ngoài khoảng nào thì mô hình bị bác bỏ (không được “fit lại” bằng cách thêm tham số mới sau khi có dữ liệu, trừ khi bạn tuyên bố đó là một mô hình hiệu dụng mở).

---

 5) Quy trình Phản biện Toán học: câu hỏi Socratic “đau”

Trước khi công bố, YÊU CÂU PHẢI trả lời được bằng công thức, không bằng văn.

1. Bạn có thể viết mô hình trong một dòng action không? Nếu không, bạn chưa có lý thuyết—bạn có mô tả.
2. Tham số của bạn có ý nghĩa vật lý hay chỉ là núm vặn để fit? Nêu phép đo độc lập để xác định từng tham số.
3. Bạn đã chứng minh mô hình có giới hạn chuẩn chưa? Chỉ ra phép lấy giới hạn bằng toán, không bằng lời.
4. Nếu tôi đổi hệ tọa độ / gauge / biểu diễn, dự đoán có đổi không? Nếu có: bạn đang đo artefact.
5. Nghiệm của bạn ổn định không? Một nhiễu nhỏ có nổ tung không? (linear stability, mode analysis).
6. Có ghost/tachyon không? Nếu có, cơ chế loại bỏ là gì? Bạn phải chỉ ra trong phổ.
7. Bạn có vi phạm định lý nền nào không? (Noether, CPT, spin-statistics, energy conditions, v.v.) Nếu có, giá phải trả là gì và bạn kiểm soát ra sao?
8. Bạn có thể chỉ ra một phép tính “không thể né” mà mọi referee sẽ hỏi? (renormalization, anomaly, unitarity bound, dispersion relation). Làm trước.
9. Mô hình có dự đoán mới độc lập tham số không? Nếu mọi thứ đều “tùy tham số”, nó không sắc.
10. Trong regime bạn tuyên bố, bạn có thể ước lượng sai số lý thuyết không? (cắt chuỗi nhiễu loạn, EFT truncation, numerical error).

---

 Ma trận Kiểm tra Độ vững chắc Toán học (Mathematical Robustness Test Matrix)

Hãy coi đây là “bảng chấm sống sót peer-review”.
YÊU CÂU PHẢI điền trạng thái cho từng dòng: (i) đã chứng minh, (ii) đang làm, (iii) không áp dụng—và nếu (iii) phải giải thích.

 A. Hình thức luận (Formalism)

1. YÊU CÂU PHẢI xây dựng action (S) hoặc Hamiltonian (H) rõ ràng.
2. YÊU CÂU PHẢI suy ra phương trình chuyển động bằng nguyên lý biến phân (Euler–Lagrange) hoặc phương trình Hamilton/Heisenberg.
3. YÊU CÂU PHẢI kiểm tra:

    tính cục bộ (locality) hoặc tuyên bố rõ nonlocality và hệ quả;
    điều kiện biên và các hạng bề mặt (boundary terms).
4. YÊU CÂU PHẢI chứng minh: năng lượng xác định và điều kiện ổn định (bounded below).

 B. Phân tích nhiễu loạn và ổn định (Perturbation & Stability)

1. YÊU CÂU PHẢI tuyến tính hoá quanh nghiệm nền (vacuum/background) và tìm phổ mode.
2. YÊU CÂU PHẢI chứng minh:

    không có mode với tăng trưởng mũ không kiểm soát (instability) trong miền áp dụng;
    điều kiện ổn định năng lượng bậc hai (positivity of quadratic form).
3. YÊU CÂU PHẢI tính: miền hội tụ/tiệm cận của chuỗi nhiễu loạn; và chỉ ra tham số nhỏ thực sự là gì.
4. Nếu có soliton/topological sector: YÊU CÂU PHẢI chứng minh ổn định topo hoặc điều kiện BPS (nếu có).

 C. Nhóm đối xứng và Noether (Symmetry Groups)

1. YÊU CÂU PHẢI xác định nhóm đối xứng (G): ví dụ (U(1)), (SU(2)), (SU(3)), Lorentz/Poincaré, diffeomorphism, hoặc nhóm rời rạc (P, T, C).
2. YÊU CÂU PHẢI viết representation của trường dưới (G).
3. YÊU CÂU PHẢI suy ra các dòng Noether và điện tích bảo toàn.
4. Nếu là gauge: YÊU CÂU PHẢI thực hiện gauge fixing và chỉ ra observable gauge-invariant.
5. YÊU CÂU PHẢI kiểm tra anomaly: nếu có anomaly phá đối xứng gauge → mô hình chết (trừ khi bạn có cơ chế triệt).

 D. Chuẩn hoá và vô hạn (Renormalizability / EFT discipline)

Nếu là QFT:

1. YÊU CÂU PHẢI phân tích power counting: thứ nguyên của toán tử, phân loại relevant/margina