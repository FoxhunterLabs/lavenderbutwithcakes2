import json
import uuid
from typing import Any, Dict, Optional
from db import db, now_iso
from audit import audit

CLAIMS = {
    "birthday_today",
    "birthday_within_3d",
    "birthday_within_14d",
    "birthday_date_explicit",
}


def add_evidence(
    person_key: str,
    connector_id: Optional[str],
    claim: str,
    lr: float,
    strength: str,
    excerpt: str,
    evidence_time_iso: str,
    meta: Optional[Dict[str, Any]] = None,
) -> str:
    assert claim in CLAIMS
    eid = str(uuid.uuid4())

    conn = db()
    conn.execute(
        """
        INSERT INTO evidence(
            id, person_key, connector_id,
            claim, lr, strength,
            excerpt, evidence_time,
            created_at, meta_json
        )
        VALUES(?,?,?,?,?,?,?,?,?,?)
        """,
        (
            eid,
            person_key,
            connector_id,
            claim,
            float(lr),
            strength,
            excerpt,
            evidence_time_iso,
            now_iso(),
            json.dumps(meta or {}, ensure_ascii=False),
        ),
    )
    conn.commit()
    conn.close()

    audit(
        "evidence_created",
        {"evidence_id": eid, "person_key": person_key, "claim": claim, "lr": lr},
    )
    return eid
