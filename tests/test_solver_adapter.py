import unittest

from app.solver.adapter import solve_next_guess
from app.solver.models import GuessInput
from app.solver.validation import ValidationError


class SolverAdapterTests(unittest.TestCase):
    def test_opening_guess_uses_precomputed_legacy_ranking(self) -> None:
        result = solve_next_guess([])

        self.assertEqual(result.best_guess, "reist")
        self.assertEqual(result.strategy, "precomputed-opening")
        self.assertEqual(len(result.top_guesses), 10)

    def test_solver_returns_single_remaining_candidate_when_solved(self) -> None:
        result = solve_next_guess([GuessInput(word="cigar", feedback="22222")])

        self.assertEqual(result.best_guess, "cigar")
        self.assertEqual(result.remaining_candidate_count, 1)
        self.assertEqual(result.remaining_candidates, ("cigar",))

    def test_solver_does_not_treat_guess_only_words_as_valid_answers(self) -> None:
        with self.assertRaisesRegex(ValidationError, "no valid candidate answers"):
            solve_next_guess([GuessInput(word="adieu", feedback="22222")])

    def test_solver_rejects_impossible_guess_history(self) -> None:
        with self.assertRaisesRegex(ValidationError, "no valid candidate answers"):
            solve_next_guess(
                [
                    GuessInput(word="cigar", feedback="22222"),
                    GuessInput(word="rebut", feedback="22222"),
                ]
            )


if __name__ == "__main__":
    unittest.main()
