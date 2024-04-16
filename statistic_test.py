import unittest
from statistic import Statistic, multipliers


class StatisticTest(unittest.TestCase):

    def test_init(self):
        stat = Statistic()
        self.assertEqual(stat.name, "Mysterious Aura")
        self.assertEqual(stat.multiplier, 1)
        self.assertEqual(stat.duration, 0)

    def test_init_args(self):
        stat = Statistic("Test", 2.0, 5)
        self.assertEqual(stat.name, "Test")
        self.assertEqual(stat.multiplier, 2.0)
        self.assertEqual(stat.duration, 5)

    def test_get_multiplier(self):
        stat = Statistic()
        self.assertEqual(stat.get_multiplier(), 1)

    def test_get_multiplier1(self):
        stat = Statistic()
        stats = {"attack": []}
        stats["attack"].append(Statistic(multiplier=2))
        self.assertEqual(stat.get_multiplier(ext_multipliers=stats, stat_type="attack"), 2)

    def test_get_multiplier2(self):
        stat = Statistic()
        stats = {"attack":[]}
        stats["attack"].append(Statistic(multiplier=2))
        multipliers["attack"].append(Statistic(multiplier=2))
        self.assertEqual(stat.get_multiplier(ext_multipliers=stats, stat_type="attack", is_monster=True), 4)

    def test_get_multiplier_invalid_type(self):
        stat = Statistic()
        self.assertRaises(ValueError, stat.get_multiplier, None, "movement", False, False)


if __name__ == '__main__':
    unittest.main()
