import json
import uuid
from typing import Any, Dict, List, Optional

from db import db, now_iso
from audit import audit


def upsert_connector(name: str, enabled: int, config: Dict[str, Any]) -> str:
    conn = db()
    row = conn.execute("SELECT id FROM connectors WHERE name=?", (name,)).fetchone()

    if row:
        cid = row["id"]
        conn.execute(
            "UPDATE connectors SET enabled=?, config_json=? WHERE id=?",
            (int(enabled), json.dumps(config, ensure_ascii=False), cid),
        )
    else:
        cid = str(uuid.uuid4())
        conn.execute(
            "INSERT INTO connectors(id, name, enabled, config_json, last_sync_at) VALUES(?,?,?,?,?)",
            (cid, name, int(enabled), json.dumps(config, ensure_ascii=False), None),
        )

    conn.commit()
    conn.close()

    audit("connector_upserted", {"connector_id": cid, "name": name, "enabled": int(enabled)})
    return cid


def list_connectors() -> List[Dict[str, Any]]:
    conn = db()
    rows = conn.execute("SELECT * FROM connectors ORDER BY name").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_enabled_connector_by_name(name: str) -> Optional[Dict[str, Any]]:
    conn = db()
    row = conn.execute(
        "SELECT * FROM connectors WHERE name=? AND enabled=1",
        (name,),
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def update_connector_last_sync(connector_id: str) -> None:
    conn = db()
    conn.execute("UPDATE connectors SET last_sync_at=? WHERE id=?", (now_iso(), connector_id))
    conn.commit()
    conn.close()
