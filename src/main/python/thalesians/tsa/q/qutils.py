import copy
import datetime
import io

import numpy as np

def formatQTime(thing):
    if isinstance(thing, datetime.datetime) or isinstance(thing, datetime.time):
        hour = thing.hour
        minute = thing.minute
        second = thing.second
        microsecond = thing.microsecond
    else:
        raise ValueError('Cannot create a q time string representation of "%s"' % repr(thing))
    millisecond = microsecond / 1000
    return '%02d:%02d:%02d.%03d' % (hour, minute, second, millisecond)

def formatQDate(thing):
    if isinstance(thing, datetime.datetime) or isinstance(thing, datetime.date):
        year = thing.year
        month = thing.month
        day = thing.day
    else:
        raise ValueError('Cannot create a q date string representation of "%s"' % repr(thing))
    return '%04d.%02d.%02d' % (year, month, day)

def formatQDateTime(thing1, thing2=None):
    if thing2 is not None:
        if isinstance(thing1, datetime.date) and isinstance(thing2, datetime.time):
            year = thing1.year
            month = thing1.month
            day = thing1.day
            hour = thing2.hour
            minute = thing2.minute
            second = thing2.second
            microsecond = thing2.microsecond
        elif isinstance(thing1, datetime.time) and isinstance(thing2, datetime.date):
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
        if isinstance(thing1, datetime.datetime):
            year = thing1.year
            month = thing1.month
            day = thing1.day
            hour = thing1.hour
            minute = thing1.minute
            second = thing1.second
            microsecond = thing1.microsecond
        elif isinstance(thing1, datetime.date):
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
    def __init__(self, aggr, name, symbol, char, num, nullValue, size, maker):
        self.__aggr = aggr
        self.__name = name
        self.__symbol = symbol
        self.__char = char
        self.__num = num
        self.__nullValue = nullValue
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

    def __get_nullValue(self):
        return self.__nullValue

    nullValue = property(fget=__get_nullValue)

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
    def __init__(self, value, qType):
        self.__value = copy.copy(value)
        self.__qType = qType

    def __get_value(self):
        return self.__value

    value = property(fget=__get_value)

    def __get_qType(self):
        return self.__qType

    qType = property(fget=__get_qType)

    def toLiteral(self):
        raise NotImplementedError('Pure virtual method')

    def __str__(self):
        return self.toLiteral()

    def __repr__(self):
        return self.toLiteral()

class QBooleanValue(QValue):
    def __init__(self, value=None):
        super(QBooleanValue, self).__init__(value, QTypes.BOOLEAN)

    def toLiteral(self):
        if self.value is None:
            return self.qType.nullValue
        return '1b' if self.value else '0b'

def makeQBooleanValue(value=None):
    return QBooleanValue(value)

class QCharValue(QValue):
    def __init__(self, value=None):
        super(QCharValue, self).__init__(value, QTypes.CHAR)

    def toLiteral(self, QValue):
        if self.value is None:
            return self.qType.nullValue
        return '"%s"' % str(self.value)

def makeQCharValue(value=None):
    return QCharValue(value)

def toQStringLiteral(s):
    s = s.replace('\\', '\\\\')
    s = s.replace('"', '\\"')
    s = s.replace('\n', '\\n')
    return '"%s"' % s

def toQSymbolLiteral(s):
    return '(`$%s)' % toQStringLiteral(s)

class QSymbolValue(QValue):
    def __init__(self, value=None):
        super(QSymbolValue, self).__init__(value, QTypes.SYMBOL)

    def toLiteral(self):
        if self.value is None:
            return self.qType.nullValue
        return toQSymbolLiteral(str(self.value))

def makeQSymbolValue(value=None):
    return QSymbolValue(value)

class QStringValue(QValue):
    def __init__(self, value=None):
        super(QStringValue, self).__init__(value, QTypes.CHAR_LIST)

    def toLiteral(self):
        if self.value is None:
            return self.qType.nullValue
        return toQStringLiteral(str(self.value))

def makeQStringValue(value=None):
    return QStringValue(value)

class QDateTimeValue(QValue):
    def __init__(self, value=None):
        if isinstance(value, datetime.datetime):
            # round down the microseconds
            milliseconds = int(value.microsecond / 1000)
            timeTuple = value.timetuple()
            value = (timeTuple[0], timeTuple[1], timeTuple[2], timeTuple[3], \
                    timeTuple[4], timeTuple[5], milliseconds)
        super(QDateTimeValue, self).__init__(value, QTypes.DATETIME)

    def toLiteral(self):
        if self.value is None:
            return self.qType.nullValue
        return '%04d.%02d.%02dT%02d:%02d:%02d.%03d' % self.value[0:7]

def makeQDateTimeValue(value=None):
    return QDateTimeValue(value)

class QDateValue(QValue):
    def __init__(self, value=None):
        if isinstance(value, datetime.date):
            value = value.timetuple()[0:3]
        super(QDateValue, self).__init__(value, QTypes.DATE)

    def toLiteral(self):
        if self.value is None:
            return self.qType.nullValue
        return '%04d.%02d.%02d' % self.value[0:3]

def makeQDateValue(value=None):
    return QDateValue(value)

class QTimeValue(QValue):
    def __init__(self, value=None):
        if isinstance(value, datetime.time):
            # round down the microseconds
            milliseconds = int(value.microsecond / 1000)
            value = (value.hour, value.minute, value.second, milliseconds)
        super(QTimeValue, self).__init__(value, QTypes.TIME)

    def toLiteral(self):
        if self.value is None:
            return self.qType.nullValue
        return '%02d:%02d:%02d.%03d' % self.value[0:4]

def makeQTimeValue(value=None):
    return QTimeValue(value)

class QNumericValue(QValue):
    def __init__(self, value, qType):
        super(QNumericValue, self).__init__(value, qType)

    def toLiteral(self):
        if self.value is None or np.isnan(self.value):
            return self.qType.nullValue
        return '%s%s' % (str(self.value), self.qType.char)

class QShortValue(QNumericValue):
    def __init__(self, value=None):
        super(QShortValue, self).__init__(value, QTypes.SHORT)

    def toLiteral(self):
        if self.value is None:
            return self.qType.nullValue
        return '%s%s' % (str(int(self.value)), self.qType.char)
def makeQShortValue(value=None):
    return QShortValue(value)

class QIntValue(QNumericValue):
    def __init__(self, value=None):
        super(QIntValue, self).__init__(value, QTypes.INT)

    def toLiteral(self):
        if self.value is None:
            return self.qType.nullValue
        return '%s%s' % (str(int(self.value)), self.qType.char)

def makeQIntValue(value=None):
    return QIntValue(value)

class QLongValue(QNumericValue):
    def __init__(self, value=None):
        super(QLongValue, self).__init__(value, QTypes.LONG)

    def toLiteral(self):
        if self.value is None:
            return self.qType.nullValue
        return '%s%s' % (str(long(self.value)), self.qType.char)

def makeQLongValue(value=None):
    return QLongValue(value)

class QRealValue(QNumericValue):
    def __init__(self, value=None):
        super(QRealValue, self).__init__(value, QTypes.REAL)

def makeQRealValue(value=None):
    return QRealValue(value)

class QFloatValue(QNumericValue):
    def __init__(self, value=None):
        super(QFloatValue, self).__init__(value, QTypes.FLOAT)

def makeQFloatValue(value=None):
    return QFloatValue(value)

class QUntypedListValue(QValue):
    def __init__(self, value):
        if not isinstance(value, QValue):
            if not hasattr(value, '__iter__'):
                raise ValueError('Cannot construct a q untyped list value from a Python object of type %s, which does not seem to be iterable' % str(type(value)))
            value = [makeQValue(element) for element in value]
        super(QUntypedListValue, self).__init__(value, QTypes.UNTYPED_LIST)

    def toLiteral(self):
        literal = io.StringIO()
        if len(self.value) == 1:
            literal.write('enlist')
        literal.write('(')
        for index, element in enumerate(self.value):
            if index > 0:
                literal.write(';')
            if hasattr(element, 'toLiteral'):
                literal.write(element.toLiteral())
            else:
                literal.write(str(element))
        literal.write(')')
        return literal.getvalue()

def makeQUntypedListValue(value):
    return QUntypedListValue(value)

class QIdentifierValue(QValue):
    def __init__(self, value):
        super(QIdentifierValue, self).__init__(value, QTypes.IDENTIFIER)

    def toLiteral(self):
        return self.value

def makeQIdentifierValue(value):
    return QIdentifierValue(value)

def inferQType(value, preferStringsToSymbols=False):
    if isinstance(value, QValue):
        return value.qType
    elif isinstance(value, bool):
        return QTypes.BOOLEAN
    elif isinstance(value, int):
        return QTypes.INT
    elif isinstance(value, long):
        return QTypes.LONG
    elif isinstance(value, float):
        return QTypes.FLOAT
    elif isinstance(value, str) or isinstance(value, unicode):
        return QTypes.CHAR_LIST if preferStringsToSymbols else QTypes.SYMBOL
    elif isinstance(value, datetime.datetime):
        return QTypes.DATETIME
    elif isinstance(value, datetime.date):
        return QTypes.DATE
    elif isinstance(value, datetime.time):
        return QTypes.TIME
    elif hasattr(value, '__iter__'):
        return QTypes.UNTYPED_LIST
    else:
        raise ValueError('Unable to infer the q type corresponding to the Python type %s' % str(type(value)))

def makeQValue(value, qType=None, preferStringsToSymbols=False):
    if isinstance(value, QValue):
        return value
    else:
        qType = inferQType(value, preferStringsToSymbols) if qType is None else qType
        maker = qType.maker
        if maker is None:
            raise ValueError('Unable to make the q type %s from Python type %s' % (qType.name, str(type(value))))
        return maker(value)

class QTypes(object):
    # This isn't really a type
    IDENTIFIER    = QType( False, None      , None       , None, None, None   , None, None                  )

    UNTYPED_LIST  = QType( True , None      , None       , None, 0   , None   , None, makeQUntypedListValue )

    # Primitive types
    BOOLEAN       = QType( False, 'boolean' , '`boolean' , 'b' , -1  , '0b'   , 1   , makeQBooleanValue     )
    BYTE          = QType( False, 'byte'    , '`byte'    , 'x' , -4  , '0x00' , 1   , None                  )
    SHORT         = QType( False, 'short'   , '`short'   , 'h' , -5  , '0Nh'  , 2   , makeQShortValue       )
    INT           = QType( False, 'int'     , '`int'     , 'i' , -6  , '0N'   , 4   , makeQIntValue         )
    LONG          = QType( False, 'long'    , '`long'    , 'j' , -7  , '0Nj'  , 8   , makeQLongValue        )
    REAL          = QType( False, 'real'    , '`real'    , 'e' , -8  , '0Ne'  , 4   , makeQRealValue        )
    FLOAT         = QType( False, 'float'   , '`float'   , 'f' , -9  , '0n'   , 8   , makeQFloatValue       )
    CHAR          = QType( False, 'char'    , '`char'    , 'c' , -10 , '""'   , 1   , makeQCharValue        )
    SYMBOL        = QType( False, 'symbol'  , '`'        , 's' , -11 , '`'    , None, makeQSymbolValue      )
    MONTH         = QType( False, 'month'   , '`month'   , 'm' , -13 , '0Nm'  , 4   , None                  )
    DATE          = QType( False, 'date'    , '`date'    , 'd' , -14 , '0Nd'  , 4   , makeQDateValue        )
    DATETIME      = QType( False, 'datetime', '`datetime', 'z' , -15 , '0Nz'  , 4   , makeQDateTimeValue    )
    MINUTE        = QType( False, 'minute'  , '`minute'  , 'u' , -17 , '0Nu'  , 4   , None                  )
    SECOND        = QType( False, 'second'  , '`second'  , 'v' , -18 , '0Nv'  , 4   , None                  )
    TIME          = QType( False, 'time'    , '`time'    , 't' , -19 , '0Nt'  , 4   , makeQTimeValue        )

    # Typed lists
    BOOLEAN_LIST  = QType( True , 'boolean' , '`boolean' , 'b' , 1   , '0b'   , 1   , None                  )
    BYTE_LIST     = QType( True , 'byte'    , '`byte'    , 'x' , 4   , '0x00' , 1   , None                  )
    SHORT_LIST    = QType( True , 'short'   , '`short'   , 'h' , 5   , '0Nh'  , 2   , None                  )
    INT_LIST      = QType( True , 'int'     , '`int'     , 'i' , 6   , '0N'   , 4   , None                  )
    LONG_LIST     = QType( True , 'long'    , '`long'    , 'j' , 7   , '0Nj'  , 8   , None                  )
    REAL_LIST     = QType( True , 'real'    , '`real'    , 'e' , 8   , '0Ne'  , 4   , None                  )
    FLOAT_LIST    = QType( True , 'float'   , '`float'   , 'f' , 9   , '0n'   , 8   , None                  )
    CHAR_LIST     = QType( True , 'char'    , '`char'    , 'c' , 10  , '""'   , 1   , makeQStringValue      )
    SYMBOL_LIST   = QType( True , 'symbol'  , '`'        , 's' , 11  , '`'    , None, None                  )
    MONTH_LIST    = QType( True , 'month'   , '`month'   , 'm' , 13  , '0Nm'  , 4   , None                  )
    DATE_LIST     = QType( True , 'date'    , '`date'    , 'd' , 14  , '0Nd'  , 4   , None                  )
    DATETIME_LIST = QType( True , 'datetime', '`datetime', 'z' , 15  , '0Nz'  , 4   , None                  )
    MINUTE_LIST   = QType( True , 'minute'  , '`minute'  , 'u' , 17  , '0Nu'  , 4   , None                  )
    SECOND_LIST   = QType( True , 'second'  , '`second'  , 'v' , 18  , '0Nv'  , 4   , None                  )
    TIME_LIST     = QType( True , 'time'    , '`time'    , 't' , 19  , '0Nt'  , 4   , None                  )

class QCreateTableStatementBuilder(object):
    def __init__(self, overwrite=False):
        self.__table = None
        self.__columns = []
        self.__appendedNonKeyColumns = False
        self.__keyColumnCount = 0
        self.overwrite = overwrite

    def setTable(self, table):
        self.__table = table
        return self

    def appendColumn(self, name, qType=None, key=False):
        assert not (key and self.__appendedNonKeyColumns), 'Cannot append a key column after non-key columns'
        self.__columns.append((name, qType))
        if key:
            self.__keyColumnCount += 1
        return self

    def toString(self):
        assert self.__table is not None, 'Table is not set'

        statement = io.StringIO()

        statement.write(self.__table)
        statement.write(':')

        if not self.overwrite:
            statement.write('$[')
            statement.write(toQSymbolLiteral(self.__table))
            statement.write(' in value["\\\\v"]; ')
            statement.write(self.__table)
            statement.write('; ')

        statement.write('([')
        for columnIndex in range(self.__keyColumnCount):
            column = self.__columns[columnIndex]
            statement.write(column[0])
            statement.write(':')
            if column[1] is not None and not column[1] == QTypes.CHAR_LIST:
                statement.write(column[1].symbol)
                statement.write('$')
            statement.write('()')
            if columnIndex < self.__keyColumnCount - 1:
                statement.write(';')
        statement.write('];')
        columnCount = len(self.__columns)
        for columnIndex in range(self.__keyColumnCount, len(self.__columns)):
            column = self.__columns[columnIndex]
            statement.write(column[0])
            statement.write(':')
            if column[1] is not None and not column[1] == QTypes.CHAR_LIST:
                statement.write(column[1].symbol)
                statement.write('$')
            statement.write('()')
            if columnIndex < columnCount - 1:
                statement.write(';')
        statement.write(')')

        if not self.overwrite:
            statement.write(']')

        return statement.getvalue()

    def __str__(self):
        return self.toString()

    def __repr__(self):
        return self.toString()

class QUpsertStatementBuilder(object):
    def __init__(self):
        self.__table = None
        self.__qValues = []

    def setTable(self, table):
        self.__table = table
        return self

    def append(self, qValue):
        self.__qValues.append(qValue)
        return self

    def toString(self):
        assert self.__table is not None, 'Table is not set'

        statement = io.StringIO()

        statement.write('upsert[')
        statement.write(toQSymbolLiteral(self.__table))
        statement.write('](')
        for index, qValue in enumerate(self.__qValues):
            if isinstance(qValue, QValue):
                statement.write(qValue.toLiteral())
            else:
                statement.write(qValue)
            if index < len(self.__qValues) - 1:
                statement.write(';')
        statement.write(')')

        return statement.getvalue()

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
    def makePlusExpression(self, lhs, rhs):
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
            if isinstance(self.rhs, QValue) and self.rhs.qType == QTypes.SYMBOL:
                s.write('enlist ')
            s.write(str(self.rhs))
        else:
            if len(self.rhs) == 1 and self.rhs[0].qType == QTypes.SYMBOL:
                s.append('enlist ')
            rhsLen = len(self.rhs)
            for rhsIndex, rhsItem in enumerate(self.rhs):
                if rhsIndex > 0:
                    s.write(';')
                s.write(str(rhsItem))
        s.write('))')
        return s.getvalue()

class QConstraintFactory(object):
    def makeEqualConstraint(self, lhs, rhs):
        return QConstraint('=', lhs, rhs)

    def makeNotEqualConstraint(self, lhs, rhs):
        return QConstraint('<>', lhs, rhs)

    def makeLessThanConstraint(self, lhs, rhs):
        return QConstraint('<', lhs, rhs)

    def makeGreaterThanConstraint(self, lhs, rhs):
        return QConstraint('>', lhs, rhs)

    def makeLessThanOrEqualConstraint(self, lhs, rhs):
        return QConstraint('<=', lhs, rhs)

    def makeGreaterThanOrEqualConstraint(self, lhs, rhs):
        return QConstraint('>=', lhs, rhs)

    def makeLikeConstraint(self, lhs, rhs):
        return QConstraint('like', lhs, rhs)

    def makeInConstraint(self, lhs, rhs):
        return QConstraint('in', lhs, makeQUntypedListValue((rhs,)))

    def makeWithinConstraint(self, lhs, rhs):
        return QConstraint('within', lhs, rhs)

class QSelectStatementBuilder(object):
    def __init__(self):
        self.__table = None
        self.__selectColumns = []
        self.__byPhraseColumns = []
        self.__constraints = []

    def setTable(self, table):
        self.__table = table
        return self

    def appendSelectColumn(self, value, name=None):
        if name is None:
            if isinstance(value, QValue) and value.qType == QTypes.SYMBOL:
                name = value
            else:
                raise ValueError('Cannot deduce the name of the select column "%s"' % str(value))

        self.__selectColumns.append((name, value))
        return self

    def appendConstraint(self, constraint):
        self.__constraints.append(constraint)
        return self

    def appendByPhraseColumn(self, value, name=None):
        if name is None:
            if isinstance(value, QValue) and value.qType == QTypes.SYMBOL:
                name = value
            else:
                raise ValueError('Cannot deduce the name of the by-phrase column "%s"' % str(value))

        self.__byPhraseColumns.append((name, value))
        return self

    def toString(self):
        assert self.__table is not None, 'Table is not set'

        statement = io.StringIO()

        statement.write('?[')
        statement.write(self.__table)
        statement.write(';(')
        constraintsLen = len(self.__constraints)
        if constraintsLen == 0:
            statement.write('enlist 1b')
        elif constraintsLen == 1:
            statement.write('enlist ')
        for constraintIndex, constraint in enumerate(self.__constraints):
            if constraintIndex > 0:
                statement.write(';')
            statement.write(str(constraint))
        statement.write(');')
        if len(self.__byPhraseColumns) == 0:
            statement.write('0b')
        else:
            statement.write('(')
            byPhraseColumnsLen = len(self.__byPhraseColumns)
            if byPhraseColumnsLen == 1:
                statement.write('enlist ')
            for byPhraseColumnIndex, byPhraseColumn in enumerate(self.__byPhraseColumns):
                if byPhraseColumnIndex > 0:
                    statement.write(';')
                statement.write(str(byPhraseColumn[0]))
            statement.write(')!(')
            if byPhraseColumnsLen == 1:
                statement.write('enlist ')
            for byPhraseColumnIndex, byPhraseColumn in enumerate(self.__byPhraseColumns):
                if byPhraseColumnIndex > 0:
                    statement.write(';')
                statement.write(str(byPhraseColumn[1]))
            statement.write(')')
        statement.write(';(')

        selectColumnsLen = len(self.__selectColumns)
        if selectColumnsLen == 1:
            statement.write('enlist ')
        for selectColumnIndex, selectColumn in enumerate(self.__selectColumns):
            if selectColumnIndex > 0:
                statement.write(';')
            statement.write(str(selectColumn[0]))
        statement.write(')!(')
        if selectColumnsLen == 1:
            statement.write('enlist ')
        for selectColumnIndex, selectColumn in enumerate(self.__selectColumns):
            if selectColumnIndex > 0:
                statement.write(';')
            statement.write(str(selectColumn[1]))
        statement.write(')')
        statement.write(']')

        return statement.getvalue()

    def __str__(self):
        return self.toString()

    def __repr__(self):
        return self.toString()

def convertTimeZone(qResult, fromTimeZone, toTimeZone, columnIndices=((0,1),), implicitDate=None):
    if not hasattr(columnIndices, '__iter__'):
        columnIndices = [columnIndices]
    if implicitDate is None:
        implicitDate = datetime.datetime.today().date()
    processedQResult = []
    for row in qResult:
        rowCopy = [v for v in row]
        for columnIndex in columnIndices:
            if hasattr(columnIndex, '__iter__'):
                if rowCopy[columnIndex[0]] is None or rowCopy[columnIndex[1]] is None:
                    continue
                if isinstance(rowCopy[columnIndex[0]], datetime.date) and isinstance(rowCopy[columnIndex[1]], datetime.time):
                    dateTime = datetime.datetime.combine(rowCopy[columnIndex[0]], rowCopy[columnIndex[1]])
                elif isinstance(rowCopy[columnIndex[1]], datetime.date) and isinstance(rowCopy[columnIndex[0]], datetime.time):
                    dateTime = datetime.datetime.combine(rowCopy[columnIndex[1]], rowCopy[columnIndex[0]])
                else:
                    raise ValueError('Date and time expected at specified column indices (%s)' % str(columnIndex))
                dateTime = fromTimeZone.localize(dateTime)
                dateTime = toTimeZone.normalize(dateTime.astimezone(toTimeZone))
                if isinstance(rowCopy[columnIndex[0]], datetime.date):
                    rowCopy[columnIndex[0]] = dateTime.date()
                else:
                    rowCopy[columnIndex[0]] = dateTime.time()
                if isinstance(rowCopy[columnIndex[1]], datetime.date):
                    rowCopy[columnIndex[1]] = dateTime.date()
                else:
                    rowCopy[columnIndex[1]] = dateTime.time()
            else:
                if rowCopy[columnIndex] is None:
                    continue
                if isinstance(rowCopy[columnIndex], datetime.time):
                    dateTime = datetime.datetime.combine(implicitDate, rowCopy[columnIndex])
                elif isinstance(rowCopy[columnIndex], datetime.datetime):
                    dateTime = rowCopy[columnIndex]
                else:
                    raise ValueError('Time or date-time expected at specified column index(%s)' % str(columnIndex))
                dateTime = fromTimeZone.localize(dateTime)
                dateTime = toTimeZone.normalize(dateTime.astimezone(toTimeZone))
                rowCopy[columnIndex] = dateTime
            processedQResult.append(rowCopy)
    return processedQResult
