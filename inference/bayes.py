import math
from datetime import datetime, timedelta
from typing import Dict, List
from config import ENGINE, UTC
from db import db


def logit(p: float) -> float:
    p = min(1 - 1e-9, max(1e-9, p))
    return math.log(p / (1 - p))


def sigmoid(x: float) -> float:
    return 1 / (1 + math.exp(-x))


def get_recent_evidence(person_key: str) -> List[Dict]:
    cutoff = (
        datetime.now(tz=UTC)
        - timedelta(days=ENGINE["evidence_decay_days"])
    ).isoformat()

    conn = db()
    rows = conn.execute(
        """
        SELECT * FROM evidence
        WHERE person_key=? AND evidence_time >= ?
        """,
        (person_key, cutoff),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def compute_posteriors(person_key: str) -> Dict:
    ev = get_recent_evidence(person_key)

    L_today = logit(ENGINE["priors"]["today"])
    L_3d = logit(ENGINE["priors"]["within_3d"])
    L_14d = logit(ENGINE["priors"]["within_14d"])

    for e in ev:
        log_lr = math.log(max(1e-9, float(e["lr"])))
        if e["claim"] == "birthday_today":
            L_today += log_lr
        elif e["claim"] == "birthday_within_3d":
            L_3d += log_lr
        elif e["claim"] == "birthday_within_14d":
            L_14d += log_lr
        else:
            L_today += log_lr
            L_3d += log_lr
            L_14d += log_lr

    return {
        "p_today": round(sigmoid(L_today), 4),
        "p_3d": round(sigmoid(L_3d), 4),
        "p_14d": round(sigmoid(L_14d), 4),
        "evidence_count": len(ev),
    }
