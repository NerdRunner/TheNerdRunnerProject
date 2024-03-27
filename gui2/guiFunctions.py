import calendar
import datetime
from time import strftime

import customtkinter

import activityMetrics
import importUtils
import mysqlCredentials
import mysqltools
import plotUtils
import lcarsSettings
from plotList import plotList
from framedTable import framedTable
from framedBoxes import framedBoxes


def gui_getFitFiles(app, mydb, label):
    '''
    Imports the Fit Files and gives Feedback to a textfield
    :param self:
    :param mydb:
    :param label:
    :return:
    '''
    label.configure(text="Importing Fit Files ...")
    app.update()
    mysqltools.getFitFiles(mydb)
    label.configure(text="Importing done.")


def createUpperPlots(main, mydb, preserveSettings=False):
    upperTable = framedTable(main, "titel2", ('Date', 'Type', 'Distance', 'Mean HR', 'Trimp'), lcarsSettings.blue)
    lastAct = mysqltools.getLastActivities(mydb, ["*"], 10)
    upperTable.insertMySQLTableValues(lastAct)
    upperTable.grid(column=1, row=1, padx=10, pady=10)
    if preserveSettings:
        sel = main.actBoxes.get()
    actList = mysqltools.getActivitiesAndNumber(mydb)

    if preserveSettings:
        main.actBoxes = framedBoxes(main, "titel", actList, lcarsSettings.blue, upperTable, autocheck=False)
        tl = []
        for s in sel:
            tl.append([s, True])
        main.actBoxes.set(tl)
    else:
        main.actBoxes = framedBoxes(main, "titel", actList, lcarsSettings.blue, upperTable, autocheck=False)
        prefAct = mysqltools.getSetting(mydb, "preferredActType")[2]
        main.actBoxes.set([[prefAct, True]])
    main.actBoxes.grid(column=0, row=1, padx=10, pady=10)

def createLowerPlots(app, mydb, currcw, actList):
    backWeeks = 0
    if currcw>1:
        backWeeks = currcw
    if currcw>10:
        backWeeks = 11
    currYear = datetime.datetime.today().year
    app.fig, app.ax = plotUtils.totalperWeekPlot(mysqltools.connect(), mysqlCredentials.cn_trimp, currYear, currcw - backWeeks+1,
                                                 currcw, actList)
    plotUtils.setAxisColor(app.ax, lcarsSettings.yellow)


    app.fig2, app.ax2 = plotUtils.PMC(mydb, datetime.datetime.today(), 100, actList)


    plotUtils.setAxisColor(app.ax2, lcarsSettings.yellow)

    app.plot = plotList(app, [app.fig, app.fig2])
    app.plot.grid(row=1, column=0, padx=10, pady=20, sticky="nsw")


def createRightFrame(main, mydb, actList):
    subFrame = customtkinter.CTkFrame(main, fg_color="black")
    subFrame.grid(column=0, row=1, padx=10, pady=10)
    textFieldRight = customtkinter.CTkLabel(subFrame, text="Summary", text_color=lcarsSettings.yellow, justify="left")
    textFieldRight.grid(column=0, row=0, padx=10, pady=10, sticky="nw")
    today = datetime.datetime.today()
    #actList = ["running"]
    currCTL = activityMetrics.calculateDayCTL(mydb, today, actList)
    currATL = activityMetrics.calculateDayATL(mydb, today, actList)
    monotony = activityMetrics.monotony(mydb,today, actList)
    sum = "Current stats:\n\n"
    sum += "CTL: " + "{:4.2f}".format(currCTL) + "\n"
    sum += "ATL: " + "{:4.2f}".format(currATL) + "\n"
    sum += "TSB: " + "{:4.2f}".format(currCTL - currATL) + "\n"
    sum += "Ratio (0.8-1.3): " + "{:4.2f}".format(currATL / currCTL) + "\n"
    sum += "Monotony: (< 1.5): " + "{:4.2f}".format(monotony) + "\n"
    textFieldRight.configure(text=sum)

    #### Comparison weekly/monthly stats ###
    textFieldRight2 = customtkinter.CTkLabel(subFrame, text="Comparison weekly/monthly stats", text_color=lcarsSettings.yellow, justify="left")
    textFieldRight2.grid(column=0, row=1, padx=10, pady=10, sticky="nw")
    delta = 0
    sum=[]
    actType = mysqltools.getSetting(mydb, "preferredActType")[2]

    while delta<10:
        d1 = today - datetime.timedelta(days=31*delta)
        d2 = calendar.monthrange(d1.year, d1.month)
        startdate = datetime.date(d1.year, d1.month, 1)
        enddate = datetime.datetime(d1.year, d1.month, d2[1])
        cm = activityMetrics.summary(mydb, actList, startdate ,enddate)
        cm.insert(0,d1.month)
        cm.insert(0,d1.year)
        sum.append(cm)
        delta+=1

    #yearly summary
    tf2 = "" #String für Ausgabe zusammenstückeln
    sumYear = activityMetrics.summaryYearly(mydb, [actType], [today.year, today.year-1, today.year-2])
    tf2+=sumYear[1]
    # Calculate relavtive values
    for i, ll in enumerate(sum):
        if(i<len(sum)-1):
            s=float(sum[i+1][2])
            if s==0:
                s=-1
            relkm = float(ll[2])/s*100
            relkm = "{:2.0f}".format(relkm)+"%"
            s = float(sum[i + 1][4])
            if s==0:
                s=-1
            relTrimp = float(ll[4]) / s * 100
            relTrimp = "{:2.0f}".format(relTrimp)+"%"
            tf =[ll[0], ll[1], ll[2], relkm, ll[4], relTrimp]
            tf2+= str(ll[1])+"/"+str(ll[0])+": "+ll[2]+"km ("+relkm+") - "+str(ll[4])+" aTr ("+relTrimp+")\n"
    textFieldRight2.configure(text=tf2)
