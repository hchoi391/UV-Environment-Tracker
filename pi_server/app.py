import json
import os
import math
from flask import Flask, render_template, request
from flask_socketio import SocketIO
from datetime import datetime
from statistics import mean, median, mode

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

def median(dataset):
    data = sorted(dataset)
    index = len(data) // 2
    
    # If the dataset is odd  
    if len(dataset) % 2 != 0:
        return data[index]
    
    # If the dataset is even
    return (data[index - 1] + data[index]) / 2

def get_uv_data(date, time, wavelength):

	try:
		path = os.path.join(data_path, date+'.json')
		with open(path, 'r') as f:
			data = json.load(f)
			tmp_list = []
			
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
				
			overall_list = []
			ceiling_val = 400
			for i, key in enumerate(data.keys()):
				for angle, uv_tmp_data in data[key].items():
					if uv_tmp_data[idx] < ceiling_val:
						overall_list.append(uv_tmp_data[idx])
					else:
						overall_list.append(uv_tmp_data[idx])
						print(f"wrong_data: {uv_tmp_data[idx]}")
			
			med_val = median(overall_list)
			med_val = med_val * 3
			
			for i, val in enumerate(overall_list):
				if val > med_val:
					overall_list.remove(val)
					
			list1 = [ele for ele in overall_list if ele < med_val]
			
			max_val = max(list1)
			min_val = min(list1)
			
			print(max_val, min_val)
				
			if not (time in data.keys()):
				return None
			tmp_dict = data[time]
			
			

			for key, val in tmp_dict.items():
				if (val[idx] < med_val):
					tmp_list.append((key, (val[idx]-min_val)/(max_val-min_val)))
				else:
					tmp_list.append((key, (med_val-min_val)/(max_val-min_val)))
					
			angles = [x / 1000.0 for x in range(0, 360000, 5625)]
			
			angles_curr = []
			for angle, val in tmp_list:
				angles_curr.append(float(angle))
			
			print(angles_curr)
			for angle in angles:
				if angle not in angles_curr:
					print(angle)
					tmp_list.append((angle, 0))
					pass 
				
			return tmp_list
		return None

	except FileNotFoundError:
		return None


def normalize_values(values, date):
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

	if values['uv_data'] == None :
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
