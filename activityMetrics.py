import datetime
import math
from datetime import timedelta

import numpy as np

import Utils
import mysqlCredentials
import mysqltools
import statistics

def averageDailyTrimps(mydb, d1, nDays, actList,wl=[]):
    '''
    Calculates the average of summed and weighted daily trimp values starting from a given date. Weights exponentially for delta to start date
    :param mydb: MYSQL-Handler
    :param d1: Start date
    :param nDays: number of days to go back to average the trimp values
    :param wl (weight list; weight for each day). Has to be the same lenght as number of days
    :return:
    '''
    n=0
    trimps = []

    while(n<nDays):
        d = d1 - timedelta(days=n)
        res = mysqltools.getByDateRange(mydb, mysqlCredentials.cn_trimp, actList,d, d)
        trimpsDaily=0
        if len(wl)!= nDays:
            weight = math.exp(-3 * n / nDays)
            wl.append(weight)
        for d in res:
            t = d[1]
            trimpsDaily = trimpsDaily+t
        n = n+1
        trimps.append(trimpsDaily)
    travg = np.average(trimps, weights=wl)
    return travg


def calculateDayCTL(mydb, d1, actList, wl=[]):
    '''
    calculates the CTL (Cronic Training Load) for a given date
    :param mydb: MYSQL-Handler
    :param d1: Day for which the CTL is calculated
    :param wl: weightlist for weight the trimps. wl[0] = startdate weight ... typically 1
    :return:
    '''
    #ctl = averageTrimps(mydb, d1, 42)
    ctl = averageDailyTrimps(mydb, d1, 42, actList, wl)
    return ctl

def calculateDayATL(mydb, d1, actList):
    '''
    Calculates the ATL (Acute Training Load) for a given date
    :param mydb: MYSQL-Handler
    :param d1: day for which the ATL is calculated
    :return:
    '''
    #atl = averageTrimps(mydb, d1, 7)
    atl = averageDailyTrimps(mydb, d1, 7, actList, [1,0.8,0.7,0.6,0.4,0.2,0.1])
    return atl

def monotony(mydb, d, actList=[]):
    '''
    calculates the training monotony Monotony = average(TRIMP)/stddev(TRIMP) TRIMP values over 7 days

    :param mydb:
    :param actList: Per default, it takes all activities into account
    :param d1:
    :return:
    '''

    d2 = d - timedelta(days=7)

    res = mysqltools.getByDateRange(mydb, mysqlCredentials.cn_trimp, actList, d, d2)
    tl = [a[1] for a in res]
    mon = 0
    if len(tl)>0:
        avg =  (sum(tl)/len(tl))
        st = statistics.pstdev(tl)
        mon = avg/st
    return mon
def summary(mydb, act, d1, d2):
    '''
    Gets the summary of an activity type between two dates
    :param mydb: MYSQL-Handler
    :param act: Actitivity Type
    :param d1: First Date
    :param d2: Second Date
    :return: [totalMeters, meanHR, TotalTRIMP]
    '''
    rv=[]
    #Get the activities
    res = mysqltools.getActivitiesByDateRange(mydb, act, d1, d2)
    dist = 0
    meanHR = 0
    totalTrimp = 0
    if len(res) > 0:
        for ll in res:
            dist = dist+ll[4]
            meanHR = meanHR + ll[5]
            totalTrimp = totalTrimp+ll[7]
            meanHR = meanHR/len(res)
        dist = dist/1000

    dist = "{:4.2f}".format(dist)
    meanHR = "{:4.2f}".format(meanHR)

    return [dist, meanHR, totalTrimp]

def summaryYearly(mydb, act, yyyy):
    '''
    Gets the yearly summary of an activity type
    :param mydb:
    :param act:
    :param yyyy:
    :return:
    '''
    summ = []
    totalSum = []
    formattedString = ""
    for a in act:
        summ = []
        formattedString+=a +"\n\n"
        for y in yyyy:
            d1 = datetime.date(y, 1, 1)
            d2 = datetime.date(y, 12, 31)
            yy = summary(mydb, [a], d1, d2)
            yy.insert(0,y)
            summ.append(yy)
            formattedString+=str(yy)+"\n"
        totalSum.append(summ)
        formattedString+="-------------\n"



    return totalSum, formattedString