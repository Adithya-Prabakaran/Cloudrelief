import L from "leaflet";
import { CircleMarker, MapContainer, Popup, TileLayer } from "react-leaflet";
import { severityColor } from "../../components/SeverityBadge";

// Default incidents to a sensible fallback center when there's no data yet.
const DEFAULT_CENTER = [37.7749, -122.4194];

export default function IncidentMap({ incidents }) {
  const center =
    incidents.length > 0 ? [incidents[0].latitude, incidents[0].longitude] : DEFAULT_CENTER;

  return (
    <MapContainer center={center} zoom={12} style={{ height: "420px", width: "100%" }}>
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {incidents.map((incident) => (
        <CircleMarker
          key={incident.incident_id}
          center={[incident.latitude, incident.longitude]}
          radius={10}
          pathOptions={{
            color: severityColor(incident.severity_score),
            fillColor: severityColor(incident.severity_score),
            fillOpacity: 0.8,
          }}
        >
          <Popup>
            <div className="text-sm">
              <p className="font-semibold">{incident.incident_type}</p>
              <p>{incident.description}</p>
              <p>Severity: {incident.severity_score.toFixed(2)}</p>
              <p>Status: {incident.status}</p>
            </div>
          </Popup>
        </CircleMarker>
      ))}
    </MapContainer>
  );
}

// Fixes a common Vite/Leaflet marker icon issue for any default L.marker usage.
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
  iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
});
