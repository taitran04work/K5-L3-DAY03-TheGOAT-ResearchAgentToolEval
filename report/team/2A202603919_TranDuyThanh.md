# Báo cáo cá nhân — Trần Duy Thành-2A202603919

## 1. Thông tin thành viên

- Họ tên: Trần Duy Thành
- MSSV: 2A202603919
- Email: .

## 2. Phần việc phụ trách

Phụ trách CP3 — Tool mới và unit test và CP5 — UI, chạy thử và phần báo cáo liên quan.

## 3. Đóng góp cụ thể

### CP3 — Tool mới và unit test

- Bổ sung `deduplicate_sources`. Tool loại nguồn trùng URL, giữ item đầu tiên cùng metadata và thứ tự; không sửa input.
- Đăng ký trong `tools/__init__.py`, khai báo trong `artifacts/tools.yaml` và bổ sung `tools/deduplicate/TOOL.md`.
- Bổ sung 5 hàm test vào `tests/test_tools_todo.py`, thay 3 stub dành cho tool mới. Có 15 trường hợp thực thi, bao gồm happy path, input xấu, lỗi xử lý, URL khác tham số nội dung và list rỗng.
- Chạy kiểm thử trên máy; `85 passed in 0.92s`. 


Tool chỉ chạy khi model chọn gọi; không tự chạy ở mọi prompt hoặc trước mọi bản tổng hợp. Tool bỏ fragment và tham số tracking `utm_*`, `fbclid`, `gclid` khi so sánh; vẫn phân biệt HTTP/HTTPS, path, slash cuối và tham số nội dung để tránh gộp nhầm. Tool không gọi mạng, không tìm tin mới và không xác minh sự thật. Input sai được trả về dạng error dict.

### CP5 — UI và chạy thử

- Thực hiện giao diện Streamlit `app.py` và phần điều phối `ui_backend.py;
- Bổ sung cấu hình provider/model/version, chat nhiều lượt, hiển thị tool calls/kết quả, lưu transcript JSON và tải transcript từ UI.
- Chạy tests/test_ui.py: log cho thấy 10 passed, 1 failed. Lỗi nằm ở test đọc transcript UTF-8 bằng encoding mặc định cp1252 của Windows; cách sửa là dùng .read_text(encoding="utf-8"). Ghi nhận 11/11 pass sau khi sửa.

## 4. Bằng chứng

### File/commit/PR

| Phần | File bằng chứng |
|---|---|
| Tool mới | [tool.py](../../starter_v0/tools/deduplicate/tool.py), [TOOL.md](../../starter_v0/tools/deduplicate/TOOL.md) |
| Tích hợp tool | [tools/__init__.py](../../starter_v0/tools/__init__.py), [tools.yaml](../../starter_v0/artifacts/tools.yaml) |
| Test tool | [test_tools_todo.py](../../starter_v0/tests/test_tools_todo.py), [cp3_pytest.txt](evidence/cp3_pytest.txt) |
| UI và điều phối | [app.py](../../starter_v0/app.py), [ui_backend.py](../../starter_v0/ui_backend.py) |
| Test UI | [test_ui.py](../../starter_v0/tests/test_ui.py)
| Dependency | [requirements.txt](../../starter_v0/requirements.txt) |



Lệnh kiểm tra trên máy, từ `starter_v0/`:

```bash
python -m pytest tests/test_ui.py -v
python -m pytest tests/ -v
python -m streamlit run app.py
```

## 5. Tự đánh giá

Đã thực hiện phần code, test và tài liệu của CP3; bổ sung UI, test và chạy thử chat cơ bản cho CP5. Việc kiểm tra trên Windows phát hiện thiếu encoding tường minh trong test, dù bản test đã chạy qua trên môi trường hỗ trợ. Cần chú ý khác biệt môi trường và kiểm tra lại sau mỗi chỉnh sửa.

