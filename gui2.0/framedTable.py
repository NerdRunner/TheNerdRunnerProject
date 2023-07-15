import datetime
from tkinter import ttk

import customtkinter

import mysqltools
from gui import lcarsSettings


class framedTable(customtkinter.CTkFrame):
    def __init__(self, master, title, columns, color):
        super().__init__(master)
        self.columns = columns
        self.title = title
        self.color = color

        self.configure(fg_color="black", border_color=self.color, border_width=0)

        self.table = ttk.Treeview(self)
        self.table['columns'] = columns

        self.table.column("#0", width=0, stretch="NO")
        for col in columns:
            self.table.column(col, width=80, stretch="NO")

        self.table.heading('#0', text="", anchor="nw")
        for head in columns:
            self.table.heading(head, text=head, anchor="nw")
        self.table.grid(row=1, column=0, padx=10, pady=(0), sticky="ew")
        style = ttk.Style(self.table)
        # style.theme_use("clam")  # set theam to clam
        style.configure("Treeview", background="black",
                        fieldbackground="black", foreground=color, borderwidth=0)
        style.configure('Treeview.Heading', background=color)

    def insertValuesIntoTable(self, rowValues):
        '''
        inserts the values in the table
        :param rowValues: ( (row1), (row2), ...)
        :return:
        '''
        i = 0
        for val in rowValues:
            self.table.insert(parent='', index='end', iid=i, text='', values=val)
            i = i + 1

    def deleteAllRows(self):
        for item in self.table.get_children():
            self.table.delete(item)
        return

    def insertMySQLTableValues(self, actList):
        '''
        :param actList: List of activities got from mysqltools. ... getactivities
        :return:
        '''
        rv = []
        for act in actList:
            dt = str(act[2].day)+"."+str(act[2].month)+"."+str(act[2].year)
            t = (dt, act[3], act[4], act[5], act[7])
            rv.append(t)
        self.insertValuesIntoTable(rv)
