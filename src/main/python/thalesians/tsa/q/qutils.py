import copy
import datetime as dt
import io
import sys

import numpy as np

def format_q_time(thing):
    if isinstance(thing, dt.datetime) or isinstance(thing, dt.time):
        hour = thing.hour
        minute = thing.minute
        second = thing.second
        microsecond = thing.microsecond
    else:
        raise ValueError('Cannot create a q time string representation of "%s"' % repr(thing))
    millisecond = microsecond / 1000
    return '%02d:%02d:%02d.%03d' % (hour, minute, second, millisecond)

def format_q_date(thing):
    if isinstance(thing, dt.datetime) or isinstance(thing, dt.date):
        year = thing.year
        month = thing.month
        day = thing.day
    else:
        raise ValueError('Cannot create a q date string representation of "%s"' % repr(thing))
    return '%04d.%02d.%02d' % (year, month, day)

def format_q_datetime(thing1, thing2=None):
    if thing2 is not None:
        if isinstance(thing1, dt.date) and isinstance(thing2, dt.time):
            year = thing1.year
            month = thing1.month
            day = thing1.day
            hour = thing2.hour
            minute = thing2.minute
            second = thing2.second
            microsecond = thing2.microsecond
        elif isinstance(thing1, dt.time) and isinstance(thing2, dt.date):
            year = thing2.year
            month = thing2.month
            day = thing2.day
            hour = thing1.hour
            minute = thing1.minute
            second = thing1.second
            microsecond = thing1.microsecond
        else:
            raise ValueError('Cannot create a q datetime string representation of "%s" and "%s"' % (repr(thing1), repr(thing2)))
    else:
        if isinstance(thing1, dt.datetime):
            year = thing1.year
            month = thing1.month
            day = thing1.day
            hour = thing1.hour
            minute = thing1.minute
            second = thing1.second
            microsecond = thing1.microsecond
        elif isinstance(thing1, dt.date):
            year = thing1.year
            month = thing1.month
            day = thing1.day
            hour = 0
            minute = 0
            second = 0
            microsecond = 0
        else:
            raise ValueError('Cannot create a q datetime string representation of "%s"' % repr(thing1))
    millisecond = microsecond / 1000
    return '%04d.%02d.%02dT%02d:%02d:%02d.%03d' % (year, month, day, hour, minute, second, millisecond)

class QType(object):
    def __init__(self, aggr, name, symbol, char, num, null_value, size, maker):
        self.__aggr = aggr
        self.__name = name
        self.__symbol = symbol
        self.__char = char
        self.__num = num
        self.__null_value = null_value
        self.__size = size
        self.__maker = maker

    def __is_aggr(self):
        return self.__aggr

    aggr = property(fget=__is_aggr)

    def __get_name(self):
        return self.__name

    name = property(fget=__get_name)

    def __get_symbol(self):
        return self.__symbol

    symbol = property(fget=__get_symbol)

    def __get_char(self):
        return self.__char

    char = property(fget=__get_char)

    def __get_num(self):
        return self.__num

    num = property(fget=__get_num)

    def __get_null_value(self):
        return self.__null_value

    null_value = property(fget=__get_null_value)

    def __get_size(self):
        return self.__size

    size = property(fget=__get_size)

    def __get_maker(self):
        return self.__maker

    maker = property(fget=__get_maker)

    def __str__(self):
        return self.__name

    def __repr__(self):
        return self.__name

    def __eq__(self, other):
        return isinstance(other, QType) and self.num == other.num

    def __hash__(self):
        return hash(self.__name)

class QValue(object):
    def __init__(self, value, q_type):
        self.__value = copy.copy(value)
        self.__q_type = q_type

    def __get_value(self):
        return self.__value

    value = property(fget=__get_value)

    def __get_q_type(self):
        return self.__q_type

    q_type = property(fget=__get_q_type)

    def to_literal(self):
        raise NotImplementedError('Pure virtual method')

    def __str__(self):
        return self.to_literal()

    def __repr__(self):
        return self.to_literal()

class QBooleanValue(QValue):
    def __init__(self, value=None):
        super(QBooleanValue, self).__init__(value, QTypes.BOOLEAN)

    def to_literal(self):
        if self.value is None:
            return self.q_type.null_value
        return '1b' if self.value else '0b'

def make_q_boolean_value(value=None):
    return QBooleanValue(value)

class QCharValue(QValue):
    def __init__(self, value=None):
        super(QCharValue, self).__init__(value, QTypes.CHAR)

    def to_literal(self, QValue):
        if self.value is None:
            return self.q_type.null_value
        return '"%s"' % str(self.value)

def make_q_char_value(value=None):
    return QCharValue(value)

def to_q_string_literal(s):
    s = s.replace('\\', '\\\\')
    s = s.replace('"', '\\"')
    s = s.replace('\n', '\\n')
    return '"%s"' % s

def to_q_symbol_literal(s):
    return '(`$%s)' % to_q_string_literal(s)

class QSymbolValue(QValue):
    def __init__(self, value=None):
        super(QSymbolValue, self).__init__(value, QTypes.SYMBOL)

    def to_literal(self):
        if self.value is None:
            return self.q_type.null_value
        return to_q_symbol_literal(str(self.value))

def make_q_symbol_value(value=None):
    return QSymbolValue(value)

class QStringValue(QValue):
    def __init__(self, value=None):
        super(QStringValue, self).__init__(value, QTypes.CHAR_LIST)

    def to_literal(self):
        if self.value is None:
            return self.q_type.null_value
        return to_q_string_literal(str(self.value))

def make_q_string_value(value=None):
    return QStringValue(value)

class QDateTimeValue(QValue):
    def __init__(self, value=None):
        if isinstance(value, dt.datetime):
            # round down the microseconds
            milliseconds = int(value.microsecond / 1000)
            timeTuple = value.timetuple()
            value = (timeTuple[0], timeTuple[1], timeTuple[2], timeTuple[3], \
                    timeTuple[4], timeTuple[5], milliseconds)
        super(QDateTimeValue, self).__init__(value, QTypes.DATETIME)

    def to_literal(self):
        if self.value is None:
            return self.q_type.null_value
        return '%04d.%02d.%02dT%02d:%02d:%02d.%03d' % self.value[0:7]

def make_q_datetime_value(value=None):
    return QDateTimeValue(value)

class QDateValue(QValue):
    def __init__(self, value=None):
        if isinstance(value, dt.date):
            value = value.timetuple()[0:3]
        super(QDateValue, self).__init__(value, QTypes.DATE)

    def to_literal(self):
        if self.value is None:
            return self.q_type.null_value
        return '%04d.%02d.%02d' % self.value[0:3]

def make_q_date_value(value=None):
    return QDateValue(value)

class QTimeValue(QValue):
    def __init__(self, value=None):
        if isinstance(value, dt.time):
            # round down the microseconds
            milliseconds = int(value.microsecond / 1000)
            value = (value.hour, value.minute, value.second, milliseconds)
        super(QTimeValue, self).__init__(value, QTypes.TIME)

    def to_literal(self):
        if self.value is None:
            return self.q_type.null_value
        return '%02d:%02d:%02d.%03d' % self.value[0:4]

def make_q_time_value(value=None):
    return QTimeValue(value)

class QNumericValue(QValue):
    def __init__(self, value, q_type):
        super(QNumericValue, self).__init__(value, q_type)

    def to_literal(self):
        if self.value is None or np.isnan(self.value):
            return self.q_type.null_value
        return '%s%s' % (str(self.value), self.q_type.char)

class QShortValue(QNumericValue):
    def __init__(self, value=None):
        super(QShortValue, self).__init__(value, QTypes.SHORT)

    def to_literal(self):
        if self.value is None:
            return self.q_type.null_value
        return '%s%s' % (str(int(self.value)), self.q_type.char)

def make_q_short_value(value=None):
    return QShortValue(value)

class QIntValue(QNumericValue):
    def __init__(self, value=None):
        super(QIntValue, self).__init__(value, QTypes.INT)

    def to_literal(self):
        if self.value is None:
            return self.q_type.null_value
        return '%s%s' % (str(int(self.value)), self.q_type.char)

def make_q_int_value(value=None):
    return QIntValue(value)

class QLongValue(QNumericValue):
    def __init__(self, value=None):
        super(QLongValue, self).__init__(value, QTypes.LONG)

    def to_literal(self):
        if self.value is None:
            return self.q_type.null_value
        if sys.version_info >= (3, 0):
            result = '%s%s' % (str(int(self.value)), self.q_type.char)
        else:
            result = '%s%s' % (str(long(self.value)), self.q_type.char)
        return result

def make_q_long_value(value=None):
    return QLongValue(value)

class QRealValue(QNumericValue):
    def __init__(self, value=None):
        super(QRealValue, self).__init__(value, QTypes.REAL)

def make_q_real_value(value=None):
    return QRealValue(value)

class QFloatValue(QNumericValue):
    def __init__(self, value=None):
        super(QFloatValue, self).__init__(value, QTypes.FLOAT)

def make_q_float_value(value=None):
    return QFloatValue(value)

class QUntypedListValue(QValue):
    def __init__(self, value):
        if not isinstance(value, QValue):
            if not hasattr(value, '__iter__'):
                raise ValueError('Cannot construct a q untyped list value from a Python object of type %s, which does not seem to be iterable' % str(type(value)))
            value = [make_q_value(element) for element in value]
        super(QUntypedListValue, self).__init__(value, QTypes.UNTYPED_LIST)

    def to_literal(self):
        literal = io.StringIO()
        if len(self.value) == 1:
            literal.write('enlist')
        literal.write('(')
        for index, element in enumerate(self.value):
            if index > 0:
                literal.write(';')
            if hasattr(element, 'to_literal'):
                literal.write(element.to_literal())
            else:
                literal.write(str(element))
        literal.write(')')
        return literal.getvalue()

def make_q_untyped_list_value(value):
    return QUntypedListValue(value)

class QIdentifierValue(QValue):
    def __init__(self, value):
        super(QIdentifierValue, self).__init__(value, QTypes.IDENTIFIER)

    def to_literal(self):
        return self.value

def make_q_identifier_value(value):
    return QIdentifierValue(value)

def infer_q_type(value, prefer_strings_to_symbols=False):
    if isinstance(value, QValue):
        return value.q_type
    elif isinstance(value, bool):
        return QTypes.BOOLEAN
    elif isinstance(value, int):
        return QTypes.INT if sys.version_info < (3, 0) else QTypes.LONG
    elif sys.version_info < (3, 0) and isinstance(value, long):
        return QTypes.LONG
    elif isinstance(value, float):
        return QTypes.FLOAT
    elif isinstance(value, str) or (sys.version_info < (3, 0) and isinstance(value, unicode)):
        return QTypes.CHAR_LIST if prefer_strings_to_symbols else QTypes.SYMBOL
    elif isinstance(value, dt.datetime):
        return QTypes.DATETIME
    elif isinstance(value, dt.date):
        return QTypes.DATE
    elif isinstance(value, dt.time):
        return QTypes.TIME
    elif hasattr(value, '__iter__'):
        return QTypes.UNTYPED_LIST
    else:
        raise ValueError('Unable to infer the q type corresponding to the Python type %s' % str(type(value)))

def make_q_value(value, q_type=None, prefer_strings_to_symbols=False):
    if isinstance(value, QValue):
        return value
    else:
        q_type = infer_q_type(value, prefer_strings_to_symbols) if q_type is None else q_type
        maker = q_type.maker
        if maker is None:
            raise ValueError('Unable to make the q type %s from Python type %s' % (q_type.name, str(type(value))))
        return maker(value)

class QTypes(object):
    # This isn't really a type
    IDENTIFIER    = QType( False, None      , None       , None, None, None   , None, None                      )

    UNTYPED_LIST  = QType( True , None      , None       , None, 0   , None   , None, make_q_untyped_list_value )

    # Primitive types
    BOOLEAN       = QType( False, 'boolean' , '`boolean' , 'b' , -1  , '0b'   , 1   , make_q_boolean_value      )
    BYTE          = QType( False, 'byte'    , '`byte'    , 'x' , -4  , '0x00' , 1   , None                      )
    SHORT         = QType( False, 'short'   , '`short'   , 'h' , -5  , '0Nh'  , 2   , make_q_short_value        )
    INT           = QType( False, 'int'     , '`int'     , 'i' , -6  , '0N'   , 4   , make_q_int_value          )
    LONG          = QType( False, 'long'    , '`long'    , 'j' , -7  , '0Nj'  , 8   , make_q_long_value         )
    REAL          = QType( False, 'real'    , '`real'    , 'e' , -8  , '0Ne'  , 4   , make_q_real_value         )
    FLOAT         = QType( False, 'float'   , '`float'   , 'f' , -9  , '0n'   , 8   , make_q_float_value        )
    CHAR          = QType( False, 'char'    , '`char'    , 'c' , -10 , '""'   , 1   , make_q_char_value         )
    SYMBOL        = QType( False, 'symbol'  , '`'        , 's' , -11 , '`'    , None, make_q_symbol_value       )
    MONTH         = QType( False, 'month'   , '`month'   , 'm' , -13 , '0Nm'  , 4   , None                      )
    DATE          = QType( False, 'date'    , '`date'    , 'd' , -14 , '0Nd'  , 4   , make_q_date_value         )
    DATETIME      = QType( False, 'datetime', '`datetime', 'z' , -15 , '0Nz'  , 4   , make_q_datetime_value     )
    MINUTE        = QType( False, 'minute'  , '`minute'  , 'u' , -17 , '0Nu'  , 4   , None                      )
    SECOND        = QType( False, 'second'  , '`second'  , 'v' , -18 , '0Nv'  , 4   , None                      )
    TIME          = QType( False, 'time'    , '`time'    , 't' , -19 , '0Nt'  , 4   , make_q_time_value         )

    # Typed lists
    BOOLEAN_LIST  = QType( True , 'boolean' , '`boolean' , 'b' , 1   , '0b'   , 1   , None                      )
    BYTE_LIST     = QType( True , 'byte'    , '`byte'    , 'x' , 4   , '0x00' , 1   , None                      )
    SHORT_LIST    = QType( True , 'short'   , '`short'   , 'h' , 5   , '0Nh'  , 2   , None                      )
    INT_LIST      = QType( True , 'int'     , '`int'     , 'i' , 6   , '0N'   , 4   , None                      )
    LONG_LIST     = QType( True , 'long'    , '`long'    , 'j' , 7   , '0Nj'  , 8   , None                      )
    REAL_LIST     = QType( True , 'real'    , '`real'    , 'e' , 8   , '0Ne'  , 4   , None                      )
    FLOAT_LIST    = QType( True , 'float'   , '`float'   , 'f' , 9   , '0n'   , 8   , None                      )
    CHAR_LIST     = QType( True , 'char'    , '`char'    , 'c' , 10  , '""'   , 1   , make_q_string_value       )
    SYMBOL_LIST   = QType( True , 'symbol'  , '`'        , 's' , 11  , '`'    , None, None                      )
    MONTH_LIST    = QType( True , 'month'   , '`month'   , 'm' , 13  , '0Nm'  , 4   , None                      )
    DATE_LIST     = QType( True , 'date'    , '`date'    , 'd' , 14  , '0Nd'  , 4   , None                      )
    DATETIME_LIST = QType( True , 'datetime', '`datetime', 'z' , 15  , '0Nz'  , 4   , None                      )
    MINUTE_LIST   = QType( True , 'minute'  , '`minute'  , 'u' , 17  , '0Nu'  , 4   , None                      )
    SECOND_LIST   = QType( True , 'second'  , '`second'  , 'v' , 18  , '0Nv'  , 4   , None                      )
    TIME_LIST     = QType( True , 'time'    , '`time'    , 't' , 19  , '0Nt'  , 4   , None                      )

class QCreateTableStatementBuilder(object):
    def __init__(self, overwrite=False):
        self.__table = None
        self.__columns = []
        self.__appended_non_key_columns = False
        self.__key_column_count = 0
        self.overwrite = overwrite

    def set_table(self, table):
        self.__table = table
        return self

    def append_column(self, name, q_type=None, key=False):
        assert not (key and self.__appended_non_key_columns), 'Cannot append a key column after non-key columns'
        self.__columns.append((name, q_type))
        if key:
            self.__key_column_count += 1
        return self

    def to_string(self):
        assert self.__table is not None, 'Table is not set'

        statement = io.StringIO()

        statement.write(self.__table)
        statement.write(':')

        if not self.overwrite:
            statement.write('$[')
            statement.write(to_q_symbol_literal(self.__table))
            statement.write(' in value["\\\\v"]; ')
            statement.write(self.__table)
            statement.write('; ')

        statement.write('([')
        for column_index in range(self.__key_column_count):
            column = self.__columns[column_index]
            statement.write(column[0])
            statement.write(':')
            if column[1] is not None and not column[1] == QTypes.CHAR_LIST:
                statement.write(column[1].symbol)
                statement.write('$')
            statement.write('()')
            if column_index < self.__key_column_count - 1:
                statement.write(';')
        statement.write('];')
        column_count = len(self.__columns)
        for column_index in range(self.__key_column_count, len(self.__columns)):
            column = self.__columns[column_index]
            statement.write(column[0])
            statement.write(':')
            if column[1] is not None and not column[1] == QTypes.CHAR_LIST:
                statement.write(column[1].symbol)
                statement.write('$')
            statement.write('()')
            if column_index < column_count - 1:
                statement.write(';')
        statement.write(')')

        if not self.overwrite:
            statement.write(']')

        return statement.getvalue()

    def __str__(self):
        return self.to_string()

    def __repr__(self):
        return self.to_string()

class QUpsertStatementBuilder(object):
    def __init__(self):
        self.__table = None
        self.__q_values = []

    def set_table(self, table):
        self.__table = table
        return self

    def append(self, q_value):
        self.__q_values.append(q_value)
        return self

    def to_string(self):
        assert self.__table is not None, 'Table is not set'

        statement = io.StringIO()

        statement.write('upsert[')
        statement.write(to_q_symbol_literal(self.__table))
        statement.write('](')
        for index, q_value in enumerate(self.__q_values):
            if isinstance(q_value, QValue):
                statement.write(q_value.to_literal())
            else:
                statement.write(q_value)
            if index < len(self.__q_values) - 1:
                statement.write(';')
        statement.write(')')

        return statement.getvalue()

class QBatchAppendStatementBuilder(object):
    def __init__(self, rows_per_batch=100):
        self.__table = None
        self.__rows_per_batch = rows_per_batch
        self.__rows = []

    def set_table(self, table):
        self.__table = table
        return self

    def start_new_row(self):
        self.__rows.append([])

    def append(self, q_value):
        assert len(self.__rows) > 0, 'No row has been started'
        self.__rows[-1].append(q_value)

    def to_list(self):
        assert self.__table is not None, 'Table is not set'

        batches = []

        i = 0
        while i < len(self.__rows):
            statement = io.StringIO()
            statement.write('.[')
            statement.write(to_q_symbol_literal(self.__table))
            statement.write(';();,;(')
            for j in range(self.__rows_per_batch):
                if i >= len(self.__rows): break
                statement.write('(')
                for index, q_value in enumerate(self.__rows[i]):
                    if isinstance(q_value, QValue):
                        statement.write(q_value.to_literal())
                    else:
                        statement.write(q_value)
                    if index < len(self.__rows[i]) - 1:
                        statement.write(';')
                statement.write(')')
                if j < self.__rows_per_batch - 1 and i < len(self.__rows) - 1:
                    statement.write(';')
                i += 1
            statement.write(')]')
            batches.append(statement.getvalue())

        return batches

class QExpression(object):
    def __init__(self, operator, lhs, rhs):
        self.operator = operator
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self):
        s = io.StringIO()
        s.write('(')
        s.write(self.operator)
        s.write(';')
        s.write(str(self.lhs))
        s.write(';')
        s.write(str(self.rhs))
        s.write(')')
        return s.getvalue()

class QExpressionFactory(object):
    def make_plus_expression(self, lhs, rhs):
        return QExpression('+', lhs, rhs)

class QConstraint(object):
    def __init__(self, relation, lhs, rhs):
        self.relation = relation
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self):
        s = io.StringIO()
        s.write('(')
        s.write(str(self.relation))
        s.write(';')
        s.write(str(self.lhs))
        s.write(';(')
        if not hasattr(self.rhs, '__iter__'):
            if isinstance(self.rhs, QValue) and self.rhs.q_type == QTypes.SYMBOL:
                s.write('enlist ')
            s.write(str(self.rhs))
        else:
            if len(self.rhs) == 1 and self.rhs[0].q_type == QTypes.SYMBOL:
                s.append('enlist ')
            rhsLen = len(self.rhs)
            for rhsIndex, rhsItem in enumerate(self.rhs):
                if rhsIndex > 0:
                    s.write(';')
                s.write(str(rhsItem))
        s.write('))')
        return s.getvalue()

class QConstraintFactory(object):
    def make_equal_constraint(self, lhs, rhs):
        return QConstraint('=', lhs, rhs)

    def make_not_equal_constraint(self, lhs, rhs):
        return QConstraint('<>', lhs, rhs)

    def make_less_than_constraint(self, lhs, rhs):
        return QConstraint('<', lhs, rhs)

    def make_greater_than_constraint(self, lhs, rhs):
        return QConstraint('>', lhs, rhs)

    def make_less_than_or_equal_constraint(self, lhs, rhs):
        return QConstraint('<=', lhs, rhs)

    def make_greater_than_or_equal_constraint(self, lhs, rhs):
        return QConstraint('>=', lhs, rhs)

    def make_like_constraint(self, lhs, rhs):
        return QConstraint('like', lhs, rhs)

    def make_in_constraint(self, lhs, rhs):
        return QConstraint('in', lhs, make_q_untyped_list_value((rhs,)))

    def make_within_constraint(self, lhs, rhs):
        return QConstraint('within', lhs, rhs)

class QSelectStatementBuilder(object):
    def __init__(self):
        self.__table = None
        self.__select_columns = []
        self.__by_phrase_columns = []
        self.__constraints = []

    def set_table(self, table):
        self.__table = table
        return self

    def append_select_column(self, value, name=None):
        if name is None:
            if isinstance(value, QValue) and value.q_type == QTypes.SYMBOL:
                name = value
            else:
                raise ValueError('Cannot deduce the name of the select column "%s"' % str(value))

        self.__select_columns.append((name, value))
        return self

    def append_constraint(self, constraint):
        self.__constraints.append(constraint)
        return self

    def append_by_phrase_column(self, value, name=None):
        if name is None:
            if isinstance(value, QValue) and value.q_type == QTypes.SYMBOL:
                name = value
            else:
                raise ValueError('Cannot deduce the name of the by-phrase column "%s"' % str(value))

        self.__by_phrase_columns.append((name, value))
        return self

    def to_string(self):
        assert self.__table is not None, 'Table is not set'

        statement = io.StringIO()

        statement.write('?[')
        statement.write(self.__table)
        statement.write(';(')
        constraints_len = len(self.__constraints)
        if constraints_len == 0:
            statement.write('enlist 1b')
        elif constraints_len == 1:
            statement.write('enlist ')
        for constraint_index, constraint in enumerate(self.__constraints):
            if constraint_index > 0:
                statement.write(';')
            statement.write(str(constraint))
        statement.write(');')
        if len(self.__by_phrase_columns) == 0:
            statement.write('0b')
        else:
            statement.write('(')
            by_phrase_columns_len = len(self.__by_phrase_columns)
            if by_phrase_columns_len == 1:
                statement.write('enlist ')
            for by_phrase_column_index, by_phrase_column in enumerate(self.__by_phrase_columns):
                if by_phrase_column_index > 0:
                    statement.write(';')
                statement.write(str(by_phrase_column[0]))
            statement.write(')!(')
            if by_phrase_columns_len == 1:
                statement.write('enlist ')
            for by_phrase_column_index, by_phrase_column in enumerate(self.__by_phrase_columns):
                if by_phrase_column_index > 0:
                    statement.write(';')
                statement.write(str(by_phrase_column[1]))
            statement.write(')')
        statement.write(';(')

        select_columns_len = len(self.__select_columns)
        if select_columns_len == 1:
            statement.write('enlist ')
        for select_column_index, select_column in enumerate(self.__select_columns):
            if select_column_index > 0:
                statement.write(';')
            statement.write(str(select_column[0]))
        statement.write(')!(')
        if select_columns_len == 1:
            statement.write('enlist ')
        for select_column_index, select_column in enumerate(self.__select_columns):
            if select_column_index > 0:
                statement.write(';')
            statement.write(str(select_column[1]))
        statement.write(')')
        statement.write(']')

        return statement.getvalue()

    def __str__(self):
        return self.to_string()

    def __repr__(self):
        return self.to_string()

def convert_time_zone(q_result, from_time_zone, to_time_zone, column_indices=((0,1),), implicit_date=None):
    if not hasattr(column_indices, '__iter__'):
        column_indices = [column_indices]
    if implicit_date is None:
        implicit_date = dt.datetime.today().date()
    processed_q_result = []
    for row in q_result:
        row_copy = [v for v in row]
        for column_index in column_indices:
            if hasattr(column_index, '__iter__'):
                if row_copy[column_index[0]] is None or row_copy[column_index[1]] is None:
                    continue
                if isinstance(row_copy[column_index[0]], dt.date) and isinstance(row_copy[column_index[1]], dt.time):
                    datetime = dt.datetime.combine(row_copy[column_index[0]], row_copy[column_index[1]])
                elif isinstance(row_copy[column_index[1]], dt.date) and isinstance(row_copy[column_index[0]], dt.time):
                    datetime = dt.datetime.combine(row_copy[column_index[1]], row_copy[column_index[0]])
                else:
                    raise ValueError('Date and time expected at specified column indices (%s)' % str(column_index))
                datetime = from_time_zone.localize(datetime)
                datetime = to_time_zone.normalize(datetime.astimezone(to_time_zone))
                if isinstance(row_copy[column_index[0]], dt.date):
                    row_copy[column_index[0]] = datetime.date()
                else:
                    row_copy[column_index[0]] = datetime.time()
                if isinstance(row_copy[column_index[1]], dt.date):
                    row_copy[column_index[1]] = datetime.date()
                else:
                    row_copy[column_index[1]] = datetime.time()
            else:
                if row_copy[column_index] is None:
                    continue
                if isinstance(row_copy[column_index], dt.time):
                    datetime = dt.datetime.combine(implicit_date, row_copy[column_index])
                elif isinstance(row_copy[column_index], dt.datetime):
                    datetime = row_copy[column_index]
                else:
                    raise ValueError('Time or date-time expected at specified column index(%s)' % str(column_index))
                datetime = from_time_zone.localize(datetime)
                datetime = to_time_zone.normalize(datetime.astimezone(to_time_zone))
                row_copy[column_index] = datetime
            processed_q_result.append(row_copy)
    return processed_q_result
