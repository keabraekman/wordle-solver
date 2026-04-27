from __future__ import annotations

from functools import lru_cache
from importlib import resources
import pickle
from typing import Iterable


DATA_PACKAGE = "app.solver.data"


def _resource(name: str):
    return resources.files(DATA_PACKAGE).joinpath(name)


def _normalize_words(raw_words: Iterable[object]) -> tuple[str, ...]:
    words: list[str] = []
    seen: set[str] = set()

    for raw_word in raw_words:
        word = str(raw_word).strip().lower()
        if not word or word in seen:
            continue
        seen.add(word)
        words.append(word)

    return tuple(words)


def _load_word_file(name: str) -> tuple[str, ...]:
    return _normalize_words(_resource(name).read_text(encoding="utf-8").splitlines())


@lru_cache(maxsize=1)
def load_answers() -> tuple[str, ...]:
    return _load_word_file("answers.txt")


@lru_cache(maxsize=1)
def load_allowed_guesses() -> tuple[str, ...]:
    return _load_word_file("allowed_guesses.txt")


@lru_cache(maxsize=1)
def load_valid_guesses() -> tuple[str, ...]:
    return _normalize_words((*load_answers(), *load_allowed_guesses()))


def load_answer_words() -> tuple[str, ...]:
    return load_answers()


def load_guess_words() -> tuple[str, ...]:
    return load_valid_guesses()


@lru_cache(maxsize=1)
def load_answer_word_set() -> frozenset[str]:
    return frozenset(load_answers())


@lru_cache(maxsize=1)
def load_valid_guess_set() -> frozenset[str]:
    return frozenset(load_valid_guesses())


def load_guess_word_set() -> frozenset[str]:
    return load_valid_guess_set()


@lru_cache(maxsize=2)
def load_first_word_rankings(metric: str = "median") -> dict[str, float]:
    filename = {
        "median": "first_word_dict_test.pkl",
        "mean": "first_word_dict.pkl",
    }.get(metric)
    if filename is None:
        raise ValueError(f"Unsupported ranking metric: {metric}")
    raw = pickle.loads(_resource(filename).read_bytes())
    return {str(word): float(score) for word, score in raw.items()}
