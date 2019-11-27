import unittest

from ariadne import Map as M

class TestMap(unittest.TestCase):

    def test_set_value_one_level(self):
        m = M()
        m.a = 10
        self.assertEqual(m.a, 10)
        self.assertEqual(m['a'], 10)

if __name__ == '__main__':
    unittest.main()