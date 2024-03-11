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



        def updatePlotFrames():

            activitytype = activityFrame.get()
            years = yearFrame.get()
            if(len(years)==0):
                years=yearFrame.values
            lowerFrame = framedArea(surroundingFrame, lcarsSettings.magenta)
            lowerFrame.grid(column=0, row=1, padx=10, pady=10, sticky="nsew")

            d1=datetime.date(years[0],1,1)
            d2 = datetime.date(years[len(years)-1], 12, 31)
            d1curr = datetime.date(datetime.date.today().year, 1, 1)
            d2curr = datetime.date(datetime.date.today().year, 12, 31)
            distlist = [10000, 21100, 42195, 100000]
            recordList = []
            recordListcurr = []
            for d in distlist:
                filter = [mysqlCredentials.cn_distance, d*0.95, d*1.05]
                res = mysqltools.getActivitiesByDateRange(mydb,activitytype,d1, d2, filter, orderValue="duration", orderType="ASC", limit="10")
                recordList.append([[s[2], s[4], s[9]] for s in res])

                rescurr = mysqltools.getActivitiesByDateRange(mydb, activitytype, d1curr, d2curr, filter, orderValue="duration",orderType="ASC", limit="1")
                recordListcurr.append([[s[2], s[4], s[9]] for s in rescurr])
            i=0
            for r in recordList:
                recordFrame = framedArea(lowerFrame,lcarsSettings.green)
                recordFrame.grid(column=i, row=0, padx=10, pady=10, sticky="nsew")
                tx = CTkLabel(recordFrame, text=str(distlist[i]/1000)+"km", text_color=lcarsSettings.yellow, fg_color="black")
                tx.grid(column=0, row=0, padx=10, pady=(10,1), sticky="nsew")
                j=1
                for t in r:
                    dy = t[0].strftime('%d.%m.%Y')
                    tx = CTkLabel(recordFrame,text=dy, text_color=lcarsSettings.yellow, fg_color="black")
                    tx.grid(column=0, row=j, padx=10, pady=2, sticky="nsew")
                    dur = str(datetime.timedelta(seconds=t[2]))
                    tx = CTkLabel(recordFrame, text=dur, text_color=lcarsSettings.yellow, fg_color="black")
                    tx.grid(column=1, row=j, padx=10, pady=2, sticky="nsew")
                    j=j+1
                if(len(recordListcurr[i])>0):
                    dy = recordListcurr[i][0][0].strftime('%d.%m.%Y')
                    tx = CTkLabel(recordFrame, text=dy, text_color=lcarsSettings.yellow, fg_color="black")
                    tx.grid(column=0, row=j+1, padx=10, pady=(0,10), sticky="nsew")
                    dur = str(datetime.timedelta(seconds=recordListcurr[i][0][2]))
                    tx = CTkLabel(recordFrame, text=dur, text_color=lcarsSettings.yellow, fg_color="black")
                    tx.grid(column=1, row=j+1, padx=10, pady=(0,10), sticky="nsew")

                tx = CTkLabel(recordFrame, text=" ", text_color=lcarsSettings.yellow, fg_color="black")
                tx.grid(column=0, row=j, padx=10, pady=(1,1), sticky="nsew")
                i=i+1

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


#mydb = mysqltools.connect()
#nm = main_records(mydb)

#yy = mysqltools.getYears(mydb)
#print(yy)