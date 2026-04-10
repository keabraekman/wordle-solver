from __future__ import annotations

from functools import lru_cache
from importlib import resources
import pickle


DATA_PACKAGE = "app.solver.data"


def _resource(name: str):
    return resources.files(DATA_PACKAGE).joinpath(name)


@lru_cache(maxsize=1)
def load_answer_words() -> tuple[str, ...]:
    contents = _resource("wordle-answers-alphabetical.txt").read_text(encoding="utf-8")
    return tuple(word.strip().lower() for word in contents.splitlines() if word.strip())


@lru_cache(maxsize=1)
def load_guess_words() -> tuple[str, ...]:
    return tuple(pickle.loads(_resource("all_guesses.pkl").read_bytes()))


@lru_cache(maxsize=1)
def load_guess_word_set() -> frozenset[str]:
    return frozenset(load_guess_words())


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
