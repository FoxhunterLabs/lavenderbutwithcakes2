import re
from typing import Dict, List, Optional
from datetime import datetime
from config import UTC
from models.evidence import add_evidence
from inference.patterns import (
    DEFAULT_LRS,
    BIRTHDAY_PATTERNS,
    DATE_EXPLICIT_PATTERNS,
)


def redact_excerpt(text: str, limit: int = 180) -> str:
    t = (text or "").strip().replace("\n", " ")
    return t[:limit] + ("…" if len(t) > limit else "")


def extract_evidence_from_text(
    person_key: str,
    connector_id: Optional[str],
    text: str,
    occurred_at_iso: str,
    source_meta: Optional[Dict] = None,
) -> List[str]:
    created = []
    raw = text or ""
    t = raw.lower()

    for pat in DATE_EXPLICIT_PATTERNS:
        if re.search(pat, t):
            created.append(
                add_evidence(
                    person_key,
                    connector_id,
                    "birthday_date_explicit",
                    DEFAULT_LRS["birthday_date_explicit"],
                    "explicit",
                    redact_excerpt(raw),
                    occurred_at_iso,
                    source_meta,
                )
            )
            break

    for bucket, pats in BIRTHDAY_PATTERNS.items():
        for pat in pats:
            if re.search(pat, t):
                claim = (
                    "birthday_today"
                    if "today" in bucket
                    else "birthday_within_3d"
                    if "3d" in bucket
                    else "birthday_within_14d"
                )
                lr_key = f"birthday_{bucket}"
                created.append(
                    add_evidence(
                        person_key,
                        connector_id,
                        claim,
                        DEFAULT_LRS.get(lr_key, 1.0),
                        bucket,
                        redact_excerpt(raw),
                        occurred_at_iso,
                        source_meta,
                    )
                )
                return created

    return created
