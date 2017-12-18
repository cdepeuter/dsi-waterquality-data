import React, { Component } from 'react';
import { Map, CircleMarker, Popup} from 'react-leaflet'
import { where} from 'underscore'
import Legend from './Legend';
import 'whatwg-fetch'; 

export default class StationLayer extends React.Component {

	constructor(props) {
	    super(props);
	    this.state = {
	     	stations : [],
	     	params: [],
	     	colorstat : '',
	     	colorstatname: '',
	     	dataurl:this.props.dataurl,
	     	year:'2017',
	     	month:'all'
	    }
	    this.handleViewChange = this.handleViewChange.bind(this);
	    this.changeData = this.changeData.bind(this);
	    this.renderStation = this.renderStation.bind(this);
	}

	componentDidMount() {
		this.getData(this.state.year, this.state.month);
	}

	handleViewChange(option){

	    this.setState({colorstat:option.value, colorstatname:option})
	}

	getData(year, month) {
		const url = this.props.dataurl + year + "/" + month
		console.log("getting data", url)
		fetch(url).then( (response) => {
			return response.json() })   
				.then( (json) => {
					console.log("JSON resp", json)
					if(!!json && json.stations){
						this.setState({stations: json.stations, params:json.params, years:json.years, months:json.months, month:month, year:year, colorstat:json.params[0]["value"], colorstatname:json.params[0]["label"]});
					} 
			}
		);
	}

	changeData(val){
		if( val["value"] < 15 || val["value"] == 'all'){
			// it must be a month
			this.getData(this.state.year, val["value"])
		} else {
			this.getData(val["value"], this.state.month)
		}
	}

	renderStation(s){
		let markup = "<dl> Station: " +s.Station
		for(var param in this.state.params){

			var p = this.state.params[param];
			markup += "<dd>"
			markup += p["label"] + ": " + s[p["value"]]
			markup += ",  "
			markup += p["label"] + " Min: " + s[p["value"] + "_min"]
			markup += ",   "
			markup += p["label"] + " Max: " + s[p["value"] + "_max"]
			markup += "</dd>"
		} 
		markup += "</dl>"
		return markup
	}

    render() {
    	let defaultStat = this.state.params.length > 0 ? this.state.params[0]["value"] : ''
		let displayStat = this.state.colorstat == '' ? defaultStat : this.state.colorstat
		let explainer = where(this.state.params, {'value':displayStat})
		let defaultMonth = this.state.month != 'all' ? this.state.months[this.state.month-1]["label"] : this.state.month
		let markers = this.state.stations.map((station) =>
		   	<CircleMarker center={[station.lat, station.lon]} color={station[this.state.colorstat + "_color"]} fillOpacity="1" radius={5}>
		      <Popup>
		        <span dangerouslySetInnerHTML={{ __html: this.renderStation(station) }} />
		      </Popup>
		    </CircleMarker> 
		);
        return (
	        <div>
	        	<div>
	        		<Legend explainer={explainer} stat={this.state.colorstatname} changeData={this.changeData} month={defaultMonth} months={this.state.months} year={this.state.year} years={this.state.years} country={this.props.country} params={this.state.params}  changeStat={this.handleViewChange}/>
	        	</div>
	        	<div>
	        		{markers}
	        	</div>
	        </div>
         
      )
    }
}
