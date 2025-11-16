/**
 * Animal map component using Leaflet.
 */
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import { useEffect } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import './AnimalMap.css';

// Fix for default marker icons in Leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

// Component to center map on animal
function MapCenter({ animal }) {
  const map = useMap();
  
  useEffect(() => {
    if (animal) {
      const lat = animal.location_lat || animal.lat || animal.latitude || animal.y;
      const lon = animal.location_long || animal.lon || animal.longitude || animal.x;
      
      if (lat && lon) {
        map.setView([parseFloat(lat), parseFloat(lon)], 13);
      }
    }
  }, [animal, map]);
  
  return null;
}

const AnimalMap = ({ animal }) => {
  const lat = animal
    ? parseFloat(animal.location_lat || animal.lat || animal.latitude || animal.y || 30.2672)
    : 30.2672;
  const lon = animal
    ? parseFloat(animal.location_long || animal.lon || animal.longitude || animal.x || -97.7431)
    : -97.7431;

  return (
    <div className="animal-map-container">
      <h2>Location Map</h2>
      <div className="map-wrapper">
        <MapContainer
          center={[lat, lon]}
          zoom={animal ? 13 : 10}
          style={{ height: '400px', width: '100%' }}
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          {animal && (
            <>
              <Marker position={[lat, lon]}>
                <Popup>
                  <div>
                    <strong>{animal.name || 'Unnamed'}</strong>
                    <br />
                    {animal.breed || 'Unknown breed'}
                    <br />
                    {animal.animal_type || 'Unknown type'}
                  </div>
                </Popup>
              </Marker>
              <MapCenter animal={animal} />
            </>
          )}
        </MapContainer>
      </div>
      {!animal && (
        <p className="map-hint">Select an animal from the table to view its location</p>
      )}
    </div>
  );
};

export default AnimalMap;

