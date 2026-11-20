# GSP – Sequential Pattern Mining

Đồ án cài đặt thuật toán **GSP (Generalized Sequential Pattern)** bằng Python.

## Phạm vi triển khai

- Biểu diễn dữ liệu dưới dạng sequence database.
- Tìm các frequent 1-sequences.
- Sinh candidate bằng i-extension và s-extension.
- Cắt tỉa candidate dựa trên Apriori property.
- Đếm support theo số lượng sequence chứa candidate.
- Thực nghiệm với các ngưỡng MinSup khác nhau.
- Có thể so sánh với thư viện `gsppy` nếu nhóm quyết định thực hiện.

> trước mắt là không có các mở rộng như taxonomy, sliding window, min-gap/max-gap giống trong paper


## Lưu ý làm việc nhóm

- Không commit trực tiếp lên `main`.
- Không commit `.venv/`, `__pycache__/`
- Trước khi làm nhớ check xem nhánh mình đã update đủ so với main chưa
