export function severityColor(score) {
  if (score >= 0.6) return "#dc2626"; // red
  if (score >= 0.35) return "#f59e0b"; // amber
  return "#16a34a"; // green
}

export default function SeverityBadge({ score }) {
  const color = severityColor(score);
  return (
    <span className="inline-flex items-center gap-1.5 rounded-full border border-ink/10 bg-paper px-2.5 py-1 text-xs font-medium text-ink">
      <span className="h-1.5 w-1.5 rounded-full" style={{ backgroundColor: color }} />
      {score.toFixed(2)}
    </span>
  );
}
