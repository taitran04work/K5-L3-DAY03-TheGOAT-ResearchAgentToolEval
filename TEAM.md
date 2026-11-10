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
|   3 | Phan Đào Minh Quân | 2A202603971 | | Shirou191 | Researcher, Coder |
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

## PhanDaoMinhQuan-2A202603971

Báo cáo chi tiết: [report/team/2A202603971_PhanDaoMinhQuan.md](report/team/2A202603971_PhanDaoMinhQuan.md)

### Phần việc phụ trách

- Researcher.
- CP0: chuẩn bị repo nhóm, tạo báo cáo cá nhân đúng tên file.
- CP1: setup provider, chạy baseline v0 đầu tiên của nhóm (OpenRouter) và phân loại case FAIL.
- CP2: đề xuất giả thuyết cho v1 → v3 từ các case FAIL của v0.
- Báo cáo nhóm: mục 1, Phần A (A1, A2, A3), B1, B2.

### Đóng góp cụ thể

- CP1: chạy base eval v0 hai lần trên `openai/gpt-4o-mini` với starter chưa sửa. Cả hai run hợp lệ (0 provider error, 20/20 measured) và cho cùng kết quả: Case 0.65, Routing 0.75, Argument 0.65, Multiturn 1.00. Phân loại 7 case FAIL:
  - `missing_tool_call`: R10, R11, R12 (đoán thay vì hỏi lại, tự `send` khi chưa xác nhận);
  - `unexpected_tool_call`: R08, R14 (gọi tool cho câu ngoài phạm vi);
  - `wrong_arg_value`: R03 (`query="AI news"`), R13 (`topic=None`).
- CP2: từ 7 case FAIL, đề xuất lộ trình mỗi version một giả thuyết:
  - v1: thiếu handle/URL thì `clarify` → R10, R11;
  - v2: scope + boundary xác nhận trước khi `send` → R08, R12, R14;
  - v3: convention args tin tức, cho phép nhiều tool → R03, R13.

  Sau khi OpenRouter hết budget, nhóm chuyển sang `claude-haiku-4-5`; run chính thức v0–v4 do Trần Hữu Tài chạy theo hướng này.
- Phần A: viết A1 (agent làm được gì) và A3 (3 câu hỏi mẫu), điền tên nhóm và provider; phối hợp với Trần Hữu Tài hoàn thiện A2 (bảng 11 tool).
- B1: trình bày lại Metric Before/After đủ 4 metric (Case, Routing, Argument, Multiturn Accuracy), đối chiếu với `summary` của 5 run JSON v0–v4. Nhờ đó thấy được routing ở v3 giảm 1.00 → 0.95 dù case accuracy giữ 0.90.
- B2: phối hợp với Trần Hữu Tài hoàn thiện bảng 3 case FAIL của v0 (R03, R10, R12). Đối chiếu với baseline gpt-4o-mini: cả 3 case cũng FAIL ở đó, nên đây là lỗi do prompt/tool declaration chứ không riêng một model.

### Bằng chứng

- Run: `v0_B_base_openrouter_20261110T183429128095.json`, `v0_B_base_openrouter_20261110T185424076072.json` (`openai/gpt-4o-mini`; đã gỡ khỏi `runs/` ở `2ef5d75` vì khác model với v0–v4, xem lại bằng `git show b9c7075:starter_v0/runs/<tên file>`)
- File: `report/team/group_report.md` (mục 1, Phần A, B1, B2), `report/team/2A202603971_PhanDaoMinhQuan.md`
- Commit: `bd20fcc` (CP0), `b9c7075` (CP1 baseline runs), `2c72281` (Phần A + giả thuyết v1 → v3), `0a651f2`, `d18eda0`, `f8455d2` (B1)

---

## HoVaTen-MSSV

### Phần việc phụ trách

-

### Đóng góp cụ thể

-

### Bằng chứng

-
