from __future__ import annotations

from collections import Counter
from typing import Iterable, Sequence

from .models import GuessInput
from .resources import load_answer_words


def wordle_feedback(guess: str, answer: str) -> str:
    """Return a Wordle-style 0/1/2 feedback string."""

    result = ["0"] * 5
    remaining = Counter()

    for index, (guess_letter, answer_letter) in enumerate(zip(guess, answer)):
        if guess_letter == answer_letter:
            result[index] = "2"
        else:
            remaining[answer_letter] += 1

    for index, guess_letter in enumerate(guess):
        if result[index] != "0":
            continue
        if remaining[guess_letter] > 0:
            result[index] = "1"
            remaining[guess_letter] -= 1

    return "".join(result)


def candidate_matches(guess: GuessInput, candidate: str) -> bool:
    return wordle_feedback(guess.word, candidate) == guess.feedback


def filter_candidates(
    guesses: Sequence[GuessInput],
    candidates: Iterable[str] | None = None,
) -> list[str]:
    remaining = list(candidates or load_answer_words())
    for guess in guesses:
        remaining = [candidate for candidate in remaining if candidate_matches(guess, candidate)]
    return remaining


def rank_candidates_by_frequency(candidates: Sequence[str]) -> list[tuple[str, int]]:
    letter_counts: Counter[str] = Counter()
    for candidate in candidates:
        letter_counts.update(candidate)

    ranked: list[tuple[str, int]] = []
    for candidate in candidates:
        score = 0
        seen_letters: set[str] = set()
        for letter in candidate:
            if letter in seen_letters:
                continue
            score += letter_counts[letter]
            seen_letters.add(letter)
        ranked.append((candidate, score))

    return sorted(ranked, key=lambda item: (-item[1], item[0]))
