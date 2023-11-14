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

class main_globalanalyze():
    def __init__(self, mydb):
        super().__init__()



        def updatePlotFrames():

            activitytype = activityFrame.get()
            years = yearFrame.get()
            datatype = datatoDisplay.get()
            if(len(datatype)>0):
                datatype=datatype[0]
            lowerFrame = framedArea(surroundingFrame, lcarsSettings.blue)
            lowerFrame.grid(column=0, row=1, padx=10, pady=10, sticky="nsew")
            yearList = yearFrame.get()
            data = mysqltools.getCummulativeValues(mydb, years, activitytype, datatype)
            fig, ax = plotUtils.plotXY(data, legend=yearList)

            if (fig != None):
                lowerFrame.plot = plotList(lowerFrame, [fig])
                lowerFrame.plot.grid(row=0, column=0, padx=10, pady=10, sticky="nsw")
                plotUtils.setAxisColor(ax, lcarsSettings.yellow)

            doy = Utils.dayOfYear(datetime.datetime.today(), type="dt")
            ax.axvspan(doy-1, doy+1, facecolor=lcarsSettings.ice, alpha=0.5, zorder=-100)
            currkm = []
            st = "Total values until today:"+"\n"
            i=0
            for d in data:
                currkm.append(d[doy])
                st =st+ str(yearList[i])+ " " +str('{:.2f}'.format(d[doy][1]))+"\n"
                i+=1
            frameAheadBehind=framedArea(lowerFrame, lcarsSettings.magenta)
            frameAheadBehind.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
            ll = CTkLabel(frameAheadBehind,text=st, text_color=lcarsSettings.yellow, justify="left")
            ll.grid(row=0, column=0,padx=10, pady=10)

            dataorg = mysqltools.getCummulativeValues(mydb, years, activitytype, datatype, cummulate=False)
            fig, ax = plotUtils.plotXY(dataorg, histogram=True)
            fig.set_figwidth(2.75)

            pp = []
            i=0
            for y in data:
                pp.append([yearList[i], y[len(y)-1][1]])
                i=i+1
            fig2, ax2 = plotUtils.plotXY([pp])
            ax2.yaxis.grid(linestyle='--', color=lcarsSettings.yellow)
            if (len(yearList)>1):
                d= math.ceil((yearList[len(yearList)-1]-yearList[0])/5)
                ax2.set_xticks(np.arange(yearList[0], yearList[len(yearList)-1]+1,d))
            fig2.set_figwidth(4)
            fig2.set_figheight(2)



            if (fig != None):
                lowerrightFrame.plot = plotList(lowerrightFrame, [fig, fig2])
                lowerrightFrame.plot.grid(row=0, column=0, padx=10, pady=10, sticky="nsw")
                plotUtils.setAxisColor(ax, lcarsSettings.yellow)
                plotUtils.setAxisColor(ax2, lcarsSettings.yellow)

            #upperrightFrame -
            #https://matplotlib.org/stable/gallery/images_contours_and_fields/image_annotated_heatmap.html
            months=[1,2,3,4,5,6,7,8,9,10,11,12]
            dists = [[50,200], [40,50],[30,40],[20,30],[10,20], [5,10]]
            harvest=[]
            i=0
            while i < len(dists):
                monthList=[]
                for m in months:
                    actyear=0
                    for y in years:
                        d2 = calendar.monthrange(y, m)[1]
                        actyearRes = mysqltools.getActivitiesByDateRange(mydb, activitytype,
                                                                   datetime.date(y, m, 1), datetime.date(y, m,d2),
                                                                   filter=[mysqlCredentials.cn_distance, dists[i][0]*1000,dists[i][1]*1000])

                        actyear+= len(actyearRes)
                    monthList.append(actyear)
                mm = max(monthList)
                if(mm==0): mm=1 #Wenn keine Aktivitäten in dem Monat vorhanden sind.
                monthList = [float(i) / mm for i in monthList]

                harvest.append(monthList)
                i+=1
                #print(len(actMonth))

            cmap = (matplotlib.colors.ListedColormap(['black', 'red', 'blue','green']))
            bounds = [0, 0.0000000001, 0.26, 0.75, 1.1]
            norm = matplotlib.colors.BoundaryNorm(bounds, cmap.N)

            fig, ax = plt.subplots()
            #fig.set_figure(figsize=(4.5, 4.5), dpi=100)
            fig.set_figwidth(6)
            fig.set_figheight(3)
            #fig.tight_layout()
            #plt.subplots_adjust(left=0.125, right=1, top=1, bottom=0.4)
            im = plotUtils.heatmap(harvest, dists, months, ax=ax,cmap=cmap, norm=norm)
            texts = plotUtils.annotate_heatmap(im, valfmt="{x:.2f}")
            ax.set_facecolor("black")
            #ax.autoscale(False)
            #ax.autoscale_view('tight')
            #ax.margins(y=0, x=0)
            #plt.margins(y=0, x=0)
            #ax.set_aspect('auto')
            #ax.spines[['right', 'top']].set_visible(False)
            ax.set_aspect('auto')
            fig.set_facecolor("black")
            fig.tight_layout()
            #plt.show()


            #im = ax.imshow(harvest)
            upperrightFrame.plot = plotList(upperrightFrame, [fig])
            upperrightFrame.plot.grid(row=0, column=0, padx=10, pady=10)

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
        yearFrame = framedBoxes(checkBoxFrame, "Years", mysqltools.getYears(mydb), lcarsSettings.blue, None, autocheck=False)
        yearFrame.button.configure(command=lambda: updatePlotFrames())
        yearFrame.grid(column=0, row=0, padx=10, pady=10, sticky="new")

        activityFrame = framedBoxes(checkBoxFrame, "Activities", mysqltools.getActivitiesAndNumber(mydb,justNames=True), lcarsSettings.blue, None, button=False, autocheck=False)
        activityFrame.grid(column=0, row=1, padx=10, pady=10, sticky="new")
        prefAct = mysqltools.getSetting(mydb, "preferredActType")[2]
        activityFrame.set([[prefAct, True]])

        datatoDisplay = framedBoxes(checkBoxFrame, "Activities", [["Distance"], ["Trimp"]], lcarsSettings.violetCreme, None, button=False, autocheck=False)
        datatoDisplay.set([["Distance", True]])
        datatoDisplay.grid(column=1, row=1, padx=10, pady=10, sticky="new")


        upperrightFrame = framedArea(surroundingFrame, lcarsSettings.magenta)
        upperrightFrame.grid(column=1, row=0, padx=10, pady=10, sticky="nsew")

        lowerrightFrame = framedArea(surroundingFrame, lcarsSettings.blue)
        lowerrightFrame.grid(column=1, row=1, padx=10, pady=10, sticky="nsew")

        updatePlotFrames()

        #imger = PhotoImage(file="radius.png")
        #imger = Utils.changeColorOfImage(imger, lcarsSettings.yellowRGB)
        #t = CTkLabel(text = "bla", master=upperrightFrame, image = imger)
        #t.grid(column=0, row=0, padx=10, pady=10)


        main.mainloop()


mydb = mysqltools.connect()
nm = main_globalanalyze(mydb)

#yy = mysqltools.getYears(mydb)
#print(yy)