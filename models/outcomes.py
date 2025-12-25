import uuid
from typing import Tuple
from db import db, now_iso
from audit import audit


def log_outcome(
    candidate_id: str,
    delivered: bool,
    delight: int,
    notes: str = "",
) -> Tuple[bool, str]:
    if delight not in {-1, 0, 1}:
        return False, "invalid delight"

    oid = str(uuid.uuid4())
    conn = db()
    conn.execute(
        """
        INSERT INTO outcomes(
            id, candidate_id,
            delivered, delight,
            notes, created_at
        )
        VALUES(?,?,?,?,?,?)
        """,
        (oid, candidate_id, int(delivered), delight, notes, now_iso()),
    )
    conn.commit()
    conn.close()

    audit(
        "outcome_logged",
        {
            "candidate_id": candidate_id,
            "delivered": delivered,
            "delight": delight,
        },
    )
    return True, oid
