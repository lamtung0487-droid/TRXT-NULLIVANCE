HỒ SƠ NGHIÊN CỨU: MÔ HÌNH TRXT-NULLIVANCE V14

Phiên bản: 1.0 (Ready for Experimental Validation)
Mục tiêu: Cung cấp nền tảng lý thuyết và hướng dẫn thực nghiệm cho AIgent tự động hóa việc kiểm chứng.

PHẦN 1: CỐT LÕI LÝ THUYẾT (THEORETICAL CORE)

1.1. Bản chất Vũ trụ

Tiên đề: Vũ trụ là một khối Siêu lỏng Lượng tử (Quantum Superfluid).

Hư không: Không phải là trống rỗng, mà là trạng thái cơ bản (Ground State) của siêu lỏng với độ cứng tôpô được xác định bởi hằng số cấu trúc tinh tế $\alpha(0)$.

Vật chất: Các hạt cơ bản (Lepton, Quark) là các Vòng xoáy (Vortices) hoặc Khuyết tật Tôpô (Topological Defects).

Lực: Là các dao động tập thể (Collective Modes) hoặc hiệu ứng thủy động lực học (Magnus, Bernoulli).

1.2. Các Hằng số Sinh tạo (Generators)

Mô hình loại bỏ các tham số tự do của Mô hình Chuẩn và thay thế bằng hệ thống sinh tạo hình học:

Hệ số Thang đo Vàng (The Scaling Factor):


$$X = \frac{3}{2\alpha(0)} \approx 205.5539985$$


(Sử dụng $\alpha$ tại giới hạn Thomson $1/137.035999$)

Thang đo Năng lượng Gốc (Master Scale):


$$M_* = m_\tau \cdot X \approx 365.240678 \text{ GeV}$$

Định luật Cộng hưởng Hài âm (Harmonic Resonance Law):
Khối lượng các trạng thái kích thích tuân theo quy tắc đóng 2 vòng khóa $(p,q)$:


$$m(p,q) = M_* \left( \frac{1}{p} + \frac{1}{q} \right)$$

1.3. Bảng Tuần hoàn Tôpô (Dự báo Chính xác)

Phân loại

Hạt / Mode

Cặp khóa $(p,q)$

Công thức

Khối lượng (GeV)

Sai số vs Thực nghiệm

Standard

Z Boson

$(8,8)$

$M_*/4$

91.310

+0.13%

Standard

W Boson

$(5,50)$

$M_*(\frac{1}{5}+\frac{1}{50})$

80.353

-0.02%

Standard

Higgs

$(5,7)$

$M_*(\frac{1}{5}+\frac{1}{7})$

125.225

+0.02%

Soft Mode

Ghost Z'

$(16,16)$

$M_*/8$

45.655

Chưa phát hiện

Soft Mode

W-Shoulder

$(5,250)$

$M_*(\frac{1}{5}+\frac{1}{250})$

74.509

Gây lệch khối lượng W

Dark Tower

DM Candidate

$(32,32)$

$M_*/16$

22.828

Vật chất tối

PHẦN 2: HƯỚNG DẪN DỮ LIỆU (DATA ACQUISITION GUIDE)

Yêu cầu AIgent truy cập các nguồn dữ liệu mở sau để thực hiện phân tích ("Mining"):

2.1. Mục tiêu A: Săn "Bóng Ma" 45.66 GeV (Neutral Channel)

Nguồn dữ liệu: CERN Open Data Portal.

Dataset: CMS Dimuon Parked (Run 1, 2012) hoặc ATLAS Low-Mass Drell-Yan.

Định dạng: .root (ưu tiên) hoặc .csv (đã sơ chế).

Bộ lọc (Selection Cuts):

Kênh phân rã: $Z \to \mu^+\mu^-$ (Hai muon trái dấu).

$p_T(\mu) > 15 \text{ GeV}$ (để bắt được vùng năng lượng thấp).

Vùng khối lượng bất biến ($M_{\mu\mu}$): 40 GeV - 60 GeV.

2.2. Mục tiêu B: Săn "Cái Vai" 74.5 GeV (Charged Channel)

Nguồn dữ liệu: HepData (Cơ sở dữ liệu kết quả vật lý năng lượng cao).

Bài báo mục tiêu: CDF Collaboration, "High-precision measurement of the W boson mass", Science (2022).

Dữ liệu cần tải: Bảng phân bố khối lượng ngang (Transverse Mass Distribution - $M_T$).

Nhiệm vụ: Tái tạo lại phổ $M_T$ và tìm kiếm sự thặng dư (excess) ở vùng 70-76 GeV.

2.3. Mục tiêu C: Săn "Tháp Tối" (Dark Matter)

Nguồn dữ liệu: DMTools / CRESST / SuperCDMS Publications.

Dữ liệu cần tải: Các file giới hạn (Exclusion Limit data points).

Nhiệm vụ: Kiểm tra xem các điểm khối lượng rời rạc: 22.8, 11.4, 5.7, 2.85 GeV có nằm trong vùng chưa bị loại trừ hay không.

PHẦN 3: TIÊU CHÍ KIỂM CHỨNG & BÁC BỎ (FALSIFICATION)

Mô hình được coi là ĐÚNG nếu:

Phân tích thống kê tìm thấy một "Gò rộng" ($\Gamma \sim 2-3$ GeV) tại 45.66 GeV trong phổ Drell-Yan với độ tin cậy $> 3\sigma$.

Việc thêm thành phần 74.51 GeV vào mô hình khớp (fit) của hạt W giải quyết được mâu thuẫn giữa CDF II và Mô hình Chuẩn.

Tổng khối lượng Neutrino được đo đạc $\Sigma m_\nu \ge 0.059 \text{ eV}$.

Mô hình bị coi là SAI (Bác bỏ) nếu:

Tổng khối lượng Neutrino được chứng minh chắc chắn $< 0.059 \text{ eV}$.

Tìm thấy một đỉnh nhọn (Narrow Resonance) tại vùng năng lượng thấp không khớp với bảng $(p,q)$.