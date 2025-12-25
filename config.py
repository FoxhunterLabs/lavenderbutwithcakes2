import os
from datetime import timezone

APP_NAME = "LavenderButWithCakes2"
DB_PATH = os.environ.get("LBC_DB", "lavenderbutwithcakes2.db")
UTC = timezone.utc

ENGINE = {
    "evidence_decay_days": 30,
    "observation_decay_days": 90,
    "min_confidence": 0.35,
    "threshold_today": 0.80,
    "threshold_3d": 0.75,
    "threshold_14d": 0.68,
    "respect_privacy_mode": True,
    "respect_do_not_surprise": True,
    "priors": {
        "today": 1.0 / 365.0,
        "within_3d": 3.0 / 365.0,
        "within_14d": 14.0 / 365.0,
    },
}
