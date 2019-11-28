import unittest

from ariadne import Caja


class UnitTestCajaNoneSourceSingleLevel(unittest.TestCase):

    def testSetOneLevelAttrAccessAttr(self):
        m = Caja()
        m.a = 'value'
        self.assertEqual(m.a, 'value')

    def testSetOneLevelKeyAccessKey(self):
        m = Caja()
        m['a'] = 'value'
        self.assertEqual(m['a'], 'value')

    def testSetOneLevelAttrAccessKey(self):
        m = Caja()
        m.a = 'value'
        self.assertEqual(m['a'], 'value')

    def testSetOneLevelKeyAccessAttr(self):
        m = Caja()
        m['a'] = 'value'
        self.assertEqual(m.a, 'value')


class UnitTestCajaNoneSourceMultipleLevel(unittest.TestCase):

    def testSetMultipleLevelAttrAccessAttr(self):
        m = Caja()
        m.a.b = 'value'
        self.assertEqual(m.a.b, 'value')

    def testSetMultipleLevelKeyAccessKey(self):
        m = Caja()
        m['a.b'] = 'value'
        self.assertEqual(m['a.b'], 'value')

    def testSetMultipleLevelAttrAccessKey(self):
        m = Caja()
        m.a.b = 'value'
        self.assertEqual(m['a.b'], 'value')

    def testSetMultipleLevelKeyAccessAttr(self):
        m = Caja()
        m['a.b'] = 'value'
        self.assertEqual(m.a.b, 'value')


class UnitTestCajaDictSource(unittest.TestCase):
    
    def testUnitTestCajaDictSourceNoList(self):

        m = Caja({
            'a': 'value_a',
            'b': 'value_b',
            'c':{
                'd':{
                    'e': 'value_e',
                    'f': {'g': 'value_g'}
                    }
                }})

        self.assertEqual(m['a'], 'value_a')
        self.assertEqual(m['b'], 'value_b')
        self.assertEqual(m['c.d.e'], 'value_e')
        self.assertEqual(m['c.d.f.g'], 'value_g')
        self.assertEqual(m['c/d.e'], 'value_e')
        self.assertEqual(m['c.d/f.g'], 'value_g')
        self.assertEqual(m.a, 'value_a')
        self.assertEqual(m.b, 'value_b')
        self.assertEqual(m.c.d.e, 'value_e')
        self.assertEqual(m.c.d.f.g, 'value_g')
        self.assertEqual(m['c'].d.f['g'], 'value_g')


if __name__ == '__main__':
    unittest.main()