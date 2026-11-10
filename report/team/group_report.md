# Báo cáo nhóm — Day 03 Research Agent Tool Eval

> Báo cáo gồm 2 phần có hạn khác nhau:
> - **Phần A (mục 2)** — giới thiệu agent, ngắn gọn 1 trang. **Xong trước Team showdown (16:30)** để team khác hiểu nhanh agent có tool gì, làm được gì. Có thể làm thêm poster `report/team/poster.html` hoặc `poster.svg`.
> - **Phần B (mục 3–7)** — chi tiết và bằng chứng, dựa trên log thật. Hoàn thiện trước deadline nộp bài.
>
> Mỗi bảng phải trỏ được tới file thật: run JSON, transcript, commit. Cách chấm xem [RUBRIC.md](../../RUBRIC.md).

## 1. Thông tin nhóm

- Tên nhóm: TheGOAT
- Thành viên và phân công: xem [TEAM.md](../../TEAM.md)
- Provider/model dùng cho v0–v4: `anthropic` / `claude-haiku-4-5-20251001` (model mặc định của provider, không truyền `--model`)

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
| clarify | Hỏi lại user khi thiếu thông tin (text) hoặc xin xác nhận trước khi gửi (yes_no) | không |
| timeline | Lấy tweet gần đây của một tài khoản X cụ thể (RapidAPI) | không |
| social_search | Tìm tweet theo chủ đề/từ khóa, sắp xếp Latest hoặc Top | không |
| lookup | Tìm kiếm web/tin tức (Tavily) theo `topic` và `timeframe` | không |
| fetch | Đọc nội dung một URL cụ thể (Firecrawl) | không |
| format | Trình bày danh sách nguồn thành bản tin (brief, sections, bullets, thread…) | không |
| send | Gửi nội dung lên Telegram, chỉ khi user đã xác nhận (`confirmed=true`) | không |
| policy | Tra cứu chính sách nội bộ công ty | không |
| papers | Tìm bài báo khoa học trên arXiv | không |
| paper_text | Lấy nội dung text của một bài arXiv | không |
| deduplicate_sources | Loại nguồn trùng URL (bỏ UTM/fragment khi so sánh), giữ bản đầu và metadata | **có** |

### A3. Câu hỏi mẫu để thử

> 3–5 câu hỏi/yêu cầu mẫu để team khác tự thử agent ngay.

1. Tin tức AI hôm nay có gì nổi bật?
2. Lấy 5 tweet mới nhất của Elon Musk.
3. Tóm tắt bài này: https://nhandan.vn/tong-bi-thu-chu-tich-nuoc-to-lam-tiep-nguyen-chu-tich-lien-minh-nghi-si-huu-nghi-nhat-viet-va-thong-doc-mot-so-dia-phuong-post1001586.html

## 3. Giải pháp

> Tóm tắt các thay đổi chính trong `starter_v0/artifacts/system_prompt.md` và `starter_v0/artifacts/tools.yaml`, và tool mới nhóm viết (tên, làm gì, khi nào agent nên gọi).

**`system_prompt.md`** (bỏ 3 chỉ dẫn xấu cố ý của starter):

- **v1:** bỏ "đừng hỏi lại, cứ đoán / chọn Sam Altman / tự giả định URL". Thay bằng: không bịa tài khoản hay URL; thiếu handle/URL thì gọi `clarify(response_type="text")`; tên người nổi tiếng thì tự map sang handle (Sam Altman → `sama`) và gọi tool luôn, không hỏi thừa.
- **v2:** bỏ "gửi ngay cho user đỡ chờ" và "luôn làm trong một bước, chọn một tool". Thay bằng 3 mục:
  - **Scope:** câu ngoài phạm vi research (toán, viết code) thì không gọi tool, trả lời ngắn và định hướng lại.
  - **Sending:** `send` là hành động ghi ra ngoài; phải `clarify(yes_no)` trước, chỉ `send(confirmed=true)` sau khi user đồng ý.
  - **Steps:** được gọi nhiều tool khi request cần nhiều nguồn.
- **v3:** thêm ngoại lệ ưu tiên: yêu cầu gửi/đăng luôn dùng `yes_no`, kể cả khi thiếu nội dung.

**`tools.yaml`** (v4; v0–v3 giữ nguyên tools hash `52991d62c549` để mỗi version chỉ đổi một artifact):

- Mọi tool (11/11) có description theo khuôn **làm gì · dùng khi · không dùng khi**, chỉ rõ tool thay thế (vd. `timeline` vs `social_search`, `lookup` vs `fetch`/`papers`/`policy`).
- Convention args:
  - `timeline.screenname` không có `@`, kèm ví dụ map tên → handle;
  - `lookup.query` chỉ chứa chủ đề cốt lõi, không chứa "tin tức/news/hôm nay";
  - `lookup.topic=news` cho tin tức; bảng đổi "hôm nay/tuần này/tháng này" → `day/week/month`;
  - `social_search.search_type`: `Top` cho phổ biến/top, `Latest` mặc định.
- Boundary:
  - `clarify.response_type`: `yes_no` cho xác nhận hành động ghi, `text` cho thông tin còn thiếu;
  - `send` là hành động ghi không hoàn tác, chỉ gọi sau khi user trả lời "có", `confirmed=true` chỉ khi đã xác nhận, không dùng để trả lời câu hỏi.
- Giữ nguyên tên tool và tham số. `pytest tests/test_tool_contract.py` vẫn xanh.

**Tool mới `deduplicate_sources`** (`starter_v0/tools/deduplicate/`): nhận danh sách nguồn đã thu thập, loại các item trùng URL sau khi chuẩn hóa (bỏ fragment, tham số tracking `utm_*`, chữ hoa ở host), giữ item đầu tiên cùng metadata. Trả về `items`, `input_count`, `item_count`, `removed_count`, `duplicates`; lỗi thì trả error dict, không raise. Agent nên gọi khi user đã có danh sách nguồn và muốn làm sạch trước khi `format`; không dùng để tìm tin, đọc URL hay gộp bài khác URL.

## 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

Lấy từ `starter_v0/artifacts/version_log.csv` và `starter_v0/runs/*.json`. Chỉ dùng run có `provider_error_cases == 0` và `measured_cases == total_cases`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---|---|---|
| v0 | baseline (chưa sửa) | Đo starter gốc (`p eb1c8179815b`, `t 52991d62c549`) | – | Case Accuracy: 0.85<br>Routing Accuracy: 0.95<br>Argument Accuracy: 0.85<br>Multiturn Accuracy: 1.00 | `starter_v0/runs/v0_B_base_anthropic_20261110T185714788317.json` |
| v1 | `system_prompt.md` | Prompt bảo "đoán khi thiếu thông tin" → thay bằng: thiếu handle/URL thì gọi `clarify(response_type="text")`, tên người nổi tiếng thì tự map sang handle. Kỳ vọng sửa R10 | Case Accuracy: 0.85<br>Routing Accuracy: 0.95<br>Argument Accuracy: 0.85<br>Multiturn Accuracy: 1.00 | Case Accuracy: 0.90<br>Routing Accuracy: 1.00<br>Argument Accuracy: 0.90<br>Multiturn Accuracy: 1.00 | `starter_v0/runs/v1_B_base_anthropic_20261110T190337487498.json` |
| v2 | `system_prompt.md` | Prompt bảo "gửi ngay" + "chỉ một bước" → thay bằng boundary `send` (`clarify` yes_no trước, `send(confirmed=true)` chỉ sau khi user đồng ý), rule scope, cho phép nhiều tool call. Kỳ vọng sửa R12 | Case Accuracy: 0.90<br>Routing Accuracy: 1.00<br>Argument Accuracy: 0.90<br>Multiturn Accuracy: 1.00 | Case Accuracy: 0.90<br>Routing Accuracy: 1.00<br>Argument Accuracy: 0.90<br>Multiturn Accuracy: 1.00 | `starter_v0/runs/v2_B_base_anthropic_20261110T190641839759.json` |
| v3 | `system_prompt.md` | R12 ở v2 vẫn hỏi bằng `text` vì rule thiếu-info (v1) khớp trước rule send (v2) → thêm câu ưu tiên: yêu cầu gửi/đăng luôn dùng `yes_no` kể cả khi thiếu nội dung. Kỳ vọng sửa R12 | Case Accuracy: 0.90<br>Routing Accuracy: 1.00<br>Argument Accuracy: 0.90<br>Multiturn Accuracy: 1.00 | Case Accuracy: 0.90<br>Routing Accuracy: 0.95<br>Argument Accuracy: 0.90<br>Multiturn Accuracy: 1.00 | `starter_v0/runs/v3_B_base_anthropic_20261110T191540035836.json` |
| v4 | `tools.yaml` | Lỗi còn lại nằm ở tool declaration: `lookup.query` chỉ ghi "Truy vấn", `clarify.response_type` chỉ ghi "Kiểu trả lời" → viết lại description mọi tool (dùng khi / không dùng khi) và convention args. Kỳ vọng sửa R03 và R12 | Case Accuracy: 0.90<br>Routing Accuracy: 0.95<br>Argument Accuracy: 0.90<br>Multiturn Accuracy: 1.00 | Case Accuracy: 0.95<br>Routing Accuracy: 1.00<br>Argument Accuracy: 0.95<br>Multiturn Accuracy: 1.00 | `starter_v0/runs/v4_B_base_anthropic_20261110T194411961520.json` |

Nhận xét:

- v1 là thay đổi duy nhất tăng điểm: R10 FAIL → PASS, không case nào hồi quy.
- v2 và v3 **không** sửa được R12 dù đã thêm rule và rule ưu tiên. Ở cả hai run, model vẫn gọi `clarify(response_type="text")` hỏi "Bạn muốn đăng nội dung nào…". Giả thuyết "xung đột thứ tự rule trong prompt" bị bác bỏ một phần: thêm ưu tiên trong prompt chưa đủ. Giả thuyết tiếp theo: khai báo `clarify` trong `tools.yaml` chỉ mô tả `response_type` là "Kiểu trả lời", không nói khi nào dùng `yes_no` → sửa ở tool declaration (v4).
- Ở v3, R03 ngoài lỗi query còn có thêm `extra tool call social_search`. Ở v2 R03 chỉ gọi `lookup`. Có thể đây là tác dụng phụ của rule "Use as many tool calls as the request needs" (thêm ở v2), hoặc là nhiễu giữa các lần chạy. Cần theo dõi ở version sau.
- v4 (chỉ đổi tools hash `52991d62c549` → `9348c98e2756`, prompt giữ `d5217c9a0a41`):
  - **R03 FAIL → PASS:** model gọi `lookup(query="AI", topic="news", timeframe="day")`. Không còn nhồi "news today" vào query, cũng hết lệnh gọi thừa `social_search` đã thấy ở v3.
  - R13 vẫn PASS với `query="AI"` cho cả hai tool.
  - **R12 vẫn FAIL:** `clarify(response_type="text", "Bản tin nào mà bạn muốn đăng?…")`. Đã sửa ở cả prompt (v2, v3) lẫn tool declaration (v4) mà model vẫn ưu tiên hỏi nội dung khi user không đưa nội dung.
- v1→v3 chỉ đổi prompt hash, v4 chỉ đổi tools hash, đúng nguyên tắc mỗi version một thay đổi.

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

Run: `starter_v0/runs/v3_B_group_anthropic_20261110T192952220848.json` (`v3+pd5217c9a0a41+t52991d62c549`, `claude-haiku-4-5`, 10/10 measured, 0 provider error).

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
| G01_cross_source_research (single) | Một yêu cầu cần hai nguồn: tin tức + bài báo học thuật | `lookup(topic=news)` + `papers` | PASS: `lookup(query="AI accelerator hardware", topic="news")` + `papers(query="evaluating AI accelerators")` |
| G02_source_restriction (single) | Tuân thủ giới hạn "chỉ đọc đúng URL này" | `fetch(url="https://www.anthropic.com/research")`, không search thêm | PASS |
| G03_dedup_utm_fragment (single) | Route tới tool mới khi user đưa danh sách nguồn và yêu cầu loại trùng | `deduplicate_sources` | PASS |
| G04_monthly_news (single) | `timeframe=month` (bộ base chỉ có day/week) | `lookup(topic=news, timeframe=month)` | PASS |
| G05_internal_privacy_policy (single) | Câu hỏi về chính sách nội bộ → `policy`, không search web | `policy(policy_area=data_privacy)` | PASS |
| G06_multiturn_dedup (multi) | Giữ danh sách nguồn qua nhiều lượt rồi route tới tool mới | `deduplicate_sources` | PASS |
| G07_multiturn_social_preferences (multi) | Carry `search_type=Top` và cập nhật `limit=7` | `social_search(search_type=Top, limit=7)` | PASS |
| G08_multiturn_monthly_topic_change (multi) | Đổi chủ đề nhưng giữ `topic=news`, `timeframe=month` | `lookup(topic=news, timeframe=month)` | PASS: `query="AI privacy risks"` |
| G09_multiturn_publish_confirmation (multi) | Đã có nội dung cuối → xin xác nhận trước khi gửi | `clarify(response_type=yes_no)` | PASS: hỏi "I will send this message to Telegram: …" |
| G10_multiturn_source_switch (multi) | Lượt cuối đổi từ papers sang web news tuần này | `lookup(topic=news, timeframe=week)` | PASS |

Nhận xét:

- 10/10 PASS. Bộ case nhóm viết **chưa đủ khó để phân biệt các version**: mọi case đều có thông tin rõ ràng, nên không đo được các điểm yếu còn lại ở bộ base.
- G09 PASS nhưng R12 (base) FAIL ở cùng prompt v3. Khác biệt: G09 có nội dung cuối cùng rõ ràng, R12 chỉ nói "bản tin này". Như vậy agent đã biết xin xác nhận `yes_no`; nó chỉ chuyển sang hỏi nội dung (`text`) khi nội dung chưa có. Lỗi R12 là xung đột "thiếu thông tin" vs "xin xác nhận", không phải agent bỏ qua boundary.
- G03/G06 chỉ kiểm tra routing (`args: {}`). Tính đúng của việc loại trùng do unit test của tool kiểm tra (xem B5a), vì eval chỉ chấm lựa chọn của model.
- Lần sau nên thêm case khó hơn: thiếu cả nội dung lẫn nơi gửi, hoặc yêu cầu loại trùng nhưng chưa đưa danh sách (kỳ vọng `clarify`).

### B4. Live Chat Evidence

Lấy từ `starter_v0/transcripts/*.transcript.json`.

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
|  |  |  |  |  |

### B5a. Required Evidence — Tool mới, unit test, UI

| Item | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Tool mới (`tools/<tên>/`) | `starter_v0/tools/deduplicate/tool.py`, `TOOL.md`; đăng ký trong `tools/__init__.py` (`TOOL_FUNCTIONS["deduplicate_sources"]`) và `artifacts/tools.yaml` | Model route đúng tới tool ở cả single-turn (G03) và multi-turn (G06): `starter_v0/runs/v3_B_group_anthropic_20261110T192952220848.json` | Tool chỉ xử lý dữ liệu local, `side_effect: false`. Không gộp các URL khác nhau dù cùng nội dung. Lỗi trả error dict |
| Unit test tool mới (≥ 3 test/tool) | `starter_v0/tests/test_tools_todo.py` (5 hàm test `test_deduplicate_*`, trong đó `test_deduplicate_bad_input_from_model` được parametrize); `pytest`: 82 passed, 0 failed | Happy path, input xấu từ model, nhánh lỗi trả error dict, URL khác nhau không bị gộp, list rỗng | Test không gọi mạng; nhánh lỗi được giả lập bằng `monkeypatch` |
| UI (lệnh chạy + link dùng thử) | *TODO CP5* |  |  |

Tool unit tests: nhóm viết 5 hàm test cho `deduplicate_sources`. Ví dụ unit test bắt được nhưng eval không bắt được: eval G03/G06 chỉ kiểm tra model có **gọi** `deduplicate_sources` hay không (`args: {}`). Nếu hàm chuẩn hóa URL sai (vd. không bỏ `?utm_source=` nên vẫn giữ bản trùng), eval vẫn PASS. Chỉ `test_deduplicate_happy_path` mới phát hiện được, vì nó kiểm tra `item_count` và `removed_count` của kết quả.

### B5. Bonus Evidence

Chỉ điền nếu nhóm làm bonus (ghi riêng, tối đa 10 điểm). Tool có sẵn (`send`, `policy`, `papers`, `paper_text`) không tự được bonus.

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Small Local Model | xem B7 |  |  |
| Hơn 3 tool mới (≥ 4) |  |  |  |
| `send` gửi thật lên Telegram sau xác nhận | transcript |  |  |
| Test challenge (0 skipped / regression test) | `pytest` output |  |  |

Test challenge: số bug tìm được trong tool có sẵn (nếu có), cách sửa, và test regression tương ứng.

Bug tìm được trong code starter (không phải tool, nên chưa tính bonus; ghi lại làm bằng chứng):

1. **`run_eval.normalize_value` không so sánh được list các object.** Hàm này `sorted()` list trước khi so sánh, nên khi `expect.args` chứa list dict (vd. `items` của `deduplicate_sources`) sẽ ném `TypeError: '<' not supported between instances of 'dict' and 'dict'`. Lỗi bị bắt trong `try` của `main()` nên case bị ghi là `provider_error`, làm cả run không hợp lệ. Nhóm tái hiện bằng cách gọi `run_eval.compare_subset` với expect ban đầu của G03. Không sửa `run_eval.py` (ngoài danh sách file được sửa); thay vào đó expect của G03/G06 chỉ kiểm tra tên tool.
2. **`providers/anthropic_provider.py` không chạy với `anthropic>=1.0`:** xem mục 5. Xử lý bằng cách pin `anthropic<1`.

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
- **Kết quả không tất định:** khi còn dùng gpt-4o-mini, nhóm thấy cùng prompt và cùng hash nhưng R03 lúc PASS lúc FAIL. Các run gpt-4o-mini đã bị loại khỏi repo vì khác model với v0–v4, nên đây chỉ là quan sát, không dùng làm bằng chứng. Bài học: so sánh từng case giữa các version thay vì chỉ nhìn điểm tổng.
- **Hash đổi dù nội dung không đổi:** `tools.yaml` được lưu lại trong editor nên đổi line ending (LF/CRLF), hash đổi từ `e69bc53ed884` sang `52991d62c549` dù `git diff` rỗng. Vì vậy v0 được chạy lại để v0–v3 dùng chung tools hash.
- **Gắn nhầm nhãn version:** có lần prompt v1 đã được commit nên `git stash` không đưa prompt về bản gốc, và run "v0" thực chất dùng prompt v1 (hash `p27bc123aba94`). Nhóm phát hiện bằng cách đối chiếu prompt hash trong mỗi run, xóa các run sai, rồi khôi phục prompt gốc bằng `git checkout 0fc07b6 -- artifacts/system_prompt.md`.

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong [TEAM.md](../../TEAM.md) và các báo cáo cá nhân `report/team/MSSV_HoTen.md`.

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- **Fix nào thuộc `system_prompt.md`?** Các lỗi do **hành vi chung** của agent: đoán thay vì hỏi (R10), gửi không xác nhận, gọi tool cho câu ngoài phạm vi, ép một bước. Đây là chính sách áp dụng cho mọi tool, nên đặt trong prompt (v1–v3). Bằng chứng: v1 sửa R10.
- **Fix nào thuộc `tools.yaml`?** Các lỗi do **cách điền tham số của một tool cụ thể**: R03 nhồi "tin tức hôm nay" vào `query` dù đã điền đúng `topic=news` và `timeframe=day`, vì description của tham số chỉ ghi "Truy vấn". Bằng chứng: hai rule trong prompt (v2, v3) không đổi được R03, còn một dòng description cho `lookup.query` ở v4 sửa được ngay (`query="AI"`). Với lỗi điền tham số, description của tham số hiệu quả hơn rule chung trong prompt.
- **Failure nào cần review thủ công?**
  - **R12:** sau 3 lần sửa (v2, v3, v4), model vẫn hỏi "Bản tin nào bạn muốn đăng?" bằng `text` khi user chỉ nói "bản tin này". Còn ở G09, khi nội dung đã có, model hỏi `yes_no` đúng. Nghĩa là agent không bỏ qua boundary: nó không bao giờ tự gửi, chỉ chọn hỏi nội dung trước vì chưa có gì để xác nhận. Hành vi này an toàn và hợp lý, nhưng eval chỉ chấp nhận `yes_no`. Nhóm cho rằng case này cần người review, không nên ép model đạt điểm bằng mọi giá.
  - **Kết quả tool:** eval không chấm `tool_results` (vd. run đầu tiên Tavily trả 401 mà điểm không đổi), nên chất lượng câu trả lời cuối phải kiểm tra bằng transcript.
  - **Thay đổi ±1 case:** cần xem lại từng case trước khi kết luận, vì kết quả LLM không tất định.
- **Nếu có thêm một vòng (v5):** với R12, thử hai hướng (mỗi hướng một version):
  - (a) Trong prompt, cho ví dụ cụ thể "Đăng bản tin này lên Telegram" → `clarify(yes_no, "Bạn muốn mình đăng bản tin vừa tổng hợp lên Telegram chứ?")`, vì rule trừu tượng chưa đủ.
  - (b) Đề xuất sửa expect của R12 để chấp nhận cả `clarify(text)` hỏi nội dung, vì đây cũng là hành vi đúng boundary.

  Ngoài ra, bổ sung group case khó hơn (bộ group hiện 10/10, chưa phân biệt được các version).

## 8. Tài liệu tham khảo

- Đề bài và cách chấm: [README.md](../../README.md), [CHECKPOINTS.md](../../CHECKPOINTS.md), [RUBRIC.md](../../RUBRIC.md)
- Hướng dẫn starter và contract tool: `starter_v0/README.md`, `starter_v0/tools/README.md`
- Cấu hình key tool: [docs/TOOL-SETUP.md](../../docs/TOOL-SETUP.md)
- Bằng chứng: `starter_v0/runs/*.json`, `starter_v0/artifacts/version_log.csv`
