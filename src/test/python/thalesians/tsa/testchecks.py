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

if __name__ == '__main__':
    unittest.main()
