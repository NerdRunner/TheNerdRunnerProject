import datetime
import os

from fitparse import FitFile

import mysqlCredentials
import mysqltools
from Activity import Activity
from Trackpoint import Trackpoint


def FitFileToTPList(f)->Trackpoint:
    '''
    Reads a .fit file and generates a list of Trackpoints
    :param f:
    :return: Trackpoint[]
    '''
    if os.path.isfile(f) and f.endswith('.fit'):
        fitfile = FitFile(f)
        tpList = []
        mess = fitfile.get_messages("session")
        for t in mess:
            typ = t.get_value("sport")
        for record in fitfile.get_messages('record'):
            tp = Trackpoint()
            tp.lat = record.get_value('position_lat')
            if tp.lat is not None:  # Wenn Koordinaten vorhanden sind
                tp.lat = tp.lat * (180 / 2147483648.0)  # Umrechnung Semicircles in Koordinaten
                tp.lon = record.get_value('position_long') * (180 / 2147483648.0)
            ts = record.get_value('timestamp')
            if not isinstance(ts, datetime.datetime):
                ts = datetime.now()
            tp.timestamp = ts
            tp.distance = record.get_value('distance')
            tp.hr = record.get_value('heart_rate')
            tp.speed = record.get_value('enhanced_speed')
            tp.typ = typ

            tpList.append(tp)
        return tpList

def addFitFilesToDB(mydb, path):
    '''
    Adds all the fit Files to the Database.
    :return:
    '''
    dir_list = []
    dir_list += [each for each in os.listdir(path) if each.endswith('.fit')]
    dir_list = checkForMissingEntries(mydb, dir_list)
    i = 0
    nFiles = len(dir_list)
    for ff in dir_list:
        if ff.endswith('.fit'):
            imp = FitFileToTPList(path + ff)
            act = Activity(imp, ff, mydb)
            act.filename = ff
            act.addActivitytoDatabse(mydb)
            ps = act.print_short()
            print("Done: "+str(i/nFiles*100.0) + " % - Added: "+ps)
            i = i + 1
        else:
            print("Skipping: "+ff)


    return


def checkForMissingEntries(mydb, ff):
    '''
    Compares the list of given files with the one named in the database and returns the ones which are not in the database
    :param ff:
    :return:
    '''
    mycursor = mydb.cursor()

    sql = "SELECT dateiname FROM "+mysqlCredentials.activitytable
    mycursor.execute(sql)
    sqlresult = mycursor.fetchall()

    srList = []
    for sr in sqlresult: #convert to list
        srList.append(sr[0])

    delta = set(ff) - set(srList) #difference between list in mysql database and files in folder
    return delta