import io

import thalesians.tsa.checks as checks

def enquote(s, quote='"', escape=True):
    s = str(s)
    if escape: s = str(s).replace('\\', "\\\\").replace(quote, '\\' + quote)
    return quote + s + quote

class ToStringHelper(object):
    def __init__(self, typ=None):
        self.set_type(typ)
        self._properties = []
        self._str = None
        
    def set_type(self, typ=None):
        if typ is not None:
            if not checks.is_type(typ): typ = type(typ)
            typ = typ.__name__
        self._type_name = typ
        return self
        
    def add(self, name, value):
        self._properties.append((name, value))
        self._str = None
        return self
    
    def add_all_properties(self, o, ignore_dunders=True):
        if hasattr(o, '__dict__'):
            for prop, value in vars(o).items():
                if ignore_dunders and prop.startswith('__'): continue
                self.add(prop, value)
        return self
    
    def _should_enquote(self, o):
        return checks.is_string(o)
    
    def to_string(self):
        if self._str is None:
            s = io.StringIO()
            if self._type_name is not None: s.write(self._type_name)
            s.write('(')
            for i, p in enumerate(self._properties):
                if i > 0: s.write(', ')
                s.write(p[0])
                s.write('=')
                v = p[1]
                if self._should_enquote(v): s.write(enquote(v))
                else: s.write(str(v))
            s.write(')')
            self._str = s.getvalue()
        return self._str
                
    def __str__(self):
        return self.to_string()
    