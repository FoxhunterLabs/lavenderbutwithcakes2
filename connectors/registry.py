import json
from typing import Any, Dict, List, Tuple

from audit import audit
from db import db
from models.connectors import (
    list_connectors,
    upsert_connector,
    update_connector_last_sync,
)

from connectors.base import (
    BaseConnector,
    ConnectorResult,
    SMSiMessageImportConnector,
    EmailImportConnector,
    SlackImportConnector,
    TeamsImportConnector,
    CalendarImportConnector,
)

CONNECTOR_REGISTRY: Dict[str, BaseConnector] = {
    "sms_imessage_import": SMSiMessageImportConnector(),
    "email_import": EmailImportConnector(),
    "slack_import": SlackImportConnector(),
    "teams_import": TeamsImportConnector(),
    "calendar_import": CalendarImportConnector(),
}


def ensure_default_connectors() -> None:
    existing = {c["name"] for c in list_connectors()}

    defaults: List[Tuple[str, int, Dict[str, Any]]] = [
        ("sms_imessage_import", 1, {"note": "explicit import only"}),
        ("email_import", 0, {"note": "explicit import only"}),
        ("slack_import", 0, {"note": "explicit import only"}),
        ("teams_import", 0, {"note": "explicit import only"}),
        ("calendar_import", 0, {"note": "explicit import only"}),
    ]

    for name, enabled, cfg in defaults:
        if name not in existing:
            upsert_connector(name, enabled, cfg)


def run_connector_sync(connector_id: str) -> ConnectorResult:
    conn = db()
    row = conn.execute("SELECT * FROM connectors WHERE id=?", (connector_id,)).fetchone()
    conn.close()

    if not row:
        return ConnectorResult(0, 0, ["connector not found"])
    if int(row["enabled"]) != 1:
        return ConnectorResult(0, 0, ["connector disabled"])

    name = row["name"]
    impl = CONNECTOR_REGISTRY.get(name)
    if not impl:
        return ConnectorResult(0, 0, [f"no registered implementation for {name}"])

    config = json.loads(row["config_json"] or "{}")
    res = impl.sync(row["id"], config)

    update_connector_last_sync(row["id"])
    audit(
        "connector_synced",
        {"connector_id": row["id"], "name": name, "observations": res.observations, "evidence": res.evidence},
    )
    return res
