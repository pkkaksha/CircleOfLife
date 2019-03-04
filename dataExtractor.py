import requests
import json
import datetime
import os
import sys
import pandas as pd
from pandas.io.json import json_normalize
from pymongo import MongoClient

rootDir = sys.argv[1]

# Get the current datetime
current_datetime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
os.makedirs(os.path.join(rootDir,current_datetime))

# Initialize the pymongo (Setting up the local database)
client = MongoClient()
client = MongoClient('192.168.2.212', 27017)
db = client.circle_of_life
collection_maxtemp = db.max_temp
collection_data = db.weather_data

with open('cityList.txt', 'r') as fr:
	cityList = fr.read().split('\n')

# Create empty dataframe
df = pd.DataFrame()

max_temperature_dict = {}
temperature_dict = {'datetime': current_datetime, 'max_temp': max_temperature_dict}

weather_data = {}
weather_data_fin = {'starttime': current_datetime, 'data': weather_data}


for city in cityList:
	
	# Call to database
	url ="http://api.openweathermap.org/data/2.5/weather?appid=b02e97b5bfb08e278f211490ee1cb9ed&q="+ city
	
	# Get the response
	response = requests.get(url).json()

	status_code = None
	if response['cod'] == 200:
		# Call successful
		status_code = 'success'

		# Convert response to Pandas parseable format
		response['weather'] = response['weather'][0]

		# Converting the JSON response into pandas dataframe
		df_temp = pd.DataFrame.from_dict(json_normalize(response), orient='columns')

		# Concat the temp dataframe to the original dataframe
		df = pd.concat([df, df_temp], sort=True, axis=0)

		max_temperature_dict[city.split(',')[0]] = response['main']['temp']

		weather_data[city.split(',')[0]] = response

	else:
		status_code = 'failed'
		print('Response code : {}'.format(response['code']))

print(df.head())
print('Total number of rows:{} and columns:{}'.format(len(df), len(df.iloc[0])))

weather_data_fin['endtime'] = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

# Insert into mongo
collection_maxtemp.insert_one(temperature_dict)
collection_data.insert_one(weather_data_fin)
