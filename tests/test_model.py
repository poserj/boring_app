import unittest

from helpers import get_similar


class TestSimilarity(unittest.TestCase):
    def test_equal(self):
        a = [1, "test", 23, 0.9]
        b = [1, "test", 23, 0.9]
        self.assertEqual(get_similar([a, b, b]), {'matcher': 1.0,  'activity': b})

    def test_not_equal(self):
        a = [7, "relax", '23', 0]
        b = [1, "test", 23, 0.9]
        self.assertEqual(get_similar([a, b, b]), {'matcher': 0.0,  'activity': b})

    def test_partial_equal(self):
        a = [7, "relax", 23, 0]
        b = [7, "test", 23, 0.9]
        self.assertEqual(get_similar([a, b, b]), {'matcher': 0.5,  'activity': b})


if __name__ == '__main__':
    unittest.main()
