import unittest

from app import app


class FlaskApplicationTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home_route_returns_expected_response(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_data(as_text=True),
            "Hello, Jenkins Multi-Stage Pipeline!",
        )


if __name__ == "__main__":
    unittest.main()
