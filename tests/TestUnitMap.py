import unittest

from ariadne import Map as M

class TestMap(unittest.TestCase):

    # one level

    def testSetOneLevelAttrAccessAttr(self):
        m = M()
        m.a = 'value'
        self.assertEqual(m.a, 'value')

    def testSetOneLevelKeyAccessKey(self):
        m = M()
        m['a'] = 'value'
        self.assertEqual(m['a'], 'value')

    def testSetOneLevelAttrAccessKey(self):
        m = M()
        m.a = 'value'
        self.assertEqual(m['a'], 'value')

    def testSetOneLevelKeyAccessAttr(self):
        m = M()
        m['a'] = 'value'
        self.assertEqual(m.a, 'value')

    # multiple levels

    def testSetMultipleLevelAttrAccessAttr(self):
        m = M()
        m.a.b = 'value'
        self.assertEqual(m.a.b, 'value')

    def testSetMultipleLevelKeyAccessKey(self):
        m = M()
        m['a.b'] = 'value'
        self.assertEqual(m['a.b'], 'value')

    def testSetMultipleLevelAttrAccessKey(self):
        m = M()
        m.a.b = 'value'
        self.assertEqual(m['a.b'], 'value')

    def testSetMultipleLevelKeyAccessAttr(self):
        m = M()
        m['a.b'] = 'value'
        self.assertEqual(m.a.b, 'value')

if __name__ == '__main__':
    unittest.main()