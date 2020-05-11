import pandas as pd
import numpy as np
import glob
import re 
from datetime import date,timedelta
import io
import requests

# url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports_us/05-03-2020.csv'
# response = requests.get(url).content
# print(response)
# a = date.yesterday()
# print(a)
def dat(source='web'):
	if source == 'web':

		files_date = date(2020 ,1,22)
		
		dates=[]

		while files_date <= date.today():

			dates.append(files_date)
			files_date +=timedelta(days = 1)
		files=[]
		for file in dates:
			file = file.strftime("%m-%d-%Y")
			url = r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports_us/{}.csv'.format(file)
			raw_string = requests.get(url).content
			print(raw_string)
			df = pd.read_csv(io.StringIO(raw_string.decode('utf-8')))
			if b'404:Not Found' not in raw_string:
				df.to_csv('/data/raw/{}.csv'.format(file),index=False)
				print(file)
			df['date'] = pd.to_datetime(file)	
			df.rename(columns={'Province_State': 'Province/State',
							   'Country_Region': 'Country/Region',
							   'Lat': 'Latitude',
							   'Long_': 'Longitude'}, inplace=True)
			files.append(df)
	elif source=='folder':

		path = '/data'
		all_files = glob.glob(path + "/*.csv")

		files = []

		for filename in all_files:
			file = re.search(r'([0-9]{2}\-[0-9]{2}\-[0-9]{4})', filename)[0]
			print(file)
			df = pd.read_csv(filename, index_col=None, header=0)
			df['date'] = pd.to_datetime(file)
			df.rename(columns={'Province_State': 'Province/State',
							   'Country_Region': 'Country/Region',
							   'Lat': 'Latitude',
							   'Long_': 'Longitude'}, inplace=True)
			files.append(df)

	df = pd.concat(files, axis=0, ignore_index=True, sort=False)

	df = df[['date',
			 'Country/Region',
			 'Province/State',
			 'Confirmed',
			 'Deaths',
			 'Recovered',
			 'Latitude',
			 'Longitude']]
	df['Confirmed'] = df['Confirmed'].fillna(0).astype(int)
	df['Deaths'] = df['Deaths'].fillna(0).astype(int)
	df['Recovered'] = df['Recovered'].fillna(0).astype(int)
	df['Active'] = df['Confirmed'] - df['Deaths'] - df['Recovered']

	# Replace missing values for latitude and longitude
	df['Latitude'] = df['Latitude'].fillna(df.groupby('Province/State')['Latitude'].transform('mean'))
	df['Longitude'] = df['Longitude'].fillna(df.groupby('Province/State')['Longitude'].transform('mean'))
	return df

def us(data):
	states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California',
		  'Colorado', 'Connecticut', 'Delaware', 'District of Columbia',
		  'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana',
		  'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland',
		  'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi',
		  'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire',
		  'New Jersey', 'New Mexico', 'New York', 'North Carolina',
		  'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania',
		  'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee',
		  'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington',
		  'West Virginia', 'Wisconsin', 'Wyoming','Recovered']
	df_us = data[data['Province/State'].isin(states)]
	# df_us = df_us.drop('Country/Region', axis=1)
	# df_us = df_us.rename(columns={'Province/State': 'Country/Region'})
	return df_us
def us_county():
	path = '/data/raw'
	all_files = glob.glob(path + "/*.csv")

	files = []

	process = False
	for filename in all_files:
		file = re.search(r'([0-9]{2}\-[0-9]{2}\-[0-9]{4})',filename)[0]
		if file =='04-12-2020':
			process = True
		if process:
			df = pd.read_csv(filename,index_col=None,header = 0)
			df['date'] = pd.to_datetime(file)
			files.append(df)
	df = pd.concat(files,axis=0 , ignore_index=True , sort=False)
	df = df.loc[df['Country_Region']=='US']
	# # df = df.dropna(subset=['Admin2'])
	df['key']=df['Province_State']

	df['Confirmed']=df['Confirmed'].fillna(0).astype(int)
	df['Deaths'] = df['Deaths'].fillna(0).astype(int)
	df['Recovered'] = df['Recovered'].fillna(0).astype(int)
	df['Active']=df['Confirmed'] - df['Deaths'] - df['Recovered']
	df = df[['date',
			 'key',
			 'Province_State',
			 'Confirmed',
			 'Deaths',
			 'Recovered',
			 'Active',
			 'Lat',
			 'Long_']]		

	df1 = df[df['date']<='2020-04-13'].copy()
	df2 = df[df['date'] >'2020-04-13'].copy()

	#Collect state-level data from the day
	prev = pd.read_csv('/data/raw/04-12-2020.csv')
	prev = prev[prev['Country_Region'] == 'US']

	#Calculate share_of_last_week as the same for each county in the state,for the first week of availability
	df1 = df1.merge(prev ,left_on= 'Province_State' , right_on='Province_State')
	df1 = df1.rename(columns={'Confirmed_x': 'Confirmed',
							'Deaths_x': 'Deaths',
							'Active_x':'Active',
							'Lat_x':'Lat',
							'Long__x':'Long_',
							'Recovered_x': 'Recovered'})
	df1 = df1.join(df1.groupby('Province_State').agg({'Confirmed': 'sum', 'Confirmed_y': 'first'}),
				on='Province_State',
				rsuffix='_r')
	df1['share_of_last_week'] = 100 * (df1['Confirmed_r'] - df1['Confirmed_y']) / df1['Confirmed_r']
	df1['percentage'] = df1['share_of_last_week'].fillna(0).apply(lambda x: '{:.1f}'.format(x))
	df1.dropna(inplace=True)
	columns = ['date',
			'key',
			'Confirmed',
			'Deaths',
			'Recovered',
			'Active',
			'Lat',
			'Long_',
			'share_of_last_week',
			'percentage']
	df1 = df1[columns]

	# Calculate share_of_last_week appropriately once data from previous week is available
	df3 = pd.concat([df1, df2], sort=True)
	df3['previous_week'] = df3.groupby('key')['Confirmed'].shift(7)
	df3['share_of_last_week'] = 100 * (df3['Confirmed'] - df3['previous_week']) / df3['Confirmed']
	df3 = df3.loc[df2.index]
	df3['percentage'] = df3['share_of_last_week'].fillna(0).apply(lambda x: '{:.1f}'.format(x))

	df2 = df3[columns]

	# Combine the two dataframes
	df = pd.concat([df1, df2], ignore_index=True)

	df.rename(columns={'Lat': 'Latitude',
					   'Long_': 'Longitude'}, inplace=True)

	# Add in all data prior to county availability
	df2 = pd.read_csv('/data/df_us1.csv')
	df2 = df2[(df2['date'] < '2020-03-22') & (df2['Country/Region'] == 'US')]
	df2 = df2.groupby(['date', 'Province/State'], as_index=False).agg({'Country/Region': 'first',
															 'Confirmed': 'sum',
															 'Deaths': 'sum',
															 'Recovered': 'sum',
															 'Active': 'sum'})
	df2 = df2.merge(pd.read_csv('/home/abhay/GUI/data/geo_us.csv'), left_on='Province/State', right_on='Province/State')
	df2 = df2.merge(df2.groupby(['date', 'Province/State'], as_index=False).agg({'Confirmed': 'sum'}),
				on=['date', 'Province/State'])
	df2['prev_value'] = df2.groupby(['Province/State'])['Confirmed_y'].shift(7, fill_value=0)
	df2['share_of_last_week'] = (100 * (df2['Confirmed_y'] - df2['prev_value']) / df2['Confirmed_y'])
	df2 = df2.replace([np.inf, -np.inf], np.nan)
	df2['share_of_last_week'] = df2['share_of_last_week'].fillna(0)
	df2['percentage'] = df2['share_of_last_week'].fillna(0).apply(lambda x: '{:.1f}'.format(x))
	df2['key'] = df2['Province/State']
	df2 = df2.rename(columns={'Confirmed_x': 'Confirmed'})
	df = pd.concat([df2[df.columns], df], ignore_index=True)

	return df
if __name__=='__main__':
	data = dat()

	df_us=us(data)
	df_us.to_csv('/data/df_us1.csv',index = False )

	df_us_county = us_county()
	df_us_county.to_csv('/data/df_us_county.csv',index=False)