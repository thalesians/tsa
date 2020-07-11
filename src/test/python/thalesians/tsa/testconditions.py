import unittest

from thalesians.tsa.conditions import precondition, postcondition

class TestConditions(unittest.TestCase):
    def test_unary_function_precondition(self):
        @precondition(lambda arg: arg >= 0,
                'arg must be greater than or equal to 0')
        def plus_one(arg):
            return arg + 1
        self.assertEqual(plus_one(1), 2)        
        with self.assertRaises(AssertionError) as ae:
            plus_one(-1)
        self.assertEqual(ae.exception.args[0],
                'arg must be greater than or equal to 0')
        
    def test_unary_function_precondition_level_too_low(self):
        @precondition(lambda arg: arg >= 0,
                'arg must be greater than or equal to 0',
                level=0)
        def plus_one(arg):
            return arg + 1
        self.assertEqual(plus_one(1), 2)
        # Even though the precondition is violated, its level is less than
        # tsa_settings.MIN_PRECONDITION_LEVEL, so it is not checked:
        self.assertEqual(plus_one(-1), 0)
        
    def test_binary_function_precondition(self):
        @precondition(lambda arg1, arg2: arg1 >= 0 and arg2 >= 0,
                'both arguments must be greater than or equal to 0')
        def add(arg1, arg2):
            return arg1 + arg2
        self.assertEqual(add(100, 200), 300)
        with self.assertRaises(AssertionError) as ae:
            add(100, -200)
        self.assertEqual(ae.exception.args[0],
                'both arguments must be greater than or equal to 0')
             
    def test_binary_function_precondition_composition(self):
        @precondition(lambda arg1, arg2: arg1 >= 0,
                'arg1 must be greater than or equal to 0')
        @precondition(lambda arg1, arg2: arg2 >= 0,
                'arg2 must be greater than or equal to 0')
        def add(arg1, arg2):
            return arg1 + arg2
        self.assertEqual(add(100, 200), 300)
        with self.assertRaises(AssertionError) as ae:
            add(100, -200)
        self.assertEqual(ae.exception.args[0],
                'arg2 must be greater than or equal to 0')
                
    def test_binary_function_with_default_args_precondition(self):
        @precondition(lambda arg1, arg2=0: arg1 >= 0 and arg2 >= 0,
                'both arguments must be greater than or equal to 0')
        def add(arg1, arg2=0):
            return arg1 + arg2
        self.assertEqual(add(100, 200), 300)
        self.assertEqual(add(100), 100)
        with self.assertRaises(AssertionError) as ae:
            add(100, -200)
        self.assertEqual(ae.exception.args[0],
                'both arguments must be greater than or equal to 0')
                
    def test_method_precondition(self):
        class Adder(object):
            @precondition(lambda self, arg: arg >= 0,
                    'arg must be greater than or equal to 0')
            def plus_one(self, arg):
                return arg + 1
        adder = Adder()
        self.assertEqual(adder.plus_one(1), 2)
        with self.assertRaises(AssertionError) as ae:
            adder.plus_one(-1)
        self.assertEqual(ae.exception.args[0],
                'arg must be greater than or equal to 0')
        
    def test_function_postcondition(self):
        @postcondition(lambda result: result >= 0,
                'result must be greater than or equal to 0')
        def plus_one(arg):
            return arg + 1
        self.assertEqual(plus_one(1), 2)
        self.assertEqual(plus_one(-1), 0)
        with self.assertRaises(AssertionError) as ae:
            plus_one(-2)
        self.assertEqual(ae.exception.args[0],
                'result must be greater than or equal to 0')
            
    def test_function_postcondition_level_too_low(self):
        @postcondition(lambda result: result >= 0,
                'result must be greater than or equal to 0', level=0)
        def plus_one(arg):
            return arg + 1
        self.assertEqual(plus_one(1), 2)
        self.assertEqual(plus_one(-1), 0)
        # Even though the postcondition is violated, its level is less than
        # tsa_settings.MIN_POSTCONDITION_LEVEL, so it is not checked:
        self.assertEqual(plus_one(-2), -1)
            
    def test_method_postcondition(self):
        class Adder(object):
            @postcondition(lambda result: result >= 0,
                    'result must be greater than or equal to 0')
            def plus_one(self, arg):
                return arg + 1
        adder = Adder()
        self.assertEqual(adder.plus_one(1), 2)
        self.assertEqual(adder.plus_one(-1), 0)
        with self.assertRaises(AssertionError) as ae:
            adder.plus_one(-2)
        self.assertEqual(ae.exception.args[0],
                'result must be greater than or equal to 0')
            
    def test_method_pre_and_postcondition_1_order_1(self):
        # Preconditions, then postcondition
        class Subtractor(object):
            @precondition(lambda self, arg1, arg2: arg1 >= 0,
                    'arg1 must be greater than or equal to 0')
            @precondition(lambda self, arg1, arg2: arg2 >= 0,
                    'arg2 must be greater than or equal to 0')
            @postcondition(lambda result: result >= 0,
                    'result must be greater than or equal to 0')
            def subtract(self, arg1, arg2):
                return arg1 - arg2
        subtractor = Subtractor()
        self.assertEqual(subtractor.subtract(300, 200), 100)
        with self.assertRaises(AssertionError) as ae:
            subtractor.subtract(-300, 200)
        self.assertEqual(ae.exception.args[0],
                'arg1 must be greater than or equal to 0')
        with self.assertRaises(AssertionError) as ae:
            subtractor.subtract(300, -200)
        self.assertEqual(ae.exception.args[0],
                'arg2 must be greater than or equal to 0')
        with self.assertRaises(AssertionError) as ae:
            subtractor.subtract(-300, -200)
        self.assertEqual(ae.exception.args[0],
                'arg1 must be greater than or equal to 0')
        with self.assertRaises(AssertionError) as ae:
            subtractor.subtract(200, 300)
        self.assertEqual(ae.exception.args[0],
                'result must be greater than or equal to 0')
        
    def test_method_pre_and_postcondition_1_order_2(self):
        # Putting the postcondition before the preconditions makes no observable
        # difference
        class Subtractor(object):
            @postcondition(lambda result: result >= 0,
                    'result must be greater than or equal to 0')
            @precondition(lambda self, arg1, arg2: arg1 >= 0,
                    'arg1 must be greater than or equal to 0')
            @precondition(lambda self, arg1, arg2: arg2 >= 0,
                    'arg2 must be greater than or equal to 0')
            def subtract(self, arg1, arg2):
                return arg1 - arg2
        subtractor = Subtractor()
        self.assertEqual(subtractor.subtract(300, 200), 100)
        with self.assertRaises(AssertionError) as ae:
            subtractor.subtract(-300, 200)
        self.assertEqual(ae.exception.args[0],
                'arg1 must be greater than or equal to 0')
        with self.assertRaises(AssertionError) as ae:
            subtractor.subtract(300, -200)
        self.assertEqual(ae.exception.args[0],
                'arg2 must be greater than or equal to 0')
        with self.assertRaises(AssertionError) as ae:
            subtractor.subtract(-300, -200)
        self.assertEqual(ae.exception.args[0],
                'arg1 must be greater than or equal to 0')
        with self.assertRaises(AssertionError) as ae:
            subtractor.subtract(200, 300)
        self.assertEqual(ae.exception.args[0],
                'result must be greater than or equal to 0')

    def test_method_pre_and_postcondition_1_order_3(self):
        # Reordering the preconditions makes an observable difference
        class Subtractor(object):
            @precondition(lambda self, arg1, arg2: arg2 >= 0,
                    'arg2 must be greater than or equal to 0')
            @precondition(lambda self, arg1, arg2: arg1 >= 0,
                    'arg1 must be greater than or equal to 0')
            @postcondition(lambda result: result >= 0,
                    'result must be greater than or equal to 0')
            def subtract(self, arg1, arg2):
                return arg1 - arg2
        subtractor = Subtractor()
        with self.assertRaises(AssertionError) as ae:
            subtractor.subtract(-300, -200)
        self.assertEqual(ae.exception.args[0],
                'arg2 must be greater than or equal to 0')
        
if __name__ == '__main__':
    unittest.main()
