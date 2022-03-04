import unittest
import swirler

"""TESTING CASES

Cumulative
Associative
Distributive
Identity
"""


"""DO THIS
1. Create two folders, one for macros, another for packages
2. Create 10 macros/packages in their respective folders
3. Do 3 test cases, only macros, only packages, and with both"""


class EvalTest(unittest.TestCase):
    def setUp(self) -> None:

        self.cache_path = "tests/cache"
        self.env_path = "tests/test_env"

    def test_init(self):
        self.env = swirler.get_env_data(self.cache_path, self.env_path)
        print(swirler.swirl("math.bmi(50, 1.7)", self.env))


if __name__ == "__main__":
    unittest.main()
