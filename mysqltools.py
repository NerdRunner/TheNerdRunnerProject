import mysql.connector
import mysqlCredentials


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

def createAllTables(mydb):
    '''
    Creates all the necessary tables
    :param mydb:
    :return:
    '''
    createActivityTable(mydb)
    createUserHealthTable(mydb)
    createUserGeneralTable(mydb)