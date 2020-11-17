#!/usr/bin/env python
##-*- coding: iso-8859-15 -*-
'''
	RPi WEb Server for Temperature and Humidity captured data with Graph plot  
'''
# how to control service:
# sudo systemctl (start|stop|restart|status) uwsgi.service

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io

from flask import Flask, render_template, send_file, make_response, request
app = Flask(__name__)

import sqlite3
from datetime import datetime

# Temperature Notification Threshold
# this the temperature above which the application
# background will turn to red. 
NTemp=29
# Seconds between succesive samples above which the application
# background will turn to red. 
NTime=50



# Retrieve LAST data from database
def getLastData():
	conn=sqlite3.connect('/home/pi/Documents/webServer/sensorData.db')
	curs=conn.cursor()
	for row in curs.execute("SELECT dtime,tmpHOT,hmHOT FROM TmLine ORDER BY dtime DESC LIMIT 1"):
		time = str(row[0])
		temp = row[1]
		hum = row[2]
	conn.close()
	return time, temp, hum


def getHistData (numSamples):
	conn=sqlite3.connect('/home/pi/Documents/webServer/sensorData.db')
	curs=conn.cursor()
	curs.execute("SELECT tmpHOT,tmpCOLD FROM TmLine ORDER BY dtime DESC LIMIT "+str(numSamples))
	data = curs.fetchall()
	temps = []
	hums = []
	for row in reversed(data):
		temps.append(row[0])
		hums.append(row[1])
	conn.close()
	#print temps, hums
	return temps, hums

def maxRowsTable():
	conn=sqlite3.connect('/home/pi/Documents/webServer/sensorData.db')
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
	
def getData():
	conn=sqlite3.connect('/home/pi/Documents/webServer/sensorData.db')
	curs=conn.cursor()
	for row in curs.execute("SELECT dtime,tmpHOT,hmHOT,tmpCOLD,hmCOLD FROM TmLine ORDER BY dtime DESC LIMIT 1"):
		time = str(row[0])
		temp = round(row[1],2)
		hum = round(row[2],2)
		temp2 = round(row[3],2)
		hum2 = round(row[4],2)
	#print(time, temp, hum, temp2, hum2)
	conn.close()
	return time, temp, hum, temp2, hum2
	
def getDateTimeDif_fromToday(Time):
	date_object1 = datetime.now()
	date_object2 = datetime.strptime(Time, "%Y-%m-%d %H:%M:%S")
	TimeDif = (date_object1 - date_object2).seconds
# Change background color if data are older than NTime seconds ago from real time
	if TimeDif > NTime:
		return 'rgb(255, 20, 20)'
	return ''
	
# main route 
@app.route("/")
def index():
	time, temp, hum, temp2, hum2 = getData()
	clr = getDateTimeDif_fromToday(time)
# Change background color if temp > NTemp
	if temp > NTemp:
		clr = 'rgb(255, 20, 20)'
	templateData = {
		'time': time,
		'temp': temp,
		'hum': hum,
		'temp2': temp2,
		'hum2': hum2,
		'clr': clr
	}
	return render_template('index.html', **templateData)


@app.route('/', methods=['POST'])
def my_form_post():
    global numSamples 
    numSamples = int (request.form['numSamples'])
    numMaxSamples = maxRowsTable()
    if (numSamples > numMaxSamples):
        numSamples = (numMaxSamples-1)
    
    time, temp, hum = getLastData()
    
    
    templateData = {
	  'time'		: time,
      'temp'		: temp,
      'hum'			: hum,
      'numSamples'	: numSamples
	}
    return render_template('index.html', **templateData)
	
	
@app.route('/plot/temp')
def plot_temp():
	temps, hums = getHistData(numSamples)
	ys = temps
	fig = Figure()
	axis = fig.add_subplot(1, 1, 1)
	axis.set_title("Temperature")
	axis.set_xlabel("Samples")
	axis.grid(True)
	xs = range(numSamples)
	axis.plot(xs, ys)
	canvas = FigureCanvas(fig)
	output = io.BytesIO()
	canvas.print_png(output)
	response = make_response(output.getvalue())
	response.mimetype = 'image/png'
	return response
'''
@app.route('/plot/hum')
def plot_hum():
	temps, hums = getHistData(numSamples)
	ys = hums
	fig = Figure()
	axis = fig.add_subplot(1, 1, 1)
	axis.set_title("t2")
	axis.set_xlabel("Samples")
	axis.grid(True)
	xs = range(numSamples)
	axis.plot(xs, ys)
	canvas = FigureCanvas(fig)
	output = io.BytesIO()
	canvas.print_png(output)
	response = make_response(output.getvalue())
	response.mimetype = 'image/png'
	return response
'''

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8080, debug=False)
