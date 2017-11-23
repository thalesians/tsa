import io

class Interval:
    def __init__(self, left, right, left_closed=False, right_closed=False):
        self._left = left
        self._right = right
        self._left_closed = left_closed
        self._right_closed = right_closed
        self._str_Interval = None
        
    @property
    def left(self):
        return self._left
        
    @property
    def right(self):
        return self._right
    
    @property
    def left_closed(self):
        return self._left_closed
    
    @property
    def right_closed(self):
        return self._right_closed
        
    def replace_left(self, new_left, new_left_closed=None):
        if new_left_closed is None: new_left_closed = self._left_closed
        return Interval(new_left, self._right, new_left_closed, self._right_closed)
    
    def replace_right(self, new_right, new_right_closed=None):
        if new_right_closed is None: new_right_closed = self._right_closed
        return Interval(self._left, new_right, self._left_closed, new_right_closed)
    
    def __eq__(self, other):
        return self._left == other.left and self._right == other.right and \
            self._left_closed == other.left_closed and self._right_closed == other.right_closed
    
    def __str__(self):
        if self._str_Interval is None:
            s = io.StringIO()
            s.write('[' if self._left_closed else '(')
            s.write(str(self._left))
            s.write(', ')
            s.write(str(self._right))
            s.write(']' if self._right_closed else ')')
            self._str_Interval = s.getvalue()
        return self._str_Interval
                
    def __repr__(self):
        return str(self)
