from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GuessInput:
    word: str
    feedback: str

    def to_dict(self) -> dict[str, str]:
        return {"word": self.word, "feedback": self.feedback}


@dataclass(frozen=True)
class RankedGuess:
    word: str
    score: float
    tie_breaker: float | None = None

    def to_dict(self) -> dict[str, float | str | None]:
        payload: dict[str, float | str | None] = {
            "word": self.word,
            "score": round(float(self.score), 3),
        }
        if self.tie_breaker is not None:
            payload["tie_breaker"] = round(float(self.tie_breaker), 3)
        return payload


@dataclass(frozen=True)
class SolveResult:
    best_guess: str
    top_guesses: tuple[RankedGuess, ...]
    remaining_candidate_count: int
    remaining_candidates: tuple[str, ...] | None
    strategy: str
    ranking_label: str

    def to_dict(self) -> dict[str, object]:
        return {
            "best_guess": self.best_guess,
            "top_guesses": [guess.to_dict() for guess in self.top_guesses],
            "remaining_candidate_count": self.remaining_candidate_count,
            "remaining_candidates": list(self.remaining_candidates)
            if self.remaining_candidates is not None
            else None,
            "strategy": self.strategy,
            "ranking_label": self.ranking_label,
        }
