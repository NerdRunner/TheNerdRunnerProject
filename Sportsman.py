from datetime import datetime, timedelta

import mysqlCredentials
import mysqltools


class Sportsman:
    '''
    class Sportsman
    manages heart rate values
    '''

    def __init__(self):

        return

    def addHRValuesToDatabase(self, maxHR, restHR):
        '''
        Adds maxHR and restHR of today to the database
        :param hr:
        :param restHR:
        :return:
        '''

        mydb = mysqltools.connect()
        mycursor = mydb.cursor()
        sql = "INSERT INTO "+mysqlCredentials.userstats+ " VALUES (%s, %s, %s, %s)"
        val = (None, datetime.today(), maxHR, restHR)
        mycursor.execute(sql, val)
        mydb.commit()

    def getHRValues(self, d: datetime):
        '''
        Returns the HR values (max and rest HR) from the database closest to a given date
        :param d: Datetime object
        :return:
        '''
        mydb = mysqltools.connect()
        mycursor = mydb.cursor()
        sql = "SELECT * from "+mysqlCredentials.userstats+" WHERE DATE(datum) <= '" + d.strftime("%Y-%m-%d")+"'"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        td = timedelta(-1000)
        for l in myresult: #get closest to the given date
            #TODO2: Eretzen durch MYSQL syntax
            tdtemporay = l[1]-d
            if tdtemporay > td:
                td = tdtemporay
                rv = l
        return rv