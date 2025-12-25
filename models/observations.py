import json
import uuid
from typing import Any, Dict, Optional
from db import db
from audit import audit


def add_observation(
    person_key: str,
    connector_id: Optional[str],
    source_ref: Optional[str],
    payload: Dict[str, Any],
    occurred_at_iso: str,
) -> str:
    oid = str(uuid.uuid4())
    conn = db()
    conn.execute(
        """
        INSERT INTO observations(
            id, person_key, connector_id,
            source_ref, payload_json, occurred_at
        )
        VALUES(?,?,?,?,?,?)
        """,
        (
            oid,
            person_key,
            connector_id,
            source_ref,
            json.dumps(payload, ensure_ascii=False),
            occurred_at_iso,
        ),
    )
    conn.commit()
    conn.close()
    audit(
        "observation_ingested",
        {"obs_id": oid, "person_key": person_key, "connector_id": connector_id},
    )
    return oid
