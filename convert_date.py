import dateutil.parser
from babel.dates import format_date, format_datetime, format_time

value = '2035-04-15T20:00:00.000Z'

date = dateutil.parser.parse(value)
if format == 'full':
    format="EEEE MMMM, d, y 'at' h:mma"
elif format == 'medium':
    format="EE MM, dd, y h:mma"
print(format_datetime(date, locale='en_US'))

pass