import datetime

import customtkinter

import SingleActivityTools
import Utils
import mysqlCredentials
import mysqltools
import plotUtils
import tpUtils
from TrainingPlan import TrainingPlan
from framedTable import framedTable
from framedArea import framedArea
from lcarsButton import lcarsButton
from plotList import plotList
from gui2.framedBoxes import framedBoxes

import lcarsSettings





class main_trainingplan():
    def __init__(self, mydb):
        super().__init__()

        def updateRightFrame():
            rightFrame = framedArea(main, lcarsSettings.magenta)
            rightFrame.grid(column=1, row=0, padx=10, pady=10, sticky="nsew")
            sel = planList.get()
            tpList = []
            for single in sel:
                tp = TrainingPlan()
                tp.fillFromMYSQLDatabase(mydb, single)
                tpList.append(tp)

            fig, ax = tpUtils.plotTrainingsplan(tpList, withcurrentData=True, mydb=mydb)

            plotUtils.setAxisColor(ax, lcarsSettings.yellow)
            rightFrame.plot = plotList(rightFrame, [fig])
            rightFrame.plot.grid(row=1, column=0, padx=10, pady=20, sticky="nsw")

            weekFrame = framedArea(rightFrame, lcarsSettings.blue)
            weekFrame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

            wl = tp.getTrainingWeeks()
            i = 0
            cw = Utils.getCalendarWeekFromDate(datetime.date.today())
            for w in wl:
                wi = w.display(weekFrame, calendarWeekToBeBold=cw, dbHandler=mydb)
                wi.grid(row=0, column=i+1, padx=5,pady=10, sticky="ns")
                i=i+1

            tt = customtkinter.CTkLabel(weekFrame, text="Mon \n Tue \n Wed \n Thu \n Fri \n Sat \n Sun", text_color=lcarsSettings.ice)
            tt.grid(row=0, column=0, padx=10, pady=10, sticky="ns")


        main = customtkinter.CTk()

        main.title("The NerdRunner Project - TNRP - Trainingplan")

        screen_width = main.winfo_screenwidth()
        screen_height = main.winfo_screenheight()
        main.geometry(str(1.5*int(3*screen_width/4)) + "x" + str(int(3*screen_height/4)))

        main.configure(fg_color="black")



        leftFrame = framedArea(main,lcarsSettings.yellow, title="Training plans")
        leftFrame.grid(column=0, row=0, padx=10, pady=10)
        buttTPList = lcarsButton(leftFrame, "Update", lcarsSettings.yellow)
        buttTPList.grid(column=0, row=1, padx=10, pady=10)
        buttTPList.configure(command=lambda: updateRightFrame())

        tpList = mysqltools.getActivitiesAndNumber(mydb, justNames=True, table=mysqlCredentials.trainingplantable)
        #al = mysqltools.getActivitiesAndNumber(mydb, justNames=True) TDO: Prüfen, wieso bei al in der Checkbox keine geschweiften Klammern dargestellt werden


        planList = framedBoxes(leftFrame,"Plans", tpList, lcarsSettings.yellow, None, False, autocheck=False)
        planList.grid(column=0, row=2, padx=10, pady=10)

        main.mainloop()

#mydb = mysqltools.connect()

#tpList = mysqltools.getActivitiesAndNumber(mydb, justNames=True, table="trainingplan")
#test = tpUtils.getTrainingplan(mydb, "Osterbackyard 2023")
#print(test)

#nm = main_trainingplan(mydb)

#t = TrainingPlan()
#t.fillFromMYSQLDatabase(mydb, "Osterbackyard 2023")
#ll = t.splitWeeks()
#wl = t.getTPList(mydb)
#t.getActivities(mydb)
#tpUtils.splitTP(t, mydb)

#print(t.splittedWeeks)


