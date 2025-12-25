import json
import uuid
from typing import Dict, List, Tuple
from db import db, now_iso
from audit import audit


def create_candidate(
    person_key: str,
    window: str,
    posterior: float,
    confidence: float,
    rationale: Dict,
    required_checks: List[str],
) -> str:
    cid = str(uuid.uuid4())
    conn = db()
    conn.execute(
        """
        INSERT INTO candidates(
            id, person_key, window,
            posterior, confidence,
            rationale_json, required_checks_json,
            status, created_at
        )
        VALUES(?,?,?,?,?,?,?,?,?)
        """,
        (
            cid,
            person_key,
            window,
            posterior,
            confidence,
            json.dumps(rationale, ensure_ascii=False),
            json.dumps(required_checks, ensure_ascii=False),
            "PENDING",
            now_iso(),
        ),
    )
    conn.commit()
    conn.close()

    audit(
        "candidate_created",
        {
            "candidate_id": cid,
            "person_key": person_key,
            "window": window,
            "posterior": posterior,
        },
    )
    return cid
