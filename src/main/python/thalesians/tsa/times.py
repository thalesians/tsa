import pytz

NANOSECONDS_PER_MICROSECOND = 1000

MICROSECONDS_PER_MILLISECOND = 1000
NANOSECONDS_PER_MILLISECOND = 1000000  

MILLISECONDS_PER_SECOND = 1000
MICROSECONDS_PER_SECOND = 1000000
NANOSECONDS_PER_SECOND = 1000000000    

SECONDS_PER_MINUTE = 60
MILLISECONDS_PER_MINUTE = 60000
MICROSECONDS_PER_MINUTE = 60000000
NANOSECONDS_PER_MINUTE = 60000000000

MINUTES_PER_HOUR = 60
SECONDS_PER_HOUR = 3600
MILLISECONDS_PER_HOUR = 3600000
MICROSECONDS_PER_HOUR = 3600000000
NANOSECONDS_PER_HOUR = 3600000000000

HOURS_PER_DAY = 24
MINUTES_PER_DAY = 1440
SECONDS_PER_DAY = 86400
MILLISECONDS_PER_DAY = 86400000
MICROSECONDS_PER_DAY = 86400000000
NANOSECONDS_PER_DAY = 86400000000000

_us_eastern = pytz.timezone('US/Eastern')
_london = pytz.timezone('Europe/London')
_paris = pytz.timezone('Europe/Paris')
_milan = pytz.timezone('Europe/Rome')
_frankfurt = pytz.timezone('Europe/Berlin')
_moscow = pytz.timezone('Europe/Moscow')
_hong_kong = pytz.timezone('Asia/Hong_Kong')
_shanghai = pytz.timezone('Asia/Shanghai')
_singapore = pytz.timezone('Asia/Singapore')
_tokyo = pytz.timezone('Asia/Tokyo')
_sydney = pytz.timezone('Australia/Sydney')

def utc_to_tz(datetime, tz):
    return pytz.utc.localize(datetime).astimezone(tz)
    
def utc_to_us_eastern(datetime):
    return utc_to_tz(datetime, _us_eastern)

def utc_to_new_york(datetime):
    return utc_to_us_eastern(datetime)

def utc_to_london(datetime):
    return utc_to_tz(datetime, _london)

def utc_to_paris(datetime):
    return utc_to_paris(datetime, _paris)

def utc_to_milan(datetime):
    return utc_to_milan(datetime, _milan)

def utc_to_frankfurt(datetime):
    return utc_to_tz(datetime, _frankfurt)

def utc_to_moscow(datetime):
    return utc_to_tz(datetime, _moscow)

def utc_to_hong_kong(datetime):
    return utc_to_tz(datetime, _hong_kong)

def utc_to_shanghai(datetime):
    return utc_to_tz(datetime, _shanghai)

def utc_to_singapore(datetime):
    return utc_to_tz(datetime, _singapore)

def utc_to_tokyo(datetime):
    return utc_to_tokyo(datetime, _tokyo)

def utc_to_sydney(datetime):
    return utc_to_sydney(datetime, _sydney)

def tz_to_utc(datetime, tz):
    return tz.localize(datetime).astimezone(pytz.utc)

def us_eastern_to_utc(datetime):
    return tz_to_utc(datetime, _us_eastern)

def new_york_to_utc(datetime):
    return us_eastern_to_utc(datetime)

def london_to_utc(datetime):
    return tz_to_utc(datetime, _london)

def paris_to_utc(datetime):
    return tz_to_utc(datetime, _paris)

def milan_to_utc(datetime):
    return tz_to_utc(datetime, _milan)

def frankfurt_to_utc(datetime):
    return tz_to_utc(datetime, _frankfurt)

def moscow_to_utc(datetime):
    return tz_to_utc(datetime, _moscow)

def hong_kong_to_utc(datetime):
    return tz_to_utc(datetime, _hong_kong)

def shanghai_to_utc(datetime):
    return tz_to_utc(datetime, _shanghai)

def singapore_to_utc(datetime):
    return tz_to_utc(datetime, _singapore)

def tokyo_to_utc(datetime):
    return tz_to_utc(datetime, _tokyo)

def sydney_to_utc(datetime):
    return tz_to_utc(datetime, _sydney)
