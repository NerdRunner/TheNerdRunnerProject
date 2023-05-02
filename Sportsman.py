from datetime import datetime, timedelta

import mysqlCredentials
import mysqltools


class Sportsman:

    def __init__(self):
        return
    '''
    class Sportsman
    manages heart rate values
    '''
    def __init__(self, name:str, dayofbirth:datetime, gender:str):
        '''
        Sportsman - Class
        :param name: Name of Sportsman
        :param dayofbirth: datetime.datetime(YYYY-MM-DD)
        :param gender: String: m or f
        '''
        self.name = name
        self.dayofBirth = dayofbirth
        self.gender = gender
        return

    def getFromDB(self, mydb):
        '''
        Sportsman-Class with values from Database
        :param mydb: MySQL-Connector
        '''
        #mydb = mysqltools.connect()
        mycursor = mydb.cursor()
        sql = "SELECT * from " + mysqlCredentials.userstats_general
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        # Only first sportsman is read out
        self.name = myresult[0][1]
        self.gender = myresult[0][2]
        self.dayofBirth= myresult[0][3]

    def setGeneralValuesToDatabase(self, mydb):
        '''
        Deletes the current data in the general database and adds the current values to the Database
        :param mydb:
        :return:
        '''
        mycursor = mydb.cursor()
        sql = "SELECT * FROM " + mysqlCredentials.userstats_general +" WHERE name='"+self.name+"'"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        id = None
        if len(myresult)>0:
            id = myresult[0][0] #use the same id for updated Sportsman
            sql = "DELETE FROM " + mysqlCredentials.userstats_general + " WHERE name='" + self.name + "'"
            mycursor.execute(sql)
        sql = "INSERT INTO " + mysqlCredentials.userstats_general + " VALUES (%s, %s, %s, %s)"
        val = (id, self.name, self.gender, self.dayofBirth)
        mycursor.execute(sql, val)
        mydb.commit()
        return

    def addVitalValuesToDatabase(self, date, maxHR, restHR, weight):
        '''
         Adds maxHR, restHR and weight of today to the database
         :param maxhr: Maximum heart rate
         :param restHR: Rest heart rate
         :param weight: current weight in kg
         :return:
         '''

        mydb = mysqltools.connect()
        mycursor = mydb.cursor()
        sql = "INSERT INTO " + mysqlCredentials.userstats_health + " VALUES (%s, %s, %s, %s, %s)"
        val = (None, date, maxHR, restHR, weight)
        mycursor.execute(sql, val)
        mydb.commit()
        return
    def addTodaysVitalValuesToDatabase(self, maxHR, restHR, weight):
        self.addVitalValuesToDatabase(datetime.today(), maxHR, restHR, weight)


    def getVitalValues(self, mydb, d: datetime):
        '''
        Returns the Vital values (max, rest HR and weight) from the database closest to a given date
        :param d: Datetime object
        :return:
        '''
        mycursor = mydb.cursor()
        sql = "SELECT * from " + mysqlCredentials.userstats_health + " WHERE DATE(datum) <= '" + d.strftime("%Y-%m-%d") + "' ORDER BY datum DESC LIMIT 1"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        rv = 0
        if len(myresult)>0:
            rv = myresult[0]
        else:
            print("Error: No vital infos found. Please make sure vital infos dated before activity date are available")
        return rv