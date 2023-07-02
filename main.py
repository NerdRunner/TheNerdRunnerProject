import datetime
import numpy as np
import Utils
import activityMetrics
import importUtils
import mysqlCredentials
import mysqltools
import plotUtils

mydb = mysqltools.connect()


path = '/home/simon/ownCloud/clientsync/NerdRunner/garmin-connect-export-master/MyActivities/'
file =  'activity_10831909205.fit'
#importUtils.addFitFilesToDB(mydb, path)

#td = Utils.getCalendarWeekFromDate(datetime.datetime.today())
d1, d2= Utils.getDateRangeFromWeek(2023, 18)
#print(d1, d2)
#print(Utils.dayOfYear(datetime.datetime.today()))

#currcw = Utils.getCalendarWeekFromDate(datetime.datetime.today())
#p = plotUtils.totalperWeekPlot(mydb,mysqlCredentials.cn_trimp,2023,1, currcw)

#last = mysqltools.getLastActivities(mydb,["running","cycling"], 5)
#tl = mysqltools.getActivitiesAndNumber(mydb)
#avg = activityMetrics.averageTrimps(mydb,datetime.datetime.today(), 100)
#ctl = activityMetrics.calculateDayCTL(mydb, datetime.datetime.today())
#print(avg, ctl)
#mysqltools.getFitFiles()
#mysqltools.createSettingsTable(mydb)
#activityMetrics.summary(mydb, mysqlCredentials.)
#ll = mysqltools.getActivitiesByDateRange(mydb, "running", d1, d2)
#ll = activityMetrics.summary(mydb, "running" d1, d2)
#print(mysqltools.getSetting(mydb, "wetter"))
#print(ll)


