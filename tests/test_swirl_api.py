import sys
import unittest
import swirler

"""TESTING CASES

basic
intensive
"""


"""DO THIS
1. Create two folders, one for macros, another for packages
2. Create 10 macros/packages in their respective folders
3. Do 3 test cases, only macros, only packages, and with both"""


class MacroEvalTestCase(unittest.TestCase):
    def setUp(self) -> None:

        self.cache_path = "tests/cache"
        self.env_path = "tests/test_macros"

    def test_add(self):
        basic1 = swirler.swirl(
            "addOne(5) + minusOne(3)", self.cache_path, self.env_path
        )
        basic2 = swirler.swirl(
            "minusOne(4) + addOne(1)", self.cache_path, self.env_path
        )
        basic3 = swirler.swirl(
            "factorial(5) + multiplyTwo(3)", self.cache_path, self.env_path
        )
        basic4 = swirler.swirl("(square(5) + 4) + 30", self.cache_path, self.env_path)
        self.assertEqual(basic1, "8")
        self.assertEqual(basic2, "5")
        self.assertEqual(basic3, "126")
        self.assertEqual(basic4, "59")

    def test_subtract(self):
        basic1 = swirler.swirl("addOne(5)", self.cache_path, self.env_path)
        basic2 = swirler.swirl(
            "minusOne(4) + addOne(1)", self.cache_path, self.env_path
        )
        basic3 = swirler.swirl(
            "factorial(5) + multiplyTwo(3)", self.cache_path, self.env_path
        )
        basic4 = swirler.swirl("(square(5) + 4) + 30", self.cache_path, self.env_path)

    def test_multiply(self):
        ...

    def test_divide(self):
        ...

    def test_power(self):
        ...

    def test_modulus(self):
        ...

    def test_equals(self):
        ...

    def test_less_than(self):
        ...

    def test_greater_than(self):
        ...

    def test_less_than_or_equal(self):
        ...

    def test_greater_than_or_equal(self):
        ...

    def test_right_shift(self):
        ...

    def test_left_shift(self):
        ...

    def test_in_operator(self):
        ...


if __name__ == "__main__":
    unittest.main()
