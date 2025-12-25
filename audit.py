import json
import uuid
from typing import Any, Dict, Optional

from db import db, now_iso


def audit(event: str, data: Optional[Dict[str, Any]] = None) -> None:
    """
    Append-only audit log.
    This should never raise; failures must not block core logic.
    """
    try:
        conn = db()
        conn.execute(
            "INSERT INTO audit_log(id, event, data_json, created_at) VALUES(?,?,?,?)",
            (
                str(uuid.uuid4()),
                event,
                json.dumps(data or {}, ensure_ascii=False),
                now_iso(),
            ),
        )
        conn.commit()
        conn.close()
    except Exception:
        # Audit must never crash the system
        pass
