import calendar
import datetime


now = datetime.datetime.now()

print(calendar.monthrange(now.year, 2)[1])
