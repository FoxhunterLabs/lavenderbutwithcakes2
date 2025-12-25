from typing import Optional
from config import ENGINE
from inference.bayes import compute_posteriors
from models.people import get_person
from models.candidates import create_candidate


def create_candidate_if_needed(person_key: str) -> Optional[str]:
    person = get_person(person_key)
    if not person:
        return None

    if person.get("privacy_mode") == 1:
        return None
    if person.get("do_not_surprise") == 1:
        return None

    post = compute_posteriors(person_key)

    if post["p_today"] >= ENGINE["threshold_today"]:
        return create_candidate(
            person_key,
            "today",
            post["p_today"],
            1.0,
            post,
            [],
        )

    if post["p_3d"] >= ENGINE["threshold_3d"]:
        return create_candidate(
            person_key,
            "3d",
            post["p_3d"],
            1.0,
            post,
            [],
        )

    if post["p_14d"] >= ENGINE["threshold_14d"]:
        return create_candidate(
            person_key,
            "14d",
            post["p_14d"],
            1.0,
            post,
            [],
        )

    return None
