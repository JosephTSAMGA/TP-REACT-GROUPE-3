// =============================================================
// PARTIE 2/4 — Le cœur du jeu (carte & manches)
// Fichiers de cette partie : GamePage.tsx, RoundScreen.tsx (+.css),
// InteractiveMap.tsx.
// Rôle de ce fichier : la carte interactive (librairie react-leaflet)
// sur laquelle le joueur clique pour placer sa réponse.
// =============================================================
import { useState } from "react";
import { MapContainer, TileLayer, Marker, Popup, useMapEvents } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import type { Coordinates } from "../../shared/types";

// Leaflet a besoin qu'on lui décrive explicitement l'icône du marqueur
// (image + taille + point d'ancrage), sinon il utilise une icône cassée
// par défaut. On la définit une seule fois, en dehors des composants,
// pour ne pas la recréer à chaque rendu.
const markerIcon = L.icon({
  iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
});

type ClickMarkerProps = {
  onPositionChange: (coords: Coordinates) => void;
};

// Composant "invisible" placé à l'intérieur de <MapContainer> dont le
// seul but est d'écouter les clics sur la carte (via le hook
// `useMapEvents` fourni par react-leaflet) et d'afficher un marqueur
// à l'endroit cliqué.
function ClickMarker({ onPositionChange }: ClickMarkerProps) {
  // Position du marqueur, gérée en interne pour l'afficher immédiatement ;
  // en plus, on prévient le parent (RoundScreen) via onPositionChange.
  const [position, setPosition] = useState<Coordinates | null>(null);

  useMapEvents({
    click(event) {
      const coordinates: Coordinates = {
        lat: event.latlng.lat,
        lng: event.latlng.lng,
      };
      setPosition(coordinates);
      onPositionChange(coordinates);
    },
  });

  // Tant que le joueur n'a pas cliqué, on n'affiche aucun marqueur.
  if (position === null) return null;

  return (
    <Marker position={[position.lat, position.lng]} icon={markerIcon}>
      <Popup>
        Latitude : {position.lat.toFixed(5)}
        <br />
        Longitude : {position.lng.toFixed(5)}
      </Popup>
    </Marker>
  );
}

type InteractiveMapProps = {
  onPositionChange?: (coords: Coordinates) => void;
};

// Composant exporté : une carte OpenStreetMap plein cadre, centrée sur
// Paris par défaut, zoomable/déplaçable, avec le marqueur cliquable
// ci-dessus intégré dedans.
export default function InteractiveMap({ onPositionChange = () => {} }: InteractiveMapProps) {
  return (
    <MapContainer
      center={[48.8566, 2.3522]}
      zoom={5}
      scrollWheelZoom={true}
      style={{ height: "100%", width: "100%", borderRadius: "10px" }}
    >
      {/* TileLayer = les tuiles d'images qui forment le fond de carte,
          fournies gratuitement par OpenStreetMap. */}
      <TileLayer
        attribution="&copy; OpenStreetMap contributors"
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <ClickMarker onPositionChange={onPositionChange} />
    </MapContainer>
  );
}
