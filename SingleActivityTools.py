import mysqlCredentials
import mysqltools


def getPointListfromActivity(mydb, run, typ="pointlist"):
    '''
    Gets lat/lon coordinates of an activity identified by its filename
    :param mydb: MYSQL-Handler
    :param run: filname of activity
    :param typ: String, either "pointlist" or "hr": Type of what shall be given back
    :return:
    '''
    mycursor = mydb.cursor()
    query = "SELECT ST_AsText(pointlist) FROM "+mysqlCredentials.activitytable +" WHERE dateiname= '"+run+"' ORDER BY datum ASC"
    if(typ=="hr"):
        query = "SELECT ST_AsText(hrlist) FROM " + mysqlCredentials.activitytable + " WHERE dateiname= '" + run + "' ORDER BY datum ASC"
    mycursor.execute(query)
    myresult = mycursor.fetchall()
    ls = myresult[0][0]
    pointlist = mysqltools.linestringtoList(ls)

    xlist = []
    ylist = []
    pl = []
    for ll in pointlist:
        if(ll[0] and ll[1] > 5):
            xlist.append(ll[1])
            ylist.append(ll[0])
            pl.append((ll[0],ll[1]))
    return xlist,ylist,pl