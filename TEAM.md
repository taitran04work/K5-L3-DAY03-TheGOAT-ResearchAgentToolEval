# Team

## Thông tin nhóm

- Tên nhóm: TheGOAT
- Lớp: L3A / L3B
- Repo nhóm: `K5-L3?-DAY03-TheGOAT-ResearchAgentToolEval` (xem [SUBMISSION.md](SUBMISSION.md))
- URL repo, nhánh nộp, commit chốt:

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Trần Hữu Tài (nhóm trưởng) | 2A202603944 |  | taitran04work | Tester, Evaluator |
|   2 | Lê Thế Anh | 2A202603983 |  | LETHESHIYING | Planner, Researcher |
|   3 | Phan Đào Minh Quân | 2A202603971 |  | Shirou191 | Researcher |
|   4 | Trần Duy Thành | 2A202603919 |  | thanh289 | Coder (BE, FE) |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/20241234_NguyenVanAn.md`.

Sao chép mục dưới đây cho từng thành viên.

## TranHuuTai-2A202603944

Báo cáo chi tiết: [report/team/2A202603944_TranHuuTai.md](report/team/2A202603944_TranHuuTai.md)

### Phần việc phụ trách

- Nhóm trưởng; Tester, Evaluator.
- Setup môi trường và provider (CP1); chạy baseline v0 và các vòng tối ưu v1 → v4 (CP2); chạy group eval (CP4).
- Tổng hợp bằng chứng vào báo cáo nhóm: B1, B2, B3, B5, B6, mục 5.

### Đóng góp cụ thể

- Chẩn đoán và xử lý lỗi môi trường: thiếu thư viện, key RapidAPI/Tavily sai, OpenRouter hết budget (`403`), model free bị `429`, bug SDK `anthropic>=1.0` bỏ `temperature` (pin `anthropic<1`).
- Chạy v0 (0.85) trên `claude-haiku-4-5`; phân tích các case FAIL theo `failures` và `observed_mismatch`.
- Vòng tối ưu, mỗi version một giả thuyết:
  - v1 `system_prompt.md`: thiếu thông tin thì `clarify`, 0.85 → 0.90;
  - v2 `system_prompt.md`: boundary `send` + scope, 0.90 → 0.90;
  - v3 `system_prompt.md`: rule ưu tiên `yes_no`, 0.90 → 0.90;
  - v4 `tools.yaml`: viết lại description và convention args, 0.90 → 0.95.
- Kiểm soát chất lượng run: phát hiện run gắn nhầm version bằng prompt/tools hash, loại run sai và run khác model, giữ mỗi version một run.
- CP4: review 10 case của nhóm; phát hiện `run_eval.normalize_value` lỗi `TypeError` với expect là list object (G03/G06); sửa expect; group eval 10/10.
- Git: xử lý merge `main` → `taitran`, khôi phục `data/eval_group.json` bị xóa nhầm.

### Bằng chứng

- Run: `starter_v0/runs/v0_B_base_anthropic_20261110T185714788317.json`, `v1_..._190337487498.json`, `v2_..._190641839759.json`, `v3_..._191540035836.json`, `v3_B_group_..._192952220848.json`, `v4_..._194411961520.json`
- File: `starter_v0/artifacts/system_prompt.md`, `starter_v0/artifacts/tools.yaml`, `starter_v0/artifacts/version_log.csv`, `starter_v0/data/eval_group.json`, `report/team/group_report.md`
- Commit: `e2670c9` (v1), `f90f224` (v2), `16032fe` (v3), `9c8f6c2` (merge), `f5374d2` (CP4)

---

## TranDuyThanh-2A202603919

Báo cáo chi tiết: [report/team/2A202603919_TranDuyThanh.md](report/team/2A202603919_TranDuyThanh.md)

### Phần việc phụ trách

- Coder (BE, FE); phụ trách CP3 — Tool mới và unit test, CP5 — UI và chạy thử.
- Viết code, kiểm thử và tài liệu liên quan đến tool `deduplicate_sources` và giao diện Streamlit.

### Đóng góp cụ thể

- CP3: xây dựng `deduplicate_sources` để loại nguồn trùng URL, giữ item đầu tiên cùng metadata và thứ tự, không sửa input.
- Chuẩn hóa URL khi so sánh: bỏ fragment và tham số tracking `utm_*`, `fbclid`, `gclid`; vẫn phân biệt HTTP/HTTPS, path, slash cuối và tham số nội dung để tránh gộp nhầm. Input sai trả về error dict; tool không gọi mạng và chỉ chạy khi model chọn gọi.
- Đăng ký tool trong `tools/__init__.py`
- Bổ sung 5 hàm test trong `tests/test_tools_todo.py`, bao phủ 15 trường hợp thực thi, gồm happy path, input xấu, lỗi xử lý, URL khác tham số nội dung và list rỗng. Kết quả kiểm thử được ghi nhận trong báo cáo cá nhân: `85 passed in 0.92s`.
- CP5: thực hiện giao diện Streamlit `app.py` và phần điều phối `ui_backend.py`; hiển thị tool calls/kết quả, lưu transcript JSON và tải transcript từ UI.
- Chạy thử chat cơ bản và kiểm thử UI. Phát hiện lỗi đọc 

### Bằng chứng

- Tool và tài liệu: `starter_v0/tools/deduplicate/tool.py`, `starter_v0/tools/deduplicate/TOOL.md`.
- Tích hợp tool: `starter_v0/tools/__init__.py`, `starter_v0/artifacts/tools.yaml`.
- Kiểm thử CP3: `starter_v0/tests/test_tools_todo.py`, `report/team/evidence/cp3_pytest.txt`.
- UI và kiểm thử CP5: `starter_v0/app.py`, `starter_v0/ui_backend.py`, `starter_v0/tests/test_ui.py`, `starter_v0/requirements.txt`.
- Báo cáo cá nhân: `report/team/2A202603919_TranDuyThanh.md`.
