import datetime
import os
from datetime import timedelta

import mysql.connector
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

def getLastActivities(mydb, activityType, lastN):
    '''
    Gets the lastN activities of a given type
    :param mydb: MySQL-Handler
    :param activityType: activityType[]
    :param lastN: Last activities to get
    :return:
    '''
    mycursor = mydb.cursor()
    actlist = ""
    for a in activityType:
        actlist = actlist+" typ = '" + a + "' OR "
    actlist = actlist[:-4]
    sql = "SELECT * from " + mysqlCredentials.activitytable + " WHERE "+actlist + " ORDER by datum DESC LIMIT "+str(lastN)+""
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return myresult

def getActivitiesAndNumber(mydb):
    '''
    gets all Activitytypes in the database and how often they are in the database
    :param mydb:
    :return: list [(act1, num1), (act2, num2), ...]
    '''
    cursor = mydb.cursor()
    sql = "SELECT typ, count(typ) FROM "+ mysqlCredentials.activitytable +" group by typ ORDER BY typ ASC"
    cursor.execute(sql)
    myresult = cursor.fetchall()
    rv=[]
    for l in myresult:
        rv.append(l)
    return rv

def getByDateRange(mydb, col, d1, d2):
    '''
    Gets the col-Values which are between a specific date range
    :param mydb: MYSQL-Handler
    :param col: name of column. See mysqlcredential.cn_XXX
    :param d1: first date
    :param d2: second date
    :return: (date, col)
    '''
    mycursor = mydb.cursor()
    sql = "SELECT datum," + col + " from " + mysqlCredentials.activitytable + " WHERE DATE(datum) <= '" + d1.strftime(
        "%Y-%m-%d") + "' and DATE(datum) >= '" + d2.strftime("%Y-%m-%d") + "' ORDER by datum DESC"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return myresult

def getActivitiesByDateRange(mydb, act, d1, d2):
    '''
    Gets all activities for a given date range
    :param mydb: MYSQL-Handler
    :param act: Activity-Type
    :param d1: first date
    :param d2: second date
    :return:
    '''
    mycursor = mydb.cursor()
    sql = "SELECT * from " + mysqlCredentials.activitytable + " WHERE typ = '"+act+"' and DATE(datum) >= '" + d1.strftime(
        "%Y-%m-%d") + "' and DATE(datum) <= '" + d2.strftime("%Y-%m-%d") + "' ORDER by datum DESC"

    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return myresult

def getFitFiles(mydb):
    comm = mysqltools.getSetting(mydb, "importScript")
    os.system(comm[2])