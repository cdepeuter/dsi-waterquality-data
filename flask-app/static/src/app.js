import React from 'react';
import ReactDOM from 'react-dom';
import SouthAfricaLayer from './components/SouthAfricaLayer'
import ChinaLayer from './components/ChinaLayer'


 let accessToken = 'pk.eyJ1IjoiY2RlcGV1dGVyIiwiYSI6ImNqMWUyOXVubTAwMDQycXVzYnNrcGtmdnAifQ.7fCYPAnsWbjiR5RW4tyRKA';

if (window.location.href.includes("china")){
	ReactDOM.render(<ChinaLayer  />, document.getElementById("china_container"));
}else{	
	ReactDOM.render(<SouthAfricaLayer  />, document.getElementById("container"));
}

