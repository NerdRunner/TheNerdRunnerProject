import math

import customtkinter

import mysqltools


class framedBoxes(customtkinter.CTkFrame):
    def __init__(self, master, title, values, color, targetTable, button=True, autocheck=True):
        super().__init__(master)
        self.master = master
        self.values = values
        self.title = title
        self.checkboxes = []

        self.color = color

        self.configure(fg_color="black", border_color=self.color, border_width=0)

        if(button==True):
            self.button = customtkinter.CTkButton(self, text="Update", corner_radius=100, command=lambda: self.button_callback(targetTable), fg_color=self.color, text_color="black")
            self.button.grid(row=1, column=0, padx=10, pady=10, sticky="ew", columnspan=2)



        for i, value in enumerate(self.values):
            checkbox = customtkinter.CTkCheckBox(self, text=value, border_color=self.color, text_color=self.color)
            if autocheck:
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
                tt=checkbox.cget("text")
                if type(tt) != int:
                    tt = tt[0]
                checked_checkboxes.append(tt)
        return checked_checkboxes

    def set(self, namesAndValues):
        '''
        Checks / unchecks the given checkboxes
        :param namesAndValues: [ [name, bool], [name, bool], ... ]: name: String
        :return:
        '''
        for nv in namesAndValues:
            for checkbox in self.checkboxes:
                s = checkbox.cget("text")
                if type(s) is not int:
                    s = s[0]
                if s == nv[0]:
                    if(nv[1] == True):
                        checkbox.select()
                    else:
                        checkbox.deselect()
