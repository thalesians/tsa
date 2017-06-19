import _pickle
import datetime
import unittest

import thalesians.tsa.q as kdb

class TestDataTypes(unittest.TestCase):
    def setUp(self):
        self.conn = kdb.q('localhost', 41822)

    def testInteger(self):
        self.conn.k('{[x]test::x}', (15,))
        self.assertEqual(self.conn.k('test'), 15)
        self.conn.k('test:2')
        self.assertEqual(self.conn.k('test'), 2)

    def testFloat(self):
        self.conn.k('{[x]test::x}', (15.,))
        self.assertEqual(self.conn.k('test'), 15.)
        self.conn.k('test:2f')
        self.assertEqual(self.conn.k('test'), 2.0)

    def testMonth(self):
        self.conn.k('{[x]test::x}', (kdb.Month(1),))
        self.assertEqual(self.conn.k('test').i, kdb.Month(1).i)
        self.conn.k('test:2008.09m')
        self.assertEqual(str(self.conn.k('test')), '2008-09')

    def testSecond(self):
        self.conn.k('{[x]test::x}', (kdb.Second(61),))
        self.assertEqual(self.conn.k('test').i, kdb.Second(61).i)
        self.conn.k('test:00:01:01')
        self.assertEqual(str(self.conn.k('test')), '00:01:01')
        self.assertEqual(self.conn.k('test'), kdb.Second(61))

    def testMinute(self):
        self.conn.k('{[x]test::x}', (kdb.Minute(61),))
        self.assertEqual(self.conn.k('test').i, kdb.Minute(61).i)
        self.conn.k('test:01:01')
        self.assertEqual(str(self.conn.k('test')), '01:01')
        self.assertEqual(self.conn.k('test'), kdb.Minute(61))

    def testDate(self):
        d = datetime.date(2000,1,1)
        self.conn.k('{[x;y]test::y}', [0,d])
        self.assertEqual(self.conn.k('test'), d)
        self.conn.k('test:2008.09.09')
        self.assertEqual(str(self.conn.k('test')), '2008-09-09')
        self.conn.k('test:1908.09.09')
        self.assertEqual(str(self.conn.k('test')), '1908-09-09')
        self.assertEqual(self.conn.k('{x}',[datetime.date(2009,7,12)]), datetime.date(2009,7,12))

    def testDateTime(self):
        dt = datetime.datetime(2000,1,1,12,00)
        self.conn.k('{[x]test::x}', (dt,))
        self.assertEqual(self.conn.k('test'), dt)
        self.conn.k('{[x;y]test::y}', [0,dt])
        self.assertEqual(self.conn.k('test'), dt)
        self.conn.k('test:2008.09.09T01:01:01.001')
        self.assertEqual(str(self.conn.k('test')), '2008-09-09 01:01:01.001000')
        self.conn.k('test:1999.09.09T01:01:01.001')
        self.assertEqual(str(self.conn.k('test')), '1999-09-09 01:01:01.001000')
        self.conn.k('test:1908.09.13T01:01:01.005')
        self.assertEqual(str(self.conn.k('test')), '1908-09-13 01:01:01.005000')


    def testTime(self):
        t = datetime.datetime(2000,1,1,12,00).time()
        self.conn.k('{[x]test::x}', (t,))
        self.assertEqual(self.conn.k('test'), t)
        self.conn.k('test:01:01:01.001')
        self.assertEqual(str(self.conn.k('test')), '01:01:01.001000')
        self.conn.k('test:15:30:15.001')
        self.assertEqual(str(self.conn.k('test')), '15:30:15.001000')

    def testString(self):
        string = 'teststring'
        self.conn.k('{[x]test::x}', (string,))
        self.assertEqual(self.conn.k('test'), string)
        self.conn.k('test:`$"'+string+'"')
        self.assertEqual(str(self.conn.k('test')), string)

    def testChar(self):
        string = ['t','e']
        self.conn.k('{[x]test::x}', (string,))
        self.assertEqual(self.conn.k('test'), string)
        self.conn.k('test:"'+"".join(string)+'"')
        self.assertEqual(self.conn.k('test'), string)
        string = 't'
        self.conn.k('{[x]test::x}', (string,))
        self.assertEqual(self.conn.k('test'), string)
        self.conn.k('test:"'+"".join(string)+'"')
        self.assertEqual(self.conn.k('test'), string)

    def testBlob(self):
        dict = {'hello': 'world'}
        self.conn.k('test:`$"'+cPickle.dumps(dict)+'"')
        self.assertEqual(cPickle.loads(self.conn.k('test')), dict)

    def testDict(self):
        self.conn.k('test:(enlist `key)!(enlist `value)')
        self.conn.k('test')
        x = ['key',]
        y = ['value',]
        dict = kdb.Dict(x, y)
        self.assertEqual(self.conn.k('test'), dict)
        self.conn.k('{[x]test::x}', (dict,))
        self.conn.k('test')
        self.assertEqual(self.conn.k('test'), dict)

    def testFlip(self):
        self.conn.k('test:([]a: 1 2 3;b:`foo`bar`baz)')
        self.conn.k('test')
        x = ['a','b']
        y = [[1, 2, 3],['foo','bar','baz']]
        flip = kdb.Flip(kdb.Dict(x,y))
        self.assertEqual(self.conn.k('test'), flip)
        self.conn.k('{[x]test::x}',(flip,))
        self.conn.k('test')
        self.assertEqual(self.conn.k('test'), flip)
        t = self.conn.k('select b, a from test')
        x = ['b','a']
        y = [['foo','bar','baz'],[1, 2, 3]]
        flip = kdb.Flip(kdb.Dict(x,y))
        self.assertEqual(t.x, flip.x)
        
    def testKeyedTables(self):
        self.conn.k('test:([a: `a`b`c]b:`foo`bar`baz)')
        kdb.td(self.conn.k('test'))
        self.conn.k('test:([a: `a`b`c;c: 1 2 3]b:`foo`bar`baz;d: `here`I`come)')
        self.assertEqual(str(self.conn.k('test')), """[a,1]foo,here
[b,2]bar,I
[c,3]baz,come
""")

    def tearDown(self):
        self.conn.close()

if __name__ == '__main__':
    unittest.main()
