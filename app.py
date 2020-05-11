import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import csv
import glob
from datetime import date,timedelta
from dash.dependencies import Input ,Output
import plotly.graph_objects as go

external_stylesheets = ['/assets/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'COVID-19'
# body = {
# 'background-color':'red'
# }
data = pd.read_csv('/data/df_us1.csv')
data['date'] = pd.to_datetime(data['date'])

# selects the "data last updated" date
update =data['date'].dt.strftime('%B %d, %Y').iloc[-1]

colors = {
	'bg':'#ffffff',
	'background': '#111111',
	'text': '#BEBEBE',
	'grid': 'black',
	'red': '#BF0000',
	'blue': '#466fc2',
	'green': '#5bc246'
}
available_countries = sorted(data['Country/Region'].unique())

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
		  'West Virginia', 'Wisconsin', 'Wyoming']
		  
region_options = {'United States':states}
df_us = pd.read_csv('/data/df_us1.csv')
# df_us_full = data[data['Country/Region'] == 'US']
# print(df_us)
df_us_counties = pd.read_csv('/data/df_us_county.csv')
df_us_counties['percentage'] = df_us_counties['percentage'].astype(str)
df_us_counties['key'] = df_us_counties['key'].astype(str)
# print(df_us_counties)
@app.callback(
	Output('confirmed_ind','figure'),
	[Input('global_format','value')]
	)
def confirmed(view):
	if view == 'United States':
		df= df_us
		# print(df)
	else:
		df = data

	value = df[df['date'] == df['date'].iloc[-1]]['Confirmed'].sum()
	delta = df[df['date'] == df['date'].unique()[-2]]['Confirmed'].sum()
	return {
			'data': [{'type': 'indicator',
					'mode': 'number+delta',
					'value': value,
					'delta': {'reference': delta,
							  'valueformat': ',g',
							  'relative': False,
							  'increasing': {'color': colors['blue']},
							  'decreasing': {'color': colors['green']},
							  'font': {'size': 25}},
					'number': {'valueformat': ',',
							  'font': {'size': 50}},
					'domain': {'y': [0, 1], 'x': [0, 1]}}],
			'layout': go.Layout(
				title={'text': "CUMULATIVE CONFIRMED"},
				font=dict(color=colors['red']),
				paper_bgcolor=colors['background'],
				plot_bgcolor=colors['background'],
				height=200,
				width=333.75
				)
			}
@app.callback(
	Output('active_ind','figure'),
	[Input('global_format','value')])
def active(view):
	if view == 'United States':
		df = df_us
	else:
		df = data

	value = df[df['date'] == df['date'].iloc[-1]]['Active'].sum()
	delta = df[df['date'] == df['date'].unique()[-2]]['Active'].sum()
	return {
			'data': [{'type': 'indicator',
					'mode': 'number+delta',
					'value': value,
					'delta': {'reference': delta,
							  'valueformat': ',g',
							  'relative': False,
							  'increasing': {'color': colors['blue']},
							  'decreasing': {'color': colors['green']},
							  'font': {'size': 25}},
					'number': {'valueformat': ',',
							  'font': {'size': 50}},
					'domain': {'y': [0, 1], 'x': [0, 1]}}],
			'layout': go.Layout(
				title={'text': "CURRENTLY ACTIVE"},
				font=dict(color=colors['red']),
				paper_bgcolor=colors['background'],
				plot_bgcolor=colors['background'],
				height=200,
				width=333.75
				)
			}
@app.callback(
	Output('recovered_ind','figure'),
	[Input('global_format','value')]
	)
def recovered(view):

	if view == 'United States':
		df = df_us
	else:
		df= data

	value = df[df['date'] == df['date'].iloc[-1]]['Recovered'].sum()
	delta = df[df['date'] == df['date'].unique()[-2]]['Recovered'].sum()
	return {
			'data': [{'type': 'indicator',
					'mode': 'number+delta',
					'value': value,
					'delta': {'reference': delta,
							  'valueformat': ',g',
							  'relative': False,
							  'increasing': {'color': colors['blue']},
							  'decreasing': {'color': colors['green']},
							  'font': {'size': 25}},
					'number': {'valueformat': ',',
							  'font': {'size': 50}},
					'domain': {'y': [0, 1], 'x': [0, 1]}}],
			'layout': go.Layout(
				title={'text': "RECOVERED CASES"},
				font=dict(color=colors['red']),
				paper_bgcolor=colors['background'],
				plot_bgcolor=colors['background'],
				height=200,
				width=333.75
				)
			}
@app.callback(
	Output('deaths_ind','figure'),
	[Input('global_format','value')])
def deaths(view):

	if view =='United States':
		df=df_us
	else:
		df = data
	value = df[df['date'] == df['date'].iloc[-1]]['Deaths'].sum()
	delta = df[df['date'] == df['date'].unique()[-2]]['Deaths'].sum()
	return {
			'data': [{'type': 'indicator',
					'mode': 'number+delta',
					'value': value,
					'delta': {'reference': delta,
							  'valueformat': ',g',
							  'relative': False,
							  'increasing': {'color': colors['blue']},
							  'decreasing': {'color': colors['green']},
							  'font': {'size': 25}},
					'number': {'valueformat': ',',
							  'font': {'size': 50}},
					'domain': {'y': [0, 1], 'x': [0, 1]}}],
			'layout': go.Layout(
				title={'text': "DEATHS TO DATE"},
				font=dict(color=colors['red']),
				paper_bgcolor=colors['background'],
				plot_bgcolor=colors['background'],
				height=200

				)
			}
@app.callback(
	Output('worldwide_trend','figure'),
	[Input('global_format','value')])
def worldwide_trand(view):

	if view == 'United States':
		df =df_us
	else:
		df = data

	traces = [go.Scatter(
					x=df.groupby('date')['date'].first(),
					y=df.groupby('date')['Confirmed'].sum(),
					hovertemplate='%{y:,g}',
					name="Confirmed",
					mode='lines'),
				go.Scatter(
					x=df.groupby('date')['date'].first(),
					y=df.groupby('date')['Active'].sum(),
					hovertemplate='%{y:,g}',
					name="Active",
					mode='lines'),
				go.Scatter(
					x=df.groupby('date')['date'].first(),
					y=df.groupby('date')['Recovered'].sum(),
					hovertemplate='%{y:,g}',
					name="Recovered",
					mode='lines'),
				go.Scatter(
					x=df.groupby('date')['date'].first(),
					y=df.groupby('date')['Deaths'].sum(),
					hovertemplate='%{y:,g}',
					name="Deaths",
					mode='lines')]
	return {
			'data': traces,
			'layout': go.Layout(
				title="{} Infections".format(view),
				xaxis_title="Date",
				yaxis_title="Number of Cases",
				font=dict(color=colors['text']),
				paper_bgcolor=colors['bg'],
				plot_bgcolor=colors['bg'],
				xaxis=dict(gridcolor=colors['grid']),
				yaxis=dict(gridcolor=colors['grid'])
				)
			}
@app.callback(
	Output('country_select','options'),
	[Input('global_format','value')])
def set_active_options(selected_view):
	'''
	sets allowable options for regions in the upper-right chart drop-down
	'''
	# return [{'label': i, 'value': i} for i in region_options[selected_view]]

@app.callback(
	Output('country_select','value'),
	[Input('global_format','value'),
	Input('country_select','options')])
def set_countries_value(view,available_options):

	if view =='United States':
		return['New York','New Jersey','Massachusetts','Pennsylvania','California','Michigan','Washington','Illinois']
	else:
		return['US']	
@app.callback(
	Output('active_countries', 'figure'),
	[Input('global_format', 'value'),
	 Input('country_select', 'value'),
	 Input('column_select', 'value')])
def active_countries(view, countries, column):
	'''
	creates the upper-right chart (sub-region analysis)
	'''
	if view == 'United States':
		df =df_us
	else:
		df = data

	traces = []
	countries = df[(df['Province/State'].isin(countries)) &
				   (df['date'] == df['date'].max())].groupby('Province/State')['Active'].sum().sort_values(ascending=False).index.to_list()
	# print(countries)			   
	for country in countries:
		traces.append(go.Scatter(
					x=df[df['Province/State'] == country].groupby('date')['date'].first(),
					y=df[df['Province/State'] == country].groupby('date')[column].sum(),
					hovertemplate='%{y:,g}<br>%{x}',
					name=country,
					mode='lines'))
	if column == 'Recovered':
		traces.append(go.Scatter(
					x=df[df['Province/State'] == 'Recovered'].groupby('date')['date'].first(),
					y=df[df['Province/State'] == 'Recovered'].groupby('date')[column].sum(),
					hovertemplate='%{y:,g}<br>%{x}',
					name='Unidentified',
					mode='lines'))
	return {
			'data': traces,
			'layout': go.Layout(
					title="{} by Region".format(column),
					xaxis_title="Date",
					yaxis_title="Number of Cases",
					font=dict(color=colors['text']),
					paper_bgcolor=colors['bg'],
					plot_bgcolor=colors['bg'],
					xaxis=dict(gridcolor=colors['grid']),
					yaxis=dict(gridcolor=colors['grid']),
					hovermode='closest',
					height=426
				)
			}

@app.callback(
	Output('world_map', 'figure'),
	[Input('global_format', 'value'),
	 Input('date_slider', 'value')])
def world_map(view, date_index):
	'''
	creates the lower-left chart (map)
	'''
	if view == 'United States':
		scope='usa'
		projection_type='albers usa'
		df = df_us_counties
		# df = df[df['date'] == df['date'].unique()[date_index]]
		df = df.rename(columns={'key': 'Country/Region'})
		sizeref=3
	else:
		df = data
		df = world_map_processing(df, date_index)
		scope='world'
		projection_type='natural earth',
		sizeref=10
	return {
			'data': [
				go.Scattergeo(
					lon = df['Longitude'],
					lat = df['Latitude'],
					text = df['Country/Region'] + ': ' +\
						['{:,}'.format(i) for i in df['Confirmed']] +\
						' total cases, ' + df['percentage'] +\
						'% from previous week',
					hoverinfo = 'text',
					mode = 'markers',
					marker = dict(reversescale = False,
						autocolorscale = False,
						symbol = 'circle',
						size = np.sqrt(df['Confirmed']),
						sizeref = sizeref,
						sizemin = 0,
						line = dict(width=.5, color='rgba(0, 0, 0)'),
						colorscale = 'Reds',
						cmin = 0,
						color = df['share_of_last_week'],
						cmax = 100,
						colorbar = dict(
							title = "Percentage of<br>cases occurring in<br>the previous week",
							thickness = 30)
						)
					)
			],
			'layout': go.Layout(
				title ='Number of Cumulative Confirmed Cases (size of marker)<br>and Share of New Cases from the Previous Week (color)',
				geo=dict(scope=scope,
						projection_type=projection_type,
						showland = True,
						landcolor = "rgb(100, 125, 100)",
						showocean = True,
						oceancolor = "rgb(80, 150, 250)",
						showcountries=True,
						showlakes=True),
				font=dict(color=colors['text']),
				paper_bgcolor=colors['bg'],
				plot_bgcolor=colors['background']
			)
		}

def world_map_processing(df, date_index):
	'''
	
	'''
	# World map
	date = df['date'].unique()[date_index]

	df_world_map = df[df['date'] == date].groupby('Country/Region').agg({'Confirmed': 'sum',
																		'Longitude': 'mean',
																		'Latitude': 'mean',
																		'Country/Region': 'first'})

	if date_index > 7:
		idx7 = date_index - 7
	else:
		idx7 = 0

	df_world_map['share_of_last_week'] = ((df[df['date'] == date].groupby('Country/Region')['Confirmed'].sum() -
								df[df['date'] == df['date'].unique()[idx7]].groupby('Country/Region')['Confirmed'].sum()) /
								df[df['date'] == date].groupby('Country/Region')['Confirmed'].sum()) * 100

	df_world_map['percentage'] = df_world_map['share_of_last_week'].fillna(0).apply(lambda x: '{:.1f}'.format(x))

	# Manually change some country centroids which are mislocated due to far off colonies
	df_world_map.loc[df_world_map['Country/Region'] == 'US', 'Latitude'] = 39.810489
	df_world_map.loc[df_world_map['Country/Region'] == 'US', 'Longitude'] = -98.555759

	# df_world_map.loc[df_world_map['Country/Region'] == 'France', 'Latitude'] = 46.2276
	# df_world_map.loc[df_world_map['Country/Region'] == 'France', 'Longitude'] = 2.2137

	# df_world_map.loc[df_world_map['Country/Region'] == 'United Kingdom', 'Latitude'] = 55.3781
	# df_world_map.loc[df_world_map['Country/Region'] == 'United Kingdom', 'Longitude'] = -3.4360

	# df_world_map.loc[df_world_map['Country/Region'] == 'Denmark', 'Latitude'] = 56.2639
	# df_world_map.loc[df_world_map['Country/Region'] == 'Denmark', 'Longitude'] = 9.5018

	# df_world_map.loc[df_world_map['Country/Region'] == 'Netherlands', 'Latitude'] = 52.1326
	# df_world_map.loc[df_world_map['Country/Region'] == 'Netherlands', 'Longitude'] = 5.2913

	# df_world_map.loc[df_world_map['Country/Region'] == 'Canada', 'Latitude'] = 59.050000
	# df_world_map.loc[df_world_map['Country/Region'] == 'Canada', 'Longitude'] = -112.833333

	# df_world_map = df_world_map[df_world_map['Country/Region'] != 'Cruise Ship']
	# df_world_map = df_world_map[df_world_map['Country/Region'] != 'Diamond Princess']

	return df_world_map

app.layout = html.Div(style={'backgroundColor':colors['background']}, children=[
	html.H1(children='COVID-19',
		style={
			'textAlign': 'center',
			'color': colors['text']
			}
		),

	html.Div(children='Data last updated {} end-of-day'.format(update), style={
		'textAlign': 'center',
		'color':colors['text']
		}),
	
	html.Div(children='Select focus for the dashboard:', style={
		'textAlign': 'center',
		'color': colors['text']
		}),

	html.Div(dcc.RadioItems(id='global_format',
			options=[{'label': 'United States', 'value': 'United States'}],
			value='United States',
			labelStyle={'float': 'center', 'display': 'inline-block'}
			), style={'textAlign': 'center',
				'color': colors['text'],
				'width': '100%',
				'float': 'center',
				'display': 'inline-block'
			}
		),

	html.Div(dcc.Graph(id='confirmed_ind'),
		style={
			'textAlign': 'center',
			'color': colors['red'],
			'width': '25%',
			'float': 'left',
			'display': 'inline-block'
			}
		),

	html.Div(dcc.Graph(id='active_ind'),
		style={
			'textAlign': 'center',
			'color': colors['red'],
			'width': '25%',
			'float': 'left',
			'display': 'inline-block'
			}
		),

	html.Div(dcc.Graph(id='deaths_ind'),
		style={
			'textAlign': 'center',
			'color': colors['red'],
			'width': '25%',
			'float': 'left',
			'display': 'inline-block',
			'background':colors['background']
			}
		),

	html.Div(dcc.Graph(id='recovered_ind'),
		style={
			'textAlign': 'center',
			'color': colors['red'],
			'width': '25%',
			'float': 'left',
			'display': 'inline-block'
			}
		),

	html.Div([html.Div(dcc.Graph(id='worldwide_trend'),
			style={'width': '49%', 'float': 'left', 'display': 'inline-block','border':'2px solid red'}
			),
		html.Div([
			dcc.Graph(id='active_countries'),
			html.Div([
				dcc.RadioItems(
					id='column_select',
					options=[{'label': i, 'value': i} for i in ['Confirmed', 'Active', 'Recovered', 'Deaths']],
					value='Active',
					labelStyle={'float': 'center', 'display': 'inline-block'},
					style={'textAlign': 'center',
						'color': colors['text'],
						'width': '100%',
						'float': 'center',
						'display': 'inline-block',
						'backgroundColor':colors['bg']
						}),
				dcc.Dropdown(
					id='country_select',
					multi=True,
					style={'width': '95%', 'float': 'center'}
					)],
				style={'width': '100%', 'float': 'center', 'display': 'inline-block'})
			],
			style={'width': '49%', 'float': 'right', 'vertical-align': 'bottom','border':'2px solid red'}
		)],
		style={'width': '98%', 'float': 'center', 'vertical-align': 'bottom'}
		),

	html.Div(dcc.Graph(id='world_map'),
		style={'width': '48%',
			'display': 'inline-block',
			'margin-top': '15px',
    		'border': '2px solid red',}
		),

	# html.Div([dcc.Graph(id='trajectory')],
	#     style={'width': '50%',
	#         'float': 'right',
	#         'display': 'inline-block'}),

	html.Div(html.Div(dcc.Slider(id='date_slider',
				min=list(range(len(data['date'].unique())))[0],
				max=list(range(len(data['date'].unique())))[-1],
				value=list(range(len(data['date'].unique())))[-1],
				marks={(idx): (date.format(u"\u2011", u"\u2011") if
					(idx-4)%7==0 else '') for idx, date in
					enumerate(sorted(set([item.strftime("%m{}%d{}%Y") for
					item in data['date']])))},
				step=1,
				vertical=False,
				updatemode='mouseup'),
			style={'width': '88.89%', 'float': 'left'}), # width = 1 - (100 - x) / x
		style={'width': '90%', 'float': 'right'}), # width = x

			])

if __name__ == '__main__':
	app.run_server(debug=False)