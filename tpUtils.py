#training
#rest
#tapering
#race
import typing

from matplotlib.figure import Figure

import tpUtils
from TrainingPlan import TrainingPlan
from gui2 import lcarsSettings

import mysqlCredentials
import mysqltools



def plotTrainingsplan(tpList: typing.List[TrainingPlan], withcurrentData=False, mydb = 0):
    '''
    Plots a List of trainingsplans
    :param tpList: List of Trainingplans
    :param withcurrentData: Boolean, if current activities shall also be drawn
    :param mydb: MySQL-Handler
    :return:
    '''

    fig = Figure(figsize=(11, 3.0), dpi=100)
    ax = fig.add_subplot()
   # cList = [lcarsSettings.yellow, lcarsSettings.violetCreme, lcarsSettings.green, lcarsSettings.red]

    for tp in tpList: #TODO: tp auf Klasse Trainingsplan umschreiben
        i = 0
        for single in tp.tp:
            xval = []
            yval = []
            for t in single:
                xval.append(t[2])
                yval.append(t[3])
                col = tpUtils.tpTypeToColor(t[4])
            ax.bar(xval, yval, color=col, width=5)
            i=i+1

        if withcurrentData:
            currData = tp.getActivitiesAccordingToTrainingplan(mydb)
            xval=[]
            yval=[]
            for d in currData:
                xval.append(d[0])
                yval.append(d[1]/1000)
            ax.plot(xval, yval, color=lcarsSettings.evening, linewidth=5)

    #ax.set_xlabel("Calendar week")
    ax.set_title(tp.name)
    ax.set_facecolor("black")
    fig.set_facecolor("black")

    return fig, ax

def tpTypeToColor(type):
    col = 0
    if type == "training":
        col = lcarsSettings.yellow
    if type == "rest":
        col = lcarsSettings.violetCreme
    if type == "tapering":
        col = lcarsSettings.green
    if type == "race":
        col = lcarsSettings.red
    return col



