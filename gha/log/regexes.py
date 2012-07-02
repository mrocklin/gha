import re
from datetime import datetime

email_regex = r"""[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+(?:[A-Z]{2}|com|org|net|edu|gov|mil|biz|info|mobi|name|aero|asia|jobs|museum)\b"""

fullcommit = "[a-f0-9]{40}"
commit = "commit (?P<commit>%s)"%fullcommit
author = "Author: (?P<name>[\w ]+\w)"
email = "<(?P<email>%s)>"%email_regex

day_of_week = "(?P<day_of_week>\w+)"
month = "(?P<month>\w+)"
day_number = "(?P<day_number>\d+)"
time = "(?P<hour>\d\d):(?P<minute>\d\d):(?P<second>\d\d)"
year = "(?P<year>\d\d\d\d)"
timezone = "(?P<timezone>[+-]\d\d\d\d)"

date = "Date:\s*"+'\s*'.join((day_of_week, month, day_number, time, year, timezone))

header = '\s*'.join((commit, author, email, date))




def parse_logfile(file):
    s = file.read() # sorry
    prog = re.compile(header)
    return [{k:L[v-1] for k,v in prog.groupindex.items()}
                      for L in prog.findall(s)]

month_to_int = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6,
                'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
def make_datetime(d):
    return datetime(int(d['year']), month_to_int[d['month']],
            int(d['day_number']), int(d['hour']), int(d['minute']),
            int(d['second']))
