import React, { Component } from 'react'
import { Map, TileLayer, GeoJson} from 'react-leaflet';
import StationLayer from './StationLayer';
import 'whatwg-fetch'; 

const leafletUrl = "https://api.mapbox.com/styles/v1/mapbox/light-v9/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1IjoiY2RlcGV1dGVyIiwiYSI6ImNqMWUyOXVubTAwMDQycXVzYnNrcGtmdnAifQ.7fCYPAnsWbjiR5RW4tyRKA"

export default class SouthAfricaLayer extends Component {

  constructor(props) {
    super(props);
      this.state = {
        lat: 38.7501236,
        lng: 120.9370523,
        zoom: window.innerWidth < 600 ? 3 : 4,
        bluemarble: false,
        dataurl : "/stations/china/"
      }
  }
  
  render () {
    return (
      <Map
        center={[this.state.lat, this.state.lng]}
        zoom={this.state.zoom}
        onClick={this.onClick}>
        <TileLayer
          layers='ne:ne'
          url={leafletUrl}
        />
        <StationLayer country='china' dataurl={this.state.dataurl}  /> 
      </Map>
    )
  }
}