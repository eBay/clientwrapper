import unittest

from clientwrapper import ClientWrapper


class DummyClientWrapper(ClientWrapper):
    def __init__(self):
        super().__init__()

    def method1(self, str1, int1, bool1):
        return [str1, int1, bool1]

    def method2(self, list1, tuple1, dict1):
        return [list1, tuple1, dict1]

    def method3(self, str1, int1, bool1, list1, tuple1, dict1, **kwargs):
        return [str1, int1, bool1, list1, tuple1, dict1, kwargs]


class WrapperTestCase(unittest.TestCase):
    def test_method1(self):
        dummy = DummyClientWrapper()
        args = "method1 str1 str int1 1 bool1 True".split()
        actualstr, actualint, actualbool = dummy.run(args)
        self.assertEqual(actualstr, "str")
        self.assertEqual(actualint, 1)
        self.assertEqual(actualbool, True)

    def test_method2(self):
        dummy = DummyClientWrapper()
        args = "method2 list1 [1,2,3] tuple1 (1,2,3) dict1 {'a':1,'b':2,'c':3}".split()
        actual_list, actual_tuple, actual_dict = dummy.run(args)
        self.assertEqual(actual_list, [1, 2, 3])
        self.assertEqual(actual_tuple, (1, 2, 3))
        self.assertEqual(actual_dict, {'a': 1, 'b': 2, 'c': 3})

    def test_method3(self):
        dummy = DummyClientWrapper()
        args = "method3 str1 str int1 1 bool1 True list1 [1,2,3] tuple1 (1,2,3) dict1 {'a':1,'b':2,'c':3}  str2 str int2 1 bool2 True list2 [1,2,3] tuple2 (1,2,3) dict2 {'a':1,'b':2,'c':3}".split()
        actualstr, actualint, actualbool, actual_list, actual_tuple, actual_dict, kwargs = dummy.run(args)
        self.assertEqual(actualstr, "str")
        self.assertEqual(actualint, 1)
        self.assertEqual(actualbool, True)
        self.assertEqual(actual_list, [1, 2, 3])
        self.assertEqual(actual_tuple, (1, 2, 3))
        self.assertEqual(actual_dict, {'a': 1, 'b': 2, 'c': 3})
        self.assertEqual(kwargs, {'str2': 'str', 'int2': 1, 'bool2': True, 'list2': [1, 2, 3], 'tuple2': (1, 2, 3),
                                  'dict2': {'a': 1, 'b': 2, 'c': 3}})

    def test_method4(self):
        dummy = DummyClientWrapper()
        args = "method3 str1 '' int1 0 bool1 False list1 [] tuple1 () dict1 None str2 '' int2 None bool2 False list2 [] tuple2 () dict2 {0:'zero'}".split()
        str1, int1, bool1, list1, tuple1, dict1, kwargs = dummy.run(args)
        self.assertEqual(str1, '')
        self.assertEqual(int1, 0)
        self.assertEqual(bool1, False)
        self.assertEqual(list1, [])
        self.assertEqual(tuple1, ())
        self.assertEqual(dict1, None)
        self.assertEqual(kwargs,
                         {'str2': '', 'int2': None, 'bool2': False, 'list2': [], 'tuple2': (), 'dict2': {0: 'zero'}})
