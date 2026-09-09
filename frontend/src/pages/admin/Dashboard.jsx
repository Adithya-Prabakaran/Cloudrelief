import { useEffect, useState } from "react";
import apiClient from "../../api/client";
import { Button } from "../../components/ui";
import { useAuth } from "../../context/AuthContext";
import IncidentMap from "./IncidentMap";
import IncidentTable from "./IncidentTable";
import Stats from "./Stats";

const POLL_INTERVAL_MS = 8000;

export default function Dashboard() {
  const { user, logout } = useAuth();
  const [incidents, setIncidents] = useState([]);
  const [stats, setStats] = useState(null);
  const [teams, setTeams] = useState([]);
  const [error, setError] = useState("");

  const refresh = async () => {
    try {
      const [incidentsRes, statsRes, teamsRes] = await Promise.all([
        apiClient.get("/api/incidents"),
        apiClient.get("/api/incidents/stats"),
        apiClient.get("/api/incidents/teams"),
      ]);
      setIncidents(incidentsRes.data);
      setStats(statsRes.data);
      setTeams(teamsRes.data.teams);
      setError("");
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to load dashboard data");
    }
  };

  useEffect(() => {
    refresh();
    // Simple polling stands in for a live feed; swapping to WebSockets/SSE
    // later would only touch this effect, not the child components.
    const id = setInterval(refresh, POLL_INTERVAL_MS);
    return () => clearInterval(id);
  }, []);

  const handleAssign = async (incidentId, team) => {
    await apiClient.patch(`/api/incidents/${incidentId}/assign`, { assigned_team: team });
    refresh();
  };

  const handleStatusChange = async (incidentId, status) => {
    await apiClient.patch(`/api/incidents/${incidentId}/status`, { status });
    refresh();
  };

  return (
    <div className="mx-auto max-w-page px-6 pb-20 sm:px-10">
      <div className="mb-8 flex items-center justify-between">
        <h1 className="text-3xl tracking-tighter text-ink">Admin dashboard</h1>
        <div className="flex items-center gap-3 text-sm text-graphite">
          <span>{user?.email}</span>
          <Button variant="ghost" onClick={logout}>
            Log out
          </Button>
        </div>
      </div>

      {error && <p className="mb-4 text-red-600">{error}</p>}

      <div className="mb-6">
        <Stats stats={stats} />
      </div>

      <div className="mb-6 overflow-hidden rounded-3xl border border-ink/[0.06]">
        <IncidentMap incidents={incidents} />
      </div>

      <IncidentTable
        incidents={incidents}
        teams={teams}
        onAssign={handleAssign}
        onStatusChange={handleStatusChange}
      />
    </div>
  );
}
