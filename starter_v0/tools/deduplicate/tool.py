"""Conservative URL deduplication; never fetches URLs or judges factual accuracy."""

from copy import deepcopy
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from tools._shared import err


def _url_key(value: str) -> str:
    parsed = urlsplit(value.strip())
    if parsed.scheme.lower() not in {"http", "https"} or not parsed.hostname:
        raise ValueError("Each URL must be an absolute HTTP(S) URL")
    if parsed.username is not None or parsed.password is not None:
        raise ValueError("URLs must not contain credentials")
    port = parsed.port  # Validate malformed port numbers.
    host = parsed.hostname.lower()
    if ":" in host:
        host = f"[{host}]"
    if port is not None and (parsed.scheme.lower(), port) not in {("http", 80), ("https", 443)}:
        host += f":{port}"
    # Preserve query order, content parameters, scheme, path case, and trailing slash.
    query = [(k, v) for k, v in parse_qsl(parsed.query, keep_blank_values=True)
             if not k.lower().startswith("utm_") and k.lower() not in {"fbclid", "gclid"}]
    return urlunsplit((parsed.scheme.lower(), host, parsed.path or "/", urlencode(query), ""))


def deduplicate_sources(items: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """Keep the first item per normalized URL and report duplicate input indices."""
    try:
        if not isinstance(items, list):
            raise ValueError("items must be a list (an empty list is allowed)")
        if len(items) > 500:
            raise ValueError("At most 500 items are allowed")
        seen: dict[str, int] = {}
        kept: list[dict[str, Any]] = []
        duplicates = []
        for index, item in enumerate(items):
            if not isinstance(item, dict):
                raise ValueError(f"items[{index}] must be an object")
            url = item.get("url")
            if not isinstance(url, str) or not url.strip():
                raise ValueError(f"items[{index}].url must be a nonempty string")
            key = _url_key(url)
            if key in seen:
                duplicates.append({"index": index, "kept_index": seen[key]})
            else:
                seen[key] = index
                kept.append(deepcopy(item))
        return {"tool": "deduplicate_sources", "items": kept, "input_count": len(items),
                "item_count": len(kept), "removed_count": len(duplicates), "duplicates": duplicates}
    except Exception as exc:
        return err("deduplicate_sources", exc)
