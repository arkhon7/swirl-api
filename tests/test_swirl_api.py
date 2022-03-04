import unittest
import swirler

"""TESTING CASES

single macros
with other macros

single packages
with other packages

with packages and macros
"""


"""DO THIS
1. Create two folders, one for macros, another for packages
2. Create 10 macros/packages in their respective folders
3. Do 3 test cases, only macros, only packages, and with both"""

cache_path = "tests/cache"
env_path = "tests/test_env"
env = swirler.get_env_data(cache_path, env_path)


class MacroTest(unittest.TestCase):
    def setUp(self) -> None:
        self.env = env

    def test_cuboid(self):
        self.assertEqual(
            swirler.swirl("VolumeOfCuboid(5, 5)", self.env),
            swirler.swirl("VolumeOfCuboid(5, 5)", self.env),
        )

    def test_coc(self):
        self.assertEqual(
            swirler.swirl("CircumferenceOfCircle(5)", self.env),
            swirler.swirl("CircumferenceOfCircle(5)", self.env),
        )

    def test_aoc(self):
        self.assertEqual(
            swirler.swirl("AreaofCircle(5)", self.env),
            swirler.swirl("AreaofCircle(5)", self.env),
        )

    def test_sine(self):
        self.assertEqual(
            swirler.swirl("Sine(5)", self.env),
            swirler.swirl("Sine(5)", self.env),
        )

    def test_cosine(self):
        self.assertEqual(
            swirler.swirl("Cosine(5)", self.env),
            swirler.swirl("Cosine(5)", self.env),
        )

    def test_tangent(self):
        self.assertEqual(
            swirler.swirl("Tangent(5)", self.env),
            swirler.swirl("Tangent(5)", self.env),
        )


class PackageTest(unittest.TestCase):
    def setUp(self) -> None:
        self.env = env

    def test_marky_package(self):
        self.assertEqual(
            swirler.swirl(
                "mk.grav_pot_esc_spd(mass=20, radius=5) + mk.force(40, 45)", self.env
            ),
            swirler.swirl(
                "mk.grav_pot_esc_spd(mass=20, radius=5) + mk.force(40, 45)", self.env
            ),
        )

        self.assertEqual(
            swirler.swirl("mk.best_girl()", self.env),
            swirler.swirl("mk.best_girl()", self.env),
        )


class RandomTest(unittest.TestCase):
    def setUp(self) -> None:
        self.env = env

    def test_swirl(self):
        print(swirler.swirl("science.force(5, 5)", self.env))


if __name__ == "__main__":
    unittest.main()
