from typing import Any, Dict, List, Optional

from audit import audit
from models.people import get_person, upsert_person
from models.connectors import get_enabled_connector_by_name
from models.observations import add_observation
from inference.extract import extract_evidence_from_text, redact_excerpt
from inference.candidates import create_candidate_if_needed
from inference.bayes import compute_posteriors
from ingestion.normalize import normalize_batch_item


def ingest_batch(
    person_key: str,
    connector_name: str,
    items: List[Any],
    default_meta: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Hard-gated unified ingestion:
      - connector must exist + enabled
      - writes minimized observations
      - runs evidence extraction
      - attempts candidate creation (human gate still required)
    """
    if not get_person(person_key):
        upsert_person(person_key, consent_scope="import")

    connector = get_enabled_connector_by_name(connector_name)
    if not connector:
        audit(
            "batch_import_rejected",
            {"person_key": person_key, "connector": connector_name, "reason": "connector_disabled_or_unknown"},
        )
        return {"ok": False, "status": 403, "message": "connector disabled or unknown"}

    connector_id = connector["id"]
    obs_count = 0
    ev_count = 0

    for raw in items:
        n = normalize_batch_item(raw)
        if not n:
            continue

        occurred_at = str(n["occurred_at"]).strip()
        text = n["text"]
        meta = dict(default_meta or {})
        meta.update(n.get("meta") or {})

        meta.setdefault("source", connector_name.replace("_import", "").replace("sms_imessage", "sms_imessage"))

        add_observation(
            person_key,
            connector_id,
            n.get("source_ref"),
            {**meta, "text": redact_excerpt(text, 800)},
            occurred_at,
        )
        obs_count += 1

        ev_ids = extract_evidence_from_text(person_key, connector_id, text, occurred_at, meta)
        ev_count += len(ev_ids)

    cand_id = create_candidate_if_needed(person_key)

    audit(
        "batch_import_ingested",
        {
            "person_key": person_key,
            "connector": connector_name,
            "items": len(items),
            "observations": obs_count,
            "evidence": ev_count,
            "candidate_id": cand_id,
        },
    )

    return {
        "ok": True,
        "status": 200,
        "person_key": person_key,
        "connector": connector_name,
        "observations": obs_count,
        "evidence_created": ev_count,
        "candidate_id": cand_id,
        "posteriors": compute_posteriors(person_key),
    }
