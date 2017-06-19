import unittest

from thalesians.tsa.conditions import precondition, postcondition

class TestConditions(unittest.TestCase):
    def testunaryfunctionprecondition(self):
        @precondition(lambda arg: arg >= 0,
                'arg must be greater than or equal to 0')
        def plusone(arg):
            return arg + 1
        self.assertEqual(plusone(1), 2)        
        with self.assertRaises(AssertionError) as ae:
            plusone(-1)
        self.assertEqual(ae.exception.args[0],
                'arg must be greater than or equal to 0')
        
    def testunaryfunctionpreconditionleveltoolow(self):
        @precondition(lambda arg: arg >= 0,
                'arg must be greater than or equal to 0',
                level=0)
        def plusone(arg):
            return arg + 1
        self.assertEqual(plusone(1), 2)
        # Even though the precondition is violated, its level is less than
        # settings.MIN_PRECONDITION_LEVEL, so it is not checked:
        self.assertEqual(plusone(-1), 0)
        
    def testbinaryfunctionprecondition(self):
        @precondition(lambda arg1, arg2: arg1 >= 0 and arg2 >= 0,
                'both arguments must be greater than or equal to 0')
        def add(arg1, arg2):
            return arg1 + arg2
        self.assertEqual(add(100, 200), 300)
        with self.assertRaises(AssertionError) as ae:
            add(100, -200)
        self.assertEqual(ae.exception.args[0],
                'both arguments must be greater than or equal to 0')
             
    def testbinaryfunctionpreconditioncomposition(self):
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
                
    def testbinaryfunctionwithdefaultargsprecondition(self):
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
                
    def testmethodprecondition(self):
        class Adder(object):
            @precondition(lambda self, arg: arg >= 0,
                    'arg must be greater than or equal to 0')
            def plusone(self, arg):
                return arg + 1
        adder = Adder()
        self.assertEqual(adder.plusone(1), 2)
        with self.assertRaises(AssertionError) as ae:
            adder.plusone(-1)
        self.assertEqual(ae.exception.args[0],
                'arg must be greater than or equal to 0')
        
    def testfunctionpostcondition(self):
        @postcondition(lambda result: result >= 0,
                'result must be greater than or equal to 0')
        def plusone(arg):
            return arg + 1
        self.assertEqual(plusone(1), 2)
        self.assertEqual(plusone(-1), 0)
        with self.assertRaises(AssertionError) as ae:
            plusone(-2)
        self.assertEqual(ae.exception.args[0],
                'result must be greater than or equal to 0')
            
    def testfunctionpostconditionleveltoolow(self):
        @postcondition(lambda result: result >= 0,
                'result must be greater than or equal to 0', level=0)
        def plusone(arg):
            return arg + 1
        self.assertEqual(plusone(1), 2)
        self.assertEqual(plusone(-1), 0)
        # Even though the postcondition is violated, its level is less than
        # settings.MIN_POSTCONDITION_LEVEL, so it is not checked:
        self.assertEqual(plusone(-2), -1)
            
    def testmethodpostcondition(self):
        class Adder(object):
            @postcondition(lambda result: result >= 0,
                    'result must be greater than or equal to 0')
            def plusone(self, arg):
                return arg + 1
        adder = Adder()
        self.assertEqual(adder.plusone(1), 2)
        self.assertEqual(adder.plusone(-1), 0)
        with self.assertRaises(AssertionError) as ae:
            adder.plusone(-2)
        self.assertEqual(ae.exception.args[0],
                'result must be greater than or equal to 0')
            
    def testmethodpreandpostcondition1order1(self):
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
        
    def testmethodpreandpostcondition1order2(self):
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

    def testmethodpreandpostcondition1order3(self):
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
