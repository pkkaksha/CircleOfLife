from flask import Flask
from flask import request, render_template
from pymongo import MongoClient
import datetime
import json

# Initialize the pymongo (Setting up the local database)
client = MongoClient()
client = MongoClient('192.168.2.212', 27017)
db = client.circle_of_life
collection_maxtemp = db.max_temp
collection_data = db.weather_data

app = Flask(__name__)

@app.route('/')
def analysis():


	# Sort the data according to endTime key
	latest_record = collection_data.find().sort([("endTime", 1)]).limit(1)[0]
	
	cities = latest_record['data'].keys()
	cities = [str(x) for x in cities]

	attrWiseVals = {'clouds': [], 'visibility': [], 'pressure': [], 'temp': [], 'humidity': [], 'wind_speed': [], 'wind_degree': []}

	for city in latest_record['data']:
		attrWiseVals['clouds'].append(latest_record['data'][city]['clouds']['all'])
		attrWiseVals['visibility'].append(latest_record['data'][city]['visibility'])

		# Value not available
		# attrWiseVals['rain'].append(latest_record['data'][city]['rain']['1h'])

		attrWiseVals['pressure'].append(latest_record['data'][city]['main']['pressure'])
		attrWiseVals['temp'].append(latest_record['data'][city]['main']['temp'])
		attrWiseVals['humidity'].append(latest_record['data'][city]['main']['humidity'])
		attrWiseVals['wind_speed'].append(latest_record['data'][city]['wind']['speed'])

		# Value not available
		# attrWiseVals['wind_degree'].append(latest_record['data'][city]['wind']['deg'])

	graph_name = 'Weather Graph'


	max_temp = {}
	for vals in collection_data.find({}):
		for city in vals['data']:
			if city not in max_temp:
				max_temp[city] = vals['data'][city]['main']['temp']

			if max_temp[city] < vals['data'][city]['main']['temp']:
				max_temp[city] = vals['data'][city]['main']['temp']

	max_temp_list = max_temp.values()

	return render_template('graph.html', name=graph_name, cities=json.dumps(cities), clouds=json.dumps(attrWiseVals['clouds']), visibility=json.dumps(attrWiseVals['visibility']), \
		 pressure=json.dumps(attrWiseVals['pressure']), \
		temp=json.dumps(attrWiseVals['temp']), humidity=json.dumps(attrWiseVals['humidity']), \
		wind_speed=json.dumps(attrWiseVals['wind_speed']), max_temp_list=json.dumps(max_temp_list))

if __name__ == '__main__':

    app.run(debug=True, host='0.0.0.0')