from __future__ import annotations

from http import HTTPStatus
from typing import Any

from app.solver import ValidationError, solve_next_guess, validate_payload


def solve_payload(payload: Any) -> dict[str, object]:
    guesses = validate_payload(payload)
    return solve_next_guess(guesses).to_dict()


def error_response(
    message: str,
    status_code: int = HTTPStatus.BAD_REQUEST,
) -> tuple[int, dict[str, object]]:
    return int(status_code), {"error": message}


def handle_payload(payload: Any) -> tuple[int, dict[str, object]]:
    try:
        return int(HTTPStatus.OK), solve_payload(payload)
    except ValidationError as exc:
        return error_response(str(exc), HTTPStatus.BAD_REQUEST)
