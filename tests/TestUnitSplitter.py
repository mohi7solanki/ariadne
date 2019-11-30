import unittest
import re

from ariadne import RegexSplitter
from ariadne import StringSplitter

class UnitTestSplitterFeatures(unittest.TestCase):
    
    def setUp(self):
        self.splitter = StringSplitter()

    def test_splitter_features_is_callable(self):
        string = 'a.b'
        self.assertTrue(callable(self.splitter))
        self.assertEqual(self.splitter(string), self.splitter.split(string))

class UnitTestDefaultRegexSplitter(unittest.TestCase):
    
    def setUp(self):
        self.splitter = RegexSplitter()

    def test_default_regex_splitter_with_one_dot_delimiter_simple_chars_only_once(self):
        string = 'a.b'
        self.assertEqual(self.splitter.range(string), (1, 2))
        self.assertEqual(self.splitter.split(string), ('a', 'b'))

    def test_default_regex_splitter_with_multiple_dots_delimiter_simple_chars_only_once(self):
        string = 'a.b.c.d'
        self.assertEqual(self.splitter.range(string), (1, 2))
        self.assertEqual(self.splitter.split(string), ('a', 'b.c.d'))

    def test_default_regex_splitter_with_no_delimiter_only_once(self):
        string = 'abcd'
        self.assertIsNone(self.splitter.range(string))
        self.assertEqual(self.splitter.split(string), (string, None))

    def test_default_regex_splitter_with_multiple_type_delimiters_simple_chars_only_once(self):
        string = 'a/b.c/d'
        self.assertEqual(self.splitter.range(string), (1, 2))
        self.assertEqual(self.splitter.split(string), ('a', 'b.c/d'))

    def test_default_regex_splitter_with_multiple_type_delimiters_to_exhaustion(self):
        string = 'root.attribute/spec'

        range1 = self.splitter.range(string)
        split1 = self.splitter.split(string)
        
        self.assertEqual(range1, (4,5))
        self.assertEqual(split1, ('root', 'attribute/spec'))

        range2 = self.splitter.range(split1[1])
        split2 = self.splitter.split(split1[1])

        self.assertEqual(range2, (9,10))
        self.assertEqual(split2, ('attribute', 'spec'))

        range3 = self.splitter.range(split2[1])
        split3 = self.splitter.split(split2[1])

        self.assertIsNone(range3)
        self.assertEqual(split3, ('spec', None))
    
    def test_default_regex_splitter_with_multiple_dots_delimiter_no_string_in_the_middle(self):
        string = 'root..attribute'

        range1 = self.splitter.range(string)
        split1 = self.splitter.split(string)

        self.assertEqual(range1, (4, 5))
        self.assertEqual(split1, ('root', '.attribute'))

        self.assertEqual(self.splitter.range(split1[1]), (0, 1))
        self.assertEqual(self.splitter.split(split1[1]), ('', 'attribute'))

class UnitTestMulticharRegexSplitter(unittest.TestCase):
    
    def setUp(self):
        pattern = re.compile(r'\.*delimiter\.*')
        self.splitter = RegexSplitter(pattern)

    def test_multichar_regex_splitter_single_split_no_dots(self):
        string = 'beforedelimiterafter'
        self.assertEqual(self.splitter.range(string), (6, 15))
        self.assertEqual(self.splitter.split(string), ('before', 'after'))
    
    def test_multichar_regex_splitter_single_split_with_dots_on_one_side(self):
        string = 'beforedelimiter......after'
        self.assertEqual(self.splitter.range(string), (6, 21))
        self.assertEqual(self.splitter.split(string), ('before', 'after'))

    def test_multichar_regex_splitter_single_split_with_dots_on_both_sides(self):
        string = 'before..delimiter......after'
        self.assertEqual(self.splitter.range(string), (6, 23))
        self.assertEqual(self.splitter.split(string), ('before', 'after'))

    def test_multichar_regex_splitter_with_no_delimiter_only_once(self):
        string = 'abcd'
        self.assertIsNone(self.splitter.range(string))
        self.assertEqual(self.splitter.split(string), (string, None))

class UnitTestDefaultStringSplitter(unittest.TestCase):
    
    def setUp(self):
        self.splitter = StringSplitter()

    def test_default_string_splitter_with_one_dot_delimiter_simple_chars_only_once(self):
        string = 'a.b'
        self.assertEqual(self.splitter.range(string), (1, 2))
        self.assertEqual(self.splitter.split(string), ('a', 'b'))

    def test_default_string_splitter_with_multiple_dots_delimiter_simple_chars_only_once(self):
        string = 'a.b.c.d'
        self.assertEqual(self.splitter.range(string), (1, 2))
        self.assertEqual(self.splitter.split(string), ('a', 'b.c.d'))

    def test_default_string_splitter_with_no_delimiter_only_once(self):
        string = 'abcd'
        self.assertIsNone(self.splitter.range(string))
        self.assertEqual(self.splitter.split(string), (string, None))

    def test_default_string_splitter_with_multiple_type_delimiters_simple_chars_only_once(self):
        string = 'a/b.c/d'
        self.assertEqual(self.splitter.range(string), (3, 4))
        self.assertEqual(self.splitter.split(string), ('a/b', 'c/d'))

    def test_default_string_splitter_with_multiple_type_delimiters_to_exhaustion(self):
        string = 'root.attribute.spec'

        range1 = self.splitter.range(string)
        split1 = self.splitter.split(string)
        
        self.assertEqual(range1, (4,5))
        self.assertEqual(split1, ('root', 'attribute.spec'))

        range2 = self.splitter.range(split1[1])
        split2 = self.splitter.split(split1[1])

        self.assertEqual(range2, (9,10))
        self.assertEqual(split2, ('attribute', 'spec'))

        range3 = self.splitter.range(split2[1])
        split3 = self.splitter.split(split2[1])

        self.assertIsNone(range3)
        self.assertEqual(split3, ('spec', None))

if __name__ == '__main__':
    unittest.main()
