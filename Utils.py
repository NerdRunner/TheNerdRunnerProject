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

def dayOfYear(d, type="dt"):
    '''
    returns the day of the year of a given date
    :param d: The date
    :type = "dt" -> Input is datetime; "d" -> input is a date
    :return:
    '''
    if(type=="dt"):
        doy = d.date().timetuple().tm_yday
    else:
        doy = d.timetuple().tm_day
    return doy

def listSum(ll):
    rv = 0
    for l in ll:
        if type(l) is not int:
            rv = rv + l[0]
        else:
            rv = rv+ l
    return rv

def changeColorOfImage(img, newValue):
    '''
    Changes the color of pixels where R+G+B > 200 to a new value
    :param img: img - Object read with PhotoImage
    :param newValue: (R,G,B)
    :return: img - Object
    '''
    width, height = img.width(), img.height()
    # Process every pixel
    for x in range(0, width - 1):
        for y in range(0, height - 1):
            current_color = img.get(x, y)
            if (current_color[0] + current_color[1] + current_color[2]) > 200: #Condition where to change the color. 200 is more or less self chosen
                img.put("#%02x%02x%02x" % newValue, (x, y))
    return img