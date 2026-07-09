# 📥 HƯỚNG DẪN TẢI DỮ LIỆU SPARC (MANUAL)

Do hệ thống tự động gặp lỗi kết nối, bạn vui lòng tải dữ liệu thủ công theo các bước sau. Đây là dữ liệu chuẩn từ Lelli et al. (2016) chứa rotation curves của 175 galaxies.

### 1. Tải File
- **URL:** [http://astroweb.cwru.edu/SPARC/MassModels_Lelli2016c.mrt](http://astroweb.cwru.edu/SPARC/MassModels_Lelli2016c.mrt)
- **Cách tải:** 
  - Click vào link trên.
  - Sau khi trang web mở ra (dạng text), ấn **Ctrl+S** (Save Page As).
  - Hoặc copy toàn bộ nội dung (Ctrl+A, Ctrl+C) và paste vào file text mới.

### 2. Lưu File
- **Tên file:** `MassModels_Lelli2016c.mrt`
- **Thư mục:** `c:\Users\NC\Music\trxt nullivance v14\trxt_validation\data\sparc\`

Đường dẫn tuyệt đối sau khi lưu phải là:
```
c:\Users\NC\Music\trxt nullivance v14\trxt_validation\data\sparc\MassModels_Lelli2016c.mrt
```

### 3. Chạy Validation
Sau khi đã lưu file, chạy lệnh sau trong terminal để thực hiện validation trên toàn bộ 175 galaxies:

```bash
cd "c:\Users\NC\Music\trxt nullivance v14\trxt_validation"
python scripts/validate_real_data.py
```

### 4. Kiểm Tra
Script sẽ tự động phát hiện file mới và chạy validation. Nếu thành công, bạn sẽ thấy kết quả cho 175 galaxies thay vì 5.
