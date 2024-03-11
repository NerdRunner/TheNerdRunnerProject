import datetime
import os

from fitparse import FitFile

import mysqlCredentials
import mysqltools
from Activity import Activity
from Trackpoint import Trackpoint

import gpxpy
from tcxreader.tcxreader import TCXReader, TCXTrackPoint


def FitFileToTPList(f)->Trackpoint:
    '''
    Reads a .fit file and generates a list of Trackpoints
    :param f:
    :return: Trackpoint[]
    '''
    if os.path.isfile(f) and f.endswith('.fit'):
        fitfile = FitFile(f)
        tpList = []
        lapList=[]
        mess = fitfile.get_messages("session")
        for t in mess:
            typ = t.get_value("sport")
            totalTime=t.get_value("total_timer_time") #TODO: Prüfen, ob das auch die Nettozeit und nicht die Bruttozeit ist
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
            tp.totalTime = totalTime


            if tp.lat is None: #If no gpsdata is available, e.g. indoor swimming, get the distance from the laps
                d = 0
                for lap in fitfile.get_messages('lap'):
                    dl= lap.get_value('total_distance')
                    if dl is None:
                        dl=0
                    d+=dl
                tp.distance = d

            tpList.append(tp)

        return tpList

def addFitFilesToDB(mydb, path):
    '''
    Adds all the fit Files in the path (folder) to the Database.
    Files already in the Database are omitted.
    :return:
    '''
    dir_list = []
    dir_list += [each for each in os.listdir(path) if each.endswith('.fit')]
    dir_list = checkForMissingEntries(mydb, dir_list)
    i = 0
    nFiles = len(dir_list)
    for ff in dir_list:
        #if ff.endswith('.fit'):
            imp = FitFileToTPList(path + ff)
            act = Activity(imp, ff, mydb)
            act.filename = ff
            act.addActivitytoDatabse(mydb)
            ps = act.print_short()
            print("Done: "+str(i/nFiles*100.0) + " % - Added: "+ps)
            i = i + 1
        #else:
         #   print("Skipping: "+ff)
    return

def addFitFilesToDBWithStatus(mydb, path, app, rv):
    '''
    Adds all the fit Files in the path (folder) to the Database.
    Files already in the Database are omitted.
    :param path: the path (folder)
    :param rv: tkinter label to set the current progress
    :return:
    '''
    dir_list = []
    dir_list += [each for each in os.listdir(path) if each.endswith('.fit')]
    dir_list = checkForMissingEntries(mydb, dir_list)
    i = 0
    nFiles = len(dir_list)
    rv.configure(text="Adding "+str(nFiles) +" Activities")
    app.update()
    for ff in dir_list:
            imp = FitFileToTPList(path + ff)
            act = Activity(imp, ff, mydb)
            act.filename = ff
            act.addActivitytoDatabse(mydb)
            percentage = i/nFiles*100.0
            percentage = "{:4.2f}".format(percentage)
            rv.configure(text=str(percentage) + " % done" )
            app.update()
            i = i + 1
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

def GPXFileToActivity(mydb, path):
    dir_list = []
    dir_list += [each for each in os.listdir(path) if each.endswith('.gpx')]#and each.startswith('Move')]
    dir_list = checkForMissingEntries(mydb, dir_list)
    i = 0
    nFiles = len(dir_list)
    for ff in dir_list:
    #if os.path.isfile(f) and f.endswith('gpx'):
        gpx_file = open(path+ff)
        gpx = gpxpy.parse(gpx_file)
        tpl = []
        strecke = gpx.length_3d()
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    tp = Trackpoint()
                    tp.timestamp = point.time
                    tp.lat = point.latitude
                    tp.lon = point.longitude
                    tp.distance = strecke
                    typ = point.type
                    if typ == None:
                        typ = 'running'

                    tp.typ = typ
                    hr = '0'
                    try:
                        hr = point.extensions[0][1].text
                    except:
                        hr = '0'
                    tp.hr = float(hr)
                    tp.speed = point.speed

                    tpl.append(tp)
               # tp.hr = point.
                #print(f'Point at ({point.latitude},{point.longitude}) -> {point.time}')
                #print(hr)
        if len(tpl) > 0:
            act = Activity(tpl, ff, mydb)

            act.filename = ff
            act.addActivitytoDatabse(mydb)
            ps = act.print_short()
            print(ps)
        else:
            print("Not imported: " + ff)


    return

def TCXFileToWorkout(mydb, path):
    dir_list = []
    dir_list += [each for each in os.listdir(path) if each.endswith('.tcx') or each.endswith('.tcx2')]
    dir_list = checkForMissingEntries(mydb, dir_list)
    i = 0
    nFiles = len(dir_list)
    for ff in dir_list:
        #if os.path.isfile(ff) and (ff.endswith('.tcx') or ff.endswith('.tcx2')):
            reader = TCXReader()
            data = reader.read(path+ff)
            tpl = []
            for singleTP in data.trackpoints:
                tp = Trackpoint()
                tp.lat = singleTP.latitude
                tp.lon = singleTP.longitude
                tp.distance = singleTP.distance
                tp.hr = singleTP.hr_value
                tp.timestamp = singleTP.time
                tp.typ = data.activity_type.lower()
                tpl.append(tp)
            if len(tpl)>0:
                act = Activity(tpl, ff, mydb)

                act.filename = ff
                act.addActivitytoDatabse(mydb)
                ps = act.print_short()
                print(ps)
            else:
                print("Not imported: "+ff)
    return

def reimportAllData():
    '''
    Re-Imports all data (specific function for Simon
    :return:
    '''
    mydb = mysqltools.connect()
    TCXFileToWorkout(mydb, "/home/simon/Nextcloud/clientsync/Dokumente/laufen/garmin/")
    GPXFileToActivity(mydb, "/home/simon/Nextcloud/clientsync/Dokumente/laufen/garmin/")
    mysqltools.deleteDoubleEntries(mydb)

    return


#mydb = mysqltools.connect()
#TCXFileToWorkout(mydb, "/home/simon/Nextcloud/clientsync/Dokumente/laufen/garmin/")
#GPXFileToActivity(mydb, "/home/simon/Nextcloud/clientsync/Dokumente/laufen/garmin/")
#print("Import")