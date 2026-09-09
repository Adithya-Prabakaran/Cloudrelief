import { useMemo, useState } from "react";
import SeverityBadge from "../../components/SeverityBadge";

const STATUS_OPTIONS = ["unassigned", "assigned", "resolved"];

const selectClasses =
  "rounded-full border border-ink/10 bg-paper px-3 py-1.5 text-xs text-ink outline-none focus:border-ink/40";

export default function IncidentTable({ incidents, teams, onAssign, onStatusChange }) {
  const [sortBy, setSortBy] = useState("severity");

  const sorted = useMemo(() => {
    const copy = [...incidents];
    if (sortBy === "severity") copy.sort((a, b) => b.severity_score - a.severity_score);
    if (sortBy === "status") copy.sort((a, b) => a.status.localeCompare(b.status));
    if (sortBy === "time") copy.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
    return copy;
  }, [incidents, sortBy]);

  return (
    <div className="overflow-hidden rounded-3xl border border-ink/[0.06] bg-paper">
      <div className="flex items-center justify-between border-b border-ink/[0.06] px-5 py-4">
        <h2 className="font-serif text-lg text-ink">Incidents</h2>
        <div className="flex items-center gap-2 text-sm">
          <span className="text-graphite">Sort by</span>
          <select className={selectClasses} value={sortBy} onChange={(e) => setSortBy(e.target.value)}>
            <option value="severity">Severity</option>
            <option value="status">Status</option>
            <option value="time">Time</option>
          </select>
        </div>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-left text-sm">
          <thead className="text-xs uppercase tracking-tight text-graphite">
            <tr>
              <th className="px-5 py-3 font-medium">Type</th>
              <th className="px-5 py-3 font-medium">Description</th>
              <th className="px-5 py-3 font-medium">Severity</th>
              <th className="px-5 py-3 font-medium">Status</th>
              <th className="px-5 py-3 font-medium">Team</th>
              <th className="px-5 py-3 font-medium">Reported</th>
              <th className="px-5 py-3 font-medium">Photo</th>
            </tr>
          </thead>
          <tbody>
            {sorted.map((incident) => (
              <tr key={incident.incident_id} className="border-t border-ink/[0.06]">
                <td className="px-5 py-3 font-medium text-ink">{incident.incident_type}</td>
                <td className="max-w-xs truncate px-5 py-3 text-graphite" title={incident.description}>
                  {incident.description}
                </td>
                <td className="px-5 py-3">
                  <SeverityBadge score={incident.severity_score} />
                </td>
                <td className="px-5 py-3">
                  <select
                    className={selectClasses}
                    value={incident.status}
                    onChange={(e) => onStatusChange(incident.incident_id, e.target.value)}
                  >
                    {STATUS_OPTIONS.map((s) => (
                      <option key={s} value={s}>
                        {s}
                      </option>
                    ))}
                  </select>
                </td>
                <td className="px-5 py-3">
                  <select
                    className={selectClasses}
                    value={incident.assigned_team || ""}
                    onChange={(e) => onAssign(incident.incident_id, e.target.value)}
                  >
                    <option value="" disabled>
                      Assign team...
                    </option>
                    {teams.map((t) => (
                      <option key={t} value={t}>
                        {t}
                      </option>
                    ))}
                  </select>
                </td>
                <td className="whitespace-nowrap px-5 py-3 text-xs text-smoke">
                  {new Date(incident.created_at).toLocaleString()}
                </td>
                <td className="px-5 py-3">
                  {incident.image_url && (
                    <a
                      href={incident.image_url}
                      target="_blank"
                      rel="noreferrer"
                      className="text-xs text-ink underline underline-offset-2"
                    >
                      View
                    </a>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
