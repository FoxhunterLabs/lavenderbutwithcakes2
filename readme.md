________________________________________
# LavenderButWithCakes2

**Consent-first, human-gated inference for detecting upcoming birthdays from authorized text imports.**

LavenderButWithCakes2 is a safety-oriented inference system that ingests **explicitly provided text** (SMS exports, email snippets, chat logs) and produces *reviewable candidates* for time-sensitive actions — never autonomous actions.

No scraping. No guessing. No surprises.

---

## Why this exists

Most “helpful” automation fails because it:
- overreaches
- infers intent without consent
- acts before a human can intervene

LavenderButWithCakes2 takes the opposite approach:

> **Inference is allowed.  
Action is gated.  
Humans stay in control.**

---

## Core principles

- **Consent-first**  
  Only text explicitly imported by a human is processed.

- **Audit-first**  
  Every observation, inference, decision, and outcome is logged.

- **Human-in-the-loop**  
  The system *suggests* candidates; humans decide.

- **No surprise actions**  
  Privacy flags and “do not surprise” flags block candidate creation.

- **Explainable logic**  
  Deterministic rules + Bayesian fusion. No opaque ML.

---

## What the system does (end-to-end)

1. **Ingest authorized text**
   - Unified batch ingestion (`/api/import_batch`)
   - Import-only connectors (SMS, email, Slack, Teams, calendar)

2. **Normalize + minimize**
   - Strip inputs to only what’s needed
   - Store minimal observations

3. **Extract evidence**
   - Auditable pattern rules (e.g. “happy birthday”, explicit dates)
   - Evidence is evidence, not truth

4. **Fuse probabilities**
   - Conservative Bayesian log-odds fusion
   - Time-windowed posteriors (today / 3d / 14d)

5. **Generate candidates**
   - Only if thresholds + confidence are met
   - Blocked by privacy or “do not surprise”

6. **Human gate**
   - Approve / defer / reject
   - Required checks surfaced (address, allergies, preferences)

7. **Log outcomes**
   - Delivered / not delivered
   - Delight score (-1 / 0 / +1)
   - Used for future calibration

---

## What this system will NOT do

- ❌ Scrape data
- ❌ Read messages without explicit import
- ❌ Autonomously message anyone
- ❌ Infer sensitive attributes
- ❌ Act without human approval

This is an **inference assistant**, not an autonomous agent.

---

## Architecture overview

app.py → thin Flask boot + wiring
config.py → thresholds, priors, global policy
db.py → SQLite schema + connection
audit.py → append-only audit log
models/ → all DB writes live here
people.py
observations.py
evidence.py
candidates.py
outcomes.py
connectors.py
inference/ → thinking only (pure logic)
patterns.py
extract.py
bayes.py
candidates.py
ingestion/ → the single intake pipe
normalize.py
ingest.py
connectors/ → import-only connectors
base.py
registry.py
api/ → REST surface
routes.py
ui/ → lightweight human gate UI
routes.py

Key rule: **logic never lives in Flask routes**.

---

## API surface

### Health
GET /health

### Unified ingestion
POST /api/import_batch

```json
{
  "person_key": "mike_smith",
  "connector": "teams_import",
  "items": [
    {
      "occurred_at": "2025-12-21T18:20:00+00:00",
      "text": "Happy birthday Mike!",
      "meta": {
        "source": "teams",
        "channel": "Engineering",
        "author": "alice",
        "is_dm": false
      }
    }
  ],
  "default_meta": {
    "ingest": "example_client"
  }
}
Posteriors
GET /api/posteriors/<person_key>
Candidates
GET /api/candidates?status=PENDING
Outcomes
POST /api/outcome
________________________________________
UI (optional)
A lightweight UI exists at:
/ui
It supports:
•	Person management
•	Viewing posteriors
•	Human review of candidates
The UI is intentionally thin and replaceable.
________________________________________
Running locally
pip install -r requirements.txt
python app.py
The system uses SQLite by default and requires no external services.
________________________________________
Design philosophy
LavenderButWithCakes2 is built around a simple idea:
Automation should reduce cognitive load without removing agency.
This system is intentionally conservative, inspectable, and reversible.
It is designed for environments where trust, safety, and accountability matter more than speed or scale.
________________________________________
Status
This is a working reference implementation, not a growth-hacked product.
It is meant to be read, audited, extended, and adapted — not blindly deployed.
________________________________________
License
MIT
