import datetime
import os
from datetime import timedelta


import mysql.connector

import Utils
import mysqlCredentials
import mysqltools


def connect():
    '''
    connects to the MYSQL Database
    :return: MYSQL-Handler
    '''
    mydb = mysql.connector.connect(
        host=mysqlCredentials.host,
        user=mysqlCredentials.user,
        password=mysqlCredentials.pw,
        database="tnrp"
    )
    return mydb

def createActivityTable(mydb):
    '''
    Creates the default table for activities
    :param mydb: MYSQL-Handler
    :return:
    '''
    mycursor = mydb.cursor()
    str =  "CREATE TABLE "+ mysqlCredentials.activitytable+" (id INT AUTO_INCREMENT PRIMARY KEY, dateiname VARCHAR(99), datum DATETIME, typ TEXT, strecke INT, hr INT, hrlist LINESTRING, trimp INT, pointlist LINESTRING)"
    mycursor.execute(str)

def createUserHealthTable(mydb):
    '''
    Creates the table for user variables
    :param mydb:
    :return:
    '''
    mycursor = mydb.cursor()
    mycursor.execute(
        "CREATE TABLE "+mysqlCredentials.userstats_health+" (id INT AUTO_INCREMENT PRIMARY KEY, datum DATETIME, maxHR INT, restHR INT, weight INT)")

    return

def createUserGeneralTable(mydb):
    '''
    Creates the table for user the non changing user info
    :param mydb:
    :return:
    '''
    mycursor = mydb.cursor()
    mycursor.execute(
        "CREATE TABLE "+mysqlCredentials.userstats_general+" (id INT AUTO_INCREMENT PRIMARY KEY, name TEXT, gender TEXT, dayofbirth DATETIME)")

    return

def createTrainingplanTable(mydb):
    '''
    Creates the table for user a training plan
    :param mydb:
    :return:
    '''
    mycursor = mydb.cursor()
    mycursor.execute(
        "CREATE TABLE "+mysqlCredentials.trainingplantable+" (id INT AUTO_INCREMENT PRIMARY KEY, typ TEXT, datum DATETIME, strecke INT, kind TEXT)")

    return

def createSettingsTable(mydb):
    '''
    Creates the table for the Gui settings
    :param mydb:
    :return:
    '''
    mycursor = mydb.cursor()
    mycursor.execute(
        "CREATE TABLE "+mysqlCredentials.settings+" (id INT AUTO_INCREMENT PRIMARY KEY, name TEXT, value TEXT)")

    return



def createAllTables(mydb):
    '''
    Creates all the necessary tables
    :param mydb:
    :return:
    '''
    createActivityTable(mydb)
    createUserHealthTable(mydb)
    createUserGeneralTable(mydb)
    createSettingsTable(mydb)
    createTrainingplanTable(mydb)

def setSetting(mydb, name, value):
    '''
    Sets the name and the value (string) to the settings database. If value already is in Database, then the value will be updated
    :param mydb:
    :param name:
    :param value:
    :return:
    '''
    mycursor = mydb.cursor()
    sql = "SELECT * FROM " + mysqlCredentials.settings + " WHERE name='" + name + "'"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    id = None
    if len(myresult) > 0:
        id = myresult[0][0]  # use the same id for updated Sportsman
        sql = "DELETE FROM " + mysqlCredentials.settings + " WHERE name='" + name + "'"
        mycursor.execute(sql)

    sql = "INSERT INTO "+mysqlCredentials.settings+" VALUES (%s, %s, %s)"
    mycursor.execute(sql, (id, name, value))
    mydb.commit()


def getSetting(mydb, name):
    '''
    gets the value (string) of the setting
    :param mydb:
    :param name:
    :return: (id, name, value)
    '''
    cursor = mydb.cursor()
    sql = "SELECT * FROM " + mysqlCredentials.settings + " WHERE name='"+name+"'"
    cursor.execute(sql)
    myresult = cursor.fetchall()
    return myresult[0]

def linestringtoList(ls):
    rv=[]
    spl = ls.split(",")
    start = spl[0].split("(")[1]
    spl[0] = start
    end = spl[len(spl)-1].split(")")[0]
    spl[len(spl)-1] = end

    for t in spl:
        s = t.split(" ")
        tp = [float(s[0]), float(s[1])]
        rv.append(tp)
    return rv

def makeORListfromActlist(actList):
    '''
    Generates a "OR" - String for MYSQL requests
    :param actList: List of activities as Strings: ["running", "cycling"]
    :return:
    '''
    rvList = ""
    for a in actList:
        rvList = rvList + " typ = '" + a + "' OR "
    rvList = rvList[:-4]
    return rvList

def getLastActivities(mydb, activityType, lastN):
    '''
    Gets the lastN activities of a given type
    :param mydb: MySQL-Handler
    :param activityType: activityType[], can also be a asterisk ["*"]
    :param lastN: Last activities to get
    :return:
    '''
    mycursor = mydb.cursor()
    actlist = makeORListfromActlist(activityType)
    sql = "SELECT * from " + mysqlCredentials.activitytable + " WHERE " + actlist + " ORDER by datum DESC LIMIT " + str(
        lastN) + ""
    if activityType[0] == "*":
        sql = "SELECT * from " + mysqlCredentials.activitytable + " ORDER by datum DESC LIMIT " + str(lastN) + ""
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return myresult

def getActivitiesAndNumber(mydb, justNames=False, table=mysqlCredentials.activitytable):
    '''
    gets all Activitytypes in the database and how often they are in the database.
    gives just the names with argument justNames = True
    :param mydb:
    :return: list [(act1, num1), (act2, num2), ...]
    '''
    cursor = mydb.cursor()
    if justNames:
        sql = "SELECT typ FROM " + table + " group by typ ORDER BY typ ASC"
    else:
        sql = "SELECT typ, count(typ) FROM "+ mysqlCredentials.activitytable +" group by typ ORDER BY typ ASC"
    cursor.execute(sql)
    myresult = cursor.fetchall()
    rv=[]
    for l in myresult:
        rv.append(l)
    return rv

def getYears(mydb):
    '''
    gets all the years for which activities are stored in the database
    :param mydb:
    :return: list [year1, year2, year3, ....]
    '''
    cursor = mydb.cursor()
    sql = "SELECT year(datum) FROM "+ mysqlCredentials.activitytable +" group by year(datum) ORDER BY year(datum) ASC"
    cursor.execute(sql)
    myresult = cursor.fetchall()
    rv=[]
    for l in myresult:
        rv.append(l[0])
    return rv

def getByDateRange(mydb, col, actList, d1, d2):
    '''
    Gets the col-Values which are between a specific date range
    :param mydb: MYSQL-Handler
    :param col: name of column. See mysqlcredential.cn_XXX
    :param actList: List of Strings which activities shall be searched.
    :param d1: first date
    :param d2: second date
    :return: (date, col)
    '''
    mycursor = mydb.cursor()
    actreq = makeORListfromActlist(actList)
    sql = "SELECT datum," + col + " from " + mysqlCredentials.activitytable + " WHERE DATE(datum) <= '" + d1.strftime(
        "%Y-%m-%d") + "' and DATE(datum) >= '" + d2.strftime("%Y-%m-%d") + "' and ("+actreq + " ) ORDER by datum DESC"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return myresult

def getActivitiesByDateRange(mydb, act, d1, d2, filter=[], table=mysqlCredentials.activitytable, orderValue="datum", orderType="DESC", limit=1000000000):
    '''
    Gets all activities for a given date range
    :param mydb: MYSQL-Handler
    :param act: Activity-Type --> list
    :param d1: first date
    :param d2: second date
    :param filter: [columntoFilter, v1, v2]. Gets all activities for which v1<"columntoFilter"<v2
    :return:
    '''
    mycursor = mydb.cursor()
    actStr = act
    if len(act)>0:
        actStr = ""
        for a in act:
            actStr+="typ='"+a +"' OR "
        actStr=actStr[:-4]
    if len(filter)>0:
        sql = "SELECT * from " + table + " WHERE ("+actStr+") and (DATE(datum) >= '" + d1.strftime(
        "%Y-%m-%d") + "' and DATE(datum) <= '" + d2.strftime("%Y-%m-%d") + "') AND ("+filter[0]+ " >"+str(filter[1])+ " AND "+filter[0]+" <"+str(filter[2])+") ORDER by "+orderValue + " "+orderType + " LIMIT "+str(limit)
    else:
        sql = "SELECT * from " + table + " WHERE ("+actStr+") and (DATE(datum) >= '" + d1.strftime(
        "%Y-%m-%d") + "' and DATE(datum) <= '" + d2.strftime("%Y-%m-%d") + "') ORDER by datum DESC"
    #sql = "SELECT CAST(datum as DATE), typ, " + mysqlCredentials.cn_distance + " from " + mysqlCredentials.activitytable + " WHERE (" + actStr + ") and (DATE(datum) >= '" + d1.strftime(
    #    "%Y-%m-%d") + "' and DATE(datum) <= '" + d2.strftime("%Y-%m-%d") + "') ORDER by datum DESC"


    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return myresult

def getFitFiles(mydb):
    comm = mysqltools.getSetting(mydb, "importScript")
    os.system(comm[2])

def getCummulativeValuesPerYear(mydb, year, actList, datatype, cummulate=True):
    '''
    gets the cummulative distance for a given year for a list of activities and datatype
    :param mydb:
    :param year: the year to get data from
    :param actList: list of activity types which shall be cummulated
    :param datatype: type of data which shall be cummulated. Currently supported "Distance" or "Trimp"
    :return:
    '''
    ay = mysqltools.getActivitiesByDateRange(mydb, actList, datetime.date(year,1,1), datetime.date(year, 12,31))
    cum = []
    i = 0
    while(i<=366): #empty array for day of year and value
        cum.append([i,0])
        i=i+1
    for a in ay: #fill array
        dt = a[2]
        doy = Utils.dayOfYear(dt)
        column = mysqlCredentials.cn_distance_value #Default is nothing checked
        scale = 1000
        if datatype=="Distance":
            column = mysqlCredentials.cn_distance_value
            scale = 1000
        elif datatype=="Trimp":
            column = mysqlCredentials.cn_trimp_value
            scale = 1
        cum[doy][1] = cum[doy][1]+a[column]/scale
    if(cummulate):
        i = 1
        while(i<len(cum)): #cummulate values
            cum[i][1] += cum[i-1][1]
            i+=1
    return cum

def getCummulativeValues(mydb, yearList, actList, datatype, cummulate=True):
    cumGes = []
    for y in yearList:
        cum = getCummulativeValuesPerYear(mydb, y, actList, datatype, cummulate=cummulate)
        cumGes.append(cum)
    return cumGes

def deleteDoubleEntries(mydb):
    '''
    Deltes double entries. Searches by Startdate and Time
    :param mydb:
    :return:
    '''
    mycursor = mydb.cursor()
    sql = "DELETE t1 FROM activities t1 INNER JOIN activities t2 WHERE t1.id < t2.id AND t1.datum = t2.datum" #todo: Machen, dass es auch von Python aus klappt. Direkt in MYSQL funzt es
    mycursor.execute(sql)

    return




#mydb = mysqltools.connect()
#deleteDoubleEntries(mydb)
#cumm = getCummulativeDistancesPerYear(mydb, 2023, ["cycling", "running"])
#cumGes = getCummulativeDistances(mydb, [2021, 2022, 2023], ["cycling", "running"])
#print("ende")
#print(cumm)