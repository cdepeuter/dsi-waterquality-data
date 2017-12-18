
# Water Quality webapp

### Setting up docker image 

Docker is not necessary for this to run, but recommended for easy environment configuration. If you wish to not use docker, make sure npm and python are installed, as well as all of the python packages in flask-app/requirements.txt.

From the root directory of this repo

`$ docker build -t <org>/<image_name> .`

`$ docker push <org>/<image_name> .`

### Flask app

To run the Flask webserver, including api and front end:

`$ python app.py `

If it started successfully you should see 
` Running on http://0.0.0.0:5000/ (Press CTRL+C to quit) `

The Stations api is available at 
http://0.0.0.0:5000/stations/south_africa/2017/all

The webapp is available at 
http://0.0.0.0:5000/

All of the code for the server is in app.py.  

### React App

Make sure your npm is installed and up to date

` $ npm -v `

Then install all required packages

` $ npm install `

Finally, build the js file

` $ npm run build `

Or run webpack so any changes appear in the main.js file.

` $ npm start `