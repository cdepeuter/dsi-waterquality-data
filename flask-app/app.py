from flask import Flask, jsonify, request, render_template
from flask_restful import Resource, Api
from flask_cache import Cache
import sys
import requests
import io
import json
import pandas as pd
import datetime
from colour import Color
import datetime
import random

app = Flask(__name__)

# set up api and caching
api = Api(app)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

with app.app_context():
	MAX_DECIMALS = 3 
	# get color range for station status and bike angels
	red = Color("red")
	green = Color("green")
	colors = list(green.range_to(red,101))
	months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
	

	# get current status and merge that with stations
	# data_url = "https://raw.githubusercontent.com/cdepeuter/dsi-waterquality-data/master/south_africa_data.csv"
	# x = requests.get(url=data_url).content 
	# data = pd.read_csv(io.StringIO(x.decode('utf8')))
	# local for testing
	sa_data = pd.read_csv("data/south_africa_data.csv")
	print("south africa data shape", sa_data.shape)
	# list all params and calc min and max for legend display
	sa_water_params = [
		{'value': 'hardness', 'label':'Hardness', 'min':round(sa_data.hardness.min(), MAX_DECIMALS), 'max' :round(sa_data.hardness.max(), MAX_DECIMALS), 'explainer': 'Hardness (mg/L)'}, 
		{'label':'pH', 'value' :'ph', 'min': round(sa_data.ph.min(), MAX_DECIMALS), 'max':round(sa_data.ph.max(), MAX_DECIMALS), 'explainer':'pH: (ph Units)'},
		{'label':'Potassium', 'value' :'k', 'min': round(sa_data.k.min(), MAX_DECIMALS), 'max':round(sa_data.k.max(), MAX_DECIMALS), 'explainer':'Potassium: (mg/L)'},
		#{'label':'Dissolved Salts', 'value' :'dms', 'min': round(sa_data.dms.min(), MAX_DECIMALS), 'max':round(sa_data.dms.max(), MAX_DECIMALS), 'explainer':'Dissolved Salts: (mg/L)'},
		#{'label':'Phosphorus', 'value' :'p', 'min': round(sa_data.dms.min(), MAX_DECIMALS), 'max':round(sa_data.dms.max(), MAX_DECIMALS), 'explainer':'Phosphorus: (mg/L)'},

		{'label':'Electrical Conductivity', 'value' :'ec', 'min': round(sa_data.ec.min(), MAX_DECIMALS), 'max':round(sa_data.ec.max(), MAX_DECIMALS), 'explainer':'Electrical Conductivity: (Millisiemens per Metre)'},
		{'label':'Chloride', 'value' :'cl', 'min': round(sa_data.ec.min(), MAX_DECIMALS), 'max':round(sa_data.ec.max(), MAX_DECIMALS), 'explainer':'Chloride: (mg/L)'},
		{'label':'Fluoride', 'value' :'f', 'min': round(sa_data.ec.min(), MAX_DECIMALS), 'max':round(sa_data.ec.max(), MAX_DECIMALS), 'explainer':'Fluoride: (mg/L)'},
		{'label':'Sodium', 'value' :'na', 'min': round(sa_data.ec.min(), MAX_DECIMALS), 'max':round(sa_data.ec.max(), MAX_DECIMALS), 'explainer':'Sodium: (mg/L)'},
		{'label':'Silicon', 'value' :'si', 'min': round(sa_data.ec.min(), MAX_DECIMALS), 'max':round(sa_data.ec.max(), MAX_DECIMALS), 'explainer':'Fluoride: (mg/L)'},
		{'label':'Total Alkalinity', 'value' :'tal', 'min': round(sa_data.ec.min(), MAX_DECIMALS), 'max':round(sa_data.ec.max(), MAX_DECIMALS), 'explainer':'Total Alkalinity: (mg/L)'},
		{'label':'Sulphate', 'value' :'so', 'min': round(sa_data.ec.min(), MAX_DECIMALS), 'max':round(sa_data.ec.max(), MAX_DECIMALS), 'explainer':'Sulphate: (mg/L)'},
		{'label':'Ammonium Nitrogen', 'value' :'amn', 'min': round(sa_data.ec.min(), MAX_DECIMALS), 'max':round(sa_data.ec.max(), MAX_DECIMALS), 'explainer':'Ammonium Nitrogen: (mg/L)'},
		{'label':'Nitrate + Nitrite Nitrogen', 'value' :'no', 'min': round(sa_data.ec.min(), MAX_DECIMALS), 'max':round(sa_data.ec.max(), MAX_DECIMALS), 'explainer':'Nitrate + Nitrite Nitrogen: (mg/L)'}
	]
   
	# get min and max values and 
	for s in sa_water_params:
		param_min = sa_data[s["value"]].min()
		param_max = sa_data[s["value"]].max()
		sa_data[s["value"] + "_color"] = sa_data[s["value"]].map(lambda x: colors[int((x-param_min)*100/(param_max-param_min))].hex)

	# get years and params available for this country
	sa_year_params = [str(y) for y in sorted(sa_data.year.unique())]

	#data_url = "https://raw.githubusercontent.com/cdepeuter/dsi-waterquality-data/master/merged_china_data_2017.csv"
	# x = requests.get(url=data_url).content 
	# data = pd.read_csv(io.StringIO(x.decode('utf8')))
	# for local testing
	china_data = pd.read_csv("data/merged_china_data.csv")
	print("china data shape", china_data.shape)
	# add colors for param, get max and min vals first so we arent doing an O(n) operation for each row
	qual_min = china_data.quality.min()
	qual_max = china_data.quality.max()
	ph_min = china_data.ph.min()
	ph_max = china_data.ph.max()
	do_min = china_data.do.min()
	do_max = china_data.do.max()
	cod_min = china_data.cod.min()
	cod_max = china_data.cod.max()
	nh_min = china_data.nh.min()
	nh_max = china_data.nh.max()
	china_data['quality_color'] = china_data.quality.map(lambda x: colors[int((x-qual_min)*100/(qual_max-qual_min))].hex)
	china_data['ph_color'] = china_data.ph.map(lambda x: colors[int(100*(x-ph_min)/(ph_max-ph_min))].hex)
	china_data['do_color'] = china_data.do.map(lambda x: colors[int((x-do_min)*100/(do_max-do_min))].hex)
	china_data['cod_color'] = china_data.cod.map(lambda x: colors[int((x-cod_min)*100/(cod_max-cod_min))].hex)
	china_data['nh_color'] = china_data.nh.map(lambda x: colors[int((x-nh_min)*100/(nh_max-nh_min))].hex)
	# get years and params available for this country
	china_year_params = [str(y) for y in range(china_data.year.min(), china_data.year.max() + 1)]
	china_water_params = [
		{'label': 'Quality', 'value':'quality', 'min':round(china_data.quality.min(),MAX_DECIMALS), 'max':round(china_data.quality.max(), MAX_DECIMALS), 'explainer':'Quality: (1-5 scale)'}, 
		{'label':'pH', 'value' :'ph', 'min':round(china_data.ph.min(), MAX_DECIMALS), 'max':round(china_data.ph.max(), MAX_DECIMALS), 'explainer':'pH: (ph Units)'}, 
		{'label':'Dissolved Oxygen', 'value':'do', 'min':round(china_data.do_min.min(), MAX_DECIMALS), 'max':round(china_data.do.max(), MAX_DECIMALS), 'explainer':'Dissolved Oxygen (mg/L)'}, 
		{'label' :'Carbon Dioxide', 'value':'cod', 'min':round(china_data.cod_min.min(), MAX_DECIMALS), 'max':round(china_data.cod.max(), MAX_DECIMALS), 'explainer':'Carbon Dioxide (mg/L)'}, 
		{'label' :'Ammonia', 'value':'nh', 'min':round(china_data.nh_min.min(), MAX_DECIMALS), 'max':round(china_data.nh.max(), MAX_DECIMALS), 'explainer':'Ammonia (mg/L)'}, 
	]

@app.route('/')
@app.route('/southafrica')
def index():
    return render_template('leaflet.html')

@app.route("/china")
def map():
	return render_template('china_leaflet.html')

class Stations(Resource):	
	@cache.cached(timeout=50)
	def get(self, country, year, month):
		# convert params to integers
		year = int(year)
		if month != 'all':
			month = int(month)
		
		if country == "south_africa":
			if year == 1000:
				filtered_sa_data = sa_data[sa_data.year == sa_data.year.max()]
			else:
				filtered_sa_data = sa_data[sa_data.year == year]
			# get month options for year before setting the month (what months are available for the chosen year?)
			month_dict = [{'value': int(i), 'label': months[i-1]} for i in sorted(filtered_sa_data.month.unique())]
			month_dict.append({'value':'all', 'label':'All Months'})
			# now filter by months
			if month != 'all':
				filtered_sa_data = filtered_sa_data[filtered_sa_data.month == month]

			return {'stations':filtered_sa_data.to_dict(orient='records'), 'params':sa_water_params, 'years' : sa_year_params, 'months':month_dict}
		elif country == "china":
			if year == 1000:
				filtered_china_data = china_data[china_data.year == china_data.year.max()]
			else:
				filtered_china_data = china_data[china_data.year == year]
			# get month options for year before setting the month
			month_dict = [{'value': int(i), 'label': months[i-1]} for i in sorted(filtered_china_data.month.unique())]
			month_dict.append({'value':'all', 'label':'All Months'})
			if month != 'all':
				filtered_china_data = filtered_china_data[filtered_china_data.month == month]

			return {'stations':filtered_china_data.to_dict(orient='records'), 'params':china_water_params,  'years' : china_year_params, 'months':month_dict}
		else:
			return "unknown country " + country, 404


api.add_resource(Stations, '/stations/<string:country>/<string:year>/<string:month>')

if __name__ == "__main__":
    #app.run(debug=True) # for dev
    app.run(host='0.0.0.0') # for prod

