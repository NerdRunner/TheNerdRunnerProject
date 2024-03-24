import datetime
import math
import os
import calendar
from tkinter import PhotoImage

import customtkinter
import matplotlib
import numpy as np
from customtkinter import CTkButton, CTkLabel
import tkinter as tk

from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.figure import Figure

import SingleActivityTools
import Utils
import mysqlCredentials
import mysqltools
import plotUtils
from framedTable import framedTable
from framedArea import framedArea
from gui2.framedBoxes import framedBoxes
from lcarsButton import lcarsButton
from plotList import plotList

import lcarsSettings





class main_records():
    def __init__(self, mydb):
        super().__init__()

        def getRecordsAccordingToParams(limit="10", orderby = "duration"):
            '''
            gets the records according to the params set in the gui
            :return: recordList, recordListcurr, params
            '''
            params = getRecordParameters()
            activitytype = params[0]
            d1 = params[2]
            d2 = params[3]
            d1curr = params[4]
            d2curr = params[5]
            distlist = params[6]
            recordList = []
            recordListcurr = []
            for d in distlist:
                filter = [mysqlCredentials.cn_distance, d * 0.95, d * 1.05]
                res = mysqltools.getActivitiesByDateRange(mydb, activitytype, d1, d2, filter, orderValue=orderby,
                                                          orderType="ASC", limit=limit)
                recordList.append([[s[2], s[4], s[9]] for s in res])

                rescurr = mysqltools.getActivitiesByDateRange(mydb, activitytype, d1curr, d2curr, filter,
                                                              orderValue="duration", orderType="ASC", limit="1")
                recordListcurr.append([[s[2], s[4], s[9]] for s in rescurr])
            return recordList, recordListcurr, params
        def createRecordFrame(parentFrame):

            recordList, recordListcurr, params= getRecordsAccordingToParams()
            distlist = params[6]
            i = 0
            for r in recordList:
                recordFrame = framedArea(parentFrame, lcarsSettings.green)
                recordFrame.grid(column=i, row=0, padx=10, pady=10, sticky="nsew")
                tx = CTkLabel(recordFrame, text=str(distlist[i] / 1000) + "km", text_color=lcarsSettings.yellow,
                              fg_color="black")
                tx.grid(column=0, row=0, padx=10, pady=(10, 1), sticky="nsew")
                j = 1
                for t in r:
                    dy = t[0].strftime('%d.%m.%Y')
                    tx = CTkLabel(recordFrame, text=dy, text_color=lcarsSettings.yellow, fg_color="black")
                    tx.grid(column=0, row=j, padx=10, pady=2, sticky="nsew")
                    dur = str(datetime.timedelta(seconds=t[2]))
                    tx = CTkLabel(recordFrame, text=dur, text_color=lcarsSettings.yellow, fg_color="black")
                    tx.grid(column=1, row=j, padx=10, pady=2, sticky="nsew")
                    j = j + 1
                if (len(recordListcurr[i]) > 0):
                    dy = recordListcurr[i][0][0].strftime('%d.%m.%Y')
                    tx = CTkLabel(recordFrame, text=dy, text_color=lcarsSettings.yellow, fg_color="black")
                    tx.grid(column=0, row=j + 1, padx=10, pady=(0, 10), sticky="nsew")
                    dur = str(datetime.timedelta(seconds=recordListcurr[i][0][2]))
                    tx = CTkLabel(recordFrame, text=dur, text_color=lcarsSettings.yellow, fg_color="black")
                    tx.grid(column=1, row=j + 1, padx=10, pady=(0, 10), sticky="nsew")

                tx = CTkLabel(recordFrame, text=" ", text_color=lcarsSettings.yellow, fg_color="black")
                tx.grid(column=0, row=j, padx=10, pady=(1, 1), sticky="nsew")
                i = i + 1

        def createSingleRunFrame(rightFrame):
            '''
            Creates the frame where the time for all runs for a given distance is plotted over time
            :param rightFrame:
            :return:
            '''
            recordList, recordListcurr, params = getRecordsAccordingToParams(limit="1000000", orderby="datum")
            i=0
            for data in recordList:
            #data=recordList[0]
                dt = [[[d[0].date(),d[2]/60/60] for d in data]]
                fig, ax = plotUtils.plotXY(dt, legend=str(params[6][i]/1000))
                fig.set_figheight(1.0)
                fig.tight_layout()
                rightFrame.plot = plotList(rightFrame, [fig])
                rightFrame.plot.grid(row=i, column=0, padx=10, pady=0, sticky="nsw")
                plotUtils.setAxisColor(ax, lcarsSettings.yellow)
                i+=1
            pass

        def getRecordParameters():
            '''
            gets the record parameters according to the preferences (type, year, etc.) in the GUI
            :return:
            '''
            activitytype = activityFrame.get()
            years = yearFrame.get()
            if (len(years) == 0):
                years = yearFrame.values

            d1 = datetime.date(years[0], 1, 1)
            d2 = datetime.date(years[len(years) - 1], 12, 31)
            d1curr = datetime.date(datetime.date.today().year, 1, 1)
            d2curr = datetime.date(datetime.date.today().year, 12, 31)
            distlist = [10000, 21100, 42195, 100000]
            return[activitytype, years, d1, d2, d1curr, d2curr, distlist]

        def updatePlotFrames():

            lowerFrame = framedArea(surroundingFrame, lcarsSettings.magenta)
            lowerFrame.grid(column=0, row=1, padx=10, pady=10, sticky="nsew")

            createRecordFrame(lowerFrame)

            rightFrame = framedArea(surroundingFrame, lcarsSettings.ice)
            rightFrame.grid(column=1, row=0, rowspan=2, padx=10, pady=10, sticky="nsew")

            createSingleRunFrame(rightFrame)
            return

        main = customtkinter.CTk()

        main.title("The NerdRunner Project - TNRP - Records")

        screen_width = main.winfo_screenwidth()
        screen_height = main.winfo_screenheight()
        main.geometry(str(1.5*int(3*screen_width/4)) + "x" + str(int(3*screen_height/4)))

        main.configure(fg_color="black")

        surroundingFrame = framedArea(main, lcarsSettings.yellow)
        surroundingFrame.grid(column=0, row=0, padx=10, pady=10,  sticky="nsew")

        checkBoxFrame = framedArea(surroundingFrame, lcarsSettings.blue)
        checkBoxFrame.grid(column=0, row=0, padx=10, pady=10, sticky="new")
        yearFrame = framedBoxes(checkBoxFrame, "Years", mysqltools.getYears(mydb), lcarsSettings.blue, None, autocheck=False)
        yearFrame.button.configure(command=lambda: updatePlotFrames())
        yearFrame.grid(column=0, row=0, padx=10, pady=10, sticky="new")

        al = mysqltools.getActivitiesAndNumber(mydb,justNames=True)
        activityFrame = framedBoxes(checkBoxFrame, "Activities", al, lcarsSettings.blue, None, button=False, autocheck=False)
        activityFrame.grid(column=0, row=1, padx=10, pady=10, sticky="new")
        prefAct = mysqltools.getSetting(mydb, "preferredActType")[2]
        activityFrame.set([[prefAct, True]])

        updatePlotFrames()




        main.mainloop()





mydb = mysqltools.connect()
nm = main_records(mydb)

#yy = mysqltools.getYears(mydb)
#print(yy)