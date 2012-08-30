
from dateutil import parser

def mysql_date(s):

    dt = parser.parse(s)
    a = str(dt)
    b = a.split('+')
    return(str(b[0]))
