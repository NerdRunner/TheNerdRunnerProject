import mysqltools
from Activity import Activity
from importUtils import FitFileToTPList

### Example 1 ### Add one activity to Database
f = '/MyActivities/activity_10831909205.fit'
parsedfitFile = FitFileToTPList(f)
act = Activity(parsedfitFile)
act.print()
mydb = mysqltools.connect()
act.addActivitytoTable(mydb)