import datetime


import customtkinter
import numpy as np
import osmnx as ox
from matplotlib.path import Path
import matplotlib.patches as patches
from matplotlib import pyplot as plt

import SingleActivityTools
import mysqltools
from gui2 import lcarsSettings
from gui2.framedArea import framedArea
from gui2.plotList import plotList
from plotUtils import plotLatLong



mydb = mysqltools.connect()

act = "activity_15040428992.fit"
actInfo = mysqltools.getSingleActivity(mydb, act)[0]
dy = str(actInfo[2].strftime('%d.%m.%Y'))
dur = str(datetime.timedelta(seconds=actInfo[9]))
actStr = dy + "  -  " + str("{:.0f}".format(actInfo[4]/1000))+"km  -  " +dur

xlist,ylist,pl = SingleActivityTools.getPointListfromActivity(mydb, act)
##
n=100 #Remove the first and last n points for data privacy
xlist =xlist[n:]
ylist =ylist[n:]
pl = pl[n:]
xlist =xlist[:len(pl)-n]
ylist =ylist[:len(pl)-n]
pl = pl[:len(pl)-n]
##
plinv = [(i[1], i[0]) for i in pl]

max_x = max(xlist)
max_y = max(ylist)
min_x = min(xlist)
min_y = min(ylist)
G = ox.graph_from_bbox(max_y, min_y, max_x, min_x, simplify=True)
ox.settings.log_console=True
# Plot
fig, ax = ox.plot_graph(G, node_color='none', edge_alpha=0.5, edge_color='y', bgcolor='k', show=False, close=False)#, figsize=(5,2.5))


path = Path(plinv)
patch = patches.PathPatch(path, edgecolor='red', fill=False, lw=3)
ax.add_patch(patch)
plt.rcParams["savefig.facecolor"] = 'black'
plt.title(actStr)
plt.text(0.5,0.5, 'Practice on GFG',bbox = dict(facecolor = 'red', alpha = 0.5))


plt.show()
#plt.savefig("/home/simon/Schreibtisch/test.jpg",bbox_inches='tight', facecolor="black", transparent=False)
