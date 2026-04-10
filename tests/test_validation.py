import unittest

from app.solver.validation import ValidationError, validate_payload


class ValidationTests(unittest.TestCase):
    def test_validate_payload_accepts_empty_guess_list(self) -> None:
        self.assertEqual(validate_payload({"guesses": []}), [])

    def test_validate_payload_rejects_bad_feedback_length(self) -> None:
        with self.assertRaisesRegex(ValidationError, "feedback"):
            validate_payload({"guesses": [{"word": "raise", "feedback": "012"}]})

    def test_validate_payload_rejects_unknown_word(self) -> None:
        with self.assertRaisesRegex(ValidationError, "allowed guess list"):
            validate_payload({"guesses": [{"word": "zzzzz", "feedback": "00000"}]})


if __name__ == "__main__":
    unittest.main()
