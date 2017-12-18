import React, { Component } from 'react'
import { Map, TileLayer, GeoJson} from 'react-leaflet';
import StationLayer from './StationLayer';
import 'whatwg-fetch'; 

const leafletUrl = "https://api.mapbox.com/styles/v1/mapbox/light-v9/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1IjoiY2RlcGV1dGVyIiwiYSI6ImNqMWUyOXVubTAwMDQycXVzYnNrcGtmdnAifQ.7fCYPAnsWbjiR5RW4tyRKA"

export default class SouthAfricaLayer extends Component {
  
  constructor(props) {
    super(props);
      this.state = {
        lat: -29.814802,
        lng: 24.4841103,
        zoom: window.innerWidth < 600 ? 5 : 6,
        dataurl : "/stations/south_africa/"
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
        <StationLayer country='sa' dataurl={this.state.dataurl}/> 
      </Map>
    )
  }
}