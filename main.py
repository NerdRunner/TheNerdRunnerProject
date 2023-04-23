import mysqltools
from Activity import Activity
from importUtils import FitFileToTPList



f = '/home/simon/ownCloud/clientsync/NerdRunner/garmin-connect-export-master/MyActivities/activity_10831909205.fit'
t2 = FitFileToTPList(f)
act = Activity(t2)
act.print()
mydb = mysqltools.connect()
act.addActivitytoTable(mydb)

