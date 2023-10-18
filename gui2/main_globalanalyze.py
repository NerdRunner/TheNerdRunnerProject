import datetime
import os
from tkinter import PhotoImage

import customtkinter
from customtkinter import CTkButton, CTkLabel
import tkinter as tk

import SingleActivityTools
import Utils
import mysqltools
import plotUtils
from framedTable import framedTable
from framedArea import framedArea
from gui2.framedBoxes import framedBoxes
from lcarsButton import lcarsButton
from plotList import plotList

import lcarsSettings

class main_globalanalyze():
    def __init__(self, mydb):
        super().__init__()



        def updateCumulativePlotFrame():

            type = activityFrame.get()
            years = yearFrame.get()

            lowerFrame = framedArea(surroundingFrame, lcarsSettings.blue)
            lowerFrame.grid(column=0, row=1, padx=10, pady=10, sticky="nsew")
            yearList = yearFrame.get()
            data = mysqltools.getCummulativeDistances(mydb, years, type)
            fig, ax = plotUtils.plotXY(data, legend=yearList)

            if (fig != None):
                lowerFrame.plot = plotList(lowerFrame, [fig])
                lowerFrame.plot.grid(row=0, column=0, padx=10, pady=10, sticky="nsw")
                plotUtils.setAxisColor(ax, lcarsSettings.yellow)

            doy = Utils.dayOfYear(datetime.datetime.today(), type="dt")
            ax.axvspan(doy-1, doy+1, facecolor=lcarsSettings.ice, alpha=0.5, zorder=-100)
            currkm = []
            st = "Total km until today:"+"\n"
            i=0
            for d in data:
                currkm.append(d[doy])
                st =st+ str(yearList[i])+ " " +str('{:.2f}'.format(d[doy][1]))+"\n"
                i+=1
            frameAheadBehind=framedArea(lowerFrame, lcarsSettings.magenta)
            frameAheadBehind.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
            ll = CTkLabel(frameAheadBehind,text=st, text_color=lcarsSettings.yellow, justify="left")
            ll.grid(row=0, column=0,padx=10, pady=10)
            #TODO: Auswahl ob km, Trimp oder Dauer
            #TODO: Histogramdarstellung
            return

        main = customtkinter.CTk()

        main.title("The NerdRunner Project - TNRP - Global analysis")

        screen_width = main.winfo_screenwidth()
        screen_height = main.winfo_screenheight()
        main.geometry(str(1.5*int(3*screen_width/4)) + "x" + str(int(3*screen_height/4)))

        main.configure(fg_color="black")

        surroundingFrame = framedArea(main, lcarsSettings.yellow)
        surroundingFrame.grid(column=0, row=0, padx=10, pady=10,  sticky="nsew")

        checkBoxFrame = framedArea(surroundingFrame, lcarsSettings.blue)
        checkBoxFrame.grid(column=0, row=0, padx=10, pady=10, sticky="new")
        yearFrame = framedBoxes(checkBoxFrame, "Years", mysqltools.getYears(mydb), lcarsSettings.blue, None)
        yearFrame.button.configure(command=lambda: updateCumulativePlotFrame())
        yearFrame.grid(column=0, row=0, padx=10, pady=10, sticky="new")
        activityFrame = framedBoxes(checkBoxFrame, "Activities", mysqltools.getActivitiesAndNumber(mydb,justNames=True), lcarsSettings.blue, None, button=False, autocheck=False)
        activityFrame.grid(column=0, row=1, padx=10, pady=10, sticky="new")
        prefAct = mysqltools.getSetting(mydb, "preferredActType")[2]
        activityFrame.set([[prefAct, True]])


        upperrightFrame = framedArea(surroundingFrame, lcarsSettings.magenta)
        upperrightFrame.grid(column=1, row=0, padx=10, pady=10, sticky="nsew")

        #updateCumulativePlotFrame()

        #imger = PhotoImage(file="radius.png")
        #imger = Utils.changeColorOfImage(imger, lcarsSettings.yellowRGB)
        #t = CTkLabel(text = "bla", master=upperrightFrame, image = imger)
        #t.grid(column=0, row=0, padx=10, pady=10)


        main.mainloop()


mydb = mysqltools.connect()
#nm = main_globalanalyze(mydb)

#yy = mysqltools.getYears(mydb)
#print(yy)