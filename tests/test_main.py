from unittest import TestCase
from main import sample


class MainTest(TestCase):
    def test_main(self) -> None:
        pass

    def test_sample(self) -> None:
        result = sample()

        self.assertEqual(result, "hoge")
