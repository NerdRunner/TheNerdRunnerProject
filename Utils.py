import datetime
import time


def getCalendarWeekFromDate(date):
    '''
    Gets the current calendar week
    :param date:
    :return:
    '''
    return date.isocalendar()[1]

def getDateRangeFromWeek(year, week):
    '''
    Gets the range of dates of a calendar week
    :param year: The year
    :param week: the calendar week
    :return: d1, d2: dates from which to which the week lasts
    '''
    atime = time.asctime(time.strptime('{} {} 1'.format(year, week), '%Y %W %w'))
    d1 = datetime.datetime.strptime(atime, "%a %b %d %H:%M:%S %Y").date()
    d2 = d1 + datetime.timedelta(days=6.9)
    return d1, d2

def dayOfYear(d):
    '''
    returns the day of the year of a given date
    :param d: The date
    :return:
    '''
    doy = d.date().timetuple().tm_yday
    return doy

def listSum(ll):
    rv = 0
    for l in ll:
        if type(l) is not int:
            rv = rv + l[0]
        else:
            rv = rv+ l
    return rv