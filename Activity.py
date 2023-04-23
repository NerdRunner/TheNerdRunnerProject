from Trackpoint import Trackpoint


class Activity:
    '''
    Activity class
    '''

    def __init__(self, tpList: Trackpoint):
        '''
        Activity init
        :param tpList: Trackpoint[]
        '''
        self.tpList = tpList
        self.start = tpList[0].timestamp
        self.trimp = 0

    def print(self):
        print("Type: ",self.tpList[0].typ)
        print("Start: ", self.tpList[0].timestamp)
        print("Duration: ", self.tpList[len(self.tpList) - 1].timestamp - self.tpList[0].timestamp)
        print("Length [m]: ", self.getStrecke())
        print("Mean HR: ", self.meanHR())
        print("TRIMP: ", self.trimp)

    def meanHR(self):
        hr = 0
        for tp in self.tpList:
            if tp.hr is None:
                hr += 0
            else:
                hr += tp.hr
        hr = hr / len(self.tpList)
        return hr

    def getHRValues(self):
        hrList = []
        for tp in self.tpList:
            hrList.append([tp.timestamp, tp.hr])
        return hrList

    def getTPList(self):
        return self.tpList

    def getStrecke(self):
        if self.tpList is not None and len(self.tpList) > 0:
            d = self.tpList[len(self.tpList) - 1].distance
            if d is None:
                d = 0
        else:
            d = 0
        return d

    def getlatList(self):
        rv = []
        for t in self.tpList:
            rv.append(t.lat)
        return rv

    def getlongList(self):
        rv = []
        for t in self.tpList:
            rv.append(t.lon)
        return rv

    def getTrimp(self):
        return -1

    def addActivitytoTable(self,mydb):
        '''
        Adds the activity to the database
        :param act:
        :return:
        '''

        mycursor = mydb.cursor()
        sql = "INSERT INTO activities VALUES (%s, %s, %s, %s, %s, %s, ST_GeomFromText(%s), %s, ST_GeomFromText(%s))"
        hrlist = self.createPointListforMysql("hr")
        latlonlist = self.createPointListforMysql("latlon")
        if self.getTPList() is not None:
            val = (None, self.getTPList()[0].timestamp, self.getTPList()[0].timestamp, self.getTPList()[0].typ, self.getStrecke(),
            self.meanHR(), hrlist, self.getTrimp(), latlonlist)
        else:
            val = (self.getTPList[0].timestamp, None, None, self.getStrecke(), hrlist, self.getTrimp(), None)

        mycursor.execute(sql, val)
        mydb.commit()

        return

    def createPointListforMysql(self, typ):
        '''
        Creates a Linestring object out of an Activity for desired values
        :param act: Activity
        :param typ: "hr" or "latlon"
        :return:
        '''
        s = "LINESTRING("
        tpl = self.getTPList()
        if tpl is not None:
            for t in tpl:
                if typ == "latlon":
                    if t.lat is not None and t.lon is not None:
                        s += str(t.lat) + " " + str(t.lon) + ", "
                if typ == "hr":
                    s += str(1) + " " + str(t.hr) + ", "
            s = s[:-2]  # Letzte zwei Zeichen (Komma und Leerzeichen) entfernen
        else:
            s += "0 0, 1 1"
        s += ")"
        return s

