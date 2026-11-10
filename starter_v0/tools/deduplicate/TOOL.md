---
name: deduplicate_sources
track: core
kind: local_formatter
provider: local
requires_env: []
inputs: [items]
outputs: [items, input_count, item_count, removed_count, duplicates]
side_effect: false
---

Loại nguồn có URL trùng trước khi format;

