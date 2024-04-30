import json
import os
import math
from flask import Flask, render_template, request
from flask_socketio import SocketIO
from datetime import datetime

data_path = 'uv_data'

app = Flask(__name__)
socketio = SocketIO(app,cors_allowed_origins="*")

values = {
	'date': "",
   'time': "",
   'UVtype': "",
   'uv_data': "",
   'timeSlider': 0,
   'statusColor': "#ffff99",
   'message': "waiting..."
}

def get_uv_data(date, time, wavelength):

	try:
		path = os.path.join(data_path, date+'.json')
		with open(path, 'r') as f:
			data = json.load(f)
			tmp_list = []
			if not (time in data.keys()):
				return None
			tmp_dict = data[time]
			idx = 0

			match wavelength:
				case 'A':
					idx = 0
					# break
				case 'B':
					idx = 1
					# break
				case 'C':
					idx = 2
					# break

			for key, val in tmp_dict.items():
				tmp_list.append((key, val[idx]))

			print(len(tmp_list))
			return tmp_list
		return None

	except FileNotFoundError:
		return None


def normalize_values(values):
	intensity = [y for x,y in values]
	if len(intensity) > 0:
		max_val = max(intensity)
		min_val = min(intensity)

		norm = [(y-min_val)/(max_val-min_val) for y in intensity]

		tmp_list = []
		for i, val in enumerate(values):
			tmp_list.append((val[0], norm[i]))
		
		print(tmp_list)	
		return tmp_list
	return values


def inputValidation(date,time,UVtype):

	if date == "" or UVtype == "" or time == "":
		return False

	try:
	   bool(datetime.strptime(date, '%Y-%m-%d'))

	except ValueError:
	   return False

	if datetime(2024, 4, 25) > datetime.strptime(date, '%Y-%m-%d') or \
		datetime.strptime(date, '%Y-%m-%d') > datetime.today():
		return False

	try:
	   bool(datetime.strptime(time, '%H:%M'))

	except ValueError:
	   return False


	if UVtype != 'A' and UVtype != 'B' and UVtype != 'C':
		return False


def timeToTimeSlider(time):
	input_time = datetime.strptime(time, '%H:%M')
	input_hour = input_time.hour
	input_min = input_time.minute
	return (input_hour * 60) + input_min


def timeSliderToTime(timeSlider):
	input_hour = math.floor(int(timeSlider)/60)
	input_min = int(timeSlider) % 60
	str_hour = str(input_hour)
	str_min = str(input_min)

	if (len(str_min) == 1):
		str_min = "0" + str_min

	if (len(str_hour) == 1):
		str_hour = "0" + str_hour

	return str_hour + ":" + str_min


@app.route('/')
def index():
	values['date'] = ""
	values['time'] = ""
	values['UVtype'] = ""
	values['timeSlider'] = 0
	values['statusColor'] = "#ffff99"
	values['message'] = "waiting..."
	values['uv_data'] = ""	
	return render_template('index.html', **values)
	
@app.route('/index.html', methods = ['POST'])
def main_page():
	if not (values['date'] == request.form['date'] and values['time'] != request.form['time'] and \
		values['UVtype'] == request.form['UVtype']):

		values['date'] = request.form['date']
		values['time'] = request.form['time']
		values['UVtype'] = request.form['UVtype']

	if inputValidation(values['date'], values['time'], values['UVtype']) == False :
		values['statusColor'] = "tomato"
		values['message'] = "Incorrect Input"
		return render_template('index.html', **values)

	print("The date, UV type, and time: ",values['date'],", ",values['UVtype'],", ",values['time'],"\n")

	values['timeSlider'] = timeToTimeSlider(values['time'])

	values['uv_data'] = get_uv_data(values['date'], values['time'], values['UVtype'])

	if values['uv_data'] != None :
		values['uv_data'] = normalize_values(values['uv_data'])

	else:
		values['statusColor'] = "tomato"
		values['message'] = "No Data"
		return render_template('index.html', **values)


	values['statusColor'] = "#99ff66"
	values['message'] = "Successful"

	return render_template('index.html', **values)


@socketio.on("update")
def update(data):
	values['timeSlider'] = data['value']
	values['time'] = timeSliderToTime(values['timeSlider'])

if __name__ == "__main__":
   socketio.run(app, host='0.0.0.0', port=5000)
