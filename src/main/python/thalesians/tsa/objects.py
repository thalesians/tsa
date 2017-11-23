from thalesians.tsa.strings import ToStringHelper

class Named(object):
    def __init__(self, name=None):
        if name is None: name = type(self).__name__ + '_' + str(id(self))
        self._name = str(name)
        self._to_string_helper_Named = None
        self._str_Named = None
    
    @property
    def name(self):
        return self._name
    
    def to_string_helper(self):
        if self._to_string_helper_Named is None:
            self._to_string_helper_Named = ToStringHelper(self).add('name', self._name)
        return self._to_string_helper_Named
    
    def __str__(self):
        if self._str_Named is None: self._str_Named = self.to_string_helper().to_string()
        return self._str_Named
        
    def __repr__(self):
        return str(self)
