import { Card, Eyebrow } from "../../components/ui";

export default function Stats({ stats }) {
  if (!stats) return null;

  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
      <Card accent className="shadow-float">
        <Eyebrow className="text-sienna/70">Total incidents</Eyebrow>
        <p className="mt-2 font-serif text-4xl tracking-tighter">{stats.total_incidents}</p>
      </Card>
      <Card className="shadow-float">
        <Eyebrow>By type</Eyebrow>
        <ul className="mt-2 space-y-1 text-sm text-ink">
          {Object.entries(stats.by_type).map(([type, count]) => (
            <li key={type} className="flex justify-between">
              <span className="text-graphite">{type}</span>
              <span className="font-semibold">{count}</span>
            </li>
          ))}
        </ul>
      </Card>
      <Card className="shadow-float">
        <Eyebrow>By status</Eyebrow>
        <ul className="mt-2 space-y-1 text-sm text-ink">
          {Object.entries(stats.by_status).map(([status, count]) => (
            <li key={status} className="flex justify-between">
              <span className="text-graphite">{status}</span>
              <span className="font-semibold">{count}</span>
            </li>
          ))}
        </ul>
      </Card>
    </div>
  );
}
