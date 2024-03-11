import datetime

import customtkinter

import Utils
import mysqltools
import tpUtils
from gui2 import framedArea, lcarsSettings


class TrainingWeek:

    #TODO: Doku class TrainingWeek

    WeekDate = 0
    type = None
    list = 0
    Monday = 0
    Tuesday = 0
    Wednesday = 0
    Thursday = 0
    Friday = 0
    Saturday = 0
    Sunday = 0

    def __init__(self, WeekDate, type, list):
        self.WeekDate = WeekDate
        self.type = type
        self.list = list
        self.Monday = list[0]
        self.Tuesday = list[1]
        self.Wednesday = list[2]
        self.Thursday = list[3]
        self.Friday = list[4]
        self.Saturday = list[5]
        self.Sunday = list[6]

    def display(self, master, calendarWeekToBeBold=None, dbHandler=None):
        col = tpUtils.tpTypeToColor(self.type)



        ff = framedArea.framedArea(master,col)
        if (calendarWeekToBeBold is not None and calendarWeekToBeBold == Utils.getCalendarWeekFromDate(self.WeekDate)):
            ff.configure(border_width=7)
        px = 15
        py = 0

        if(dbHandler is not None):
            cw = Utils.getCalendarWeekFromDate(self.WeekDate)
            d1,d2 = Utils.getDateRangeFromWeek(self.WeekDate.year, cw)
            al=[]
            sum = 0
            while d1<=d2:
                acts = mysqltools.getActivitiesByDateRange(dbHandler,["running"], d1, d1)
                if(len(acts)>0):
                    aday =0
                    for a in acts:
                           aday = aday+a[4]/1000
                    al.append(aday)
                else:
                    al.append(0)
                d1 = d1 + datetime.timedelta(days=1)
            sum = al[0]+al[1]+al[2]+al[3]+al[4]+al[5]+al[6]

        ll = customtkinter.CTkLabel(ff, text_color=self.priv_colIsTargetReached(al[0], self.Monday), text=str('{:.2f}'.format(self.Monday)) + "\n" + str(al[0]) + "\n---")
        ll.grid(row=0, column=0,padx=px, pady=(10,0))
        ll = customtkinter.CTkLabel(ff, text_color=self.priv_colIsTargetReached(al[1], self.Tuesday), text=str('{:.2f}'.format(self.Tuesday)) + "\n" + str(al[1]) + "\n---")
        ll.grid(row=1, column=0,padx=px, pady=py)
        ll = customtkinter.CTkLabel(ff, text_color=self.priv_colIsTargetReached(al[2], self.Wednesday), text=str('{:.2f}'.format(self.Wednesday)) + "\n" + str(al[2]) + "\n---")
        ll.grid(row=2, column=0,padx=px, pady=py)
        ll = customtkinter.CTkLabel(ff, text_color=self.priv_colIsTargetReached(al[3], self.Thursday), text=str('{:.2f}'.format(self.Thursday)) + "\n" + str(al[3]) + "\n---")
        ll.grid(row=3, column=0,padx=px, pady=py)
        ll = customtkinter.CTkLabel(ff, text_color=self.priv_colIsTargetReached(al[4], self.Friday), text=str('{:.2f}'.format(self.Friday)) + "\n" + str(al[4]) + "\n---")
        ll.grid(row=4, column=0,padx=px, pady=py)
        ll = customtkinter.CTkLabel(ff, text_color=self.priv_colIsTargetReached(al[5], self.Saturday), text=str('{:.2f}'.format(self.Saturday)) + "\n" + str(al[5]) + "\n---")
        ll.grid(row=5, column=0,padx=px, pady=py)
        ll = customtkinter.CTkLabel(ff, text_color=self.priv_colIsTargetReached(al[6], self.Sunday), text=str('{:.2f}'.format(self.Sunday)) + "\n" + str(al[6]) + "\n---")
        ll.grid(row=6, column=0,padx=px, pady=(0,10))
        if (dbHandler is not None):
            totalSoll = self.getTotalKM()
            ll = customtkinter.CTkLabel(ff, text_color=self.priv_colIsTargetReached(sum, totalSoll), text=str('{:.2f}'.format(totalSoll)) + "\n" + str('{:.2f}'.format(sum)))
            ll.grid(row=7, column=0, padx=px, pady=(0, 10))


        return ff

    def priv_colIsTargetReached(self, ist, soll):
        col = lcarsSettings.ice
        if 0.9*soll<=ist:
            col = lcarsSettings.green
        else:
            col = lcarsSettings.red
        if ist==0:
            col=lcarsSettings.ice
        return col

    def getTotalKM(self):
        return self.Monday+self.Tuesday+self.Wednesday+self.Thursday+self.Friday+self.Saturday+self.Sunday
