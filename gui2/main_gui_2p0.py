import datetime

import customtkinter

import Utils
import activityMetrics
import importUtils
import mysqltools

from framedArea import framedArea
from gui2.main_globalanalyze import main_globalanalyze
from gui2.main_records import main_records
from gui2.main_trainingplan import main_trainingplan
from lcarsButton import lcarsButton
from main_analyze import main_analyze
from framedBoxes import framedBoxes
from framedTable import framedTable
import lcarsSettings
import guiFunctions

import cProfile

mydb = mysqltools.connect()
path = mysqltools.getSetting(mydb, "fitFilePath")[2]
today=datetime.datetime.today()
currcw = Utils.getCalendarWeekFromDate(today)

main = customtkinter.CTk()
main.title("The NerdRunner Project - TNRP")

screen_width = main.winfo_screenwidth()
screen_height = main.winfo_screenheight()
main.geometry(str(screen_width) + "x" + str(screen_height))

main.configure(fg_color="black")
pad = 10

buttonFrame= framedArea(main, lcarsSettings.yellow, bar=False)
buttonFrame.grid(column=0, row=0, rowspan=2, sticky="nsew", padx=pad, pady=pad)

upperFrame = framedArea(main, lcarsSettings.blue, bar=False)
upperFrame.grid(column=1, row=0, padx=pad, pady=pad, sticky="nsew")

lowerFrame = framedArea(main, lcarsSettings.magenta, bar=False)
lowerFrame.grid(column=1, row=1, padx=pad, pady=pad, sticky="nsew")

### Buttons on left side ###
btnTextField = customtkinter.CTkLabel(buttonFrame, text="", text_color=lcarsSettings.yellow)
btnTextField.grid(row=3, column=0)

btn = lcarsButton(buttonFrame, "Import fit-Files", lcarsSettings.yellow, command=lambda: guiFunctions.gui_getFitFiles(main, mydb,btnTextField))
btn.grid(row=1, column=0)

btn2 = lcarsButton(buttonFrame, "Update DB", lcarsSettings.yellow, command=lambda: readFitFilesAndUpdatePlots(mydb, path, btnTextField))
btn2.grid(row=2, column=0)

btn3 = lcarsButton(buttonFrame, "Analyze", lcarsSettings.magenta, command=lambda: main_analyze(mydb))
btn3.grid(row=4, column=0)

btn4 = lcarsButton(buttonFrame, "Global analysis", lcarsSettings.magenta, command=lambda: main_globalanalyze(mydb))
btn4.grid(row=5, column=0)

btn5 = lcarsButton(buttonFrame, "Trainingplans", lcarsSettings.magenta, command=lambda: main_trainingplan(mydb))
btn5.grid(row=6, column=0)

btn5 = lcarsButton(buttonFrame, "Records", lcarsSettings.magenta, command=lambda: main_records(mydb))
btn5.grid(row=7, column=0)

### Upper Frame ###
guiFunctions.createUpperPlots(upperFrame, mydb)

### Lower Frame ###
#guiFunctions.createLowerPlots(lowerFrame, mydb, currcw)

### Right Frame ###
rightFrame = framedArea(main, lcarsSettings.yellow, bar=False)
rightFrame.grid(column=2, row=0, rowspan=2, sticky="nsew", padx=pad, pady=pad)
guiFunctions.createRightFrame(rightFrame, mydb, upperFrame.actBoxes.get())




def readFitFilesAndUpdatePlots(mydb, path, rv):
    importUtils.addFitFilesToDBWithStatus(mydb, path, buttonFrame, rv)
    actList = upperFrame.actBoxes.get()
    rv.configure(text="Updating plots ...")
    main.update()
    guiFunctions.createUpperPlots(upperFrame, mydb, preserveSettings=True)

    guiFunctions.createLowerPlots(lowerFrame, mydb, currcw, actList)
    guiFunctions.createRightFrame(rightFrame, mydb, actList)
    rv.configure(text=" ")

main.mainloop()