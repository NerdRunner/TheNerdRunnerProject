
from datetime import timedelta

import numpy as np

import mysqlCredentials
import mysqltools


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
        weight = 1 - delta/nDays #Umstellen auf exponentielle Gewichtung?
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
    ctl = averageTrimps(mydb, d1, 42)
    return ctl

def calculateDayATL(mydb, d1):
    '''
    Calculates the ATL (Acute Training Load) for a given date
    :param mydb: MYSQL-Handler
    :param d1: day for which the ATL is calculated
    :return:
    '''
    atl = averageTrimps(mydb, d1, 7)
    return atl