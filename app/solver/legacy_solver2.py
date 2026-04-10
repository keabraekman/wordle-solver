from __future__ import annotations

from statistics import mean, median
from typing import Sequence

from .legacy_solver1 import wordle_feedback
from .resources import load_first_word_rankings


def precomputed_opening_rankings(limit: int = 10) -> list[dict[str, float | str]]:
    rankings = load_first_word_rankings("median")
    ordered = sorted(rankings.items(), key=lambda item: (item[1], item[0]))
    return [
        {"word": word, "median_remaining": float(score)}
        for word, score in ordered[:limit]
    ]


def rank_candidates_by_expected_remaining(
    candidates: Sequence[str],
    guess_pool: Sequence[str] | None = None,
) -> list[dict[str, float | str]]:
    guesses = list(guess_pool or candidates)
    ranked: list[dict[str, float | str]] = []

    for guess in guesses:
        pattern_counts: dict[str, int] = {}
        patterns_for_answers: list[str] = []

        for answer in candidates:
            pattern = wordle_feedback(guess, answer)
            patterns_for_answers.append(pattern)
            pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1

        remaining_sizes = [pattern_counts[pattern] for pattern in patterns_for_answers]
        ranked.append(
            {
                "word": guess,
                "median_remaining": float(median(remaining_sizes)),
                "mean_remaining": float(mean(remaining_sizes)),
            }
        )

    return sorted(
        ranked,
        key=lambda item: (
            float(item["median_remaining"]),
            float(item["mean_remaining"]),
            str(item["word"]),
        ),
    )
