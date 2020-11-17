import sqlite3
from datetime import datetime
from retrying import retry
import appParameters

# Temperature Notification Threshold
# this the temperature above which the application
# background will turn to red. Its value comes from appParameters.
NTemp = appParameters.NTemp
# Seconds between succesive samples above which the application
# background will turn to red.  Its value comes from appParameters.
NTime = appParameters.NTime
# This is the location of the sensors database. Its value comes from appParameters.
dbLocation = appParameters.dbLocation

alertColor = appParameters.alertColor
normalColor = appParameters.normalColor
numOfSamples = appParameters.numOfSamples


# Retrieve LAST data from database
@retry(stop_max_attempt_number=5)
def getLastData():
	conn=sqlite3.connect(dbLocation)
	curs=conn.cursor()
	for row in curs.execute("SELECT dtime,tmpHOT,hmHOT FROM TmLine ORDER BY dtime DESC LIMIT 1"):
		time = str(row[0])
		temp = row[1]
		hum = row[2]
	conn.close()
	return time, temp, hum

@retry(stop_max_attempt_number=5)
def getHistData (numSamples):
    conn=sqlite3.connect(dbLocation)
    curs=conn.cursor()
    curs.execute("SELECT tmpHOT,hmHOT, press FROM TmLine ORDER BY dtime DESC LIMIT "+str(numSamples))
    data = curs.fetchall()
    temps = []
    hums = []
    press = []
    for row in reversed(data):
        temps.append(row[0])
        hums.append(row[1])
        press.append(row[2])
    conn.close()
        #print temps, hums
    return temps, hums, press

@retry(stop_max_attempt_number=5)
def getHistDataParam (numSamples, Param):
    conn=sqlite3.connect(dbLocation)
    curs=conn.cursor()
    curs.execute("SELECT "+Param+" FROM TmLine ORDER BY dtime DESC LIMIT "+str(numSamples))
    data = curs.fetchall()
    out= []
    for row in reversed(data):
        out.append(row[0])
    conn.close()
        #print temps, hums
    return out

@retry(stop_max_attempt_number=5)
def maxRowsTable():
	conn=sqlite3.connect(dbLocation)
	curs=conn.cursor()
	for row in curs.execute("select COUNT(tmpHOT) from TmLine"):
		maxNumberRows=row[0]
	conn.close()
	return maxNumberRows

#initialize global variables
global numSamples
numSamples = maxRowsTable()
if (numSamples > 5760):
	numSamples = 5760
	
@retry(stop_max_attempt_number=5)
def getData():
	conn=sqlite3.connect(dbLocation)
	curs=conn.cursor()
	for row in curs.execute("SELECT dtime,tmpHOT,hmHOT,tmpCOLD,hmCOLD,press FROM TmLine ORDER BY dtime DESC LIMIT 1"):
		time = str(row[0])
		temp = round(row[1],2)
		hum = round(row[2],2)
		temp2 = round(row[3],2)
		hum2 = round(row[4],2)
		press = round(row[5],2)
	#print(time, temp, hum, temp2, hum2)
	conn.close()
	return time, temp, hum, temp2, hum2, press
	
def getDateTimeDif_fromToday(Time):
	date_object1 = datetime.now()
	date_object2 = datetime.strptime(Time, "%Y-%m-%d %H:%M:%S")
	TimeDif = (date_object1 - date_object2).seconds
# Change background color if data are older than NTime seconds ago from real time
	if TimeDif > NTime:
		return alertColor
	return normalColor