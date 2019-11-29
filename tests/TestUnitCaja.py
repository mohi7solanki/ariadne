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


class UnitTestCajaListSource(unittest.TestCase):

    def testUnitTestCajaListSourceSimple(self):
        m = Caja([0,1,2])

        self.assertEqual(m[0], 0)
        self.assertEqual(m['0'], 0)

    def testUnitTestCajaListSourceNested(self):
        m = Caja([[1,2],[3,4],[5],[]])

        self.assertEqual(m['1.0'], 3)
        self.assertEqual(m[0][0], 1)
        self.assertEqual(m['2/0'], 5)

    def testUnitTestCajaListSourceNestedWithDict(self):
        m = Caja([[1,2],[3,4],[5],[{'a':[6,7]}]])

        self.assertEqual(m['1.0'], 3)
        self.assertEqual(m[0][0], 1)
        self.assertEqual(m['3/0.a.1'], 7)

    def testUnitTestCajaListIterate(self):
        m = Caja([1,2,3,4,5])

        i = 1
        for v in m:
            self.assertEqual(v, i)
            i += 1


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

    def testUnitTestCajaDictSourceListOneLevel(self):

        m = Caja({
            'a': 'value_a',
            'b': 'value_b',
            'c':{
                'd':{
                    'e': 'value_e',
                    'f': {'g': [1,2,{'n':3}] }
                    }
                }})

        self.assertEqual(m['a'], 'value_a')
        self.assertEqual(m['b'], 'value_b')
        self.assertEqual(m['c.d.e'], 'value_e')
        self.assertEqual(m['c/d.e'], 'value_e')
        self.assertEqual(m['c.d/f.g.0'], 1)
        self.assertEqual(m['c.d/f.g.2.n'], 3)
        self.assertEqual(m.a, 'value_a')
        self.assertEqual(m.b, 'value_b')
        self.assertEqual(m.c.d.e, 'value_e')
        self.assertEqual(m['c'].d.f['g']['1'], 2)

    def testUnitTestCajaDictSourceIterateKeysOneLevel(self):

        d = {'a':1,'b':2,'c':3}
        m = Caja(d)

        for k in m:
            self.assertEqual(d[k], m[k])

        for (k,v) in m.items():
            self.assertEqual(d[k], v)

class UnitTestCajaEqualityOperators(unittest.TestCase):

    def testUnitTestCajaEqualityOperatorsSourceList(self):
        l = [1,2,3]
        m = Caja(l)
        n = Caja(l)
        
        self.assertEqual(m, l)
        self.assertEqual(m, [1,2,3])
        self.assertEqual(m, n)

        self.assertNotEqual(m, [1,2])
        self.assertNotEqual(m, Caja([1,2]))


if __name__ == '__main__':
    unittest.main()