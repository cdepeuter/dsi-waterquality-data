# Columbia DSI Capstone Project

## Building a Webapp to give a spatial understanding of water quality
In this project our goal was to help collect data and build a tool to understand water quality in certain areas of interest. We have collected and cleaned data for South Africa and China, and built a webapp to help view the data and how it changes throught time.

![alt text](https://github.com/cdepeuter/dsi-waterquality-data/blob/master/flask-app/static/media/appview.png "View of app ")

## Data Cleaning

Cleaned versions of the data are aleady in this repo for use in the webapp, so this process does not need to be run in order for the webapp to work. This Repo contains data for South Africa and China. The data contains no NA's, so in the collection process those should be removed/replaced as desired.


### South Africa Data

South Africa data is scraped from http://www.dwa.gov.za/iwqs/wms/data/WMS_pri_txt.asp, downloaded, combined and cleaned. The scraping is done in scrape_south_africa_data.py. There are hundreds of thousands of files to download, so this process may take a few hours. This process should be run periodically in order to collect the latest data.

`$ python scrape_south_africa_data.py`

The cleaning is done in clean_south_africa_data.py and reads from the scraped files. Once saved it is written to the data/flask-app folder where it is consumed by the webapp. 

`$ python clean_south_africa_data.py`



### China Data:
The water quality data for China runs from 2016-2017 and is collected from http://www.mep.gov.cn/hjzl/shj/dbszdczb/. The data comes in a few different files, one of metadata for each station, and then various files for each parameter/year. The downloaded files are located in /china_data. With those files in place, cleaning and merging the data is done in merge_china_data.py. The output is saved to flask-app/data/merged_china_data.py for consumption by the API.

`$ python merge_china_data.py`

## Python Server/Javascript Changes

To add more sources, a few updates need to be made.
* In flask-app/app.py, add a new route and html template for the new country (https://github.com/cdepeuter/dsi-waterquality-data/blob/master/flask-app/app.py#L97)
* In flask-app/app.py, under `with app.app_context()` load the cleaned data and add parameter colors as is done for the China and South Africa sources (https://github.com/cdepeuter/dsi-waterquality-data/blob/master/flask-app/app.py#L20)
* In flask-app/app.py add a new API for the country in the same format as china and South Africa (https://github.com/cdepeuter/dsi-waterquality-data/blob/master/flask-app/app.py#L122)
* Under flask-app/static/src/components/ add a new Layer for that country, in the same format as ChinaLayer.js and SouthAfricaLayer.js. You can copy one of those files and that needs to be changed are the country specific lines (lat/long, dataurl, Station layer params, and Layer/file names.) (https://github.com/cdepeuter/dsi-waterquality-data/blob/master/flask-app/static/src/components/ChinaLayer.js)
* In flask-app/static/src/components/Legend.js, add country and label tags to the Component state. The country tag should mirror the html file route, and the labelTag should mirror the country prop in the new <Country>Layer.js component.

## Setting up docker image (not required)

Docker is not necessary for this to run, but recommended for easy environment configuration.

From the root directory of this repo

`$ docker build -t <org>/<image_name> .`

`$ docker push <org>/<image_name> .`


### Building on AWS (not required)

The recommended way to run the webapp is use Amazon Elastic Beanstalk. By building a container using Docerrun.aws.json, an environment with Python and Node, and all the required packages is easily installed. When changes are made to this github repo, they will automatically rebuild the image, and changes show in the production environment by simply clicking "Rebuild Environment". 

However, all that really needs to be done is install the required python packages, and run one command from the /flask-app directory.
* `$ python app.py`

Once this is run, the app will be available at http://0.0.0.0:5000

If any javascript changes are made then nodejs/npm needs to be installed, and one more command needs to be run:

* `$ npm start`

More detailed instructions are in the README in the flask-app directory