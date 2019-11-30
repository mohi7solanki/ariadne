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

    def testUnitTestCajaEqualityOperatorsSourceDict(self):
        d = {'k1':'a', 'k2':'b'}
        m = Caja(d)
        n = Caja(d)
        
        self.assertEqual(m, d)
        self.assertEqual(m, {'k1':'a', 'k2':'b'})
        self.assertEqual(m, n)

        self.assertNotEqual(m, {'k1':'a', 'k2':'c'})
        self.assertNotEqual(m, Caja({'k3':'a', 'k2':'b'}))

    def testUnitTestCajaEqualityOperatorsSourceDictNested(self):
        d = {'k1':'a', 'k2':'b', 'nested': {'a':'value_a'}}
        m = Caja(d)
        n = Caja(d)
        
        self.assertEqual(m, d)
        self.assertEqual(m, {'k1':'a', 'k2':'b', 'nested': {'a':'value_a'}})
        self.assertEqual(m, n)

        self.assertNotEqual(m, {'k1':'a', 'k2':'b', 'nested': {}})
        self.assertNotEqual(m, Caja({'k1':'a', 'k2':'b', 'nested': {'a':'value_b'}}))

    def testUnitTestCajaEqualityOperatorsSourceDictMixed(self):
        d = {'k1':'a', 'k2':'b', 'nested': {'a':[1,2,3]}}
        m = Caja(d)
        n = Caja(d)
        
        self.assertEqual(m, d)
        self.assertEqual(m, {'k1':'a', 'k2':'b', 'nested': {'a':[1,2,3]}})
        self.assertEqual(m['nested.a'], [1,2,3])
        self.assertEqual(m.nested.a, [1,2,3])
        self.assertEqual(m, n)

        self.assertNotEqual(m, {'k1':'a', 'k2':'b', 'nested': {}})
        self.assertNotEqual(m, Caja({'k1':'a', 'k2':'b', 'nested': {'a':'value_b'}}))

class UnitTestCajaStringRepresentationOperators(unittest.TestCase):

    def testUnitTestCajaStringRepresentation(self):
        d = {'k1':'a', 'k2':'b', 'nested': {'a':[1,2,3]}}
        m = Caja(d)
        
        self.assertEqual(m.__str__(), d.__str__())
        self.assertEqual(m.__repr__(), d.__repr__())

class UnitTestCajaBoolConversion(unittest.TestCase):

    def testUnitTestCajaBoolConversion(self):
        d = {'k1':'a', 'k2':'b', 'nested': {'a':[1,2,3]}}
        m = Caja(d)
        
        self.assertTrue(m)
        self.assertTrue(m.k1)
        self.assertTrue(m.nested.a)

        self.assertFalse(m.nested.c)
        self.assertFalse(m.notexisting)

class UnitTestCajaRaw(unittest.TestCase):

    def testUnitTestCajaRawSimple(self):
        din = {'k1':'a', 'k2':'b', 'nested': {'a':[1,2,3]}}
        caja = Caja(din)
        dout = caja.raw()

        self.assertIsInstance(dout, type(din))
        self.assertEqual(dout, din)

if __name__ == '__main__':
    unittest.main()