import mysqltools
from Activity import Activity
from Sportsman import Sportsman
from importUtils import FitFileToTPList

### Example 1 ### Create databases
mydb = mysqltools.connect()
mysqltools.createActivityTable()
mysqltools.createUserTable()

### Example 1.5 ### Add at least one user information to db
sm = Sportsman()
sm.addHRValuesToDatabase(183, 39)

### Example 2 ### Add an activity to the Database
f = '/MyActivities/activity_10831909205.fit'
parsedfitFile = FitFileToTPList(f)
act = Activity(parsedfitFile)
act.print()
mydb = mysqltools.connect()
act.addActivitytoDatabse(mydb)