import unittest

from ariadne import Caja


class UnitTestCajaNoneSourceSingleLevel(unittest.TestCase):

    def test_set_one_level_attr_access_attr(self):
        m = Caja()
        m.a = 'value'
        self.assertEqual(m.a, 'value')

    def test_set_one_level_key_access_key(self):
        m = Caja()
        m['a'] = 'value'
        self.assertEqual(m['a'], 'value')

    def test_set_one_level_attr_access_key(self):
        m = Caja()
        m.a = 'value'
        self.assertEqual(m['a'], 'value')

    def test_set_one_level_key_access_attr(self):
        m = Caja()
        m['a'] = 'value'
        self.assertEqual(m.a, 'value')


class UnitTestCajaNoneSourceMultipleLevel(unittest.TestCase):

    def test_set_multiple_level_attr_access_attr(self):
        m = Caja()
        m.a.b = 'value'
        self.assertEqual(m.a.b, 'value')

    def test_set_multiple_level_key_access_key(self):
        m = Caja()
        m['a.b'] = 'value'
        self.assertEqual(m['a.b'], 'value')

    def test_set_multiple_level_attr_access_key(self):
        m = Caja()
        m.a.b = 'value'
        self.assertEqual(m['a.b'], 'value')

    def test_set_multiple_level_key_access_attr(self):
        m = Caja()
        m['a.b'] = 'value'
        self.assertEqual(m.a.b, 'value')


class UnitTestCajaListSource(unittest.TestCase):

    def test_unit_test_caja_list_source_simple(self):
        m = Caja([0,1,2])

        self.assertEqual(m[0], 0)
        self.assertEqual(m['0'], 0)

    def test_unit_test_caja_list_source_nested(self):
        m = Caja([[1,2],[3,4],[5],[]])

        self.assertEqual(m['1.0'], 3)
        self.assertEqual(m[0][0], 1)
        self.assertEqual(m['2/0'], 5)

    def test_unit_test_caja_list_source_nested_with_dict(self):
        m = Caja([[1,2],[3,4],[5],[{'a':[6,7]}]])

        self.assertEqual(m['1.0'], 3)
        self.assertEqual(m[0][0], 1)
        self.assertEqual(m['3/0.a.1'], 7)

    def test_unit_test_caja_list_iterate(self):
        m = Caja([1,2,3,4,5])

        i = 1
        for v in m:
            self.assertEqual(v, i)
            i += 1


class UnitTestCajaDictSource(unittest.TestCase):
    
    def test_unit_test_caja_dict_source_no_list(self):

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

    def test_unit_test_caja_dict_source_list_one_level(self):

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

    def test_unit_test_caja_dict_source_iterate_keys_one_level(self):

        d = {'a':1,'b':2,'c':3}
        m = Caja(d.copy())

        for k in m:
            self.assertEqual(d[k], m[k])

        for (k,v) in m.items():
            self.assertEqual(d[k], v)

class UnitTestCajaEqualityOperators(unittest.TestCase):

    def test_unit_test_caja_equality_operators_source_list(self):
        l = [1,2,3]
        m = Caja(l.copy())
        n = Caja(l.copy())
        
        self.assertEqual(m, l)
        self.assertEqual(m, [1,2,3])
        self.assertEqual(m, n)

        self.assertNotEqual(m, [1,2])
        self.assertNotEqual(m, Caja([1,2]))

    def test_unit_test_caja_equality_operators_source_dict(self):
        d = {'k1':'a', 'k2':'b'}
        m = Caja(d.copy())
        n = Caja(d.copy())
        
        self.assertEqual(m, d)
        self.assertEqual(m, {'k1':'a', 'k2':'b'})
        self.assertEqual(m, n)

        self.assertNotEqual(m, {'k1':'a', 'k2':'c'})
        self.assertNotEqual(m, Caja({'k3':'a', 'k2':'b'}))

    def test_unit_test_caja_equality_operators_source_dict_nested(self):
        d = {'k1':'a', 'k2':'b', 'nested': {'a':'value_a'}}
        m = Caja(d)
        n = Caja(d)
        
        self.assertEqual(m, d)
        self.assertEqual(m, {'k1':'a', 'k2':'b', 'nested': {'a':'value_a'}})
        self.assertEqual(m, n)

        self.assertNotEqual(m, {'k1':'a', 'k2':'b', 'nested': {}})
        self.assertNotEqual(m, Caja({'k1':'a', 'k2':'b', 'nested': {'a':'value_b'}}))

    def test_unit_test_caja_equality_operators_source_dict_mixed(self):
        d = {'k1':'a', 'k2':'b', 'nested': {'a':[1,2,3]}}
        m = Caja(d.copy())
        n = Caja(d.copy())
        
        self.assertEqual(m, d)
        self.assertEqual(m, {'k1':'a', 'k2':'b', 'nested': {'a':[1,2,3]}})
        self.assertEqual(m['nested.a'], [1,2,3])
        self.assertEqual(m.nested.a, [1,2,3])
        self.assertEqual(m, n)

        self.assertNotEqual(m, {'k1':'a', 'k2':'b', 'nested': {}})
        self.assertNotEqual(m, Caja({'k1':'a', 'k2':'b', 'nested': {'a':'value_b'}}))

class UnitTestCajaStringRepresentationOperators(unittest.TestCase):

    def test_unit_test_caja_string_representation(self):
        d = {'k1':'a', 'k2':'b', 'nested': {'a':[1,2,3]}}
        m = Caja(d)
        
        self.assertEqual(m.__str__(), d.__str__())
        self.assertEqual(m.__repr__(), d.__repr__())

class UnitTestCajaBoolConversion(unittest.TestCase):

    def test_unit_test_caja_bool_conversion(self):
        d = {'k1':'a', 'k2':'b', 'nested': {'a':[1,2,3]}}
        m = Caja(d)
        
        self.assertTrue(m)
        self.assertTrue(m.k1)
        self.assertTrue(m.nested.a)

        self.assertFalse(m.nested.c)
        self.assertFalse(m.notexisting)

class UnitTestCajaRaw(unittest.TestCase):

    def test_unit_test_caja_raw_simple(self):
        din = {'k1':'a', 'k2':'b', 'nested': {'a':[1,2,3]}}
        caja = Caja(din.copy())
        dout = caja.raw()

        self.assertIsInstance(dout, type(din))
        self.assertEqual(dout, din)

    def test_unit_test_caja_raw_with_created_on_access(self):
        din = {'k1':'a', 'k2':'b', 'nested': {'a':[1,2,3]}}
        caja = Caja(din.copy())

        self.assertFalse(caja.nonexistantkey.subkey)
        self.assertIsInstance(caja.raw(), type(din))
        self.assertEqual(caja.raw(), din)
        
        caja.nonexistantkey.subkey = 'test'
        self.assertEqual(caja.raw(), {'k1':'a', 'k2':'b', 'nested': {'a':[1,2,3]}, 'nonexistantkey':{'subkey':'test'}})


if __name__ == '__main__':
    unittest.main()