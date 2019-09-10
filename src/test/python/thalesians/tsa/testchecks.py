import unittest

import thalesians.tsa.checks as checks

class TestConditions(unittest.TestCase):
    def test_check(self):
        checks.check(True is True)
        checks.check(False is False)
        checks.check(1 < 3)
        checks.check(3 == 3)
        checks.check(3 > 1)
        with self.assertRaises(AssertionError):
            checks.check(True is False)
        with self.assertRaises(AssertionError):
            checks.check(False is True)
        with self.assertRaises(AssertionError):
            checks.check(1 >= 3)
        with self.assertRaises(AssertionError):
            checks.check(3 != 3)
        with self.assertRaises(AssertionError):
            checks.check(3 <= 1)
            
    def test_check_none(self):
        checks.check_none(None)
        with self.assertRaises(AssertionError):
            checks.check_none(3)
            
    def test_check_not_none(self):
        checks.check_not_none(3)
        with self.assertRaises(AssertionError):
            checks.check_not_none(None)
            
    def test_are_all_not_none(self):
        self.assertTrue(checks.are_all_not_none(1, 2, 3))
        self.assertFalse(checks.are_all_not_none(None, 2, 3))
        self.assertFalse(checks.are_all_not_none(1, None, 3))
        self.assertFalse(checks.are_all_not_none(1, 2, None))
        self.assertFalse(checks.are_all_not_none(1, None, None))
        self.assertFalse(checks.are_all_not_none(None, 2, None))
        self.assertFalse(checks.are_all_not_none(None, None, 3))
        
        self.assertTrue(checks.are_all_not_none(1, 2, 3, 'hi'))
        self.assertFalse(checks.are_all_not_none(None, 2, 3, 'hi'))
        self.assertFalse(checks.are_all_not_none(1, None, 3, 'hi'))
        self.assertFalse(checks.are_all_not_none(1, 2, None, 'hi'))
        self.assertFalse(checks.are_all_not_none(1, None, None, 'hi'))
        self.assertFalse(checks.are_all_not_none(None, 2, None, 'hi'))
        self.assertFalse(checks.are_all_not_none(None, None, 3, 'hi'))
        
        self.assertFalse(checks.are_all_not_none(None, None, None))
        
        self.assertFalse(checks.are_all_not_none(None))
    
    def test_check_all_not_none(self):
        checks.check_all_not_none(1, 2, 3)
        with self.assertRaises(AssertionError):
            checks.check_all_not_none(None, 2, 3)
        with self.assertRaises(AssertionError):
            checks.check_all_not_none(1, None, 3)
        with self.assertRaises(AssertionError):
            checks.check_all_not_none(1, 2, None)
        with self.assertRaises(AssertionError):
            checks.check_all_not_none(1, None, None)
        with self.assertRaises(AssertionError):
            checks.check_all_not_none(None, 2, None)
        with self.assertRaises(AssertionError):
            checks.check_all_not_none(None, None, 3)
        
        checks.check_all_not_none(1, 2, 3, 'hi')
        with self.assertRaises(AssertionError):
            checks.check_all_not_none(None, 2, 3, 'hi')
        with self.assertRaises(AssertionError):
            checks.check_all_not_none(1, None, 3, 'hi')
        with self.assertRaises(AssertionError):
            checks.check_all_not_none(1, 2, None, 'hi')
        with self.assertRaises(AssertionError):
            checks.check_all_not_none(1, None, None, 'hi')
        with self.assertRaises(AssertionError):
            checks.check_all_not_none(None, 2, None, 'hi')
        with self.assertRaises(AssertionError):
            checks.check_all_not_none(None, None, 3, 'hi')
        
        with self.assertRaises(AssertionError):
            checks.check_all_not_none(None, None, None)
        
        with self.assertRaises(AssertionError):
            checks.check_all_not_none(None)
    
    def test_are_all_none(self):
        self.assertFalse(checks.are_all_none(1, 2, 3))
        self.assertFalse(checks.are_all_none(None, 2, 3))
        self.assertFalse(checks.are_all_none(1, None, 3))
        self.assertFalse(checks.are_all_none(1, 2, None))
        self.assertFalse(checks.are_all_none(1, 2, 3))
        self.assertFalse(checks.are_all_none(1, None, None))
        self.assertFalse(checks.are_all_none(None, 2, None))
        self.assertFalse(checks.are_all_none(None, None, 3))
        
        self.assertFalse(checks.are_all_none(1, 2, 3, 'hi'))
        self.assertFalse(checks.are_all_none(None, 2, 3, 'hi'))
        self.assertFalse(checks.are_all_none(1, None, 3, 'hi'))
        self.assertFalse(checks.are_all_none(1, 2, None, 'hi'))
        self.assertFalse(checks.are_all_none(1, None, None, 'hi'))
        self.assertFalse(checks.are_all_none(None, 2, None, 'hi'))
        self.assertFalse(checks.are_all_none(None, None, 3, 'hi'))
        
        self.assertTrue(checks.are_all_none(None, None, None))
        
        self.assertTrue(checks.are_all_none(None))
    
    def test_check_all_none(self):
        with self.assertRaises(AssertionError):
            checks.check_all_none(1, 2, 3)
        with self.assertRaises(AssertionError):
            checks.check_all_none(None, 2, 3)
        with self.assertRaises(AssertionError):
            checks.check_all_none(1, None, 3)
        with self.assertRaises(AssertionError):
            checks.check_all_none(1, 2, None)
        with self.assertRaises(AssertionError):
            checks.check_all_none(1, None, None)
        with self.assertRaises(AssertionError):
            checks.check_all_none(None, 2, None)
        with self.assertRaises(AssertionError):
            checks.check_all_none(None, None, 3)
        
        with self.assertRaises(AssertionError):
            checks.check_all_none(1, 2, 3, 'hi')
        with self.assertRaises(AssertionError):
            checks.check_all_none(None, 2, 3, 'hi')
        with self.assertRaises(AssertionError):
            checks.check_all_none(1, None, 3, 'hi')
        with self.assertRaises(AssertionError):
            checks.check_all_none(1, 2, None, 'hi')
        with self.assertRaises(AssertionError):
            checks.check_all_none(1, None, None, 'hi')
        with self.assertRaises(AssertionError):
            checks.check_all_none(None, 2, None, 'hi')
        with self.assertRaises(AssertionError):
            checks.check_all_none(None, None, 3, 'hi')
        
        checks.check_all_none(None, None, None)
        
        checks.check_all_none(None)

    def test_is_exactly_one_not_none(self):
        self.assertFalse(checks.is_exactly_one_not_none(1, 2, 3))
        self.assertFalse(checks.is_exactly_one_not_none(None, 2, 3))
        self.assertFalse(checks.is_exactly_one_not_none(1, None, 3))
        self.assertFalse(checks.is_exactly_one_not_none(1, 2, None))
        self.assertTrue(checks.is_exactly_one_not_none(1, None, None))
        self.assertTrue(checks.is_exactly_one_not_none(None, 2, None))
        self.assertTrue(checks.is_exactly_one_not_none(None, None, 3))
        
        self.assertFalse(checks.is_exactly_one_not_none(1, 2, 3, 'hi'))
        self.assertFalse(checks.is_exactly_one_not_none(None, 2, 3, 'hi'))
        self.assertFalse(checks.is_exactly_one_not_none(1, None, 3, 'hi'))
        self.assertFalse(checks.is_exactly_one_not_none(1, 2, None, 'hi'))
        self.assertFalse(checks.is_exactly_one_not_none(1, None, None, 'hi'))
        self.assertFalse(checks.is_exactly_one_not_none(None, 2, None, 'hi'))
        self.assertFalse(checks.is_exactly_one_not_none(None, None, 3, 'hi'))
        
        self.assertFalse(checks.is_exactly_one_not_none(None, None, None))
        
        self.assertFalse(checks.is_exactly_one_not_none(None))
    
    def test_check_exactly_one_not_none(self):
        with self.assertRaises(AssertionError):
            checks.check_exactly_one_not_none(1, 2, 3)
        with self.assertRaises(AssertionError):
            checks.check_exactly_one_not_none(None, 2, 3)
        with self.assertRaises(AssertionError):
            checks.check_exactly_one_not_none(1, None, 3)
        with self.assertRaises(AssertionError):
            checks.check_exactly_one_not_none(1, 2, None)
        checks.check_exactly_one_not_none(1, None, None)
        checks.check_exactly_one_not_none(None, 2, None)
        checks.check_exactly_one_not_none(None, None, 3)
        
        with self.assertRaises(AssertionError):
            checks.check_exactly_one_not_none(1, 2, 3, 'hi')
        with self.assertRaises(AssertionError):
            checks.check_exactly_one_not_none(None, 2, 3, 'hi')
        with self.assertRaises(AssertionError):
            checks.check_exactly_one_not_none(1, None, 3, 'hi')
        with self.assertRaises(AssertionError):
            checks.check_exactly_one_not_none(1, 2, None, 'hi')
        with self.assertRaises(AssertionError):
            checks.check_exactly_one_not_none(1, None, None, 'hi')
        with self.assertRaises(AssertionError):
            checks.check_exactly_one_not_none(None, 2, None, 'hi')
        with self.assertRaises(AssertionError):
            checks.check_exactly_one_not_none(None, None, 3, 'hi')
        
        with self.assertRaises(AssertionError):
            checks.check_exactly_one_not_none(None, None, None)
        
        with self.assertRaises(AssertionError):
            checks.check_exactly_one_not_none(None)

    def test_is_at_least_one_not_none(self):
        self.assertTrue(checks.is_at_least_one_not_none(1, 2, 3))
        self.assertTrue(checks.is_at_least_one_not_none(None, 2, 3))
        self.assertTrue(checks.is_at_least_one_not_none(1, None, 3))
        self.assertTrue(checks.is_at_least_one_not_none(1, 2, None))
        self.assertTrue(checks.is_at_least_one_not_none(1, None, None))
        self.assertTrue(checks.is_at_least_one_not_none(None, 2, None))
        self.assertTrue(checks.is_at_least_one_not_none(None, None, 3))
        
        self.assertTrue(checks.is_at_least_one_not_none(1, 2, 3, 'hi'))
        self.assertTrue(checks.is_at_least_one_not_none(None, 2, 3, 'hi'))
        self.assertTrue(checks.is_at_least_one_not_none(1, None, 3, 'hi'))
        self.assertTrue(checks.is_at_least_one_not_none(1, 2, None, 'hi'))
        self.assertTrue(checks.is_at_least_one_not_none(1, None, None, 'hi'))
        self.assertTrue(checks.is_at_least_one_not_none(None, 2, None, 'hi'))
        self.assertTrue(checks.is_at_least_one_not_none(None, None, 3, 'hi'))
        
        self.assertFalse(checks.is_at_least_one_not_none(None, None, None))
        
        self.assertFalse(checks.is_at_least_one_not_none(None))
    
    def test_check_at_least_one_not_none(self):
        checks.check_at_least_one_not_none(1, 2, 3)
        checks.check_at_least_one_not_none(None, 2, 3)
        checks.check_at_least_one_not_none(1, None, 3)
        checks.check_at_least_one_not_none(1, 2, None)
        checks.check_at_least_one_not_none(1, None, None)
        checks.check_at_least_one_not_none(None, 2, None)
        checks.check_at_least_one_not_none(None, None, 3)
        
        checks.check_at_least_one_not_none(1, 2, 3, 'hi')
        checks.check_at_least_one_not_none(None, 2, 3, 'hi')
        checks.check_at_least_one_not_none(1, None, 3, 'hi')
        checks.check_at_least_one_not_none(1, 2, None, 'hi')
        checks.check_at_least_one_not_none(1, None, None, 'hi')
        checks.check_at_least_one_not_none(None, 2, None, 'hi')
        checks.check_at_least_one_not_none(None, None, 3, 'hi')
        
        with self.assertRaises(AssertionError):
            checks.check_at_least_one_not_none(None, None, None)
        
        with self.assertRaises(AssertionError):
            checks.check_at_least_one_not_none(None)    

    def test_is_at_most_one_not_none(self):
        self.assertFalse(checks.is_at_most_one_not_none(1, 2, 3))
        self.assertFalse(checks.is_at_most_one_not_none(None, 2, 3))
        self.assertFalse(checks.is_at_most_one_not_none(1, None, 3))
        self.assertFalse(checks.is_at_most_one_not_none(1, 2, None))
        self.assertTrue(checks.is_at_most_one_not_none(1, None, None))
        self.assertTrue(checks.is_at_most_one_not_none(None, 2, None))
        self.assertTrue(checks.is_at_most_one_not_none(None, None, 3))
        
        self.assertFalse(checks.is_at_most_one_not_none(1, 2, 3, 'hi'))
        self.assertFalse(checks.is_at_most_one_not_none(None, 2, 3, 'hi'))
        self.assertFalse(checks.is_at_most_one_not_none(1, None, 3, 'hi'))
        self.assertFalse(checks.is_at_most_one_not_none(1, 2, None, 'hi'))
        self.assertFalse(checks.is_at_most_one_not_none(1, None, None, 'hi'))
        self.assertFalse(checks.is_at_most_one_not_none(None, 2, None, 'hi'))
        self.assertFalse(checks.is_at_most_one_not_none(None, None, 3, 'hi'))
        
        self.assertTrue(checks.is_at_most_one_not_none(None, None, None))
        
        self.assertTrue(checks.is_at_most_one_not_none(None))
    
    def test_check_at_most_one_not_none(self):
        with self.assertRaises(AssertionError):
            checks.check_at_most_one_not_none(1, 2, 3)
        with self.assertRaises(AssertionError):
            checks.check_at_most_one_not_none(None, 2, 3)
        with self.assertRaises(AssertionError):
            checks.check_at_most_one_not_none(1, None, 3)
        with self.assertRaises(AssertionError):
            checks.check_at_most_one_not_none(1, 2, None)
        checks.check_at_most_one_not_none(1, None, None)
        checks.check_at_most_one_not_none(None, 2, None)
        checks.check_at_most_one_not_none(None, None, 3)
        
        with self.assertRaises(AssertionError):
            checks.check_at_most_one_not_none(1, 2, 3, 'hi')
        with self.assertRaises(AssertionError):
            checks.check_at_most_one_not_none(None, 2, 3, 'hi')
        with self.assertRaises(AssertionError):
            checks.check_at_most_one_not_none(1, None, 3, 'hi')
        with self.assertRaises(AssertionError):
            checks.check_at_most_one_not_none(1, 2, None, 'hi')
        with self.assertRaises(AssertionError):
            checks.check_at_most_one_not_none(1, None, None, 'hi')
        with self.assertRaises(AssertionError):
            checks.check_at_most_one_not_none(None, 2, None, 'hi')
        with self.assertRaises(AssertionError):
            checks.check_at_most_one_not_none(None, None, 3, 'hi')
        
        checks.check_at_most_one_not_none(None, None, None)
        
        checks.check_at_most_one_not_none(None)
    
    def test_is_same_len(self):
        with self.assertRaises(TypeError):
            # TypeError: object of type 'int' has no len()
            checks.is_same_len(1, 'aaa')

        self.assertTrue(checks.is_same_len([1], ['aaa']))
        self.assertTrue(checks.is_same_len([1, 'b'], ['aaa', 222]))
        self.assertTrue(checks.is_same_len([1, 'b', 3], ['aaa', 222, 'ccc']))
    
        self.assertFalse(checks.is_same_len([], ['aaa']))
        self.assertFalse(checks.is_same_len([1], ['aaa', 222]))
        self.assertFalse(checks.is_same_len([1, 'b'], ['aaa']))

        self.assertTrue(checks.is_same_len([1], ['aaa'], [111]))
        self.assertTrue(checks.is_same_len([1, 'b'], ['aaa', 222], [111, 'BBB']))
        self.assertTrue(checks.is_same_len([1, 'b', 3], ['aaa', 222, 'ccc'], [111, 'BBB', 333]))
    
        self.assertFalse(checks.is_same_len([], ['aaa'], [111]))
        self.assertFalse(checks.is_same_len([1], ['aaa', 222], [111, 'BBB']))
        self.assertFalse(checks.is_same_len([1, 'b'], ['aaa'], [111, 'BBB']))

        with self.assertRaises(TypeError):
            # TypeError: object of type 'NoneType' has no len()
            checks.is_same_len([1, 'b'], None)
        with self.assertRaises(TypeError):
            # TypeError: object of type 'NoneType' has no len()
            checks.is_same_len(None, ['aaa'])
        with self.assertRaises(TypeError):
            # TypeError: object of type 'NoneType' has no len()
            checks.is_same_len(None, None)

        with self.assertRaises(TypeError):
            # TypeError: object of type 'NoneType' has no len()
            checks.is_same_len([1, 'b'], None, ['aaa', 222])
        with self.assertRaises(TypeError):
            # TypeError: object of type 'NoneType' has no len()
            checks.is_same_len(None, ['aaa'], [111])
        with self.assertRaises(TypeError):
            # TypeError: object of type 'NoneType' has no len()
            checks.is_same_len(None, None, [111, 'BBB'])
        with self.assertRaises(TypeError):
            # TypeError: object of type 'NoneType' has no len()
            checks.is_same_len(None, None, None)

        with self.assertRaises(TypeError):
            # TypeError: object of type 'NoneType' has no len()
            checks.is_same_len([1], None, ['aaa', 222])
        with self.assertRaises(TypeError):
            # TypeError: object of type 'NoneType' has no len()
            checks.is_same_len(None, ['aaa'], [])
        with self.assertRaises(TypeError):
            # TypeError: object of type 'NoneType' has no len()
            checks.is_same_len(None, ['aaa'], [111, 'BBB'])
    
    def test_is_same_len_or_none(self):
        with self.assertRaises(TypeError):
            # TypeError: object of type 'int' has no len()
            checks.is_same_len_or_none(1, 'aaa')

        self.assertTrue(checks.is_same_len_or_none([1], ['aaa']))
        self.assertTrue(checks.is_same_len_or_none([1, 'b'], ['aaa', 222]))
        self.assertTrue(checks.is_same_len_or_none([1, 'b', 3], ['aaa', 222, 'ccc']))
    
        self.assertFalse(checks.is_same_len_or_none([], ['aaa']))
        self.assertFalse(checks.is_same_len_or_none([1], ['aaa', 222]))
        self.assertFalse(checks.is_same_len_or_none([1, 'b'], ['aaa']))

        self.assertTrue(checks.is_same_len_or_none([1], ['aaa'], [111]))
        self.assertTrue(checks.is_same_len_or_none([1, 'b'], ['aaa', 222], [111, 'BBB']))
        self.assertTrue(checks.is_same_len_or_none([1, 'b', 3], ['aaa', 222, 'ccc'], [111, 'BBB', 333]))
    
        self.assertFalse(checks.is_same_len_or_none([], ['aaa'], [111]))
        self.assertFalse(checks.is_same_len_or_none([1], ['aaa', 222], [111, 'BBB']))
        self.assertFalse(checks.is_same_len_or_none([1, 'b'], ['aaa'], [111, 'BBB']))

        self.assertTrue(checks.is_same_len_or_none([1, 'b'], None))
        self.assertTrue(checks.is_same_len_or_none(None, ['aaa']))
        self.assertTrue(checks.is_same_len_or_none(None, None))

        self.assertTrue(checks.is_same_len_or_none([1, 'b'], None, ['aaa', 222]))
        self.assertTrue(checks.is_same_len_or_none(None, ['aaa'], [111]))
        self.assertTrue(checks.is_same_len_or_none(None, None, [111, 'BBB']))
        self.assertTrue(checks.is_same_len_or_none(None, None, None))

        self.assertFalse(checks.is_same_len_or_none([1], None, ['aaa', 222]))
        self.assertFalse(checks.is_same_len_or_none(None, ['aaa'], []))
        self.assertFalse(checks.is_same_len_or_none(None, ['aaa'], [111, 'BBB']))

    def test_is_same_len_or_all_none(self):
        with self.assertRaises(TypeError):
            # TypeError: object of type 'int' has no len()
            checks.is_same_len_or_all_none(1, 'aaa')

        self.assertTrue(checks.is_same_len_or_all_none([1], ['aaa']))
        self.assertTrue(checks.is_same_len_or_all_none([1, 'b'], ['aaa', 222]))
        self.assertTrue(checks.is_same_len_or_all_none([1, 'b', 3], ['aaa', 222, 'ccc']))
    
        self.assertFalse(checks.is_same_len_or_all_none([], ['aaa']))
        self.assertFalse(checks.is_same_len_or_all_none([1], ['aaa', 222]))
        self.assertFalse(checks.is_same_len_or_all_none([1, 'b'], ['aaa']))

        self.assertTrue(checks.is_same_len_or_all_none([1], ['aaa'], [111]))
        self.assertTrue(checks.is_same_len_or_all_none([1, 'b'], ['aaa', 222], [111, 'BBB']))
        self.assertTrue(checks.is_same_len_or_all_none([1, 'b', 3], ['aaa', 222, 'ccc'], [111, 'BBB', 333]))
    
        self.assertFalse(checks.is_same_len_or_all_none([], ['aaa'], [111]))
        self.assertFalse(checks.is_same_len_or_all_none([1], ['aaa', 222], [111, 'BBB']))
        self.assertFalse(checks.is_same_len_or_all_none([1, 'b'], ['aaa'], [111, 'BBB']))

        self.assertFalse(checks.is_same_len_or_all_none([1, 'b'], None))
        self.assertFalse(checks.is_same_len_or_all_none(None, ['aaa']))
        self.assertTrue(checks.is_same_len_or_all_none(None, None))

        self.assertFalse(checks.is_same_len_or_all_none([1, 'b'], None, ['aaa', 222]))
        self.assertFalse(checks.is_same_len_or_all_none(None, ['aaa'], [111]))
        self.assertFalse(checks.is_same_len_or_all_none(None, None, [111, 'BBB']))
        self.assertTrue(checks.is_same_len_or_all_none(None, None, None))

        self.assertFalse(checks.is_same_len_or_all_none([1], None, ['aaa', 222]))
        self.assertFalse(checks.is_same_len_or_all_none(None, ['aaa'], []))
        self.assertFalse(checks.is_same_len_or_all_none(None, ['aaa'], [111, 'BBB']))
        
    def test_is_instance(self):
        self.assertTrue(checks.is_instance(1, int))
        self.assertTrue(checks.is_instance(3.5, float))
        self.assertTrue(checks.is_instance('hello', str))
        self.assertTrue(checks.is_instance([1, 2, 3], list))
    
        self.assertTrue(checks.is_instance(1, (int, float)))
        self.assertTrue(checks.is_instance(3.5, (int, float)))
        self.assertTrue(checks.is_instance('hello', (str, list)))
        self.assertTrue(checks.is_instance([1, 2, 3], (str, list)))
    
        self.assertFalse(checks.is_instance(1, float))
        self.assertFalse(checks.is_instance(3.5, int))
        self.assertFalse(checks.is_instance('hello', list))
        self.assertFalse(checks.is_instance([1, 2, 3], str))
    
        self.assertFalse(checks.is_instance(1, (list, str)))
        self.assertFalse(checks.is_instance(3.5, (list, str)))
        self.assertFalse(checks.is_instance('hello', (int, float)))
        self.assertFalse(checks.is_instance([1, 2, 3], (int, float)))
    
        self.assertFalse(checks.is_instance(None, int))
        self.assertFalse(checks.is_instance(None, float))
        self.assertFalse(checks.is_instance(None, str))
        self.assertFalse(checks.is_instance(None, list))
    
        self.assertFalse(checks.is_instance(None, (int, float)))
        self.assertFalse(checks.is_instance(None, (int, float)))
        self.assertFalse(checks.is_instance(None, (str, list)))
        self.assertFalse(checks.is_instance(None, (str, list)))
    
        self.assertTrue(checks.is_instance(1, int, allow_none=True))
        self.assertTrue(checks.is_instance(3.5, float, allow_none=True))
        self.assertTrue(checks.is_instance('hello', str, allow_none=True))
        self.assertTrue(checks.is_instance([1, 2, 3], list, allow_none=True))
    
        self.assertTrue(checks.is_instance(1, (int, float), allow_none=True))
        self.assertTrue(checks.is_instance(3.5, (int, float), allow_none=True))
        self.assertTrue(checks.is_instance('hello', (str, list), allow_none=True))
        self.assertTrue(checks.is_instance([1, 2, 3], (str, list), allow_none=True))
    
        self.assertFalse(checks.is_instance(1, float, allow_none=True))
        self.assertFalse(checks.is_instance(3.5, int, allow_none=True))
        self.assertFalse(checks.is_instance('hello', list, allow_none=True))
        self.assertFalse(checks.is_instance([1, 2, 3], str, allow_none=True))
    
        self.assertFalse(checks.is_instance(1, (list, str), allow_none=True))
        self.assertFalse(checks.is_instance(3.5, (list, str), allow_none=True))
        self.assertFalse(checks.is_instance('hello', (int, float), allow_none=True))
        self.assertFalse(checks.is_instance([1, 2, 3], (int, float), allow_none=True))
    
        self.assertTrue(checks.is_instance(None, int, allow_none=True))
        self.assertTrue(checks.is_instance(None, float, allow_none=True))
        self.assertTrue(checks.is_instance(None, str, allow_none=True))
        self.assertTrue(checks.is_instance(None, list, allow_none=True))
    
        self.assertTrue(checks.is_instance(None, (int, float), allow_none=True))
        self.assertTrue(checks.is_instance(None, (int, float), allow_none=True))
        self.assertTrue(checks.is_instance(None, (str, list), allow_none=True))
        self.assertTrue(checks.is_instance(None, (str, list), allow_none=True))
    
    def test_check_instance(self):
        checks.check_instance(1, int)
        checks.check_instance(3.5, float)
        checks.check_instance('hello', str)
        checks.check_instance([1, 2, 3], list)
    
        checks.check_instance(1, (int, float))
        checks.check_instance(3.5, (int, float))
        checks.check_instance('hello', (str, list))
        checks.check_instance([1, 2, 3], (str, list))
    
        with self.assertRaises(AssertionError):
            checks.check_instance(1, float)
        with self.assertRaises(AssertionError):
            checks.check_instance(3.5, int)
        with self.assertRaises(AssertionError):
            checks.check_instance('hello', list)
        with self.assertRaises(AssertionError):
            checks.check_instance([1, 2, 3], str)
    
        with self.assertRaises(AssertionError):
            checks.check_instance(1, (list, str))
        with self.assertRaises(AssertionError):
            checks.check_instance(3.5, (list, str))
        with self.assertRaises(AssertionError):
            checks.check_instance('hello', (int, float))
        with self.assertRaises(AssertionError):
            checks.check_instance([1, 2, 3], (int, float))
    
        with self.assertRaises(AssertionError):
            checks.check_instance(None, int)
        with self.assertRaises(AssertionError):
            checks.check_instance(None, float)
        with self.assertRaises(AssertionError):
            checks.check_instance(None, str)
        with self.assertRaises(AssertionError):
            checks.check_instance(None, list)
    
        with self.assertRaises(AssertionError):
            checks.check_instance(None, (int, float))
        with self.assertRaises(AssertionError):
            checks.check_instance(None, (int, float))
        with self.assertRaises(AssertionError):
            checks.check_instance(None, (str, list))
        with self.assertRaises(AssertionError):
            checks.check_instance(None, (str, list))
    
        checks.check_instance(1, int, allow_none=True)
        checks.check_instance(3.5, float, allow_none=True)
        checks.check_instance('hello', str, allow_none=True)
        checks.check_instance([1, 2, 3], list, allow_none=True)
    
        checks.check_instance(1, (int, float), allow_none=True)
        checks.check_instance(3.5, (int, float), allow_none=True)
        checks.check_instance('hello', (str, list), allow_none=True)
        checks.check_instance([1, 2, 3], (str, list), allow_none=True)
    
        with self.assertRaises(AssertionError):
            checks.check_instance(1, float, allow_none=True)
        with self.assertRaises(AssertionError):
            checks.check_instance(3.5, int, allow_none=True)
        with self.assertRaises(AssertionError):
            checks.check_instance('hello', list, allow_none=True)
        with self.assertRaises(AssertionError):
            checks.check_instance([1, 2, 3], str, allow_none=True)
    
        with self.assertRaises(AssertionError):
            checks.check_instance(1, (list, str), allow_none=True)
        with self.assertRaises(AssertionError):
            checks.check_instance(3.5, (list, str), allow_none=True)
        with self.assertRaises(AssertionError):
            checks.check_instance('hello', (int, float), allow_none=True)
        with self.assertRaises(AssertionError):
            checks.check_instance([1, 2, 3], (int, float), allow_none=True)
    
        checks.check_instance(None, int, allow_none=True)
        checks.check_instance(None, float, allow_none=True)
        checks.check_instance(None, str, allow_none=True)
        checks.check_instance(None, list, allow_none=True)
    
        checks.check_instance(None, (int, float), allow_none=True)
        checks.check_instance(None, (int, float), allow_none=True)
        checks.check_instance(None, (str, list), allow_none=True)
        checks.check_instance(None, (str, list), allow_none=True)
        
    def test_ints(self):
        import numpy as np
        
        self.assertTrue(checks.is_int(3))
        self.assertFalse(checks.is_int(3.5))
        self.assertFalse(checks.is_int(np.int64(3)))
        self.assertFalse(checks.is_int(None))
        self.assertTrue(checks.is_int(None, allow_none=True))
        self.assertFalse(checks.is_int('hi'))
        
        checks.check_int(3)
        with self.assertRaises(AssertionError):
            checks.check_int(3.5)
        with self.assertRaises(AssertionError):
            checks.check_int(np.int64(3))
        with self.assertRaises(AssertionError):
            checks.check_int(None)
        checks.check_int(None, allow_none=True)
        with self.assertRaises(AssertionError):
            checks.check_int('hi')
        
        self.assertFalse(checks.is_some_numpy_int(3))
        self.assertFalse(checks.is_some_numpy_int(3.5))
        self.assertTrue(checks.is_some_numpy_int(np.int64(3)))
        self.assertFalse(checks.is_some_numpy_int(None))
        self.assertTrue(checks.is_some_numpy_int(None, allow_none=True))
        self.assertFalse(checks.is_some_numpy_int('hi'))

        with self.assertRaises(AssertionError):
            checks.check_some_numpy_int(3)
        with self.assertRaises(AssertionError):
            checks.check_some_numpy_int(3.5)
        checks.check_some_numpy_int(np.int64(3))
        with self.assertRaises(AssertionError):
            checks.check_some_numpy_int(None)
        checks.check_some_numpy_int(None, allow_none=True)
        with self.assertRaises(AssertionError):
            checks.check_some_numpy_int('hi')

        self.assertFalse(checks.is_some_numpy_uint(3))
        self.assertFalse(checks.is_some_numpy_uint(3.5))
        self.assertTrue(checks.is_some_numpy_uint(np.uint64(3)))
        self.assertFalse(checks.is_some_numpy_uint(None))
        self.assertTrue(checks.is_some_numpy_uint(None, allow_none=True))
        self.assertFalse(checks.is_some_numpy_uint('hi'))

        with self.assertRaises(AssertionError):
            checks.check_some_numpy_uint(3)
        with self.assertRaises(AssertionError):
            checks.check_some_numpy_uint(3.5)
        checks.check_some_numpy_uint(np.uint64(3))
        with self.assertRaises(AssertionError):
            checks.check_some_numpy_uint(None)
        checks.check_some_numpy_uint(None, allow_none=True)
        with self.assertRaises(AssertionError):
            checks.check_some_numpy_uint('hi')

        self.assertTrue(checks.is_some_int(3))
        self.assertFalse(checks.is_some_int(3.5))
        self.assertTrue(checks.is_some_int(np.uint64(3)))
        self.assertFalse(checks.is_some_int(None))
        self.assertTrue(checks.is_some_int(None, allow_none=True))
        self.assertFalse(checks.is_some_int('hi'))

        checks.check_some_int(3)
        with self.assertRaises(AssertionError):
            checks.check_some_int(3.5)
        checks.check_some_int(np.int64(3))
        checks.check_some_int(np.uint64(3))
        with self.assertRaises(AssertionError):
            checks.check_some_int(None)
        checks.check_some_int(None, allow_none=True)
        with self.assertRaises(AssertionError):
            checks.check_some_int('hi')
        
    def test_floats(self):
        import numpy as np
        
        self.assertFalse(checks.is_float(3))
        self.assertTrue(checks.is_float(3.5))
        # NB! The following is true (is that right?):
        self.assertTrue(checks.is_float(np.float64(3.5)))
        # NB! The following is true (is that right?):
        self.assertTrue(checks.is_float(np.double(3.5)))
        self.assertFalse(checks.is_float(None))
        self.assertTrue(checks.is_float(None, allow_none=True))
        self.assertFalse(checks.is_float('hi'))
    
        with self.assertRaises(AssertionError):
            checks.check_float(3)
        checks.check_float(3.5)
        checks.check_float(np.float64(3.5))
        checks.check_float(np.double(3.5))
        with self.assertRaises(AssertionError):
            checks.check_float(None)
        checks.check_float(None, allow_none=True)
        with self.assertRaises(AssertionError):
            checks.check_float('hi')
        
        self.assertFalse(checks.is_some_numpy_float(3))
        self.assertFalse(checks.is_some_numpy_float(3.5))
        self.assertTrue(checks.is_some_numpy_float(np.float64(3.5)))
        # NB! The following is true (is that right?):
        self.assertTrue(checks.is_some_numpy_float(np.double(3.5)))
        self.assertFalse(checks.is_some_numpy_float(None))
        self.assertTrue(checks.is_some_numpy_float(None, allow_none=True))
        self.assertFalse(checks.is_some_numpy_float('hi'))
    
        with self.assertRaises(AssertionError):
            checks.check_some_numpy_float(3)
        with self.assertRaises(AssertionError):
            checks.check_some_numpy_float(3.5)
        checks.check_some_numpy_float(np.float64(3.5))
        checks.check_some_numpy_float(np.double(3.5))
        with self.assertRaises(AssertionError):
            checks.check_some_numpy_float(None)
        checks.check_some_numpy_float(None, allow_none=True)
        with self.assertRaises(AssertionError):
            checks.check_some_numpy_float('hi')
        
        self.assertFalse(checks.is_some_numpy_double(3))
        self.assertFalse(checks.is_some_numpy_double(3.5))
        # NB! The following is true (is that right?):
        self.assertTrue(checks.is_some_numpy_double(np.float64(3.5)))
        self.assertTrue(checks.is_some_numpy_double(np.double(3.5)))
        self.assertFalse(checks.is_some_numpy_double(None))
        self.assertTrue(checks.is_some_numpy_double(None, allow_none=True))
        self.assertFalse(checks.is_some_numpy_double('hi'))
    
        with self.assertRaises(AssertionError):
            checks.check_some_numpy_double(3)
        with self.assertRaises(AssertionError):
            checks.check_some_numpy_double(3.5)
        checks.check_some_numpy_double(np.float64(3.5))
        checks.check_some_numpy_double(np.double(3.5))
        with self.assertRaises(AssertionError):
            checks.check_some_numpy_double(None)
        checks.check_some_numpy_double(None, allow_none=True)
        with self.assertRaises(AssertionError):
            checks.check_some_numpy_double('hi')
        
        self.assertFalse(checks.is_some_float(3))
        self.assertTrue(checks.is_some_float(3.5))
        self.assertTrue(checks.is_some_float(np.float64(3.5)))
        self.assertTrue(checks.is_some_float(np.double(3.5)))
        self.assertFalse(checks.is_some_float(None))
        self.assertTrue(checks.is_some_float(None, allow_none=True))
        self.assertFalse(checks.is_some_float('hi'))
    
        with self.assertRaises(AssertionError):
            checks.check_some_float(3)
        checks.check_some_float(3.5)
        checks.check_some_float(np.float64(3.5))
        checks.check_some_float(np.double(3.5))
        with self.assertRaises(AssertionError):
            checks.check_some_float(None)
        checks.check_some_float(None, allow_none=True)
        with self.assertRaises(AssertionError):
            checks.check_some_float('hi')        
        
    def test_numbers(self):
        import numpy as np
                
        self.assertTrue(checks.is_some_number(3))
        self.assertTrue(checks.is_some_number(3.5))
        self.assertTrue(checks.is_some_number(np.int64(3)))
        self.assertTrue(checks.is_some_number(np.float64(3.5)))
        self.assertTrue(checks.is_some_number(np.double(3.5)))
        self.assertFalse(checks.is_some_number(None))
        self.assertTrue(checks.is_some_number(None, allow_none=True))
        self.assertFalse(checks.is_some_number('hi'))
    
        checks.check_some_number(3)
        checks.check_some_number(3.5)
        checks.check_some_number(np.float64(3.5))
        checks.check_some_number(np.double(3.5))
        with self.assertRaises(AssertionError):
            checks.check_some_number(None)
        checks.check_some_number(None, allow_none=True)
        with self.assertRaises(AssertionError):
            checks.check_some_number('hi')
            
    def test_numpy_arrays(self):
        import numpy as np
        self.assertTrue(checks.is_numpy_array(np.array([1, 2, 3])))
        self.assertTrue(checks.is_numpy_array(np.array([[1, 2, 3], [1, 2, 3]])))
        self.assertTrue(checks.is_numpy_array(np.array(3)))
        self.assertFalse(checks.is_numpy_array([1, 2, 3]))
        self.assertFalse(checks.is_numpy_array(3))
        self.assertFalse(checks.is_numpy_array(np.int64(3)))
        self.assertFalse(checks.is_numpy_array(3.5))
        self.assertFalse(checks.is_numpy_array(np.float64(3.5)))
        self.assertFalse(checks.is_numpy_array('hi'))
        self.assertFalse(checks.is_numpy_array(None))
        self.assertTrue(checks.is_numpy_array(None, allow_none=True))

        checks.check_numpy_array(np.array([1, 2, 3]))
        checks.check_numpy_array(np.array([[1, 2, 3], [1, 2, 3]]))
        checks.check_numpy_array(np.array(3))
        with self.assertRaises(AssertionError):
            checks.check_numpy_array([1, 2, 3])
        with self.assertRaises(AssertionError):
            checks.check_numpy_array(3)
        with self.assertRaises(AssertionError):
            checks.check_numpy_array(np.int64(3))
        with self.assertRaises(AssertionError):
            checks.check_numpy_array(3.5)
        with self.assertRaises(AssertionError):
            checks.check_numpy_array(np.float64(3.5))
        with self.assertRaises(AssertionError):
            checks.check_numpy_array('hi')
        with self.assertRaises(AssertionError):
            checks.check_numpy_array(None)
        checks.check_numpy_array(None, allow_none=True)

    def test_strings(self):
        self.assertFalse(checks.is_string([1, 2, 3]))
        self.assertFalse(checks.is_string(3))
        self.assertFalse(checks.is_string(3.5))
        self.assertTrue(checks.is_string('hi'))
        self.assertTrue(checks.is_string("hi"))
        self.assertTrue(checks.is_string("""hi"""))
        self.assertFalse(checks.is_string(None))
        self.assertTrue(checks.is_string(None, allow_none=True))

        with self.assertRaises(AssertionError):
            checks.check_string([1, 2, 3])
        with self.assertRaises(AssertionError):
            checks.check_string(3)
        with self.assertRaises(AssertionError):
            checks.check_string(3.5)
        checks.check_string('hi')
        checks.check_string("hi")
        checks.check_string("""hi""")
        with self.assertRaises(AssertionError):
            checks.check_string(None)
        checks.check_string(None, allow_none=True)
        
    def test_dates(self):
        import datetime as dt
        import numpy as np
        import pandas as pd
        
        self.assertFalse(checks.is_date([1, 2, 3]))
        self.assertFalse(checks.is_date(3))
        self.assertFalse(checks.is_date(3.5))
        self.assertFalse(checks.is_date('hi'))
        self.assertFalse(checks.is_date("hi"))
        self.assertFalse(checks.is_date("""hi"""))
        self.assertTrue(checks.is_date(dt.date(2019, 9, 10)))
        self.assertFalse(checks.is_date(dt.time(12, 3)))
        self.assertFalse(checks.is_date(dt.datetime(2019, 9, 10, 12, 3)))
        self.assertFalse(checks.is_date(dt.timedelta(seconds=5)))
        self.assertFalse(checks.is_date(np.timedelta64(5, 's')))
        self.assertFalse(checks.is_date(pd.Timedelta(5, 's')))
        self.assertFalse(checks.is_date(None))
        self.assertTrue(checks.is_date(None, allow_none=True))

        with self.assertRaises(AssertionError):
            checks.check_date([1, 2, 3])
        with self.assertRaises(AssertionError):
            checks.check_date(3)
        with self.assertRaises(AssertionError):
            checks.check_date(3.5)
        with self.assertRaises(AssertionError):
            checks.check_date('hi')
        with self.assertRaises(AssertionError):
            checks.check_date("hi")
        with self.assertRaises(AssertionError):
            checks.check_date("""hi""")
        checks.check_date(dt.date(2019, 9, 10))
        with self.assertRaises(AssertionError):
            checks.check_date(dt.time(12, 3))
        with self.assertRaises(AssertionError):
            checks.check_date(dt.datetime(2019, 9, 10, 12, 3))
        with self.assertRaises(AssertionError):
            checks.check_date(dt.timedelta(seconds=5))
        with self.assertRaises(AssertionError):
            checks.check_date(np.timedelta64(5, 's'))
        with self.assertRaises(AssertionError):
            checks.check_date(pd.Timedelta(5, 's'))
        with self.assertRaises(AssertionError):
            checks.check_date(None)
        checks.check_date(None, allow_none=True)
        
        self.assertFalse(checks.is_some_date([1, 2, 3]))
        self.assertFalse(checks.is_some_date(3))
        self.assertFalse(checks.is_some_date(3.5))
        self.assertFalse(checks.is_some_date('hi'))
        self.assertFalse(checks.is_some_date("hi"))
        self.assertFalse(checks.is_some_date("""hi"""))
        self.assertTrue(checks.is_some_date(dt.date(2019, 9, 10)))
        self.assertFalse(checks.is_some_date(dt.time(12, 3)))
        self.assertFalse(checks.is_some_date(dt.datetime(2019, 9, 10, 12, 3)))
        self.assertFalse(checks.is_some_date(dt.timedelta(seconds=5)))
        self.assertFalse(checks.is_some_date(np.timedelta64(5, 's')))
        self.assertFalse(checks.is_some_date(pd.Timedelta(5, 's')))
        self.assertFalse(checks.is_some_date(None))
        self.assertTrue(checks.is_some_date(None, allow_none=True))

        with self.assertRaises(AssertionError):
            checks.check_some_date([1, 2, 3])
        with self.assertRaises(AssertionError):
            checks.check_some_date(3)
        with self.assertRaises(AssertionError):
            checks.check_some_date(3.5)
        with self.assertRaises(AssertionError):
            checks.check_some_date('hi')
        with self.assertRaises(AssertionError):
            checks.check_some_date("hi")
        with self.assertRaises(AssertionError):
            checks.check_some_date("""hi""")
        checks.check_some_date(dt.date(2019, 9, 10))
        with self.assertRaises(AssertionError):
            checks.check_some_date(dt.time(12, 3))
        with self.assertRaises(AssertionError):
            checks.check_some_date(dt.datetime(2019, 9, 10, 12, 3))
        with self.assertRaises(AssertionError):
            checks.check_some_date(dt.timedelta(seconds=5))
        with self.assertRaises(AssertionError):
            checks.check_some_date(np.timedelta64(5, 's'))
        with self.assertRaises(AssertionError):
            checks.check_some_date(pd.Timedelta(5, 's'))
        with self.assertRaises(AssertionError):
            checks.check_some_date(None)
        checks.check_some_date(None, allow_none=True)

    def test_times(self):
        import datetime as dt
        import numpy as np
        import pandas as pd
        
        self.assertFalse(checks.is_time([1, 2, 3]))
        self.assertFalse(checks.is_time(3))
        self.assertFalse(checks.is_time(3.5))
        self.assertFalse(checks.is_time('hi'))
        self.assertFalse(checks.is_time("hi"))
        self.assertFalse(checks.is_time("""hi"""))
        self.assertFalse(checks.is_time(dt.date(2019, 9, 10)))
        self.assertTrue(checks.is_time(dt.time(12, 3)))
        self.assertFalse(checks.is_time(dt.datetime(2019, 9, 10, 12, 3)))
        self.assertFalse(checks.is_time(dt.timedelta(seconds=5)))
        self.assertFalse(checks.is_time(np.timedelta64(5, 's')))
        self.assertFalse(checks.is_time(pd.Timedelta(5, 's')))
        self.assertFalse(checks.is_time(None))
        self.assertTrue(checks.is_time(None, allow_none=True))

        with self.assertRaises(AssertionError):
            checks.check_time([1, 2, 3])
        with self.assertRaises(AssertionError):
            checks.check_time(3)
        with self.assertRaises(AssertionError):
            checks.check_time(3.5)
        with self.assertRaises(AssertionError):
            checks.check_time('hi')
        with self.assertRaises(AssertionError):
            checks.check_time("hi")
        with self.assertRaises(AssertionError):
            checks.check_time("""hi""")
        with self.assertRaises(AssertionError):
            checks.check_time(dt.date(2019, 9, 10))
        checks.check_time(dt.time(12, 3))
        with self.assertRaises(AssertionError):
            checks.check_time(dt.datetime(2019, 9, 10, 12, 3))
        with self.assertRaises(AssertionError):
            checks.check_time(dt.timedelta(seconds=5))
        with self.assertRaises(AssertionError):
            checks.check_time(np.timedelta64(5, 's'))
        with self.assertRaises(AssertionError):
            checks.check_time(pd.Timedelta(5, 's'))
        with self.assertRaises(AssertionError):
            checks.check_time(None)
        checks.check_time(None, allow_none=True)
        
        self.assertFalse(checks.is_some_time([1, 2, 3]))
        self.assertFalse(checks.is_some_time(3))
        self.assertFalse(checks.is_some_time(3.5))
        self.assertFalse(checks.is_some_time('hi'))
        self.assertFalse(checks.is_some_time("hi"))
        self.assertFalse(checks.is_some_time("""hi"""))
        self.assertFalse(checks.is_some_time(dt.date(2019, 9, 10)))
        self.assertTrue(checks.is_some_time(dt.time(12, 3)))
        self.assertFalse(checks.is_some_time(dt.datetime(2019, 9, 10, 12, 3)))
        self.assertFalse(checks.is_some_time(dt.timedelta(seconds=5)))
        self.assertFalse(checks.is_some_time(None))
        self.assertTrue(checks.is_some_time(None, allow_none=True))

        with self.assertRaises(AssertionError):
            checks.check_some_time([1, 2, 3])
        with self.assertRaises(AssertionError):
            checks.check_some_time(3)
        with self.assertRaises(AssertionError):
            checks.check_some_time(3.5)
        with self.assertRaises(AssertionError):
            checks.check_some_time('hi')
        with self.assertRaises(AssertionError):
            checks.check_some_time("hi")
        with self.assertRaises(AssertionError):
            checks.check_some_time("""hi""")
        with self.assertRaises(AssertionError):
            checks.check_some_time(dt.date(2019, 9, 10))
        checks.check_some_time(dt.time(12, 3))
        with self.assertRaises(AssertionError):
            checks.check_some_time(dt.datetime(2019, 9, 10, 12, 3))
        with self.assertRaises(AssertionError):
            checks.check_some_time(dt.timedelta(seconds=5))
        with self.assertRaises(AssertionError):
            checks.check_some_time(np.timedelta64(5, 's'))
        with self.assertRaises(AssertionError):
            checks.check_some_time(pd.Timedelta(5, 's'))
        with self.assertRaises(AssertionError):
            checks.check_some_time(None)
        checks.check_some_time(None, allow_none=True)

    def test_datetimes(self):
        import datetime as dt
        import numpy as np
        import pandas as pd
        
        self.assertFalse(checks.is_datetime([1, 2, 3]))
        self.assertFalse(checks.is_datetime(3))
        self.assertFalse(checks.is_datetime(3.5))
        self.assertFalse(checks.is_datetime('hi'))
        self.assertFalse(checks.is_datetime("hi"))
        self.assertFalse(checks.is_datetime("""hi"""))
        self.assertFalse(checks.is_datetime(dt.date(2019, 9, 10)))
        self.assertFalse(checks.is_datetime(dt.time(12, 3)))
        self.assertTrue(checks.is_datetime(dt.datetime(2019, 9, 10, 12, 3)))
        self.assertFalse(checks.is_datetime(dt.timedelta(seconds=5)))
        self.assertFalse(checks.is_datetime(np.timedelta64(5, 's')))
        self.assertFalse(checks.is_datetime(pd.Timedelta(5, 's')))
        self.assertFalse(checks.is_datetime(None))
        self.assertTrue(checks.is_datetime(None, allow_none=True))

        with self.assertRaises(AssertionError):
            checks.check_datetime([1, 2, 3])
        with self.assertRaises(AssertionError):
            checks.check_datetime(3)
        with self.assertRaises(AssertionError):
            checks.check_datetime(3.5)
        with self.assertRaises(AssertionError):
            checks.check_datetime('hi')
        with self.assertRaises(AssertionError):
            checks.check_datetime("hi")
        with self.assertRaises(AssertionError):
            checks.check_datetime("""hi""")
        with self.assertRaises(AssertionError):
            checks.check_datetime(dt.date(2019, 9, 10))
        with self.assertRaises(AssertionError):
            checks.check_datetime(dt.time(12, 3))
        checks.check_datetime(dt.datetime(2019, 9, 10, 12, 3))
        with self.assertRaises(AssertionError):
            checks.check_datetime(dt.timedelta(seconds=5))
        with self.assertRaises(AssertionError):
            checks.check_datetime(np.timedelta64(5, 's'))
        with self.assertRaises(AssertionError):
            checks.check_datetime(pd.Timedelta(5, 's'))
        with self.assertRaises(AssertionError):
            checks.check_datetime(None)
        checks.check_datetime(None, allow_none=True)
        
        self.assertFalse(checks.is_some_datetime([1, 2, 3]))
        self.assertFalse(checks.is_some_datetime(3))
        self.assertFalse(checks.is_some_datetime(3.5))
        self.assertFalse(checks.is_some_datetime('hi'))
        self.assertFalse(checks.is_some_datetime("hi"))
        self.assertFalse(checks.is_some_datetime("""hi"""))
        self.assertFalse(checks.is_some_datetime(dt.date(2019, 9, 10)))
        self.assertFalse(checks.is_some_datetime(dt.time(12, 3)))
        self.assertTrue(checks.is_some_datetime(dt.datetime(2019, 9, 10, 12, 3)))
        self.assertFalse(checks.is_some_datetime(dt.timedelta(seconds=5)))
        self.assertFalse(checks.is_some_datetime(None))
        self.assertTrue(checks.is_some_datetime(None, allow_none=True))

        with self.assertRaises(AssertionError):
            checks.check_some_datetime([1, 2, 3])
        with self.assertRaises(AssertionError):
            checks.check_some_datetime(3)
        with self.assertRaises(AssertionError):
            checks.check_some_datetime(3.5)
        with self.assertRaises(AssertionError):
            checks.check_some_datetime('hi')
        with self.assertRaises(AssertionError):
            checks.check_some_datetime("hi")
        with self.assertRaises(AssertionError):
            checks.check_some_datetime("""hi""")
        with self.assertRaises(AssertionError):
            checks.check_some_datetime(dt.date(2019, 9, 10))
        with self.assertRaises(AssertionError):
            checks.check_some_datetime(dt.time(12, 3))
        checks.check_some_datetime(dt.datetime(2019, 9, 10, 12, 3))
        with self.assertRaises(AssertionError):
            checks.check_some_datetime(dt.timedelta(seconds=5))
        with self.assertRaises(AssertionError):
            checks.check_some_datetime(np.timedelta64(5, 's'))
        with self.assertRaises(AssertionError):
            checks.check_some_datetime(pd.Timedelta(5, 's'))
        with self.assertRaises(AssertionError):
            checks.check_some_datetime(None)
        checks.check_some_datetime(None, allow_none=True)

    def test_timedeltas(self):
        import datetime as dt
        import numpy as np
        import pandas as pd
        
        self.assertFalse(checks.is_timedelta([1, 2, 3]))
        self.assertFalse(checks.is_timedelta(3))
        self.assertFalse(checks.is_timedelta(3.5))
        self.assertFalse(checks.is_timedelta('hi'))
        self.assertFalse(checks.is_timedelta("hi"))
        self.assertFalse(checks.is_timedelta("""hi"""))
        self.assertFalse(checks.is_timedelta(dt.date(2019, 9, 10)))
        self.assertFalse(checks.is_timedelta(dt.time(12, 3)))
        self.assertFalse(checks.is_timedelta(dt.datetime(2019, 9, 10, 12, 3)))
        self.assertTrue(checks.is_timedelta(dt.timedelta(seconds=5)))
        self.assertFalse(checks.is_timedelta(np.timedelta64(5, 's')))
        # NB! Note that the following is true:
        self.assertTrue(checks.is_timedelta(pd.Timedelta(5, 's')))
        self.assertFalse(checks.is_timedelta(None))
        self.assertTrue(checks.is_timedelta(None, allow_none=True))

        with self.assertRaises(AssertionError):
            checks.check_timedelta([1, 2, 3])
        with self.assertRaises(AssertionError):
            checks.check_timedelta(3)
        with self.assertRaises(AssertionError):
            checks.check_timedelta(3.5)
        with self.assertRaises(AssertionError):
            checks.check_timedelta('hi')
        with self.assertRaises(AssertionError):
            checks.check_timedelta("hi")
        with self.assertRaises(AssertionError):
            checks.check_timedelta("""hi""")
        with self.assertRaises(AssertionError):
            checks.check_timedelta(dt.date(2019, 9, 10))
        with self.assertRaises(AssertionError):
            checks.check_timedelta(dt.time(12, 3))
        with self.assertRaises(AssertionError):
            checks.check_timedelta(dt.datetime(2019, 9, 10, 12, 3))
        checks.check_timedelta(dt.timedelta(seconds=5))
        with self.assertRaises(AssertionError):
            checks.check_timedelta(np.timedelta64(5, 's'))
        # NB! Note that the following holds:
        checks.check_timedelta(pd.Timedelta(5, 's'))
        with self.assertRaises(AssertionError):
            checks.check_timedelta(None)
        checks.check_timedelta(None, allow_none=True)
        
        self.assertFalse(checks.is_some_timedelta([1, 2, 3]))
        self.assertFalse(checks.is_some_timedelta(3))
        self.assertFalse(checks.is_some_timedelta(3.5))
        self.assertFalse(checks.is_some_timedelta('hi'))
        self.assertFalse(checks.is_some_timedelta("hi"))
        self.assertFalse(checks.is_some_timedelta("""hi"""))
        self.assertFalse(checks.is_some_timedelta(dt.date(2019, 9, 10)))
        self.assertFalse(checks.is_some_timedelta(dt.time(12, 3)))
        self.assertFalse(checks.is_some_timedelta(dt.datetime(2019, 9, 10, 12, 3)))
        self.assertTrue(checks.is_some_timedelta(dt.timedelta(seconds=5)))
        self.assertTrue(checks.is_some_timedelta(np.timedelta64(5, 's')))
        self.assertTrue(checks.is_some_timedelta(pd.Timedelta(5, 's')))
        self.assertFalse(checks.is_some_timedelta(None))
        self.assertTrue(checks.is_some_timedelta(None, allow_none=True))

        with self.assertRaises(AssertionError):
            checks.check_some_timedelta([1, 2, 3])
        with self.assertRaises(AssertionError):
            checks.check_some_timedelta(3)
        with self.assertRaises(AssertionError):
            checks.check_some_timedelta(3.5)
        with self.assertRaises(AssertionError):
            checks.check_some_timedelta('hi')
        with self.assertRaises(AssertionError):
            checks.check_some_timedelta("hi")
        with self.assertRaises(AssertionError):
            checks.check_some_timedelta("""hi""")
        with self.assertRaises(AssertionError):
            checks.check_some_timedelta(dt.date(2019, 9, 10))
        with self.assertRaises(AssertionError):
            checks.check_some_timedelta(dt.time(12, 3))
        with self.assertRaises(AssertionError):
            checks.check_some_timedelta(dt.datetime(2019, 9, 10, 12, 3))
        checks.check_some_timedelta(dt.timedelta(seconds=5))
        checks.check_some_timedelta(np.timedelta64(5, 's'))
        checks.check_some_timedelta(pd.Timedelta(5, 's'))
        with self.assertRaises(AssertionError):
            checks.check_some_timedelta(None)
        checks.check_some_timedelta(None, allow_none=True)
        
    def test_iterables(self):
        import numpy as np
        
        self.assertFalse(checks.is_iterable(3))
        self.assertFalse(checks.is_iterable(3.5))
        self.assertTrue(checks.is_iterable('hi'))
        self.assertTrue(checks.is_iterable([1, 2, 3]))
        self.assertTrue(checks.is_iterable([[1, 2, 3], [1, 2, 3]]))
        self.assertTrue(checks.is_iterable(np.array([1, 2, 3])))
        self.assertTrue(checks.is_iterable(np.array([[1, 2, 3], [1, 2, 3]])))
        self.assertTrue(checks.is_iterable({'name': 'Paul', 'surname': 'Bilokon'}))
        self.assertFalse(checks.is_iterable(None))
        self.assertTrue(checks.is_iterable(None, allow_none=True))

        with self.assertRaises(AssertionError):
            checks.check_iterable(3)
        with self.assertRaises(AssertionError):
            checks.check_iterable(3.5)
        checks.check_iterable('hi')
        checks.check_iterable([1, 2, 3])
        checks.check_iterable([[1, 2, 3], [1, 2, 3]])
        checks.check_iterable(np.array([1, 2, 3]))
        checks.check_iterable(np.array([[1, 2, 3], [1, 2, 3]]))
        checks.check_iterable({'name': 'Paul', 'surname': 'Bilokon'})
        with self.assertRaises(AssertionError):
            checks.check_iterable(None)
        checks.check_iterable(None, allow_none=True)

        self.assertFalse(checks.is_iterable_not_string(3))
        self.assertFalse(checks.is_iterable_not_string(3.5))
        self.assertFalse(checks.is_iterable_not_string('hi'))
        self.assertTrue(checks.is_iterable_not_string([1, 2, 3]))
        self.assertTrue(checks.is_iterable_not_string([[1, 2, 3], [1, 2, 3]]))
        self.assertTrue(checks.is_iterable_not_string(np.array([1, 2, 3])))
        self.assertTrue(checks.is_iterable_not_string(np.array([[1, 2, 3], [1, 2, 3]])))
        self.assertTrue(checks.is_iterable_not_string({'name': 'Paul', 'surname': 'Bilokon'}))
        self.assertFalse(checks.is_iterable_not_string(None))
        self.assertTrue(checks.is_iterable_not_string(None, allow_none=True))

        with self.assertRaises(AssertionError):
            checks.check_iterable_not_string(3)
        with self.assertRaises(AssertionError):
            checks.check_iterable_not_string(3.5)
        with self.assertRaises(AssertionError):
            checks.check_iterable_not_string('hi')
        checks.check_iterable_not_string([1, 2, 3])
        checks.check_iterable_not_string([[1, 2, 3], [1, 2, 3]])
        checks.check_iterable_not_string(np.array([1, 2, 3]))
        checks.check_iterable_not_string(np.array([[1, 2, 3], [1, 2, 3]]))
        checks.check_iterable_not_string({'name': 'Paul', 'surname': 'Bilokon'})
        with self.assertRaises(AssertionError):
            checks.check_iterable_not_string(None)
        checks.check_iterable_not_string(None, allow_none=True)

        result, iterable = checks.is_iterable_over_instances(3, int)
        self.assertFalse(result)
        self.assertEqual(iterable, 3)
        result, iterable = checks.is_iterable_over_instances(3.5, float)
        self.assertFalse(result)
        self.assertEqual(iterable, 3.5)
        result, iterable = checks.is_iterable_over_instances('hi', str)
        self.assertTrue(result)
        self.assertEqual(list(iterable), ['h', 'i'])
        result, iterable = checks.is_iterable_over_instances([1, 2, 3], int)
        self.assertTrue(result)
        self.assertEqual(list(iterable), [1, 2, 3])
        result, iterable = checks.is_iterable_over_instances([[1, 2, 3], [1, 2, 3]], list)
        self.assertTrue(result)
        self.assertEqual(list(iterable), [[1, 2, 3], [1, 2, 3]])
        result, iterable = checks.is_iterable_over_instances(np.array([1, 2, 3]), np.int32)
        self.assertTrue(result)
        self.assertEqual(list(iterable), [1, 2, 3])
        # NB! In this case the iterable that was passed in does not quite match the returned iterable
        result, _ = checks.is_iterable_over_instances(np.array([[1, 2, 3], [1, 2, 3]]), np.ndarray)
        self.assertTrue(result)
        result, iterable = checks.is_iterable_over_instances({'name': 'Paul', 'surname': 'Bilokon'}, str)
        self.assertTrue(result)
        self.assertEqual(list(iterable), ['name', 'surname'])
        result, iterable = checks.is_iterable_over_instances([], int)
        self.assertFalse(result)
        result, iterable = checks.is_iterable_over_instances([], int, allow_empty=True)
        self.assertTrue(result)
        result, iterable = checks.is_iterable_over_instances(None, int)
        self.assertFalse(result)
        self.assertTrue(iterable is None)
        result, iterable = checks.is_iterable_over_instances(None, int, allow_none=True)
        self.assertTrue(result)
        self.assertTrue(iterable is None)

        with self.assertRaises(AssertionError):
            checks.check_iterable_over_instances(3, int)        
        with self.assertRaises(AssertionError):
            checks.check_iterable_over_instances(3.5, float)
        iterable = checks.check_iterable_over_instances('hi', str)
        self.assertEqual(list(iterable), ['h', 'i'])
        iterable = checks.check_iterable_over_instances([1, 2, 3], int)
        self.assertEqual(list(iterable), [1, 2, 3])
        iterable = checks.check_iterable_over_instances([[1, 2, 3], [1, 2, 3]], list)
        self.assertEqual(list(iterable), [[1, 2, 3], [1, 2, 3]])        
        iterable = checks.check_iterable_over_instances(np.array([1, 2, 3]), np.int32)
        self.assertEqual(list(iterable), [1, 2, 3])        
        # NB! In this case the iterable that was passed in does not quite match the returned iterable
        _ = checks.check_iterable_over_instances(np.array([[1, 2, 3], [1, 2, 3]]), np.ndarray)
        iterable = checks.check_iterable_over_instances({'name': 'Paul', 'surname': 'Bilokon'}, str)
        self.assertEqual(list(iterable), ['name', 'surname'])
        with self.assertRaises(AssertionError):
            checks.check_iterable_over_instances([], int)        
        iterable = checks.check_iterable_over_instances([], int, allow_empty=True)
        with self.assertRaises(AssertionError):
            checks.check_iterable_over_instances(None, int)
        iterable = checks.check_iterable_over_instances(None, int, allow_none=True)
        self.assertTrue(iterable is None)
        
    def test_dicts(self):
        import collections as col
        import numpy as np
        
        self.assertFalse(checks.is_dict(3))
        self.assertFalse(checks.is_dict(3.5))
        self.assertFalse(checks.is_dict('hi'))
        self.assertFalse(checks.is_dict([1, 2, 3]))
        self.assertFalse(checks.is_dict([[1, 2, 3], [1, 2, 3]]))
        self.assertFalse(checks.is_dict(np.array([1, 2, 3])))
        self.assertFalse(checks.is_dict(np.array([[1, 2, 3], [1, 2, 3]])))
        self.assertTrue(checks.is_dict({'name': 'Paul', 'surname': 'Bilokon'}))
        self.assertTrue(checks.is_dict(col.OrderedDict((('name', 'Paul'), ('surname', 'Bilokon')))))
        self.assertFalse(checks.is_dict(None))
        self.assertTrue(checks.is_dict(None, allow_none=True))

        with self.assertRaises(AssertionError):
            checks.check_dict(3)
        with self.assertRaises(AssertionError):
            checks.check_dict(3.5)
        with self.assertRaises(AssertionError):
            checks.check_dict('hi')
        with self.assertRaises(AssertionError):
            checks.check_dict([1, 2, 3])
        with self.assertRaises(AssertionError):
            checks.check_dict([[1, 2, 3], [1, 2, 3]])
        with self.assertRaises(AssertionError):
            checks.check_dict(np.array([1, 2, 3]))
        with self.assertRaises(AssertionError):
            checks.check_dict(np.array([[1, 2, 3], [1, 2, 3]]))
        checks.check_dict({'name': 'Paul', 'surname': 'Bilokon'})
        checks.check_dict(col.OrderedDict((('name', 'Paul'), ('surname', 'Bilokon'))))
        with self.assertRaises(AssertionError):
            checks.check_dict(None)
        checks.check_dict(None, allow_none=True)
        
        self.assertFalse(checks.is_some_dict(3))
        self.assertFalse(checks.is_some_dict(3.5))
        self.assertFalse(checks.is_some_dict('hi'))
        self.assertFalse(checks.is_some_dict([1, 2, 3]))
        self.assertFalse(checks.is_some_dict([[1, 2, 3], [1, 2, 3]]))
        self.assertFalse(checks.is_some_dict(np.array([1, 2, 3])))
        self.assertFalse(checks.is_some_dict(np.array([[1, 2, 3], [1, 2, 3]])))
        self.assertTrue(checks.is_some_dict({'name': 'Paul', 'surname': 'Bilokon'}))
        self.assertTrue(checks.is_some_dict(col.OrderedDict((('name', 'Paul'), ('surname', 'Bilokon')))))
        self.assertFalse(checks.is_some_dict(None))
        self.assertTrue(checks.is_some_dict(None, allow_none=True))

        with self.assertRaises(AssertionError):
            checks.check_some_dict(3)
        with self.assertRaises(AssertionError):
            checks.check_some_dict(3.5)
        with self.assertRaises(AssertionError):
            checks.check_some_dict('hi')
        with self.assertRaises(AssertionError):
            checks.check_some_dict([1, 2, 3])
        with self.assertRaises(AssertionError):
            checks.check_some_dict([[1, 2, 3], [1, 2, 3]])
        with self.assertRaises(AssertionError):
            checks.check_some_dict(np.array([1, 2, 3]))
        with self.assertRaises(AssertionError):
            checks.check_some_dict(np.array([[1, 2, 3], [1, 2, 3]]))
        checks.check_some_dict({'name': 'Paul', 'surname': 'Bilokon'})
        checks.check_some_dict(col.OrderedDict((('name', 'Paul'), ('surname', 'Bilokon'))))
        with self.assertRaises(AssertionError):
            checks.check_some_dict(None)
        checks.check_some_dict(None, allow_none=True)
        
    def test_callables(self):
        import numpy as np
        
        self.assertFalse(checks.is_callable(3))
        self.assertFalse(checks.is_callable(3.5))
        self.assertFalse(checks.is_callable('hi'))
        self.assertFalse(checks.is_callable([1, 2, 3]))
        self.assertFalse(checks.is_callable([[1, 2, 3], [1, 2, 3]]))
        self.assertFalse(checks.is_callable(np.array([1, 2, 3])))
        self.assertFalse(checks.is_callable(np.array([[1, 2, 3], [1, 2, 3]])))
        self.assertFalse(checks.is_callable({'name': 'Paul', 'surname': 'Bilokon'}))
        def my_func():
            return 123
        self.assertTrue(checks.is_callable(my_func))
        self.assertTrue(checks.is_callable(lambda x, y: x + y))
        self.assertFalse(checks.is_callable(None))
        self.assertTrue(checks.is_callable(None, allow_none=True))

        with self.assertRaises(AssertionError):
            checks.check_callable(3)
        with self.assertRaises(AssertionError):
            checks.check_callable(3.5)
        with self.assertRaises(AssertionError):
            checks.check_callable('hi')
        with self.assertRaises(AssertionError):
            checks.check_callable([1, 2, 3])
        with self.assertRaises(AssertionError):
            checks.check_callable([[1, 2, 3], [1, 2, 3]])
        with self.assertRaises(AssertionError):
            checks.check_callable(np.array([1, 2, 3]))
        with self.assertRaises(AssertionError):
            checks.check_callable(np.array([[1, 2, 3], [1, 2, 3]]))
        with self.assertRaises(AssertionError):
            checks.check_callable({'name': 'Paul', 'surname': 'Bilokon'})
        def my_func1():
            return 123
        checks.check_callable(my_func1)
        checks.check_callable(lambda x, y: x + y)
        with self.assertRaises(AssertionError):
            checks.check_callable(None)
        checks.check_callable(None, allow_none=True)
        
    def test_type(self):
        import numpy as np
        
        self.assertFalse(checks.is_type(3))
        self.assertFalse(checks.is_type('hi'))
        self.assertFalse(checks.is_type([1, 2, 3]))
        self.assertTrue(checks.is_type(int))
        self.assertTrue(checks.is_type(np.ndarray))
        self.assertFalse(checks.is_type(None))
        self.assertTrue(checks.is_type(None, allow_none=True))

        with self.assertRaises(AssertionError):
            checks.check_type(3)
        with self.assertRaises(AssertionError):
            checks.check_type('hi')
        with self.assertRaises(AssertionError):
            checks.check_type([1, 2, 3])
        checks.check_type(int)
        checks.check_type(np.ndarray)
        with self.assertRaises(AssertionError):
            checks.check_type(None)
        checks.check_type(None, allow_none=True)

if __name__ == '__main__':
    unittest.main()
