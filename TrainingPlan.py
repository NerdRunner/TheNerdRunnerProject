import datetime
import typing

import mysqlCredentials
import mysqltools
import tpUtils
from TrainingWeek import TrainingWeek
from enums.TPType import TPType


class TrainingPlan:
    '''
    TP has to start on a Monday and has to end on a Sunday
    '''

    kindlist = ["training", "rest", "tapering", "race"]
    tp = 0
    splitFactorsStandard = [0, 0.15, 0, 0.3, 0.1, 0, 0.45]
    splittedWeeks = []


    '''
    Class for a trainingplan
    '''
    def __init__(self, activity = "running"):
        self.activityType = activity
        self.splitFactors = TrainingPlan.splitFactorsStandard


    def __str__(self):
        rv = self.name + "\nStart: "+str(self.start)+"\nEnd: "+str(self.end) +"\nType: "+self.activityType
        return rv

    def fillFromMYSQLDatabase(self, mydb, name):
        '''
        Fills the Trainingplan with data from the Database
        :param mydb:
        :param name: Name of the Trainingsplan
        :return:
        '''

        res = []
        self.name = name
        mycursor = mydb.cursor()
        for kind in self.kindlist:
            sql = "SELECT * from " + mysqlCredentials.trainingplantable + " WHERE typ='" + name + "' and kind='" + kind + "' ORDER by datum ASC"
            mycursor.execute(sql)
            myresult = mycursor.fetchall()
            res.append(myresult)

        self.tp = res
        self.start = res[0][0][2]
        self.end = res[3][0][2]
        self.list = self.getTPList(mydb)
        self.splittedWeeks = self.priv_splitIntoTrainingWeeks()

    def getActivitiesAccordingToTrainingplan(self, mydb):
        '''
        Gets the activities according to the daterange in the Trainingplan and sums them up for each week
        :param mydb:
        :return:
        '''
        tpList = self.getTPList(mydb)
        d1 = tpList[0][0] - datetime.timedelta(days=6)
        d2 = tpList[0][0]
        summedActs = []
        i=0
        while i < len(tpList):
            actsWeek = mysqltools.getActivitiesByDateRange(mydb, [self.activityType], d1, d2)
            sum = 0
            for a in actsWeek:
                sum+=a[4]
            summedActs.append([d2, sum])

            if i<len(tpList)-1:
                d1 = tpList[i][0] + datetime.timedelta(days=1)
                d2 = tpList[i+1][0]
            i=i+1
        return summedActs

    def getTPList(self, mydb):
        '''
        Gets the Elements of the Trainingsplan ordered by Date
        :param mydb:
        :return: List
        '''
        mycursor = mydb.cursor()

        sql = "SELECT datum, strecke, kind from " + mysqlCredentials.trainingplantable + " WHERE typ='" + self.name + "' ORDER by datum ASC"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()

        return myresult

    def priv_splitIntoTrainingWeeks(self, splitFactors = None)->[TrainingWeek]:
        '''
        Splits the weeks of the trainingsplan to a daily basis and creates a list of TrainingWeeks
        :param: splitFactors: List of percentages for each day. E.g. [0, 0.15, 0, 0.3, 0.1, 0, 0.45]
        :return: [TrainingWeek]
        '''
        twList = []
        if splitFactors == None:
            splitFactors = self.splitFactors
        for w in self.list:
            km = float(w[1])
            weekkm = [km * x for x in splitFactors]
            tw = TrainingWeek(w[0], w[2], weekkm)
            twList.append(tw)

        return twList

    def getTrainingWeeks(self)->typing.List[TrainingWeek]:
        return self.splittedWeeks


