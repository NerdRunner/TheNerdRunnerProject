import importUtils
import mysqltools
mydb = mysqltools.connect()


path = '/home/simon/ownCloud/clientsync/NerdRunner/garmin-connect-export-master/MyActivities/'
file =  'activity_10831909205.fit'
importUtils.addFitFilesToDB(mydb, path)

print("ende")


