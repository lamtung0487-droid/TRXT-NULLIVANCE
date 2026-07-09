# TRXT–Nullivance – Tổng hợp toàn bộ nghiên cứu đến hiện tại

Tài liệu này gom lại đầy đủ: **giả thuyết**, **mô hình/khung lý thuyết**, **các biến và phương trình**, **quy trình thực nghiệm** bạn đã chạy (Cobaya/CLASS MCMC + Nullivance FFT/BAO-metric), **tiêu chí pass/fail**, và **các lỗi đã gặp + cách xử lý chuẩn**. Mục tiêu là để bạn mở tab khác và tiếp tục nghiên cứu mà không phải nhớ lại từ các đoạn chat rời.

---

## 0) Mục tiêu nghiên cứu

### Mục tiêu A (chuẩn hoá vũ trụ học)
Thiết lập **baseline** bằng dữ liệu thật (Planck 2018 + BAO SDSS DR12 + Pantheon SN) để có mốc so sánh.

**Output cần có**
- Posterior cho các tham số nền: \(\omega_b,\omega_{cdm},H_0,\tau,A_s,n_s\) (+ các derived: \(\sigma_8\), \(S_8\), \(\Omega_m\), \(r_s\) nếu bật).
- \(\chi^2\) theo từng likelihood (CMB lowl/highl, lensing, BAO, SN).

### Mục tiêu B (proxy giảm \(S_8\))
Kiểm tra một **proxy** có thể làm giảm \(S_8\) mà vẫn giữ fit CMB/BAO/SN.

Bạn đã chạy một proxy dạng **\(\nu\Lambda\)CDM**: thêm \(\sum m_\nu\) (tham số `m_ncdm`) để xem xu hướng \(S_8\) giảm.

Lưu ý quan trọng: proxy này **không phải** IDE (tương tác DE–DM). Nó là **mô hình khác họ**, nhưng hợp lệ để kiểm tra “liệu có đường giảm \(S_8\) mà không phá BAO/CMB không”.

### Mục tiêu C (Nullivance “rung nền”)
Xây mô hình **trường rung nội sinh** (FFT) tạo phổ \(P(k)\) và so khớp với \(P(k)\) của CLASS.

Tầng này bạn đã làm được:
- `nullivance_fft.py` fit shape mạnh (r ~ 0.98).
- `nullivance_match_planck.py` chỉ ra mismatch vị trí wiggle (BAO node) ban đầu.
- `nullivance_fft_bao.py` thêm ràng buộc BAO và giảm sai lệch xuống ~ 9.9% theo metric \(\Delta k\).

**Vấn đề hiện tại:** BAO precision thật yêu cầu ~<1% trên thước đo, nên 9.9% vẫn chưa đạt chuẩn. Do đó phải quay lại bước MCMC full trên dữ liệu thật (Cobaya/CLASS) cho proxy vật lý (IDE thật hoặc proxy khác) thay vì chỉ “fit \(P(k)\) mô phỏng”.

---

## 1) Giả thuyết TRXT–Nullivance (bản tóm tắt kỹ thuật)

### 1.1 Ý tưởng lõi
- Có một **trường/đại lượng nền** \(\Phi\) (hoặc tập biến rung) vận hành nội sinh.
- Cấu trúc phổ \(P(k)\) quan sát được (đặc biệt hình dạng + wiggles) có thể được tái tạo (hoặc xấp xỉ) bởi một **kernel rung** gồm thành phần nền + cắt + dao động.
- Nếu mô hình nội sinh tạo ra **đúng shape** và **đúng thước đo BAO** (hoặc tương đương), thì có cơ sở xem nó là một mô tả hiệu dụng có ý nghĩa.

### 1.2 3 phản biện “chí mạng” và điều kiện sống còn
- Photon bị bẻ cong bởi **metric**, không phải \(\Phi\) kéo trực tiếp.
- Nếu \(\Phi\) là spin-0: không được thay spin-2, chỉ được tác động qua metric hiệu dụng/screening.
- Nếu \(\Phi\) chỉ là thêm năng lượng vào \(T_{\mu\nu}\): rơi về quintessence. “Hồn cốt” chỉ có nếu \(\Phi\) tham gia cơ chế **tiền–hình học** sinh metric hiệu dụng.

---

## 2) Baseline dữ liệu thật: Cobaya + CLASS + Planck/BAO/SN

### 2.1 Bạn đã hoàn tất: LCDM baseline
Bạn đã chạy một chuỗi MCMC và đọc được thống kê (GetDist) với các biến như:
- `omega_b`, `omega_cdm`, `H0`, `tau_reio`, `A_s`, `n_s`, `A_planck`
- `chi2__...` theo từng likelihood

Lưu ý: GetDist output hiển thị `A_s = 0.00000 ± 0.00000` là do format/scale hoặc bạn đang in sai định dạng; `A_s` bản chất ~2e-9.

### 2.2 Vì sao chạy lâu
Mỗi bước MCMC:
1) Cobaya đề xuất bộ tham số mới.
2) CLASS chạy nền + perturbations → tính \(C_\ell\), lensing, \(P(k)\) tại các z.
3) Likelihood Planck high-l + low-l + lensing + BAO + SN tính loglike.
4) MCMC accept/reject.

Planck high-l là nặng, nên hàng trăm ngàn bước có thể kéo dài nhiều giờ đến ngày.

### 2.3 Lỗi “covmat not positive definite” (đã gặp ở LCDM)
Đây thường là vấn đề tạm thời khi Cobaya cập nhật covmat trong giai đoạn học. Nếu chạy vẫn tiếp và cuối cùng “The run has converged!” thì coi là **không chết**.

---

## 3) Proxy giảm S8: \(\nu\Lambda\)CDM (m_ncdm) – file YAML bạn đang chạy

### 3.1 Trạng thái thực tế
File bạn chạy tên “ide_proxy…” nhưng nội dung là **\(\nu\Lambda\)CDM**:
- Thêm `m_ncdm` (\(\sum m_\nu\))
- Không có tham số IDE (xi0, s_xi).

=> Gemini đúng ở chỗ “không phải IDE”. Nhưng chạy proxy \(m_\nu\) vẫn có ích: nó là một đường kiểm tra nhanh xem có giảm \(S_8\) mà không phá fit không.

### 3.2 Lỗi “chain stuck for 280 attempts”
Ý nghĩa:
- Chuỗi đang ở vùng mà phần lớn proposal cho posterior **không finite** (CLASS fail hoặc likelihood trả NaN/inf) và bị reject liên tục.
- Sau N lần không thoát được, Cobaya dừng để tránh treo vô hạn.

Nguyên nhân điển hình (theo đúng log bạn thấy):
- `ref` (điểm khởi tạo) quá xa vùng tốt.
- proposal width cho tham số “không có covmat ban đầu” (H0, A_s, m_ncdm) quá rộng, dẫn đến nhảy vào vùng invalid.
- prior/giới hạn rộng → dễ rơi vào biên/miền không ổn định.

Cách xử lý chuẩn:
1) Làm `ref` chặt hơn quanh nghiệm LCDM baseline.
2) Gán `proposal` (độ rộng bước) nhỏ cho các tham số thiếu covmat.
3) Giảm `proposal_scale` (ví dụ 0.3–0.7).
4) Bật `max_tries` lớn hơn (không khuyến khích) nếu cần.

### 3.3 Lỗi “Old and new run info not compatible” khi resume
Nguyên nhân:
- Bạn đã sửa YAML (params/prior/order) nhưng giữ nguyên output prefix.
- Cobaya bảo không thể resume vì metadata khác.

Cách chuẩn:
- Nếu đổi YAML đáng kể: **đổi output prefix** (ví dụ `runs/ide_proxy_w0nu_v2`) hoặc xóa sạch `runs/<prefix>*`.
- Nếu muốn cứu run cũ: dùng `--allow-changes` (rủi ro), hoặc tốt nhất giữ YAML y nguyên khi resume.

---

## 4) Nullivance FFT: mô hình nội tại tạo phổ \(P(k)\)

### 4.1 Pipeline đã chạy
1) Lấy tham số “best-fit” từ baseline (hoặc từ chain): \(\omega_b,\omega_{cdm},H_0,n_s,\tau,A_s\).
2) CLASS tạo \(P(k)\) mục tiêu trên dải k.
3) Nullivance tạo trường rung 2D/3D bằng FFT:
   - Sinh phổ Fourier theo kernel tham số \(\theta\)
   - IFFT ra trường thực
   - Ước lượng isotropic power spectrum \(P_{null}(k)\)
4) Fit \(\theta\) để tối thiểu hoá sai lệch \(\log P\).

### 4.2 Kết quả bạn đã đạt
- Fit shape: r ~ 0.983, MSE ~4e-2 (logP)
- Mismatch BAO node ban đầu: \(k_{osc,null}\) lệch lớn.
- Sau phiên bản BAO-aware + sửa đơn vị + metric \(\Delta k\):
  - \(\Delta(\Delta k)/\Delta k_{class} \approx 0.099\) (≈ 9.9%).

### 4.3 Diễn giải đúng (không tô hồng)
- 9.9% là **tiến bộ lớn** so với ~70% lệch.
- Nhưng vẫn **chưa đạt precision cosmology**. BAO measurement thường nhắm ~<1% (tuỳ dataset/combination).
- Do đó Nullivance FFT hiện tại là **một proof-of-concept hình dạng**, chưa đủ làm mô hình thay thế/đối thủ LCDM.

### 4.4 Vấn đề kỹ thuật gốc làm BAO lệch
Các nguyên nhân khả dĩ (theo đúng những gì bạn đã thấy):
- Kernel dao động (kosc/phase) đang “tự do” nên có thể fit shape mà đặt wiggle sai.
- Metric đo BAO chưa đúng vật lý (BAO liên quan r_s và transfer function baryon-photon).
- Mô hình rung thiếu thành phần vật lý bắt buộc (baryon drag, sound horizon imprint), nên wiggle không “neo” đúng chỗ.

=> Fix đúng hướng là: thay vì ép wiggle bằng penalty, cần **neo thước đo** bằng một tham số tương đương \(r_s\) hoặc một mapping k→k’ gắn với physics.

---

## 5) Quy trình kiểm nghiệm “đúng chuẩn” bạn đang hướng tới

### Pha 1: Baseline (đã làm)
- Chạy LCDM (Planck+BAO+SN) → lấy posterior + \(\chi^2\).

### Pha 2: Proxy / mô hình mở rộng (đang làm)
Hai nhánh lựa chọn:

**Nhánh 2A: \(\nu\Lambda\)CDM (m_ncdm)**
- Mục tiêu: kiểm tra đường giảm \(S_8\) và tác động lên BAO/CMB.
- Pass nếu: \(\Delta\chi^2\) không xấu đi đáng kể và \(S_8\) giảm theo mục tiêu.

**Nhánh 2B: IDE thật (xi0, s_xi)**
- Mục tiêu: kiểm tra giả thuyết proxy IDE theo hồ sơ gốc.
- Cần: mô hình/param IDE phải tồn tại trong CLASS hoặc patch CLASS.
- Pass nếu: fit BAO/CMB/SN tốt và \(S_8\) được điều chỉnh mà không phá r_s/BAO.

### Pha 3: Cầu nối sang Nullivance
- Nullivance FFT phải tái tạo **shape + BAO scale** trong ngưỡng sai số mục tiêu.
- Nếu không đạt, Nullivance chỉ là mô hình “shape generator”, không phải mô hình vũ trụ học precision.

---

## 6) Hướng dẫn thao tác Ubuntu tối thiểu (để bạn không bị kẹt)

### 6.1 Mở lại môi trường và chạy tiếp
```bash
cd ~/cosmo_test
source ~/cosmoenv/bin/activate
cobaya-run ide_proxy_w0nu.yaml --allow-changes
```
- `--allow-changes` chỉ dùng khi YAML thay đổi nhưng vẫn muốn resume. Tốt hơn là giữ YAML y nguyên.

### 6.2 Theo dõi tiến độ
```bash
tail -f runs/ide_proxy_w0nu_v1.progress
```
Hoặc xem file chain:
```bash
ls -lh runs/ide_proxy_w0nu_v1*.txt
```

### 6.3 Nếu muốn “chạy lại sạch”
```bash
rm -rf runs/ide_proxy_w0nu_v1*
```
Sau đó chạy lại.

---

## 7) Tiêu chí đánh giá kết quả (pass/fail)

### 7.1 Với MCMC Cobaya
- Hội tụ: `Rminus1_stop <= 0.01` (hoặc chặt hơn).
- Acceptance rate hợp lý (thường 0.2–0.6, nhưng 0.7 vẫn có thể xảy ra tuỳ blocking).
- Posterior stable, không stuck.

### 7.2 Với fit Nullivance FFT
- Shape: r(logP) > 0.98 là tốt.
- Nhưng bắt buộc thêm: BAO scale error < 1% nếu muốn “precision”.

---

## 8) Trả lời ngắn cho câu “tôi đang ở giai đoạn nào”

- Khi bạn chạy `lcdm_planck_desi` và đã ra thống kê GetDist: bạn đã xong **Pha 1 baseline**.
- Khi bạn chạy `ide_proxy_w0nu_v1` với `m_ncdm`: bạn đang ở **Pha 2 proxy giảm S8 (nhánh \(\nu\Lambda\)CDM)**.
- Khi bạn chạy `nullivance_fft.py` / `*_bao.py`: bạn đang ở **Pha 3 proof-of-concept rung nền**.

---

## 9) Việc cần làm tiếp theo (ngắn gọn, đúng thứ tự)

1) **Chốt proxy**: hoàn thành MCMC `ide_proxy_w0nu_v1` (m_ncdm) hoặc cấu hình lại để tránh stuck (ref/proposal/proposal_scale).
2) Rút \(S_8\), \(\sigma_8\), \(H_0\), \(\Omega_m\), \(\chi^2\) và so với baseline LCDM.
3) Nếu mục tiêu là IDE thật: phải dựng YAML/CLASS support cho \(\xi_0\), \(s\) (chứ không phải m_ncdm).
4) Với Nullivance: chuyển từ penalty “đánh \(\Delta k\)” sang “neo \(r_s\)/transfer physics” nếu muốn BAO <1%.

---

## 10) Ghi chú về hạn chế và tính trung thực khoa học

- Fit \(P(k)\) từ một trường rung FFT có thể đạt tương quan cao mà vẫn sai BAO. Điều này không mâu thuẫn.
- Muốn vượt ngưỡng precision cần **neo một invariant vật lý** (sound horizon / transfer imprint), không chỉ tối ưu số.
- Proxy \(m_\nu\) không phải IDE, nhưng là phép thử hợp lệ để học pipeline và kiểm tra xu hướng \(S_8\).

---

Nếu bạn muốn, bước tiếp theo tôi sẽ viết một **bản YAML “anti-stuck”** cho `m_ncdm` (ref/proposal/proposal_scale chuẩn), kèm checklist để tránh mất thêm 24h rồi dừng vì “finite=False”.

