import datetime
import math
from datetime import timedelta

import numpy as np

import Utils
import mysqlCredentials
import mysqltools

def averageDailyTrimps(mydb, d1, nDays):
    '''
    Calculates the average of summed and weighted daily trimp values starting from a given date. Weights exponentially for delta to start date
    :param mydb: MYSQL-Handler
    :param d1: Start date
    :param nDays: number of days to go back to average the trimp values
    :return:
    '''
    n=0
    trimps = []
    wl = []
    while(n<nDays):
        d = d1 - timedelta(days=n)
        res = mysqltools.getByDateRange(mydb, mysqlCredentials.cn_trimp, d, d)
        trimpsDaily=0
        weight = math.exp(-3 * n / nDays)
        wl.append(weight)
        for d in res:
            t = d[1]
            trimpsDaily = trimpsDaily+t
        n = n+1
        trimps.append(trimpsDaily)
    travg = np.average(trimps, weights=wl)
    return travg

def averageTrimps(mydb, d1, nDays):
    '''
    gets weighted averaged trimp values over the last nDays starting from d1
    :param mydb: MYSQL-Handler
    :param d1: Start date
    :param nDays: Number of days back from d1
    :return:
    '''
    d2 = d1 - timedelta(days=nDays)
    res = mysqltools.getByDateRange(mydb,mysqlCredentials.cn_trimp, d1, d2)
    i = 0.
    trimps = []
    for d in res:
        t = d[1]
        delta = (d1-d[0]).days
        weight = math.exp(-3*delta/nDays)
        trimps.append(t*weight)
        i = i+1
    if len(trimps) < nDays:
        while len(trimps) < nDays:
            trimps.append(0.)
    travg = np.average(trimps)

    return travg

def calculateDayCTL(mydb, d1):
    '''
    calculates the CTL (Cronic Training Load) for a given date
    :param mydb: MYSQL-Handler
    :param d1: Day for which the CTL is calculated
    :return:
    '''
    #ctl = averageTrimps(mydb, d1, 42)
    ctl = averageDailyTrimps(mydb, d1, 42)
    return ctl

def calculateDayATL(mydb, d1):
    '''
    Calculates the ATL (Acute Training Load) for a given date
    :param mydb: MYSQL-Handler
    :param d1: day for which the ATL is calculated
    :return:
    '''
    #atl = averageTrimps(mydb, d1, 7)
    atl = averageDailyTrimps(mydb, d1, 7)
    return atl

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
    res = mysqltools.getActivitiesByDateRange(mydb, [act], d1, d2)
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
            yy = summary(mydb, a, d1, d2)
            yy.insert(0,y)
            summ.append(yy)
            formattedString+=str(yy)+"\n"
        totalSum.append(summ)
        formattedString+="-------------\n"



    return totalSum, formattedString