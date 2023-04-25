import datetime

import mysqltools
from Activity import Activity
from Sportsman import Sportsman
from importUtils import FitFileToTPList



f = '/home/simon/ownCloud/clientsync/NerdRunner/garmin-connect-export-master/MyActivities/activity_10831909205.fit'
t2 = FitFileToTPList(f)
act = Activity(t2)
act.print()
#rv = act.calculateTRIMP()
mydb = mysqltools.connect()
act.addActivitytoDatabse(mydb)

#sm = Sportsman()

#sm.addToDatabase(182,40)
#rv = sm.getHRValues(datetime.datetime.today() - datetime.timedelta(2))

#print(rv)


