import datetime
import os

from fitparse import FitFile

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
            #else:  # Ansonten alles 0er Koordinaten
            #    tp.lat = 0
            #    tp.lon = 0
            ts = record.get_value('timestamp')
            if not isinstance(ts, datetime.datetime):
                ts = datetime.now()
            tp.timestamp = ts
            tp.distance = record.get_value('distance')
            tp.hr = record.get_value('heart_rate')
            tp.speed = record.get_value('enhanced_speed')
            # if record.get_value('activity_type') !=None:
            #    tp.typ = record.get_value('activity_type')
            # else:
            #    tp.typ = "0"
            tp.typ = typ

            tpList.append(tp)
        return tpList

#f = '/home/simon/ownCloud/clientsync/NerdRunner/garmin-connect-export-master/MyActivities/activity_10831909205.fit'

#t2 = FitFileToTPList(f)
#act = Activity(t2)

#act.print()

#print("ende")
