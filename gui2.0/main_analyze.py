import customtkinter

import mysqltools
from framedTable import framedTable
from framedArea import framedArea
from lcarsButton import lcarsButton

import lcarsSettings

class main_analyze():
    def __init__(self, mydb):
        super().__init__()
        main = customtkinter.CTk()

        main.title("The NerdRunner Project - TNRP - Analyze")

        screen_width = main.winfo_screenwidth()
        screen_height = main.winfo_screenheight()
        main.geometry(str(int(3*screen_width/4)) + "x" + str(int(3*screen_height/4)))

        main.configure(fg_color="black")

        leftFrame = framedArea(main,lcarsSettings.yellow)
        leftFrame.grid(column=0, row=0, padx=10, pady=10)

        table = framedTable(leftFrame, "titel2", ('Date', 'Type', 'Distance', 'Mean HR', 'Trimp'), lcarsSettings.yellow)
        lastAct = mysqltools.getLastActivities(mydb, ["*"], 300)
        table.insertMySQLTableValues(lastAct)
        table.grid(column=0, row=0, padx=10, pady=10)

        btn = lcarsButton(leftFrame, "Update analysis", lcarsSettings.yellow)
        btn.grid(column=0, row=1)

        lowerFrame = framedArea(main, lcarsSettings.blue)
        lowerFrame.grid(column=0, row=1, padx=10, pady=10, sticky="nsew")




        main.mainloop()
