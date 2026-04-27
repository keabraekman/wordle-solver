from __future__ import annotations

import re
from typing import Any

from .models import GuessInput
from .resources import load_valid_guess_set


WORD_PATTERN = re.compile(r"^[a-zA-Z]{5}$")
FEEDBACK_PATTERN = re.compile(r"^[012]{5}$")


class ValidationError(ValueError):
    pass


def validate_payload(payload: Any) -> list[GuessInput]:
    if not isinstance(payload, dict):
        raise ValidationError("Request body must be a JSON object.")

    raw_guesses = payload.get("guesses", [])
    if raw_guesses is None:
        raw_guesses = []
    if not isinstance(raw_guesses, list):
        raise ValidationError("'guesses' must be a list.")

    allowed_guesses = load_valid_guess_set()
    guesses: list[GuessInput] = []

    for index, raw_guess in enumerate(raw_guesses):
        if not isinstance(raw_guess, dict):
            raise ValidationError(f"Guess {index + 1} must be an object.")

        word = str(raw_guess.get("word", "")).strip().lower()
        feedback = str(raw_guess.get("feedback", "")).strip()

        if not word and not feedback:
            continue
        if not word or not feedback:
            raise ValidationError(
                f"Guess {index + 1} must include both a 5-letter word and feedback."
            )
        if not WORD_PATTERN.match(word):
            raise ValidationError(f"Guess {index + 1} must be exactly 5 letters.")
        if word not in allowed_guesses:
            raise ValidationError(f"Guess {index + 1} is not in the allowed guess list.")
        if not FEEDBACK_PATTERN.match(feedback):
            raise ValidationError(
                f"Guess {index + 1} feedback must be exactly 5 characters of 0, 1, or 2."
            )

        guesses.append(GuessInput(word=word, feedback=feedback))

    return guesses
