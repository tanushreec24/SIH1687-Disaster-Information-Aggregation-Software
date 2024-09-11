// MapComponent.js
import React from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

const position = [51.505, -0.09]; // Replace with the coordinates for the specific area

function MapComponent() {
  return (
    <MapContainer center={position} zoom={13} style={{ height: "400px", width: "100%" }}>
      {/* TileLayer provides the map tiles (background) */}
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      />
      
      {/* Marker places a pin on the map */}
      <Marker position={position}>
        <Popup>
          This is the location you've chosen!
        </Popup>
      </Marker>
    </MapContainer>
  );
}

export default MapComponent;

