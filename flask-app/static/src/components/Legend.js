import React, { Component } from 'react';
import Toggle from 'react-bootstrap-toggle';
import { Map, CircleMarker, Popup} from 'react-leaflet'
import Dropdown from 'react-dropdown';
import { where} from 'underscore';
import StatIndicatorLayer from './StatIndicatorLayer';

export default class Legend extends React.Component {

	constructor(props) {
	    super(props);
	    this.state = {
	    	countries : [{'label':'South Africa', 'value' : 'southafrica'}, {'label':'China', 'value':'china'}],
	    	labelTags: {'sa':'South Africa', 'china':'China'}

	    }
	   	this.handleStatChange = this.handleStatChange.bind(this);
	   	this.changeCountry = this.changeCountry.bind(this);
	   	this.changeData = this.changeData.bind(this);
	}

	handleStatChange(option) {
		this.props.changeStat(option);
	}

	changeCountry(val) {
		window.location.href = val['value'];
	}

	changeData(val){
		this.props.changeData(val);
	}

    render() {
    	const defaultStat = !!this.props.params ? this.props.params[0] : '';
    	const defaultMonth = this.props.month == 'all' ? 'All Months' : this.props.month;
        const displayStat = !!this.props.stat ? this.props.stat : defaultStat;
        return (
        	<div id="legend" className="legend">
        		<Dropdown options={this.props.years} onChange={this.changeData} value={this.props.year} placeholder="Select an option" />
		       	<Dropdown options={this.props.months} onChange={this.changeData} value={defaultMonth} placeholder="dsfa" />
				<Dropdown options={this.props.params} onChange={this.handleStatChange} value={displayStat} placeholder="Select an option" />
		       	<Dropdown options={this.state.countries} onChange={this.changeCountry} value={this.state.labelTags[this.props.country]} placeholder="Select an option" />
		    	<StatIndicatorLayer stat={this.props.explainer} />

	       </div>
      )
    }
}
