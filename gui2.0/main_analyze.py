import customtkinter

import SingleActivityTools
import mysqltools
import plotUtils
from framedTable import framedTable
from framedArea import framedArea
from lcarsButton import lcarsButton
from plotList import plotList

import lcarsSettings

class main_analyze():
    def __init__(self, mydb):
        super().__init__()

        def selectItem():
            curItem = table.table.focus()
            updateLowerFrame(curItem)

        def updateLowerFrame(curItem):
            act = table.table.item(curItem)['values'][0]
            fig, ax = plotUtils.plotActivityMap(mydb, act)
            if(fig!=None):
                mapFrame.plot = plotList(mapFrame, [fig])
                mapFrame.plot.grid(row=1, column=0, padx=10, pady=10)

            fig2, ax2 = plotUtils.plotActivityHR(mydb, act)
            if (fig2 != None):
                hrFrame.plot = plotList(hrFrame, [fig2])
                plotUtils.setAxisColor(ax2, lcarsSettings.yellow)
                hrFrame.plot.grid(row=1, column=0, padx=10, pady=10)

            return

        main = customtkinter.CTk()

        main.title("The NerdRunner Project - TNRP - Analyze")

        screen_width = main.winfo_screenwidth()
        screen_height = main.winfo_screenheight()
        main.geometry(str(1.5*int(3*screen_width/4)) + "x" + str(int(3*screen_height/4)))

        main.configure(fg_color="black")

        leftFrame = framedArea(main,lcarsSettings.yellow)
        leftFrame.grid(column=0, row=0, padx=10, pady=10)

        rightFrame = framedArea(main, lcarsSettings.magenta)
        rightFrame.grid(column=1, row=0, padx=10, pady=10, sticky="nsew")

        table = framedTable(leftFrame, "titel2", ('Name', 'Date', 'Type', 'Distance', 'Mean HR', 'Trimp'), lcarsSettings.yellow)

        lastAct = mysqltools.getLastActivities(mydb, ["*"], 300)
        table.insertMySQLTableValues(lastAct, name=True)
        table.grid(column=0, row=0, padx=10, pady=10)

        btn = lcarsButton(leftFrame, "Update analysis", lcarsSettings.yellow, command=lambda: selectItem() )
        btn.grid(column=0, row=1)

        mapFrame = framedArea(main, lcarsSettings.blue)
        mapFrame.grid(column=0, row=1, padx=10, pady=10, sticky="nsew")
        mapFrame.textField = customtkinter.CTkLabel(mapFrame, text="Map",  text_color=lcarsSettings.yellow, justify="left")
        mapFrame.textField.grid(column=0, row=0, padx=10, pady=10)

        hrFrame = framedArea(main, lcarsSettings.blue)
        hrFrame.grid(column=1, row=1, padx=10, pady=10, sticky="nsew")
        #hrFrame.textField = customtkinter.CTkLabel(hrFrame, text="hr", text_color=lcarsSettings.yellow,justify="left")
        #hrFrame.textField.grid(column=0, row=0, padx=10, pady=10)




        main.mainloop()

mydb = mysqltools.connect()
nm = main_analyze(mydb)
