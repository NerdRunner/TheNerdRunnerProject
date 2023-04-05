import mysql.connector
import mysqlCredentials


def connect():
    mydb = mysql.connector.connect(
        host=mysqlCredentials.host,
        user=mysqlCredentials.user,
        password=mysqlCredentials.pw,
        database="tnrp"
    )
    return mydb


# Create the database
def createDatabase(mydb):
    mycursor = mydb.cursor()
    mycursor.execute(
        "CREATE TABLE workouts (dateiname VARCHAR(99), datum DATETIME, typ TEXT, strecke INT, hr INT, hrlist LINESTRING, trimp INT, pointlist LINESTRING)")


mydb = connect()
# createDatabase(mydb)
