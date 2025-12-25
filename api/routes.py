from flask import Blueprint, request, jsonify

from ingestion.ingest import ingest_batch
from inference.bayes import compute_posteriors
from models.people import get_person
from db import db
from models.candidates import create_candidate
from models.outcomes import log_outcome

api = Blueprint("api", __name__)


@api.route("/import_batch", methods=["POST"])
def api_import_batch():
    data = request.get_json(force=True, silent=True) or {}

    person_key = (data.get("person_key") or "").strip()
    connector = (data.get("connector") or "").strip()
    items = data.get("items")
    default_meta = data.get("default_meta")

    if not person_key or not connector or not isinstance(items, list):
        return jsonify({"status": "error", "message": "person_key, connector, items[] required"}), 400

    if default_meta is not None and not isinstance(default_meta, dict):
        return jsonify({"status": "error", "message": "default_meta must be an object"}), 400

    res = ingest_batch(person_key, connector, items, default_meta)
    if not res.get("ok"):
        return jsonify({"status": "error", "message": res.get("message")}), int(res.get("status", 400))

    return jsonify({
        "status": "success",
        "observations": res["observations"],
        "evidence_created": res["evidence_created"],
        "candidate_id": res["candidate_id"],
        "posteriors": res["posteriors"],
    }), 200


@api.route("/posteriors/<person_key>", methods=["GET"])
def api_posteriors(person_key: str):
    if not get_person(person_key):
        return jsonify({"status": "error", "message": "unknown person"}), 404
    return jsonify(compute_posteriors(person_key)), 200


@api.route("/candidates", methods=["GET"])
def api_candidates():
    status = (request.args.get("status") or "PENDING").strip().upper()
    conn = db()
    rows = conn.execute(
        "SELECT * FROM candidates WHERE status=? ORDER BY created_at DESC LIMIT 200",
        (status,),
    ).fetchall()
    conn.close()
    return jsonify({"status": "success", "candidates": [dict(r) for r in rows]}), 200


@api.route("/outcome", methods=["POST"])
def api_outcome():
    data = request.get_json(force=True, silent=True) or {}

    cid = (data.get("candidate_id") or "").strip()
    delivered = bool(data.get("delivered", False))
    delight = int(data.get("delight", 0))
    notes = (data.get("notes") or "").strip()

    ok, msg = log_outcome(cid, delivered, delight, notes)
    return jsonify({"status": "success" if ok else "error", "message": msg}), (200 if ok else 400)
