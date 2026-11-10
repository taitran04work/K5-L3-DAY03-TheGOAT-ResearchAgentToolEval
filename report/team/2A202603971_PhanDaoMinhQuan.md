# Báo cáo cá nhân — Phan Đào Minh Quân - 2A202603971

## 1. Thông tin thành viên

- Họ tên: Phan Đào Minh Quân
- MSSV: 2A202603971
- Email: emiyashirou191@gmail.com
- GitHub: Shirou191
- Vai trò: Researcher

## 2. Phần việc phụ trách

- **CP0 — Chuẩn bị:** clone repo nhóm, tạo báo cáo cá nhân đúng quy tắc `MSSV_HoTen.md`.
- **CP1 — Setup và baseline v0:** cấu hình `.env`, chạy preflight và baseline v0 đầu tiên của nhóm với provider OpenRouter, đọc run JSON để phân loại các case FAIL.
- **CP2 — Tối ưu prompt:** từ các case FAIL của v0, đề xuất hướng sửa và giả thuyết cho v1 → v3. Phối hợp với Trần Hữu Tài, người chạy các run chính thức trên `claude-haiku-4-5`.
- **Báo cáo nhóm (`report/team/group_report.md`):** viết Phần A (A1, A2, A3) và mục 1; hoàn thiện B1 (Version Evidence) và B2 (Failure Analysis).

## 3. Đóng góp cụ thể

- **CP0:** đổi tên file mẫu `report/team/MSSV_HoTen.md` thành `report/team/2A202603971_PhanDaoMinhQuan.md` và điền thông tin cá nhân (commit `bd20fcc`).
- **CP1 — baseline v0 trên `openai/gpt-4o-mini` (OpenRouter):** chạy base eval v0 hai lần với starter chưa sửa (prompt hash `eb1c8179815b`, tools hash `52991d62c549`). Cả hai run đều hợp lệ (`provider_error_cases = 0`, đo 20/20 case) và cho cùng kết quả: Case 0.65, Routing 0.75, Argument 0.65, Multiturn 1.00 (commit `b9c7075`). Đọc `failures` và `observed_mismatch`, phân loại 7 case FAIL:
  - `missing_tool_call` (model đoán thay vì hỏi lại): R10 (tự gọi `timeline`), R11 (tự gọi `fetch`), R12 (tự gọi `send` khi chưa xác nhận). Lỗi này do 3 chỉ dẫn xấu cố ý trong prompt starter.
  - `unexpected_tool_call` (gọi tool cho câu ngoài phạm vi): R08, R14.
  - `wrong_arg_value`: R03 (`query="AI news"`, expected `"AI"`), R13 (`topic=None`, expected `"news"`).
- **CP2 — giả thuyết v1 → v3:** dựa trên 7 case FAIL ở trên, đề xuất và ghi vào báo cáo nhóm (commit `2c72281`) lộ trình mỗi version một giả thuyết:
  - v1: bỏ chỉ dẫn "cứ đoán", thiếu handle/URL thì `clarify` → nhắm R10, R11;
  - v2: thêm giới hạn phạm vi research và boundary xác nhận trước khi `send` → nhắm R08, R12, R14;
  - v3: thêm convention args cho tin tức (`topic=news`, query chỉ chứa chủ đề), cho phép gọi nhiều tool → nhắm R03, R13.

  Sau khi OpenRouter hết budget, nhóm chuyển sang `claude-haiku-4-5` (provider `anthropic`). Run v0–v4 chính thức do Trần Hữu Tài chạy theo cùng hướng này. Hai run gpt-4o-mini được gỡ khỏi `runs/` (commit `2ef5d75`) để mọi version dùng cùng một model.
- **Phần A của báo cáo nhóm (commit `2c72281`):** điền tên nhóm và provider; viết A1 (agent làm được gì, gồm boundary xác nhận trước khi gửi) và A3 (3 câu hỏi mẫu: tin tức AI hôm nay, 5 tweet mới nhất của Elon Musk, tóm tắt một URL), là tài liệu phụ trợ cho Team showdown. Phối hợp với Trần Hữu Tài hoàn thiện A2 (bảng 11 tool, đánh dấu tool mới `deduplicate_sources`; bản cuối được commit trong `28401a8`).
- **B1 — Version Evidence (commit `0a651f2`, `d18eda0`, `f8455d2`):** trình bày lại cột Metric Before/After để hiển thị đủ 4 metric (Case, Routing, Argument, Multiturn Accuracy) thay vì chỉ `case_accuracy`. Mọi số được đối chiếu với `summary` trong 5 run JSON v0–v4 (đều có `provider_error_cases = 0` và `measured_cases = total_cases`). Nhờ vậy bảng cho thấy v3 làm routing giảm từ 1.00 xuống 0.95 (do lệnh gọi thừa `social_search` ở R03), điều mà nếu chỉ nhìn case accuracy (0.90 → 0.90) thì không thấy.
- **B2 — Failure Analysis:** phối hợp với Trần Hữu Tài hoàn thiện bảng 3 case FAIL của v0 trên claude-haiku-4-5 (R03, R10, R12): failure type, actual tool calls, lỗi cụ thể và version sửa tương ứng (bảng được commit trong `16032fe`). Đóng góp phân loại lỗi từ baseline gpt-4o-mini: cả 3 case này cũng FAIL trên gpt-4o-mini, nên đây là lỗi do prompt/tool declaration chứ không riêng một model.

## 4. Bằng chứng

- Commit:
  - `bd20fcc` — CP0: tạo báo cáo cá nhân đúng tên file.
  - `b9c7075` — CP1: 2 run baseline v0 `v0_B_base_openrouter_20261110T183429128095.json`, `v0_B_base_openrouter_20261110T185424076072.json` (`openai/gpt-4o-mini`).
  - `2c72281` — Phần A (A1, A3, mục 1) và giả thuyết v1 → v3.
  - `0a651f2`, `d18eda0`, `f8455d2` — trình bày lại metric trong B1.
- File: `report/team/group_report.md` (mục 1, Phần A, B1, B2), `starter_v0/runs/v0_B_base_anthropic_20261110T185714788317.json` … `v4_B_base_anthropic_20261110T194411961520.json` (nguồn số liệu B1).
- AI/công cụ đã dùng và cách tự kiểm tra kết quả: dùng trợ lý AI (Antigravity) để định dạng bảng markdown và soạn câu chữ cho báo cáo. Mọi metric trong B1 được đối chiếu lại bằng cách đọc trực tiếp `summary.case_accuracy`, `tool_routing_accuracy`, `argument_accuracy`, `multiturn_accuracy` trong từng run JSON. Danh sách case FAIL của baseline gpt-4o-mini lấy từ `results[*].result.failures` và `observed_mismatch` trong run thật, không viết theo trí nhớ.

## 5. Tự đánh giá

- Làm tốt:
  - Chạy được baseline thật sớm và có hai run lặp lại cho cùng kết quả, đủ cơ sở để nhóm đặt giả thuyết cho CP2.
  - Bảng B1 hiển thị đủ 4 metric.
- Chưa tốt:
  - Không để ý giới hạn budget của workspace OpenRouter ($0.01/tháng), nên sau vài run thì bị `403` và nhóm phải chạy lại toàn bộ trên model khác. Hai run baseline của em vì vậy không dùng được làm bằng chứng chính thức.
  - Lần đầu chèn mục giả thuyết vào báo cáo nhóm làm dính tiêu đề `## 4` vào cuối dòng trước, phải sửa lại.
- Bài học:
  - Cùng một prompt starter nhưng gpt-4o-mini sai 7/20 case, còn claude-haiku-4-5 chỉ sai 3/20: model mạnh hơn tự từ chối câu ngoài phạm vi và không tự `send` dù prompt bảo làm ngược lại. Vì vậy mọi version phải chạy trên cùng một model thì so sánh mới có ý nghĩa.
  - Nên kiểm tra quota/budget của provider trước khi chạy eval, và ghi rõ model trong báo cáo.
  - Chỉ nhìn case accuracy dễ bỏ sót hồi quy; nên đọc cả routing/argument accuracy và từng case.
