from typing import Any, Dict, Optional
from db import now_iso


def normalize_batch_item(item: Any) -> Optional[Dict[str, Any]]:
    """
    Unified item schema:
      {
        "occurred_at": "...",   # optional
        "text": "...",          # REQUIRED
        "meta": {...},          # optional dict
        "source_ref": "..."     # optional
      }
    """
    if not isinstance(item, dict):
        return None

    text = item.get("text")
    if text is None:
        text = item.get("body") or item.get("message") or item.get("content")

    text = str(text or "").strip()
    if not text:
        return None

    occurred_at = str(
        item.get("occurred_at")
        or item.get("date")
        or item.get("timestamp")
        or item.get("time")
        or ""
    ).strip()
    occurred_at = occurred_at or now_iso()

    meta = item.get("meta")
    if meta is None:
        meta = {}
    if not isinstance(meta, dict):
        meta = {"meta_raw": str(meta)}

    source_ref = item.get("source_ref") or item.get("id") or item.get("message_id") or item.get("event_id")

    return {
        "occurred_at": occurred_at,
        "text": text,
        "meta": meta,
        "source_ref": str(source_ref) if source_ref is not None else None,
    }
