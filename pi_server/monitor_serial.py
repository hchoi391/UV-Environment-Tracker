import serial
import os
import json
from datetime import date, datetime
import atexit

data_path = 'uv_data'

ser = serial.Serial('/dev/ttyACM0')
print(ser.name)

today = date.today()
print(today)

todayData = {}

def exit_handler():
	with open(os.path.join(data_path, str(today)+'.json'), "w") as f:
		json.dump(todayData, f)
		f.close()
	
atexit.register(exit_handler)

path = os.path.join(data_path, str(today) + '.json')
if os.path.isfile(path):
	print('file_exists')
	with open(path, 'r') as f:
		todayData = json.load(f)
		f.close()
		
now = datetime.now()
	
curr_time = now.strftime("%H:%M")

todayData[curr_time] = {}

while True:
	data = ser.readline().decode().replace('\n','')
	if 'Start' in data:
		while True:
			data = ser.readline().decode().replace('\n','')
			if 'End' in data:
				exit_handler()
				break	
			now = datetime.now()

			curr_time = now.strftime("%H:%M")

			split_data = data.split(',')
			angle = float(split_data[1])
			
			print(curr_time, split_data)

			if len(split_data) == 8:
				if curr_time in todayData.keys():
					angle_dict = todayData[curr_time]
					angle_dict[angle] = (int(split_data[3]), int(split_data[5]), int(split_data[7]))
				else:
					todayData[curr_time] = {}	
					todayData[curr_time][angle] = (int(split_data[3]), int(split_data[5]), int(split_data[7]))
			
			#print(todayData.keys())
