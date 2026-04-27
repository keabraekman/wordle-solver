from __future__ import annotations

from typing import Sequence

from .legacy_solver1 import filter_candidates, rank_candidates_by_frequency
from .legacy_solver2 import (
    precomputed_opening_rankings,
    rank_candidates_by_expected_remaining,
)
from .models import GuessInput, RankedGuess, SolveResult
from .resources import load_answer_words, load_valid_guesses
from .validation import ValidationError


ADVANCED_RANKING_THRESHOLD = 250
REMAINING_CANDIDATE_PREVIEW_LIMIT = 50


def solve_next_guess(guesses: Sequence[GuessInput]) -> SolveResult:
    if not guesses:
        opening_rankings = precomputed_opening_rankings(limit=10)
        top_guesses = tuple(
            RankedGuess(
                word=str(item["word"]),
                score=float(item["median_remaining"]),
            )
            for item in opening_rankings
        )
        return SolveResult(
            best_guess=top_guesses[0].word,
            top_guesses=top_guesses,
            remaining_candidate_count=len(load_answer_words()),
            remaining_candidates=None,
            strategy="precomputed-opening",
            ranking_label="median remaining candidates",
        )

    candidates = filter_candidates(guesses)
    if not candidates:
        raise ValidationError(
            "That guess history leaves no valid candidate answers. Check the words and feedback."
        )

    remaining_candidates = (
        tuple(candidates)
        if len(candidates) <= REMAINING_CANDIDATE_PREVIEW_LIMIT
        else None
    )

    if len(candidates) == 1:
        only_word = candidates[0]
        return SolveResult(
            best_guess=only_word,
            top_guesses=(RankedGuess(word=only_word, score=1.0),),
            remaining_candidate_count=1,
            remaining_candidates=(only_word,),
            strategy="resolved-candidate",
            ranking_label="resolved candidate",
        )

    if len(candidates) <= ADVANCED_RANKING_THRESHOLD:
        ranked = rank_candidates_by_expected_remaining(
            candidates,
            guess_pool=load_valid_guesses(),
        )[:10]
        top_guesses = tuple(
            RankedGuess(
                word=str(item["word"]),
                score=float(item["median_remaining"]),
                tie_breaker=float(item["mean_remaining"]),
            )
            for item in ranked
        )
        return SolveResult(
            best_guess=top_guesses[0].word,
            top_guesses=top_guesses,
            remaining_candidate_count=len(candidates),
            remaining_candidates=remaining_candidates,
            strategy="expected-remaining",
            ranking_label="median remaining candidates",
        )

    ranked = rank_candidates_by_frequency(
        candidates,
        guess_pool=load_valid_guesses(),
    )[:10]
    top_guesses = tuple(RankedGuess(word=word, score=score) for word, score in ranked)
    return SolveResult(
        best_guess=top_guesses[0].word,
        top_guesses=top_guesses,
        remaining_candidate_count=len(candidates),
        remaining_candidates=remaining_candidates,
        strategy="frequency-heuristic",
        ranking_label="letter frequency score",
    )
