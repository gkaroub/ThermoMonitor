from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io
from flask import Flask, render_template, send_file, make_response, request, g, flash, redirect, url_for
from datetime import datetime
import sensorsDB as sDB
from flask_wtf import FlaskForm
from wtforms import FloatField, StringField, TextAreaField, SubmitField, SelectField, DecimalField
from wtforms.validators import DataRequired, ValidationError, InputRequired, NumberRange
from wtforms.widgets import Input
from markupsafe import Markup
from secrets import token_hex

app = Flask(__name__)
app.config["SECRET KEY"]="secret key"


# Global variables
NTemp = sDB.NTemp
NTime = sDB.NTime
alertColor = sDB.alertColor
nornalcolor = sDB.normalColor
numOfSamples = sDB.numOfSamples

# This is the class for the form at hostorical data
class samples(FlaskForm):
    smpls = FloatField('Αριθμός Δειγμάτων', validators=[InputRequired(),NumberRange(min=240,max=11000)], render_kw={"placeholder": "μεταξύ 240 και 11400"})
    sbmt = SubmitField('Ενημέρωση Γραφημάτων')

# main route - The sensors main page
@app.route("/")
def home():
	time, temp, hum, temp2, hum2, press = sDB.getData()
	clr = sDB.getDateTimeDif_fromToday(time)
# Change background color if temp > NTemp, else it comes from previous line
	if temp > NTemp:
		clr = alertColor
	templateData = {
		'time': time,
		'temp': temp,
		'hum': hum,
		'temp2': temp2,
		'hum2': hum2,
		'press': press,
		'clr': clr
	}
	return render_template('home.html', **templateData)

# Plotting of historical data. The same decorator function is being used for default 
# setting plot (that is the last hour or 240 samples), or for any samples value given by means of 
# form. 
@app.route('/history', methods=('GET', 'POST'))
def history():
	global numOfSamples
	hours = round(numOfSamples / 240, 2)
	templateData = {
		'hours': hours
		}
	form = samples()
	# Handling of the sumbit action
	if request.method == 'POST':
		if form.validate:
			f = form.smpls.data
			# check if the given data is numeric and between accepted limits
			try:
				if f < 240 or f > 11400:
					flash("Aριθμός μεταξύ 240 και 11400")
					return render_template('history.html', **templateData, form=form)
				numOfSamples = int(f)
				hours = round(numOfSamples /240, 2)
				templateData = {
					'hours': hours
				}
				return render_template('history.html', **templateData, form=form)
			except:
				flash("Πρέπει να δώσετε αριθμό μεταξύ 240 και 11400".format("title"),"danger")
				hours = round(numOfSamples / 240, 2)
				templateData = {
					'hours': hours
				}
				form.smpls.data = " "
				return render_template('history.html', **templateData, form=form)
	# Default action is to plot the last 1 hour data
	return render_template('history.html', **templateData, form=form)

# Plots the temperature as a function of samples. It is called as href from template
@app.route('/plot/temp')
def plot_temp():
	global numOfSamples
	numMaxSamples = sDB.maxRowsTable()
	if (numOfSamples > numMaxSamples):
		numOfSamples = (numMaxSamples-1)
	numSamples = numOfSamples
	temps = sDB.getHistDataParam(numSamples, 'tmpHOT')
	ys = temps
	fig = Figure()
	axis = fig.add_subplot(1, 1, 1)
	axis.set_title("Θερμοκρασία Αέρα")
	axis.set_xlabel("Δείγματα")
	axis.grid(True)
	xs = range(numSamples)
	axis.plot(xs, ys)
	canvas = FigureCanvas(fig)
	output = io.BytesIO()
	canvas.print_png(output)
	response = make_response(output.getvalue())
	response.mimetype = 'image/png'
	return response 

# Plots the relative humidity as a function of samples. It is called as href from template
@app.route('/plot/hum')
def plot_hum():
	global numOfSamples
	numMaxSamples = sDB.maxRowsTable()
	if (numOfSamples > numMaxSamples):
		numOfSamples = (numMaxSamples-1)
	numSamples = numOfSamples
	hums = sDB.getHistDataParam(numSamples, 'hmHOT')
	ys = hums
	fig = Figure()
	axis = fig.add_subplot(1, 1, 1)
	axis.set_title("Υγρασία")
	axis.set_xlabel("Δείγματα")
	axis.grid(True)
	xs = range(numSamples)
	axis.plot(xs, ys)
	canvas = FigureCanvas(fig)
	output = io.BytesIO()
	canvas.print_png(output)
	response = make_response(output.getvalue())
	response.mimetype = 'image/png'
	return response

# Plots the atmospheric pressure as a function of samples. It is called as href from template
@app.route('/plot/press')
def plot_press():
	global numOfSamples
	numMaxSamples = sDB.maxRowsTable()
	if (numOfSamples > numMaxSamples):
		numOfSamples = (numMaxSamples-1)
	numSamples = numOfSamples
	press = sDB.getHistDataParam(numSamples,'press')
	ys = press
	fig = Figure()
	axis = fig.add_subplot(1, 1, 1)
	axis.set_title("Πίεση")
	axis.set_xlabel("Δείγματα")
	axis.grid(True)
	xs = range(numSamples)
	axis.plot(xs, ys)
	canvas = FigureCanvas(fig)
	output = io.BytesIO()
	canvas.print_png(output)
	response = make_response(output.getvalue())
	response.mimetype = 'image/png'
	return response


