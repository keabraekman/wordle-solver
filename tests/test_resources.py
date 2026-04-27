import unittest

from app.solver.legacy_solver1 import filter_candidates
from app.solver.models import GuessInput
from app.solver.resources import (
    load_allowed_guesses,
    load_answers,
    load_valid_guesses,
)


class ResourceTests(unittest.TestCase):
    def test_answers_are_valid_guesses(self) -> None:
        answers = set(load_answers())
        valid_guesses = set(load_valid_guesses())

        self.assertIn("cigar", answers)
        self.assertIn("cigar", valid_guesses)
        self.assertTrue(answers.issubset(valid_guesses))

    def test_allowed_only_words_are_valid_but_not_answers(self) -> None:
        answers = set(load_answers())
        allowed_guesses = set(load_allowed_guesses())
        valid_guesses = set(load_valid_guesses())

        self.assertIn("adieu", allowed_guesses)
        self.assertIn("adieu", valid_guesses)
        self.assertNotIn("adieu", answers)

    def test_filtering_starts_from_answer_list_only(self) -> None:
        self.assertEqual(filter_candidates([]), list(load_answers()))
        self.assertEqual(
            filter_candidates([GuessInput(word="adieu", feedback="22222")]),
            [],
        )


if __name__ == "__main__":
    unittest.main()
