from typing import Optional, Dict, List
from db import db, now_iso


def upsert_person(
    person_key: str,
    display_name: Optional[str] = None,
    consent_scope: str = "import",
    privacy_mode: int = 0,
    do_not_surprise: int = 0,
    verifier_contact: Optional[str] = None,
) -> None:
    conn = db()
    row = conn.execute(
        "SELECT person_key FROM persons WHERE person_key=?", (person_key,)
    ).fetchone()
    ts = now_iso()

    if row:
        conn.execute(
            """
            UPDATE persons
            SET display_name=COALESCE(?, display_name),
                consent_scope=?,
                privacy_mode=?,
                do_not_surprise=?,
                verifier_contact=COALESCE(?, verifier_contact),
                updated_at=?
            WHERE person_key=?
            """,
            (
                display_name,
                consent_scope,
                privacy_mode,
                do_not_surprise,
                verifier_contact,
                ts,
                person_key,
            ),
        )
    else:
        conn.execute(
            """
            INSERT INTO persons(
                person_key, display_name, consent_scope,
                privacy_mode, do_not_surprise,
                verifier_contact, created_at, updated_at
            )
            VALUES(?,?,?,?,?,?,?,?)
            """,
            (
                person_key,
                display_name,
                consent_scope,
                privacy_mode,
                do_not_surprise,
                verifier_contact,
                ts,
                ts,
            ),
        )

    conn.commit()
    conn.close()


def get_person(person_key: str) -> Optional[Dict]:
    conn = db()
    row = conn.execute(
        "SELECT * FROM persons WHERE person_key=?", (person_key,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def list_people(limit: int = 50) -> List[Dict]:
    conn = db()
    rows = conn.execute(
        "SELECT * FROM persons ORDER BY updated_at DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]
