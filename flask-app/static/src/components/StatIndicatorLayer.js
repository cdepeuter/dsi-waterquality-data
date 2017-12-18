import React, { Component } from 'react';
import Toggle from 'react-bootstrap-toggle';
import Dropdown from 'react-dropdown'

export default class StatIndicatorLayer extends React.Component {
	constructor(props) {
	    super(props);
	}


    render() {

    	const defaultOption = !!this.props.params ? this.props.params[0] : '';
    	const exp = !!this.props.stat && !!this.props.stat[0] ? this.props.stat[0].explainer : '';
    	const min = !!this.props.stat && !!this.props.stat[0] ? this.props.stat[0].min : '';
    	const max = !!this.props.stat && !!this.props.stat[0] ? this.props.stat[0].max : '';
        return (
        	<div className="statIndicator">
        		<div className="indicatorContents">
	        		<div className="redCircle"/>
	        		<div className="explainerBox indicatorContents">
	        			<div className="indicatorContents">{exp}</div>
	        			<div className="minimax">
	        				<div className="min">{min}</div>
	        				<div className="max">{max}+</div>
	        			</div>
	        		</div>
	        		<div className="greenCircle"/>
        		</div>
			</div>
      )
    }
}
