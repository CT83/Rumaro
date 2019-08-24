import calendar
import datetime


def date_to_readable_string():
    month = calendar.month_abbr[int(datetime.datetime.now().strftime("%m"))]
    time_day = datetime.datetime.now().strftime("%H:%M:%S, %d")
    year = datetime.datetime.now().strftime("%Y")
    res = "{} {} {}".format(time_day, month, year)
    return res

