import os
import json
import uuid
import sqlite3
from typing import Any, Dict, Optional
from datetime import datetime

from app.core.config import UTC

DB_PATH = os.environ.get("LBC_DB", "lavenderbutwithcakes.db")

# ============================================================
# Time helpers
# ============================================================

def now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()

# ============================================================
# Connection helpers
# ============================================================

def db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ============================================================
# Schema
# ============================================================

def init_db() -> None:
    conn = db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS persons (
        person_key TEXT PRIMARY KEY,
        display_name TEXT,
        consent_scope TEXT NOT NULL,
        privacy_mode INTEGER NOT NULL,
        do_not_surprise INTEGER NOT NULL,
        verifier_contact TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS connectors (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        enabled INTEGER NOT NULL,
        config_json TEXT NOT NULL,
        last_sync_at TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS observations (
        id TEXT PRIMARY KEY,
        person_key TEXT NOT NULL,
        connector_id TEXT,
        source_ref TEXT,
        payload_json TEXT NOT NULL,
        occurred_at TEXT NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS evidence (
        id TEXT PRIMARY KEY,
        person_key TEXT NOT NULL,
        connector_id TEXT,
        claim TEXT NOT NULL,
        lr REAL NOT NULL,
        strength TEXT NOT NULL,
        excerpt TEXT,
        evidence_time TEXT NOT NULL,
        created_at TEXT NOT NULL,
        meta_json TEXT NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS candidates (
        id TEXT PRIMARY KEY,
        person_key TEXT NOT NULL,
        window TEXT NOT NULL,
        posterior REAL NOT NULL,
        confidence REAL NOT NULL,
        rationale_json TEXT NOT NULL,
        required_checks_json TEXT NOT NULL,
        status TEXT NOT NULL,
        created_at TEXT NOT NULL,
        decided_at TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS decisions (
        id TEXT PRIMARY KEY,
        candidate_id TEXT NOT NULL,
        decision TEXT NOT NULL,
        reason TEXT,
        decided_by TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS outcomes (
        id TEXT PRIMARY KEY,
        candidate_id TEXT NOT NULL,
        delivered INTEGER NOT NULL,
        delight INTEGER NOT NULL,
        notes TEXT,
        created_at TEXT NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS audit_log (
        id TEXT PRIMARY KEY,
        event TEXT NOT NULL,
        data_json TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

# ============================================================
# Audit log
# ============================================================

def audit(event: str, data: Optional[Dict[str, Any]] = None) -> None:
    conn = db()
    conn.execute(
        "INSERT INTO audit_log(id, event, data_json, created_at) VALUES(?,?,?,?)",
        (
            str(uuid.uuid4()),
            event,
            json.dumps(data or {}, ensure_ascii=False),
            now_iso(),
        )
    )
    conn.commit()
    conn.close()
