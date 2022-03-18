import unittest
from evaluator import swirl


class MacroTest(unittest.TestCase):
    """To ensure that macros are working"""

    def setUp(self) -> None:
        self.cache_path = "tests/cache"

    def test_cuboid(self):
        self.assertEqual(
            swirl("VolumeOfCuboid(5, 5)", self.cache_path),
            swirl("VolumeOfCuboid(5, 5)", self.cache_path),
        )

    def test_coc(self):
        self.assertEqual(
            swirl("CircumferenceOfCircle(5)", self.cache_path),
            swirl("CircumferenceOfCircle(5)", self.cache_path),
        )

    def test_aoc(self):
        self.assertEqual(
            swirl("AreaofCircle(5)", self.cache_path),
            swirl("AreaofCircle(5)", self.cache_path),
        )

    def test_sine(self):
        self.assertEqual(
            swirl("Sine(5)", self.cache_path),
            swirl("Sine(5)", self.cache_path),
        )

    def test_cosine(self):
        self.assertEqual(
            swirl("Cosine(5)", self.cache_path),
            swirl("Cosine(5)", self.cache_path),
        )

    def test_tangent(self):
        self.assertEqual(
            swirl("Tangent(5)", self.cache_path),
            swirl("Tangent(5)", self.cache_path),
        )


class PackageTest(unittest.TestCase):
    """To ensure that packages are working"""

    def setUp(self) -> None:
        self.cache_path = "tests/cache"

    def test_marky_package(self):
        self.assertEqual(
            swirl("mk.grav_pot_esc_spd(mass=20, radius=5) + mk.force(40, 45)", self.cache_path),
            swirl("mk.grav_pot_esc_spd(mass=20, radius=5) + mk.force(40, 45)", self.cache_path),
        )

        self.assertEqual(
            swirl("mk.best_girl", self.cache_path),
            swirl("mk.best_girl", self.cache_path),
        )

    def test_science(self):
        self.assertEqual(
            swirl("science.force(5,5)", self.cache_path),
            swirl("science.force(5,5)", self.cache_path),
        )


class RandomTest(unittest.TestCase):
    """To ensure that certain inputs are working"""

    def setUp(self) -> None:
        self.cache_path = "tests/cache"

    def test_swirl(self):
        print(swirl("mk.best_girl", self.cache_path))


if __name__ == "__main__":
    unittest.main()
