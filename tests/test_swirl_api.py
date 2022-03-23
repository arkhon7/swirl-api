import unittest
from evaluator import evaluate


class MacroTest(unittest.TestCase):
    """To ensure that macros are working"""

    def setUp(self) -> None:
        self.cache_path = "tests/cache"

    def test_cuboid(self):
        self.assertEqual(
            evaluate("VolumeOfCuboid(5, 5)", self.cache_path),
            evaluate("VolumeOfCuboid(5, 5)", self.cache_path),
        )

    def test_coc(self):
        self.assertEqual(
            evaluate("CircumferenceOfCircle(5)", self.cache_path),
            evaluate("CircumferenceOfCircle(5)", self.cache_path),
        )

    def test_aoc(self):
        self.assertEqual(
            evaluate("AreaofCircle(5)", self.cache_path),
            evaluate("AreaofCircle(5)", self.cache_path),
        )

    def test_sine(self):
        self.assertEqual(
            evaluate("Sine(5)", self.cache_path),
            evaluate("Sine(5)", self.cache_path),
        )

    def test_cosine(self):
        self.assertEqual(
            evaluate("Cosine(5)", self.cache_path),
            evaluate("Cosine(5)", self.cache_path),
        )

    def test_tangent(self):
        self.assertEqual(
            evaluate("Tangent(5)", self.cache_path),
            evaluate("Tangent(5)", self.cache_path),
        )


class PackageTest(unittest.TestCase):
    """To ensure that packages are working"""

    def setUp(self) -> None:
        self.cache_path = "tests/cache"

    def test_marky_package(self):
        self.assertEqual(
            evaluate("mk.grav_pot_esc_spd(mass=20, radius=5) + mk.force(40, 45)", self.cache_path),
            evaluate("mk.grav_pot_esc_spd(mass=20, radius=5) + mk.force(40, 45)", self.cache_path),
        )

        self.assertEqual(
            evaluate("mk.best_girl", self.cache_path),
            evaluate("mk.best_girl", self.cache_path),
        )

        self.assertEqual(
            evaluate("mk.gravity", self.cache_path),
            evaluate("mk.gravity", self.cache_path),
        )

    def test_science(self):
        self.assertEqual(
            evaluate("science.force(5,5)", self.cache_path),
            evaluate("science.force(5,5)", self.cache_path),
        )


class RandomTest(unittest.TestCase):
    """To ensure that certain inputs are working"""

    def setUp(self) -> None:
        self.cache_path = "tests/cache"

    def test_evaluate(self):
        print(evaluate("best_girl", self.cache_path))


if __name__ == "__main__":
    unittest.main()
