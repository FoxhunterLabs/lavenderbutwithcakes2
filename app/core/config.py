from datetime import timezone

APP_NAME = "LavenderButWithCakes2"
UTC = timezone.utc

# ============================================================
# Engine configuration (policy + thresholds)
# ============================================================

ENGINE = {
    "evidence_decay_days": 30,
    "observation_decay_days": 90,

    "min_confidence": 0.35,

    "threshold_today": 0.80,
    "threshold_3d": 0.75,
    "threshold_14d": 0.68,

    # Ethical gates
    "respect_privacy_mode": True,
    "respect_do_not_surprise": True,

    # Bayesian priors (calendar-normalized)
    "priors": {
        "today": 1.0 / 365.0,
        "within_3d": 3.0 / 365.0,
        "within_14d": 14.0 / 365.0,
    },
}

# ============================================================
# Claims
# ============================================================

CLAIMS = {
    "birthday_today",
    "birthday_within_3d",
    "birthday_within_14d",
    "birthday_date_explicit",
}

# ============================================================
# Likelihood Ratios (conservative defaults)
# ============================================================

DEFAULT_LRS = {
    # Explicit self-declared date
    "birthday_date_explicit": 100.0,

    # Same-day cues
    "birthday_today_strong": 25.0,
    "birthday_today_medium": 8.0,
    "birthday_today_weak": 3.0,

    # Near-term cues
    "birthday_3d_strong": 12.0,
    "birthday_3d_medium": 5.0,
    "birthday_3d_weak": 2.0,

    # Loose future cues
    "birthday_14d_strong": 6.0,
    "birthday_14d_medium": 3.0,
    "birthday_14d_weak": 1.6,
}
