import { useEffect, useState } from "react";
import apiClient from "../../api/client";
import { Card } from "../../components/ui";
import SeverityBadge from "../../components/SeverityBadge";

const STATUS_STYLES = {
  unassigned: "bg-mist text-graphite",
  assigned: "bg-amber-100 text-amber-800",
  resolved: "bg-green-100 text-green-800",
};

export default function MyReports() {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    apiClient
      .get("/api/incidents/mine")
      .then(({ data }) => setReports(data))
      .catch((err) => setError(err.response?.data?.detail || "Failed to load reports"))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="mx-auto mt-8 max-w-3xl px-6">
      <h1 className="mb-6 text-3xl tracking-tighter text-ink">My reports</h1>
      {loading && <p className="text-graphite">Loading...</p>}
      {error && <p className="text-red-600">{error}</p>}
      {!loading && reports.length === 0 && <p className="text-graphite">No reports yet.</p>}

      <div className="space-y-3">
        {reports.map((r) => (
          <Card key={r.incident_id} className="shadow-float">
            <div className="flex items-start justify-between gap-4">
              <div>
                <p className="font-medium text-ink">{r.description}</p>
                <p className="mt-1 text-xs text-smoke">
                  {r.incident_type} &middot; {new Date(r.created_at).toLocaleString()}
                </p>
              </div>
              <div className="flex flex-col items-end gap-1">
                <SeverityBadge score={r.severity_score} />
                <span className={`rounded-full px-2 py-0.5 text-xs font-semibold ${STATUS_STYLES[r.status]}`}>
                  {r.status}
                </span>
              </div>
            </div>
            {r.assigned_team && (
              <p className="mt-2 text-sm text-graphite">Assigned team: {r.assigned_team}</p>
            )}
            {r.image_url && (
              <img
                src={r.image_url}
                alt="incident"
                className="mt-3 h-32 w-32 rounded-2xl object-cover"
              />
            )}
          </Card>
        ))}
      </div>
    </div>
  );
}
