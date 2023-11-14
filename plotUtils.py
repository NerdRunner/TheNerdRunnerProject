import datetime
import math
from datetime import datetime
from datetime import timedelta

import matplotlib
import matplotlib.patches as patches
import numpy as np
import osmnx as ox
from matplotlib import pyplot as plt
from matplotlib.dates import DateFormatter
from matplotlib.figure import Figure
from matplotlib.path import Path

import Utils
import activityMetrics
import mysqlCredentials
import mysqltools
from SingleActivityTools import getPointListfromActivity
from Sportsman import Sportsman

from gui2 import lcarsSettings


def totalperWeekPlot(mydb, columnName, year, cw_start, cw_end, actList):
    '''
    Plots the total values of columnName over given calendar weeks for all acitivities
    :param mydb: MySQL-Handler
    :param columnName: Name of column for y-Values; get from mysqlCredentials.cn_xxx
    :param year: The year
    :param cw_start: Plotrange starting calendar week
    :param cw_end: Plotrange ending calendar week
    :param actList: List of Activities as String-List
    :return: figure object
    '''
    mycursor = mydb.cursor()
    d = cw_start
    xval = []
    yval = []
    xticks = []
    al = mysqltools.makeORListfromActlist(actList)
    while d <= cw_end:
        d1, d2 = Utils.getDateRangeFromWeek(year,d)
        sql = "SELECT "+columnName+" from " + mysqlCredentials.activitytable + " WHERE DATE(datum) >= '" + d1.strftime("%Y-%m-%d") + "' and DATE(datum) <= '" + d2.strftime("%Y-%m-%d")+"' and ("+al+")" #todo: hier weitermachen
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

def PMC(mydb, d1, nDays, actList):
    xval = []
    yvalCTL = []
    yvalATL = []
    yvalTSB = []
    xticks = []
    myFmt = DateFormatter("%d.%m.")
    d = d1
    n=0
    wl=[]
    k = 0
    while(k<42):
        weight = math.exp(-3 * k / 42)
        wl.append(weight)
        k+=1
    while n<=nDays:
        xval.append(d)
        xticks.append(d)
        ctl = activityMetrics.calculateDayCTL(mydb, d, actList,wl)
        atl = activityMetrics.calculateDayATL(mydb, d, actList)
        yvalCTL.append(ctl)
        yvalATL.append(atl)
        yvalTSB.append(ctl - atl)
        d = d - timedelta(days=1)
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

def plotLatLong(mydb, act):
    xlist, ylist, pointlist = getPointListfromActivity(mydb, act[0])
    fig = Figure(figsize=(5,2), dpi=100)
    ax = fig.add_subplot()
    ax.plot(xlist, ylist, "red", label="HR")  # "black" ist die Linienfarbe
    ax.set_facecolor("black")
    fig.set_facecolor("black")
    #ax.legend(facecolor="black", labelcolor='linecolor', frameon=False)
    return fig, ax

def plotXY(data, legend=" ", histogram=False):
    '''
    Plots an XY plot of data
    :param data: [ [[x1, y1], [x2, y2], ..] , [[x1, y1], [x2, y2], ..] ]
    :param legend: Legend
    :return:
    '''
    xlist = []
    ylist = []
    for einzel in data:
        yListEinzel = []
        xListEinzel = []
        for d in einzel:
            yListEinzel.append(d[1])
            xListEinzel.append(d[0])
        ylist.append(yListEinzel)
        xlist.append(xListEinzel)
    fig = Figure(figsize=(5,2), dpi=100)
    ax = fig.add_subplot()
    xlist = np.array(xlist).T
    ylist = np.array(ylist).T
    if(histogram):
        binlist=[0, 10,20, 30, 40, 50,110]
        ax.hist(ylist,bins=binlist, log=True)
        ax.set_xticks(binlist)
    else:
        ax.plot(xlist, ylist, label=legend)
        ax.legend(facecolor="black", labelcolor='linecolor', frameon=False, loc="upper left")
    ax.set_facecolor("black")
    fig.set_facecolor("black")

    return fig, ax
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
    ylist, xlist, pointlist = getPointListfromActivity(mydb, act[0], typ="hr")
    fig = Figure(figsize=(8, 1.8), dpi=100)
    ax = fig.add_subplot()
    xlist = relativetoFirstElement(xlist)
    xlist = [i/60 for i in xlist]
    ax.plot(xlist, ylist, "black",label="HR") #"black" ist die Linienfarbe
    #ax.xaxis.set_major_formatter(myFmt)
    ax.set_xlabel("min")
    ax.set_ylabel("bpm")
    ax.set_title("Heartrate")
    ax.set_facecolor("black")
    fig.set_facecolor("black")
    ax.legend(facecolor="black", labelcolor='linecolor', frameon=False)

    addHRZonebanner(mydb, ax,act[1])



    return fig, ax

def addHRZonebanner(mydb, ax, dt):
    '''
    :param mydb: MySQL-Handler
    :param ax: ax - Object
    :param dt: date 'd.m.Y'
    :return: -
    '''
    #TODO: Check HR Ranges

    # Regeneration: <60%
    # GA1: 60-75%
    # GA2: 75-85%
    # E: 85 - 95%
    sm = Sportsman("dummy", "1.1.2020", "m")
    sm.getFromDB(mydb)
    dto = datetime.strptime(dt, '%d.%m.%Y')
    maxHR = sm.getVitalValues(mydb, dto)[2]
    hRZones = str.split(mysqltools.getSetting(mydb, "hrZones")[2], ",")
    hRZones = [float(i) for i in hRZones]

    ax.axhspan(hRZones[0]*maxHR, hRZones[1]*maxHR, facecolor=lcarsSettings.ice, alpha=0.5, zorder=-100)
    ax.axhspan(hRZones[1]*maxHR, hRZones[2]*maxHR, facecolor=lcarsSettings.green, alpha=0.5, zorder=-100)
    ax.axhspan(hRZones[2] * maxHR, hRZones[3] * maxHR, facecolor=lcarsSettings.yellow, alpha=0.5, zorder=-100)
    ax.axhspan(hRZones[3]*maxHR, hRZones[4]*maxHR, facecolor=lcarsSettings.red, alpha=0.5, zorder=-100)

    return


def relativetoFirstElement(ll):
    '''
    Returns all elements relative (by substraction) to the first element
    :param ll:
    :return:
    '''
    rv = []
    for i in ll:
        rv.append(i-ll[0])
    return rv

def heatmap(data, row_labels, col_labels, ax=None,
            cbar_kw=None, cbarlabel="", **kwargs):
    """
    Create a heatmap from a numpy array and two lists of labels.

    Parameters
    ----------
    data
        A 2D numpy array of shape (M, N).
    row_labels
        A list or array of length M with the labels for the rows.
    col_labels
        A list or array of length N with the labels for the columns.
    ax
        A `matplotlib.axes.Axes` instance to which the heatmap is plotted.  If
        not provided, use current axes or create a new one.  Optional.
    cbar_kw
        A dictionary with arguments to `matplotlib.Figure.colorbar`.  Optional.
    cbarlabel
        The label for the colorbar.  Optional.
    **kwargs
        All other arguments are forwarded to `imshow`.
    """

    if ax is None:
        ax = plt.gca()

    if cbar_kw is None:
        cbar_kw = {}

    # Plot the heatmap
    im = ax.imshow(data, **kwargs)

    # Create colorbar
    #cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
    #cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")

    # Show all ticks and label them with the respective list entries.
    ax.set_xticks(np.arange(len(data[0])), labels=col_labels, color="w")
    ax.set_yticks(np.arange(len(data)), labels=row_labels, color="w")

    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=False, bottom=True,
                   labeltop=False, labelbottom=True)

    # Rotate the tick labels and set their alignment.
    #plt.setp(ax.get_xticklabels(), rotation=-30, ha="right",
             #rotation_mode="anchor")

    # Turn spines off and create white grid.
    ax.spines[:].set_visible(False)
    ax.set_xticks(np.arange(len(data[0])+1)-.5, minor=True)
    ax.set_yticks(np.arange(len(data)+1)-.5, minor=True)
    ax.grid(which="minor", color="black", linestyle='-', linewidth=5)
    ax.tick_params(which="minor", bottom=False, left=False)



    return im


def annotate_heatmap(im, data=None, valfmt="{x:.2f}",
                     textcolors=("black", "white"),
                     threshold=None, **textkw):
    """
    A function to annotate a heatmap.

    Parameters
    ----------
    im
        The AxesImage to be labeled.
    data
        Data used to annotate.  If None, the image's data is used.  Optional.
    valfmt
        The format of the annotations inside the heatmap.  This should either
        use the string format method, e.g. "$ {x:.2f}", or be a
        `matplotlib.ticker.Formatter`.  Optional.
    textcolors
        A pair of colors.  The first is used for values below a threshold,
        the second for those above.  Optional.
    threshold
        Value in data units according to which the colors from textcolors are
        applied.  If None (the default) uses the middle of the colormap as
        separation.  Optional.
    **kwargs
        All other arguments are forwarded to each call to `text` used to create
        the text labels.
    """

    if not isinstance(data, (list, np.ndarray)):
        data = im.get_array()

    # Normalize the threshold to the images color range.
    if threshold is not None:
        threshold = im.norm(threshold)
    else:
        threshold = im.norm(data.max())/2.

    # Set default alignment to center, but allow it to be
    # overwritten by textkw.
    kw = dict(horizontalalignment="center",
              verticalalignment="center")
    kw.update(textkw)

    # Get the formatter in case a string is supplied
    if isinstance(valfmt, str):
        valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)

    # Loop over the data and create a `Text` for each "pixel".
    # Change the text's color depending on the data.
    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
            text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
            texts.append(text)

    return texts