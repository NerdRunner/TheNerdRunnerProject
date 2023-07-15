import datetime

import customtkinter

import Utils
import activityMetrics
import importUtils
import mysqltools

from framedArea import framedArea
from lcarsButton import lcarsButton
from main_analyze import main_analyze
from framedBoxes import framedBoxes
from framedTable import framedTable
import lcarsSettings
import guiFunctions

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

### Upper Frame ###
guiFunctions.createUpperPlots(upperFrame, mydb)

### Lower Frame ###
#guiFunctions.createLowerPlots(lowerFrame, mydb, currcw)

### Right Frame ###
rightFrame = framedArea(main, lcarsSettings.yellow, bar=False)
rightFrame.grid(column=2, row=0, rowspan=2, sticky="nsew", padx=pad, pady=pad)
guiFunctions.createRightFrame(rightFrame, mydb)


#textFieldRight = customtkinter.CTkLabel(rightFrame, text="Summary", text_color=lcarsSettings.yellow, justify="left")
#textFieldRight.grid(column=0, row=0, padx=pad, pady=pad)
#actList = upperFrame.actBoxes.get()
#curry = datetime.date.today().year
#sum, formattedString = activityMetrics.summaryYearly(mydb,actList , [curry, curry-1, curry-2])
#textFieldRight.configure(text=formattedString)

#textFieldRight2 = customtkinter.CTkLabel(rightFrame, text="Summary", text_color=lcarsSettings.yellow, justify="left")
#textFieldRight2.grid(column=1, row=0, padx=pad, pady=pad, sticky="nw")
#formattedString2 = ""
#for a in actList:
#    formattedString2+=a+"\n\n"
#    ss = activityMetrics.summary(mydb, a, datetime.date(1900,1,1), datetime.date(2100,1,1))
#    formattedString2+=str(ss)+"\n-------------\n"
    #print
#textFieldRight2.configure(text=formattedString2)




def readFitFilesAndUpdatePlots(mydb, path, rv):
    importUtils.addFitFilesToDBWithStatus(mydb, path, buttonFrame, rv)
    rv.configure(text="Updating plots ...")
    main.update()
    guiFunctions.createUpperPlots(upperFrame, mydb)
    guiFunctions.createLowerPlots(lowerFrame, mydb, currcw)
    guiFunctions.createRightFrame(rightFrame, mydb)
    rv.configure(text=" ")

main.mainloop()