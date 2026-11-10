# Báo cáo nhóm — Day 03 Research Agent Tool Eval

> Báo cáo gồm 2 phần có hạn khác nhau:
> - **Phần A (mục 2)** — giới thiệu agent, ngắn gọn 1 trang. **Xong trước Team showdown (16:30)** để team khác hiểu nhanh agent có tool gì, làm được gì. Có thể làm thêm poster `report/team/poster.html` hoặc `poster.svg`.
> - **Phần B (mục 3–7)** — chi tiết và bằng chứng, dựa trên log thật. Hoàn thiện trước deadline nộp bài.
>
> Mỗi bảng phải trỏ được tới file thật: run JSON, transcript, commit. Cách chấm xem [RUBRIC.md](../../RUBRIC.md).

## 1. Thông tin nhóm

- Tên nhóm: TheGOAT
- Thành viên và phân công: xem [TEAM.md](../../TEAM.md)
- Provider/model dùng cho v0–v3: `anthropic` / `claude-haiku-4-5-20251001` (model mặc định của provider, không truyền `--model`)

## 2. Mục tiêu và cách tiếp cận — PHẦN A: Giới thiệu agent

### A1. Agent này làm được gì

> 1–2 câu mô tả agent dùng để làm gì (cho team khác hiểu nhanh).

Research agent hỗ trợ tìm kiếm tin tức trên web, tìm bài đăng theo tài khoản hoặc chủ đề,
đọc nội dung từ URL, xử lý tài liệu nghiên cứu và định dạng kết quả. Với thao tác gửi nội dung,
agent phải hỏi xác nhận trước khi thực hiện.

**Cách chạy UI:**

> Lệnh chạy UI (ví dụ `streamlit run app.py`) và dependency đã thêm vào `starter_v0/requirements.txt`.

**Link dùng thử (deploy):**

> Dán link public để team khác mở thử ngay. Cách deploy nhanh bằng Cloudflare Tunnel xem README. Nếu deploy Vercel/Streamlit Cloud thì dán link đó.
>
> URL:

### A2. Tool agent có

> Liệt kê các tool agent đang dùng (gồm tool mới nhóm tự thêm). Mỗi tool 1 dòng: tên + làm được gì.

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| clarify | hỏi lại người dùng khi thiếu thông tin | không |
|  |  |  |
|  |  |  |

### A3. Câu hỏi mẫu để thử

> 3–5 câu hỏi/yêu cầu mẫu để team khác tự thử agent ngay.

1. Tin tức AI hôm nay có gì nổi bật?
2. Lấy 5 tweet mới nhất của Elon Musk.
3. Tóm tắt bài này: https://nhandan.vn/tong-bi-thu-chu-tich-nuoc-to-lam-tiep-nguyen-chu-tich-lien-minh-nghi-si-huu-nghi-nhat-viet-va-thong-doc-mot-so-dia-phuong-post1001586.html

## 3. Giải pháp

> Tóm tắt các thay đổi chính trong `starter_v0/artifacts/system_prompt.md` và `starter_v0/artifacts/tools.yaml`, và tool mới nhóm viết (tên, làm gì, khi nào agent nên gọi).

-

- v1 bổ sung rule không được đoán khi thiếu handle hoặc URL; agent phải gọi
  `clarify`. Mục tiêu là sửa R10 và R11.
- v2 bổ sung giới hạn phạm vi research và boundary của `send`: không gọi tool
  cho câu hỏi toán/coding, và phải hỏi xác nhận trước khi gửi. Mục tiêu là sửa
  R08, R12 và R14.
- v3 bổ sung routing và argument convention cho news, đồng thời cho phép gọi
  nhiều tool khi user yêu cầu cả web và social search. Mục tiêu là sửa R03 và R13.# 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

Lấy từ `starter_v0/artifacts/version_log.csv` và `starter_v0/runs/*.json`. Chỉ dùng run có `provider_error_cases == 0` và `measured_cases == total_cases`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline (chưa sửa) | Đo starter gốc (`p eb1c8179815b`, `t 52991d62c549`) | – | 0.85 | `starter_v0/runs/v0_B_base_anthropic_20261110T185714788317.json` |
| v1 | `system_prompt.md` | Prompt bảo "đoán khi thiếu thông tin" → thay bằng: thiếu handle/URL thì gọi `clarify(response_type="text")`, tên người nổi tiếng thì tự map sang handle. Kỳ vọng sửa R10 | 0.85 | 0.90 | `starter_v0/runs/v1_B_base_anthropic_20261110T190337487498.json` |
| v2 | `system_prompt.md` | Prompt bảo "gửi ngay" + "chỉ một bước" → thay bằng boundary `send` (`clarify` yes_no trước, `send(confirmed=true)` chỉ sau khi user đồng ý), rule scope, cho phép nhiều tool call. Kỳ vọng sửa R12 | 0.90 | 0.90 | `starter_v0/runs/v2_B_base_anthropic_20261110T190641839759.json` |
| v3 | `system_prompt.md` | R12 ở v2 vẫn hỏi bằng `text` vì rule thiếu-info (v1) khớp trước rule send (v2) → thêm câu ưu tiên: yêu cầu gửi/đăng luôn dùng `yes_no` kể cả khi thiếu nội dung. Kỳ vọng sửa R12 | 0.90 | 0.90 | `starter_v0/runs/v3_B_base_anthropic_20261110T191540035836.json` |

Nhận xét:

- v1 là thay đổi duy nhất tăng điểm: R10 FAIL → PASS, không case nào hồi quy.
- v2 và v3 **không** sửa được R12 dù đã thêm rule và rule ưu tiên. Ở cả hai run, model vẫn gọi `clarify(response_type="text")` hỏi "Bạn muốn đăng nội dung nào…". Giả thuyết "xung đột thứ tự rule trong prompt" bị bác bỏ một phần: thêm ưu tiên trong prompt chưa đủ. Giả thuyết tiếp theo: khai báo `clarify` trong `tools.yaml` chỉ mô tả `response_type` là "Kiểu trả lời", không nói khi nào dùng `yes_no` → sửa ở tool declaration (v4).
- Ở v3, R03 ngoài lỗi query còn có thêm `extra tool call social_search`. Ở v2 R03 chỉ gọi `lookup`. Có thể đây là tác dụng phụ của rule "Use as many tool calls as the request needs" (thêm ở v2), hoặc là nhiễu giữa các lần chạy. Cần theo dõi ở version sau.
- v1→v3 chỉ đổi prompt hash, tools hash giữ nguyên `52991d62c549`, đúng nguyên tắc mỗi version một thay đổi.

### B2. Failure Analysis

Lấy từ `results[*].result.failures` trong run JSON v0 (`starter_v0/runs/v0_B_base_anthropic_20261110T185714788317.json`).

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
| R03_web_news_routing | `wrong_tool` (quan sát: `wrong_arg_value`) | `lookup(query="AI tin tức hôm nay", topic="news", timeframe="day", max_results=10)` | `query: expected 'AI', got 'AI tin tức hôm nay'`. Đã đúng `topic` và `timeframe` nhưng vẫn nhồi "tin tức hôm nay" vào query | `tools.yaml`: mô tả `query` chỉ chứa chủ đề, tin tức/thời gian đi vào `topic`/`timeframe` (v4) |
| R10_missing_handle | `missing_info` (quan sát: `missing_tool_call`) | `timeline(screenname="elonmusk", limit=5)` | `missing tool call clarify`, `extra tool call timeline`. Làm theo prompt gốc "pick a well-known account", tự đoán Elon Musk | `system_prompt.md`: bỏ chỉ dẫn đoán, thiếu handle thì `clarify(text)` (v1, đã PASS) |
| R12_confirm_before_send | `wrong_boundary` (quan sát: `wrong_arg_value`) | `clarify(question="Bản tin nào mà bạn muốn đăng lên Telegram?…", response_type="text")` | `response_type: expected 'yes_no', got 'text'`. Model không tự gửi mà hỏi lại nội dung, nhưng eval yêu cầu hỏi xác nhận yes/no | `system_prompt.md` boundary send (v2, v3: chưa PASS) → `tools.yaml` mô tả `clarify.response_type` và `send` (v4) |

Ghi chú: với `claude-haiku-4-5`, prompt gốc chỉ làm hỏng 3/20 case. Model vẫn từ chối câu ngoài phạm vi (R08, R14), vẫn hỏi lại khi thiếu URL (R11) và không tự gọi `send` (R12), dù prompt gốc bảo làm ngược lại. R12 là case có thể tranh luận: hỏi lại nội dung khi user chỉ nói "bản tin này" cũng là một hành vi an toàn, nhưng eval chỉ chấp nhận `yes_no`.

### B3. Team Eval Cases

Liệt kê đúng 10 case trong `starter_v0/data/eval_group.json` (5 single turn + 5 multi turn).

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
|  |  |  |  |

### B4. Live Chat Evidence

Lấy từ `starter_v0/transcripts/*.transcript.json`.

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
|  |  |  |  |  |

### B5a. Required Evidence — Tool mới, unit test, UI

| Item | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Tool mới (`tools/<tên>/`) |  |  |  |
| Unit test tool mới (≥ 3 test/tool) | `pytest` output (0 failed) |  |  |
| UI (lệnh chạy + link dùng thử) |  |  |  |

Tool unit tests: số test đã viết, và một ví dụ lỗi mà unit test bắt được nhưng eval không bắt được.

### B5. Bonus Evidence

Chỉ điền nếu nhóm làm bonus (ghi riêng, tối đa 10 điểm). Tool có sẵn (`send`, `policy`, `papers`, `paper_text`) không tự được bonus.

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Small Local Model | xem B7 |  |  |
| Hơn 3 tool mới (≥ 4) |  |  |  |
| `send` gửi thật lên Telegram sau xác nhận | transcript |  |  |
| Test challenge (0 skipped / regression test) | `pytest` output |  |  |

Test challenge: số bug tìm được trong tool có sẵn (nếu có), cách sửa, và test regression tương ứng.

### B7. Small Local Model Challenge (bonus)

Chỉ điền nếu nhóm làm bonus này.

| Version | Model (provider) | Prompt/Tools | case_accuracy | tool_routing | argument | multiturn | Run File |
|---|---|---|---|---|---|---|---|
| v3 | (cloud) | v3 |  |  |  |  |  |
| v3-<model> | (ollama) | v3 |  |  |  |  |  |
| v3-<model> | (ollama) | v3 |  |  |  |  |  |
| v4-local |  |  |  |  |  |  |  |
| v5-local |  |  |  |  |  |  |  |

Lỗi đặc thù của model nhỏ (đếm từ run JSON):

| Failure Pattern | Count | Example Case | Fix Tried | Helped? |
|---|---|---|---|---|
| wrong / hallucinated tool |  |  |  |  |
| invalid JSON args (`_invalid_json_arguments`) |  |  |  |  |
| no tool call / answered directly |  |  |  |  |
| missed `clarify` |  |  |  |  |
| repeated / unnecessary calls |  |  |  |  |

- Cái gì giúp model nhỏ gọi tool đúng hơn nhất? Bằng chứng?
- Bản prompt tối ưu cho local chạy trên model cloud thì sao?
- Khi nào nhóm sẽ chọn model local thay vì cloud cho agent này?

## 5. Khó khăn và cách xử lý

> Khó khăn chính và cách nhóm xử lý. Nếu gặp lỗi kỹ thuật (provider lỗi, hết quota API, tool không chạy), mô tả lỗi và dẫn bằng chứng: run JSON, log, ảnh chụp.

- **OpenRouter hết budget:** workspace OpenRouter có giới hạn $0.01/tháng. Sau vài lần chạy với `openai/gpt-4o-mini`, mọi request bị `403 - Workspace monthly budget of $0.01 exceeded`, run có `provider_error_cases = 20` nên không hợp lệ và đã bị loại. Thử model free (`google/gemma-4-31b-it:free`) thì bị `429 - Provider returned error`. Nhóm chuyển sang provider `anthropic` và chạy lại v0 để mọi version cùng một model.
- **Bug tương thích SDK Anthropic:** `requirements.txt` chỉ ghi `anthropic>=0.34.0`, nên pip cài bản 2.7.0. Từ bản 1.0, `Messages.create()` không còn nhận `temperature`, trong khi `providers/anthropic_provider.py` vẫn truyền tham số này → `TypeError: Messages.create() got an unexpected keyword argument 'temperature'`. Cách xử lý: pin `anthropic<1` (bản 0.125.0 vẫn có `temperature`).
- **Key tool sai:** run gpt-4o-mini đầu tiên có `timeline`/`social_search` lỗi `Missing RAPIDAPI_KEY` và `lookup` lỗi `401 Unauthorized` (Tavily). Eval chấm lựa chọn tool nên điểm không bị ảnh hưởng, nhưng nhóm sửa key trước khi chạy tiếp để log có dữ liệu thật.
- **Kết quả không tất định:** với gpt-4o-mini, cùng prompt và cùng hash, hai lần chạy cho 0.70 và 0.65 (R03 lúc PASS lúc FAIL). Vì vậy nhóm so sánh từng case giữa các version thay vì chỉ nhìn điểm tổng.
- **Hash đổi dù nội dung không đổi:** `tools.yaml` được lưu lại trong editor nên đổi line ending (LF/CRLF), hash đổi từ `e69bc53ed884` sang `52991d62c549` dù `git diff` rỗng. Vì vậy v0 được chạy lại để v0–v3 dùng chung tools hash.
- **Gắn nhầm nhãn version:** có lần prompt v1 đã được commit nên `git stash` không đưa prompt về bản gốc, và run "v0" thực chất dùng prompt v1 (hash `p27bc123aba94`). Nhóm phát hiện bằng cách đối chiếu prompt hash trong mỗi run, xóa các run sai, rồi khôi phục prompt gốc bằng `git checkout 0fc07b6 -- artifacts/system_prompt.md`.

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong [TEAM.md](../../TEAM.md) và các báo cáo cá nhân `report/team/MSSV_HoTen.md`.

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- Fix nào thuộc `system_prompt.md`?
- Fix nào thuộc `tools.yaml`?
- Failure nào cần review thủ công thay vì chấm tự động?
- Nếu có thêm một vòng, nhóm sẽ thử giả thuyết nào?

## 8. Tài liệu tham khảo

-
