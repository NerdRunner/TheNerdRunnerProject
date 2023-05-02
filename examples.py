import datetime

import mysqltools
from Activity import Activity
from Sportsman import Sportsman
from importUtils import FitFileToTPList

### Example 1 ### Create databases
mydb = mysqltools.connect()
mysqltools.createAllTables()

### Example 1.5 ### Add one user information to Database
mydb = mysqltools.connect()
sm = Sportsman("Nerdi", datetime.datetime(1980,5,11), "m") #Name, Day of birth, gender
sm.setGeneralValuesToDatabase(mydb)
sm.addVitalValuesToDatabase(183, 39, 73) #maxHR, restHR, weight

### Example 2 ### Add an activity to the Database
mydb = mysqltools.connect()
path = '/MyActivities/'
file = 'activity_10831909205.fit'
parsedfitFile = FitFileToTPList(path + file)
act = Activity(parsedfitFile, file, mydb)
act.print()
act.addActivitytoDatabse(mydb)