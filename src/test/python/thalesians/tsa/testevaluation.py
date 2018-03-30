import math
import time
import unittest

import thalesians.tsa.evaluation as evaluation

def pickleable_fact(x):
    time.sleep(1)
    return math.factorial(x)

class TestEvaluation(unittest.TestCase):
    def test_current_thread_evaluator(self):
        def fact(x):
            time.sleep(1)
            return math.factorial(x)

        current_thread_evaluator = evaluation.CurrentThreadEvaluator()
        status = evaluation.evaluate(fact, args=[10], evaluator=current_thread_evaluator)
        
        self.assertTrue(status.ready)
        self.assertEqual(status.result.result, 3628800)
        self.assertIsNone(status.result.exception)
        
    def test_current_thread_evaluator_callbacks(self):
        def fact(x):
            time.sleep(1)
            return math.factorial(x)

        current_thread_evaluator = evaluation.CurrentThreadEvaluator()
        status = evaluation.evaluate(fact, args=[10], evaluator=current_thread_evaluator)        

        self.assertTrue(status.ready)
        
        callback1_called = False
        def callback1(status):
            nonlocal callback1_called
            callback1_called = True
            
        callback2_called = False
        def callback2(status):
            nonlocal callback2_called
            callback2_called = True
            
        status.add_callback(callback1)
        status.add_callback(callback2)
        
        self.assertTrue(callback1_called)
        self.assertTrue(callback2_called)
        
        self.assertTrue(status.ready)
        self.assertEqual(status.result.result, 3628800)
        self.assertIsNone(status.result.exception)

    def test_ipyparallel_evaluator(self):
        def fact(x):
            time.sleep(1)
            return math.factorial(x)

        ipp_evaluator = evaluation.IPyParallelEvaluator()
        status = evaluation.evaluate(fact, args=[10], evaluator=ipp_evaluator)        
        
        self.assertFalse(status.ready)
        
        time.sleep(2)
        
        self.assertTrue(status.ready)
        self.assertEqual(status.result.result, 3628800)
        self.assertIsNone(status.result.exception)
        
    def test_ipyparallel_evaluator_callback(self):
        def fact(x):
            time.sleep(1)
            return math.factorial(x)

        ipp_evaluator = evaluation.IPyParallelEvaluator()
        status = evaluation.evaluate(fact, args=[10], evaluator=ipp_evaluator)        
        
        self.assertFalse(status.ready)
        
        callback1_called = False
        def callback1(status):
            nonlocal callback1_called
            callback1_called = True
            
        callback2_called = False
        def callback2(status):
            nonlocal callback2_called
            callback2_called = True
            
        status.add_callback(callback1)
        status.add_callback(callback2)

        self.assertFalse(callback1_called)
        self.assertFalse(callback2_called)
        
        time.sleep(2)
        
        self.assertTrue(callback1_called)
        self.assertTrue(callback2_called)
        
        self.assertTrue(status.ready)
        self.assertEqual(status.result.result, 3628800)
        self.assertIsNone(status.result.exception)
        
    def test_multiprocessing_evaluator(self):
        mp_evaluator = evaluation.MultiprocessingEvaluator()
        status = evaluation.evaluate(pickleable_fact, args=[10], evaluator=mp_evaluator)
                
        self.assertFalse(status.ready)
        
        time.sleep(2)
        
        self.assertTrue(status.ready)
        self.assertEqual(status.result.result, 3628800)
        self.assertIsNone(status.result.exception)

    def test_multiprocessing_evaluator_callback(self):
        mp_evaluator = evaluation.MultiprocessingEvaluator()
        status = evaluation.evaluate(pickleable_fact, args=[10], evaluator=mp_evaluator)
                
        self.assertFalse(status.ready)
        
        callback_called = False
        def callback(status):
            nonlocal callback_called
            callback_called = True
            
        callback1_called = False
        def callback1(status):
            nonlocal callback1_called
            callback1_called = True
            
        callback2_called = False
        def callback2(status):
            nonlocal callback2_called
            callback2_called = True
            
        status.add_callback(callback1)
        status.add_callback(callback2)

        self.assertFalse(callback1_called)
        self.assertFalse(callback2_called)
        
        time.sleep(2)
        
        self.assertTrue(callback1_called)
        self.assertTrue(callback2_called)
        
        self.assertTrue(status.ready)
        self.assertEqual(status.result.result, 3628800)
        self.assertIsNone(status.result.exception)

if __name__ == '__main__':
    unittest.main()
