"""
Parses Locust's CSV output (from `locust --csv=results/run1 ...`) and writes
a summary CSV with p50/p95/p99 latency, error rate, and a *mocked*
cost-per-1000-requests figure — same shape you'll want later when comparing
AWS Lambda/API Gateway pricing against the Oracle Cloud VM.

Usage:
    locust -f locustfile.py --host http://localhost:8000 \
        --headless --csv=results/run1 --run-time 10m

    python analyze_results.py results/run1_stats.csv --out results/summary.csv

Cost-per-1000-requests is a placeholder: it's computed from
COST_PER_REQUEST below, which you should replace with real AWS pricing
(Lambda invocation + API Gateway request cost) once you're benchmarking
against the cloud deployment. For the local Docker stack it's fixed at 0,
since there's no per-request cloud billing to compare against yet.
"""
import argparse
import csv
import sys

# Placeholder $/request used only to produce a comparable "cost per 1000
# requests" column locally. Set to real AWS pricing when this same script
# is pointed at Lambda/API Gateway results later.
COST_PER_REQUEST = 0.0


def analyze(stats_csv_path: str, out_path: str):
    with open(stats_csv_path, newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    summary_rows = []
    for row in rows:
        name = row.get("Name", "")
        if name == "Aggregated" or not name:
            continue

        request_count = int(row.get("Request Count", 0) or 0)
        failure_count = int(row.get("Failure Count", 0) or 0)
        error_rate = (failure_count / request_count * 100) if request_count else 0.0

        p50 = row.get("50%", row.get("Median Response Time", "0"))
        p95 = row.get("95%", "0")
        p99 = row.get("99%", "0")

        cost_per_1000 = COST_PER_REQUEST * 1000

        summary_rows.append(
            {
                "endpoint": name,
                "request_count": request_count,
                "failure_count": failure_count,
                "error_rate_pct": round(error_rate, 3),
                "p50_ms": p50,
                "p95_ms": p95,
                "p99_ms": p99,
                "avg_response_ms": row.get("Average Response Time", ""),
                "requests_per_sec": row.get("Requests/s", ""),
                "cost_per_1000_requests_usd": round(cost_per_1000, 4),
            }
        )

    if not summary_rows:
        print(f"No data rows found in {stats_csv_path}", file=sys.stderr)
        sys.exit(1)

    with open(out_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary_rows[0].keys()))
        writer.writeheader()
        writer.writerows(summary_rows)

    print(f"Wrote summary for {len(summary_rows)} endpoints to {out_path}")
    for row in summary_rows:
        print(
            f"  {row['endpoint']}: p50={row['p50_ms']}ms p95={row['p95_ms']}ms "
            f"p99={row['p99_ms']}ms errors={row['error_rate_pct']}%"
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stats_csv", help="Path to Locust's *_stats.csv output file")
    parser.add_argument("--out", default="benchmark_summary.csv", help="Output summary CSV path")
    args = parser.parse_args()
    analyze(args.stats_csv, args.out)
