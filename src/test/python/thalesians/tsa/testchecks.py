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

if __name__ == '__main__':
    unittest.main()
