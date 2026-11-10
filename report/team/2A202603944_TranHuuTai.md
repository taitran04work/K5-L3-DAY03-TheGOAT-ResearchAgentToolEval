# Báo cáo cá nhân — Trần Hữu Tài - 2A202603944

## 1. Thông tin thành viên

- Họ tên: Trần Hữu Tài (nhóm trưởng)
- MSSV: 2A202603944
- Email:
- Vai trò: Tester, Evaluator

## 2. Phần việc phụ trách

- Setup môi trường, kiểm tra provider và key của các tool (CP1).
- Chạy baseline v0 và vòng tối ưu prompt v1 → v3, ghi `version_log.csv` (CP1, CP2).
- Chạy group eval cho 10 case của nhóm và kiểm tra tính hợp lệ của case (CP4).
- Tổng hợp bằng chứng vào các mục B1, B2, B3, B5 và mục 5 của báo cáo nhóm.

## 3. Đóng góp cụ thể

- **Setup và chẩn đoán lỗi môi trường:** sửa thiếu thư viện (`yaml`), phát hiện key RapidAPI/Tavily sai qua `tool_results` trong run JSON. Khi OpenRouter hết budget (`403`) và model free bị `429`, chuyển sang Anthropic và phát hiện SDK `anthropic>=1.0` đã bỏ `temperature`, xử lý bằng cách pin `anthropic<1`.
- **Baseline v0 (0.85):** chạy lại v0 trên `claude-haiku-4-5` để mọi version cùng model; phân tích 3 case FAIL (R03, R10, R12) theo `observed_mismatch` và `failures`.
- **Vòng tối ưu prompt:**
  - v1 (0.85 → 0.90): bỏ chỉ dẫn "đoán khi thiếu thông tin", thiếu handle/URL thì gọi `clarify(text)`. R10 PASS, không hồi quy.
  - v2 (0.90 → 0.90): thêm boundary `send`, scope, cho phép nhiều tool call. R12 vẫn FAIL.
  - v3 (0.90 → 0.90): thêm rule ưu tiên yes_no cho yêu cầu gửi. R12 vẫn FAIL. Từ đó rút ra giả thuyết cho bước sau là sửa ở `tools.yaml`.
- **Kiểm soát chất lượng run:** phát hiện các run bị gắn nhầm version bằng cách đối chiếu prompt hash (run "v0" thực chất dùng prompt v1 và ngược lại), xóa các run sai, khôi phục prompt gốc từ commit `0fc07b6`; phát hiện tools hash đổi do line ending dù nội dung không đổi.
- **CP4:** review 10 case của nhóm; phát hiện `run_eval.normalize_value` ném `TypeError` với expect là list object (G03/G06), dẫn tới case bị tính `provider_error`. Sửa expect của G03/G06 chỉ kiểm tra routing tới `deduplicate_sources`. Group eval đạt 10/10.
- **Git:** xử lý merge `main` → `taitran`; phát hiện commit `b4b3313` vô tình xóa `data/eval_group.json` và khôi phục lại.

## 4. Bằng chứng

- Run:
  - `starter_v0/runs/v0_B_base_anthropic_20261110T185714788317.json`
  - `starter_v0/runs/v1_B_base_anthropic_20261110T190337487498.json`
  - `starter_v0/runs/v2_B_base_anthropic_20261110T190641839759.json`
  - `starter_v0/runs/v3_B_base_anthropic_20261110T191540035836.json`
  - `starter_v0/runs/v3_B_group_anthropic_20261110T192952220848.json`
- File: `starter_v0/artifacts/system_prompt.md`, `starter_v0/artifacts/version_log.csv`, `starter_v0/data/eval_group.json`, `report/team/group_report.md`
- Commit: `e2670c9` (v1), `f90f224` (v2), `16032fe` (v3 + report), `9c8f6c2` (merge, giữ `eval_group.json`)
- AI/công cụ đã dùng và cách tự kiểm tra kết quả: dùng Claude Code để được hướng dẫn từng bước, đọc run JSON và review prompt. Mọi số liệu trong báo cáo đều lấy từ run JSON thật do em tự chạy; mỗi run được kiểm tra `provider_error_cases == 0`, `measured_cases == total_cases` và prompt/tools hash trước khi ghi vào `version_log.csv`.

## 5. Tự đánh giá

- Làm tốt: giữ được nguyên tắc mỗi version một giả thuyết và kiểm tra hash cho từng run; ghi lại trung thực cả các version không tăng điểm (v2, v3) kèm nguyên nhân.
- Chưa tốt: mất thời gian vì chạy nhầm nhãn version và commit prompt v1 vào commit tên "v0 baseline". Lần sau sẽ chạy eval xong mới commit, mỗi version một commit có message rõ ràng.
- Bài học: điểm tổng có nhiễu, nên phải so sánh từng case giữa các version. Thêm rule vào prompt có thể bị rule cũ lấn át nếu không quy định thứ tự ưu tiên.
