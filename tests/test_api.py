import unittest
from http import HTTPStatus

from app.api.local_api import handle_solve_request


class LocalApiTests(unittest.TestCase):
    def test_local_api_returns_opening_guess(self) -> None:
        status_code, body = handle_solve_request({"guesses": []})

        self.assertEqual(status_code, HTTPStatus.OK)
        self.assertEqual(body["best_guess"], "reist")
        self.assertEqual(len(body["top_guesses"]), 10)

    def test_local_api_returns_validation_error(self) -> None:
        status_code, body = handle_solve_request(
            {"guesses": [{"word": "bad", "feedback": "01020"}]}
        )

        self.assertEqual(status_code, HTTPStatus.BAD_REQUEST)
        self.assertIn("5 letters", body["error"])


if __name__ == "__main__":
    unittest.main()
