import datetime

from matplotlib.dates import DateFormatter
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import Utils
import activityMetrics
import mysqlCredentials
from SingleActivityTools import getPointListfromActivity
import osmnx as ox
from matplotlib.path import Path
import matplotlib.patches as patches


def totalperWeekPlot(mydb, columnName, year, cw_start, cw_end):
    '''
    Plots the total values of columnName over given calendar weeks for all acitivities
    :param mydb: MySQL-Handler
    :param columnName: Name of column for y-Values; get from mysqlCredentials.cn_xxx
    :param year: The year
    :param cw_start: Plotrange starting calendar week
    :param cw_end: Plotrange ending calendar week
    :return: figure object
    '''
    mycursor = mydb.cursor()
    d = cw_start
    xval = []
    yval = []
    xticks = []
    while d <= cw_end:
        d1, d2 = Utils.getDateRangeFromWeek(year,d)
        sql = "SELECT "+columnName+" from " + mysqlCredentials.activitytable + " WHERE DATE(datum) >= '" + d1.strftime("%Y-%m-%d") + "' and DATE(datum) <= '" + d2.strftime("%Y-%m-%d")+"'"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        xval.append(d)
        yval.append(Utils.listSum(myresult))
        xticks.append(d)
        d=d+1

    fig = Figure(figsize=(4.5,4.5), dpi=100)
    ax = fig.add_subplot()
    ax.bar(xval, yval)
    ax.set_xticks(xticks, minor=False)
    ax.set_xlabel("Calendar week")
    ax.set_ylabel(columnName)
    ax.set_title(columnName + " vs. calender week")
    ax.set_facecolor("black")
    fig.set_facecolor("black")

    return fig, ax

def totalperWeekAndActivityPlot(mydb, columnName, actList, year, cw_start, cw_end):
    '''
    Plots the total values of columnName over given calendar weeks for a given list of activities
    :param mydb: MySQL-Handler
    :param columnName: Name of column for y-Values; get from mysqlCredentials.cn_xxx
    :param actList: List of activities
    :param year: The year
    :param cw_start: Plotrange starting calendar week
    :param cw_end: Plotrange ending calendar week
    :return: figure object
    '''
    mycursor = mydb.cursor()
    d = cw_start
    xval = []
    yval = []
    xticks = []
    while d <= cw_end:
        d1, d2 = Utils.getDateRangeFromWeek(year,d)
        xval.append(d)
        tmp =[]
        for act in actList:
            sql = "SELECT "+columnName+" from " + mysqlCredentials.activitytable + " WHERE DATE(datum) >= '" \
              + d1.strftime("%Y-%m-%d") + "' and DATE(datum) <= '" + d2.strftime("%Y-%m-%d")+"' AND typ='"+act +"'"
            mycursor.execute(sql)
            myresult = mycursor.fetchall()
            tmp.append(Utils.listSum(myresult))
        yval.append(Utils.listSum(tmp))
        xticks.append(d)
        d=d+1

    fig = Figure(figsize=(4, 3), dpi=100)
    ax = fig.add_subplot()
    ax.bar(xval, yval)
    ax.set_xticks(xticks, minor=False)
    ax.set_xlabel("Calendar week")
    ax.set_ylabel(columnName)
    ax.set_title(columnName + " vs. calender week")
    ax.set_facecolor("black")
    fig.set_facecolor("black")

    return fig, ax

def PMC(mydb, d1, nDays):
    xval = []
    yvalCTL = []
    yvalATL = []
    yvalTSB = []
    xticks = []
    myFmt = DateFormatter("%d.%m.")
    d = d1
    n=0
    while n<=nDays:
        xval.append(d)
        xticks.append(d)
        ctl = activityMetrics.calculateDayCTL(mydb, d)
        atl = activityMetrics.calculateDayATL(mydb, d)
        yvalCTL.append(ctl)
        yvalATL.append(atl)
        yvalTSB.append(ctl - atl)
        d = d - datetime.timedelta(days=1)
        n = n+1
    fig = Figure(figsize=(4.5, 4.5), dpi=100)
    ax = fig.add_subplot()
    ax.plot(xval, yvalCTL, label="CTL")
    ax.xaxis.set_major_formatter(myFmt)
    ax.set_xlabel("day")
    ax.set_ylabel("columnName")
    ax.set_title("PMC")
    ax.set_facecolor("black")
    fig.set_facecolor("black")

    ax.plot(xval, yvalATL, label="ATL")
    ax.plot(xval, yvalTSB, label="TSB")
    ax.legend(facecolor="black", labelcolor='linecolor', frameon=False)

    return fig, ax

def setAxisColor(ax, col):
    ax.spines['bottom'].set_color(col)
    ax.spines['top'].set_color(col)
    ax.spines['right'].set_color(col)
    ax.spines['left'].set_color(col)
    ax.tick_params(axis='x', colors=col)
    ax.tick_params(axis='y', colors=col)
    ax.yaxis.label.set_color(col)
    ax.xaxis.label.set_color(col)
    ax.title.set_color(col)

def plotActivityMap(mydb, act):
    xlist, ylist, pointlist = getPointListfromActivity(mydb, act)
    # change to latitude, longitude order
    plinv = [(i[1], i[0]) for i in pointlist]
    # BoundingBox
    fig=None
    ax=None
    if(len(xlist)>0 and len(ylist)>0):
        max_x = max(xlist)
        max_y = max(ylist)
        min_x = min(xlist)
        min_y = min(ylist)
        G = ox.graph_from_bbox(max_y, min_y, max_x, min_x, network_type='walk', simplify=True)
        ox.settings.log_console=True
        # Plot
        fig, ax = ox.plot_graph(G, edge_color='k', bgcolor='w', show=False, close=False, figsize=(5,2.5))
        path = Path(plinv)
        patch = patches.PathPatch(path, edgecolor='red', fill=False, lw=2)
        ax.add_patch(patch)
    #plt.show()
    return fig, ax

def plotActivityHR(mydb, act):
    ylist, xlist, pointlist = getPointListfromActivity(mydb, act, typ="hr")
    fig = Figure(figsize=(8, 1.8), dpi=100)
    ax = fig.add_subplot()
    xlist = relativetoFirstElement(xlist)
    xlist = [i/60 for i in xlist]
    ax.plot(xlist, ylist, label="HR")
    #ax.xaxis.set_major_formatter(myFmt)
    ax.set_xlabel("min")
    ax.set_ylabel("bpm")
    ax.set_title("Heartrate")
    ax.set_facecolor("black")
    fig.set_facecolor("black")
    ax.legend(facecolor="black", labelcolor='linecolor', frameon=False)
    return fig, ax

def relativetoFirstElement(ll):
    '''
    Returns all elements relative to the first element
    :param ll:
    :return:
    '''
    rv = []
    for i in ll:
        rv.append(i-ll[0])
    return rv