import { useState } from "react";
import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  useMapEvents,
} from "react-leaflet";

import "leaflet/dist/leaflet.css";
import L from "leaflet";

type Coordinates = {
  lat: number;
  lng: number;
};

// Correction de l'icône du marker avec Vite
const markerIcon = L.icon({
  iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
  iconAnchor: [12, 41],
});

function ClickMarker() {
  const [position, setPosition] = useState<Coordinates | null>(null);

  useMapEvents({
    click(event) {
      const coordinates = {
        lat: event.latlng.lat,
        lng: event.latlng.lng,
      };

      setPosition(coordinates);

      console.log("Latitude :", coordinates.lat);
      console.log("Longitude :", coordinates.lng);
    },
  });

  if (position === null) {
    return null;
  }

  return (
    <Marker position={[position.lat, position.lng]} icon={markerIcon}>
      <Popup>
        Latitude : {position.lat}
        <br />
        Longitude : {position.lng}
      </Popup>
    </Marker>
  );
}

export default function InteractiveMap() {
  return (
    <div>
      <h1>Carte interactive</h1>

      <MapContainer
        center={[48.8566, 2.3522]}
        zoom={12}
        style={{
          height: "500px",
          width: "100%",
        }}
      >
        <TileLayer
          attribution="&copy; OpenStreetMap contributors"
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        <ClickMarker />
      </MapContainer>
    </div>
  );
}
