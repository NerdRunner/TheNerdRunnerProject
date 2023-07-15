import math

import customtkinter

import mysqlCredentials
import mysqltools
import plotUtils
from gui import lcarsSettings
from gui.framedPlot import framedPlot


class framedBoxes(customtkinter.CTkFrame):
    def __init__(self, master, title, values, color, targetTable):
        super().__init__(master)
        self.master = master
        self.values = values
        self.title = title
        self.checkboxes = []

        self.color = color

        self.configure(fg_color="black", border_color=self.color, border_width=0)

        self.button = customtkinter.CTkButton(self, text="Update", corner_radius=100, command=lambda: self.button_callback(targetTable), fg_color=self.color, text_color="black")
        self.button.grid(row=1, column=0, padx=10, pady=10, sticky="ew", columnspan=2)



        for i, value in enumerate(self.values):
            checkbox = customtkinter.CTkCheckBox(self, text=value, border_color=self.color, text_color=self.color)
            checkbox.select()
            checkbox.grid(row=(i%3)+2, column=math.ceil((i+1)/3)-1, padx=10, pady=10, sticky="w")
            self.checkboxes.append(checkbox)

    def button_callback(self, targetTable):
      targetTable.deleteAllRows()
      mydb = mysqltools.connect()
      acts = self.get()
      if len(acts)>0:
            lastAct = mysqltools.getLastActivities(mydb, acts, 10)
            targetTable.insertMySQLTableValues(lastAct)

    def get(self):
        checked_checkboxes = []
        for checkbox in self.checkboxes:
            if checkbox.get() == 1:
                checked_checkboxes.append(checkbox.cget("text")[0])
        return checked_checkboxes