import re

DEFAULT_LRS = {
    "birthday_date_explicit": 100.0,
    "birthday_today_strong": 25.0,
    "birthday_today_medium": 8.0,
    "birthday_today_weak": 3.0,
    "birthday_3d_strong": 12.0,
    "birthday_3d_medium": 5.0,
    "birthday_3d_weak": 2.0,
    "birthday_14d_strong": 6.0,
    "birthday_14d_medium": 3.0,
    "birthday_14d_weak": 1.6,
}

BIRTHDAY_PATTERNS = {
    "today_strong": [
        r"\bhappy birthday\b",
        r"\bhbd\b",
        r"\bhappy bday\b",
    ],
    "today_medium": [
        r"\bit'?s your birthday\b",
        r"\byour birthday today\b",
    ],
    "today_weak": [
        r"\bbirthday vibes\b",
    ],
    "within_3d_strong": [
        r"\bbirthday (is )?in (2|3|two|three) days\b",
    ],
    "within_3d_medium": [
        r"\bbirthday coming up\b",
    ],
    "within_14d_strong": [
        r"\bbirthday next week\b",
    ],
    "within_14d_medium": [
        r"\bbirthday soon\b",
    ],
}

DATE_EXPLICIT_PATTERNS = [
    r"\bbirthday\s*[:\-]\s*(\d{4}-\d{1,2}-\d{1,2})\b",
    r"\bbirthday\s*[:\-]\s*(\d{1,2}[\/\-]\d{1,2})\b",
]
