# Khung Quy tắc và Quy trình Kiểm chứng Tính toán – Dữ liệu (Computational & Data Validation Framework)

## 1. Nguyên tắc nền tảng

### 1.1. Phân biệt hai nhiệm vụ bắt buộc

YÊU CẦU PHẢI phân biệt và thực hiện theo đúng thứ tự:

1. **Verification (kiểm chứng thuật toán/cài đặt)**: xác nhận mã nguồn và quy trình tính toán giải đúng bài toán toán học đã được phát biểu.
2. **Validation (xác thực mô hình với dữ liệu thực)**: xác nhận bài toán toán học và mô hình vật lý mô tả đúng hiện tượng quan sát trong phạm vi miền áp dụng.

Không được suy diễn kết luận vật lý nếu chưa hoàn thành Verification.

### 1.2. Chuẩn tái lập (Reproducibility Standard)

YÊU CẦU PHẢI:

1. **Đóng băng môi trường chạy**: hệ điều hành, kiến trúc CPU/GPU, phiên bản compiler/interpreter, phiên bản thư viện, cấu hình BLAS/LAPACK/cuDNN (nếu có).
2. **Cố định tính ngẫu nhiên**: seed, PRNG backend, và cơ chế sinh mẫu.
3. **Đóng gói pipeline**: quy trình tự động từ dữ liệu thô → tiền xử lý → suy luận/fit → kiểm định → tạo bảng/hình. Không chấp nhận thao tác thủ công không ghi vết.
4. **Tạo run manifest**: mỗi lần chạy phải sinh ra tệp cấu hình đầy đủ (YAML/JSON), kèm run-id duy nhất.

### 1.3. Chuẩn truy nguyên (Traceability Standard)

YÊU CẦU PHẢI bảo đảm mọi kết quả số liệu trong báo cáo đều truy xuất được về:

* commit hash của mã nguồn,
* phiên bản dữ liệu đầu vào (data version/hash),
* tham số chạy (config),
* thời điểm chạy và phần cứng,
* phương pháp ước lượng sai số và tiêu chí dừng.

---

## 2. Verification: Quy tắc kiểm chứng thuật toán và cài đặt

### 2.1. Kiểm thử đơn vị (Unit Tests) bắt buộc

YÊU CẦU PHẢI xây dựng kiểm thử tự động cho từng thành phần:

1. **Kiểm thử đại số/tensor**: định dạng, phép nhân/chuyển vị, quy ước chỉ số, tính đối xứng, Hermiticity.
2. **Kiểm thử bất biến**: nếu mô hình/thuật toán tuyên bố bất biến dưới một nhóm đối xứng (Lorentz, gauge, tịnh tiến, quay), YÊU CẦU PHẢI kiểm tra tính bất biến/equivariance ở mức hàm và mức pipeline.
3. **Kiểm thử bảo toàn**: nếu phương pháp số tuyên bố bảo toàn chuẩn hoá, năng lượng, xung lượng, điện tích, YÊU CẦU PHẢI kiểm tra bằng sai số tương đối và ngưỡng dung sai nêu rõ.

### 2.2. Kiểm thử hồi quy (Regression Tests) bắt buộc

YÊU CẦU PHẢI:

* thiết lập bộ “case chuẩn” với đầu vào cố định và đầu ra tham chiếu (golden outputs),
* chạy tự động sau mỗi thay đổi mã nguồn,
* báo cáo sai lệch theo chuẩn sai số đã định nghĩa.

### 2.3. Kiểm chứng hội tụ (Convergence Verification)

YÊU CẦU PHẢI chứng minh hội tụ bằng thí nghiệm số có cấu trúc:

1. **Refinement theo bước thời gian/bước lưới**: giảm (\Delta t), (\Delta x) theo tỉ lệ định trước; đo sai số so với nghiệm tham chiếu.
2. **Bậc hội tụ**: ước lượng slope trên log–log để xác nhận bậc phương pháp phù hợp với lý thuyết.
3. **Tiêu chí dừng**: định nghĩa rõ điều kiện dừng (residual, gradient norm, energy drift), và chứng minh tính ổn định đối với thay đổi tiêu chí trong phạm vi hợp lý.

### 2.4. Đối chiếu phương pháp độc lập (Independent Cross-Checks)

YÊU CẦU PHẢI thực hiện tối thiểu một đối chiếu độc lập:

* cùng đại lượng vật lý nhưng tính bằng hai phương pháp khác nhau (ví dụ: biến phân vs Hamilton; tích phân số vs xấp xỉ giải tích; Monte Carlo vs PDE solver),
* hoặc đối chiếu với một thư viện đã thẩm định trong cộng đồng (kèm phiên bản và điều kiện tương thích).

### 2.5. Phân tích điều kiện bài toán và ổn định số (Conditioning & Numerical Stability)

YÊU CẦU PHẢI:

1. đánh giá **condition number** hoặc dấu hiệu ill-conditioning,
2. nếu là bài toán nghịch đảo: trình bày regularization (Tikhonov, sparsity, priors Bayes) và phân tích bias–variance,
3. kiểm tra nhạy với thay đổi nhỏ của đầu vào và tham số solver.

### 2.6. Xử lý ngẫu nhiên và Monte Carlo (nếu có)

YÊU CẦU PHẢI:

* báo cáo phương pháp lấy mẫu, autocorrelation, effective sample size,
* kiểm tra luật (1/\sqrt{N}) cho sai số,
* chạy nhiều seed và báo cáo độ phân tán kết quả.

---

## 3. Validation: Quy tắc xác thực mô hình bằng dữ liệu thực

### 3.1. Nguồn gốc dữ liệu và siêu dữ liệu (Provenance & Metadata)

YÊU CẦU PHẢI lập hồ sơ dữ liệu (data dossier) gồm:

* nguồn đo, thiết bị, độ phân giải, dải đo, tần số lấy mẫu,
* điều kiện môi trường, lịch hiệu chuẩn (calibration),
* sai số hệ thống (systematic errors) đã biết và giả định còn thiếu.

Không được sử dụng dữ liệu nếu không mô tả được provenance tối thiểu.

### 3.2. Kiểm tra chất lượng dữ liệu (Data Quality Controls)

YÊU CẦU PHẢI định nghĩa quy tắc kiểm tra và xử lý:

* dữ liệu thiếu, nhiễu, drift theo thời gian, saturation,
* outliers: tiêu chí phát hiện, tiêu chí loại bỏ/giữ lại, và phân tích độ nhạy khi thay đổi quy tắc,
* biến đổi tiền xử lý (lọc, chuẩn hoá, detrend) và ảnh hưởng của chúng tới kết quả.

Mọi quy tắc lọc/tiền xử lý phải được ghi rõ và thực thi tự động trong pipeline.

### 3.3. Phân chia dữ liệu và chống rò rỉ (Splitting & Leakage Prevention)

Nếu có ước lượng tham số/học mô hình:

1. **YÊU CẦU PHẢI tách dữ liệu** thành train/validation/test theo nguyên tắc phù hợp với cấu trúc dữ liệu.
2. **Dữ liệu test** phải được niêm phong (không sử dụng để chọn mô hình/hyperparameter).
3. Với chuỗi thời gian: **bắt buộc** dùng walk-forward / rolling-origin evaluation; không được shuffle ngẫu nhiên.

### 3.4. Mô hình gốc so sánh (Baselines & Null Hypotheses)

YÊU CẦU PHẢI:

1. xây dựng **null model** (lý thuyết chuẩn, hoặc mô hình đơn giản nhất),
2. xác định metric so sánh (likelihood ratio, AIC/BIC, Bayes factor, RMSE/MAE, calibration),
3. chứng minh cải thiện là có ý nghĩa (theo tiêu chí thống kê hoặc Bayes đã định trước).

Không chấp nhận tuyên bố ưu việt nếu không có baseline định lượng.

### 3.5. Định lượng bất định (Uncertainty Quantification)

YÊU CẦU PHẢI báo cáo và lan truyền bất định tối thiểu theo ba nguồn:

1. **Measurement uncertainty**: noise và systematic error,
2. **Model uncertainty**: thiếu mô tả, xấp xỉ, truncation (EFT truncation, perturbative truncation),
3. **Numerical uncertainty**: sai số rời rạc, sai số hội tụ, sai số Monte Carlo.

Kết quả phải kèm interval (CI/credible interval) và/hoặc posterior predictive checks (nếu Bayes).

### 3.6. Kiểm tra độ bền vững (Robustness & Stress Testing)

YÊU CẦU PHẢI thực hiện tối thiểu:

1. **Bootstrap / Jackknife**: ước lượng độ ổn định tham số và metric.
2. **Noise injection**: thêm nhiễu hợp lý để kiểm tra suy giảm hiệu năng theo mức nhiễu.
3. **Ablation**: loại bỏ một phần dữ liệu/đặc trưng/khối tiền xử lý để định vị nguồn tạo tín hiệu.
4. **Domain shift** (nếu có): khác thiết bị/điều kiện đo; báo cáo suy giảm và giới hạn áp dụng.

---

## 4. Kiểm soát sai lệch suy luận và kỷ luật thống kê

### 4.1. Định nghĩa trước tiêu chí (Pre-specified Criteria)

YÊU CẦU PHẢI xác định trước khi phân tích dữ liệu:

* metric chính,
* ngưỡng chấp nhận/bác bỏ,
* quy tắc xử lý outliers,
* số lần thử nghiệm/hypothesis tests dự kiến.

### 4.2. Điều chỉnh đa kiểm định (Multiple Comparisons)

YÊU CẦU PHẢI:

* nếu kiểm tra nhiều tần số/kênh/giả thuyết, áp dụng FDR hoặc Bonferroni, hoặc mô hình Bayes tương ứng,
* báo cáo số lượng phép thử và phương pháp điều chỉnh.

### 4.3. Báo cáo đầy đủ (Complete Reporting)

YÊU CẦU PHẢI:

* báo cáo cả kết quả âm (negative results) và các thử nghiệm không đạt,
* mô tả đầy đủ các quyết định phân tích ảnh hưởng đến kết quả (researcher degrees of freedom).

---

## 5. Chuẩn đóng gói nghiên cứu tính toán (Computational Research Artifacts)

### 5.1. Gói tái lập (Reproduction Package)

YÊU CẦU PHẢI cung cấp:

1. repository mã nguồn + commit hash,
2. hướng dẫn chạy tái lập (README) và script một lệnh,
3. manifest dữ liệu (nguồn, hash, phiên bản),
4. cấu hình chạy (config files),
5. log/outputs để tái tạo toàn bộ hình/bảng trong báo cáo.

### 5.2. Hồ sơ mô hình (Model Dossier)

YÊU CẦU PHẢI kèm:

* giả định và miền áp dụng,
* cơ chế thất bại (failure modes),
* độ nhạy theo tham số,
* mô tả các xấp xỉ và sai số truncation.

---

## 6. Ma trận kiểm tra độ vững chắc tính toán (Computational Robustness Matrix)

YÊU CẦU PHẢI đánh dấu **PASS/FAIL/N/A** và đính kèm bằng chứng (đường dẫn log + run-id).

### A. Độ đúng của mã nguồn (Code Correctness)

* Unit tests: bất biến, bảo toàn, đại số tuyến tính/tensor
* Regression tests: golden outputs
* Convergence verified: (\Delta t,\Delta x) và bậc hội tụ
* Cross-check: phương pháp độc lập
* Numerical stability & conditioning assessed

### B. Toàn vẹn dữ liệu (Data Integrity)

* Provenance & calibration documented
* Quality controls: missing/outliers/drift/saturation
* Leakage-free splitting (time-series protocol đúng)
* Baselines & null models implemented
* Uncertainty propagation complete

### C. Nghiêm ngặt thống kê (Statistical Rigor)

* Metrics & thresholds pre-specified
* Multiple comparisons controlled
* Robustness tests completed (bootstrap/noise/ablation/domain shift)
* Full reporting including negative results

### D. Tái lập và truy nguyên (Reproducibility & Traceability)

* Environment locked + seeds fixed
* Run manifests + hashes
* One-command pipeline
* Reproduction package complete

---

## 7. Ba yêu cầu xác nhận tối thiểu trước khi nêu kết luận vật lý

YÊU CẦU PHẢI xác nhận (kèm bằng chứng tái lập):

1. Kết quả ổn định khi thay đổi seed trong phạm vi hợp lý và sai số thống kê được báo cáo đầy đủ.
2. Kết quả hội tụ theo tinh chỉnh lưới/bước và không phụ thuộc tùy tiện vào lựa chọn solver.
3. Kết quả giữ ý nghĩa khi lan truyền đầy đủ bất định đo, bất định mô hình và bất định số học.
