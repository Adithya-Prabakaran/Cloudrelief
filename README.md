# CloudRelief

A smart disaster response and relief management system. Citizens report incidents
(location, description, photo); the backend estimates severity from the photo
classification + description text + nearby report density, and alerts admins
when severity crosses a threshold. Admins track incidents on a live map and
table, assign rescue teams, and update status.

Everything that would normally be a managed cloud service (S3, Cognito, SNS,
Rekognition, DynamoDB) is implemented **locally behind an interface**, so the
app is fully testable today and swapping in the real AWS/Oracle service later
is a matter of adding one new file + flipping one env var — see
[Cloud Migration Guide](#cloud-migration-guide) below.

## What's mocked

| Concern | Local stand-in | Real service (later) |
|---|---|---|
| Object storage | Local filesystem (`backend/storage/uploads`, served via `/files/:key`) | S3 |
| Auth | JWT + bcrypt | Cognito |
| Notifications | Console log + `alerts` table | SNS |
| Image classification | Random label/confidence from `[flood, fire, structural_damage, normal]` | Rekognition |
| Database | Postgres (simple/key-based schema, no joins beyond FKs) | DynamoDB |
| Compute | Docker Compose on your machine | AWS Lambda / Oracle Cloud VM |

## Project structure

```
cloudrelief/
  frontend/           React + Vite + Tailwind, citizen + admin routes, Leaflet map
  backend/
    app/
      core/            config, security (JWT/bcrypt), severity algorithm, constants
      routers/         auth, incidents, files
      services/        swappable interface + implementation per cloud concern
      models/          SQLAlchemy models + Pydantic schemas
      db/              session, seed script
  benchmark/
    locustfile.py      ramps 10 -> 50 -> 200 -> 500 concurrent users
    analyze_results.py turns Locust's CSV into p50/p95/p99 + cost-per-1000
  docker-compose.yml   postgres + backend + frontend
  .env.example         all provider switches + secrets, commented
```

## Running locally

Requires Docker + Docker Compose.

```bash
cp .env.example .env
docker-compose up --build
```

- Frontend: http://localhost:5174
- Backend API docs: http://localhost:8000/docs
- Postgres: localhost:5432 (user/pass/db: `cloudrelief`)

Seed a demo admin, a demo citizen, and a few fake incidents:

```bash
docker-compose exec backend python -m app.db.seed
```

Demo logins:
- Admin: `admin@cloudrelief.local` / `admin12345`
- Citizen: `citizen@cloudrelief.local` / `citizen12345`

### Running without Docker

Backend:
```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# requires a local Postgres reachable at DATABASE_URL (see backend/app/core/config.py)
uvicorn app.main:app --reload
python -m app.db.seed
```

Frontend:
```bash
cd frontend
npm install
npm run dev
```

## End-to-end flow

1. Citizen registers/logs in, submits a report with description + location
   (browser geolocation or manual lat/lng) + photo.
2. Backend uploads the photo via `StorageService`, runs `ClassifierService`
   against it, computes severity via the weighted formula in
   `backend/app/core/severity.py`, and saves the incident.
3. If `severity_score >= ALERT_THRESHOLD`, `NotifyService` logs the alert and
   writes an `alerts` row.
4. Admin logs in, sees the incident on the Leaflet map (colored by severity)
   and in the sortable table, assigns a team, and updates status.

### Severity formula

```
classifier_score = confidence, if predicted label in [flood, fire, structural_damage], else 0
keyword_score     = count(urgent keywords in description) * URGENCY_WEIGHT
density_score     = min(nearby_report_count / DENSITY_CAP, 1.0) * DENSITY_WEIGHT
severity          = classifier_score * 0.5 + keyword_score * 0.25 + density_score * 0.25
```

All weights/constants are configurable via env vars (`URGENCY_WEIGHT`,
`DENSITY_CAP`, `DENSITY_WEIGHT`, `ALERT_THRESHOLD`, `DENSITY_RADIUS_KM`,
`DENSITY_WINDOW_HOURS` — see `.env.example`).

## Service abstraction layer

Route handlers only ever import an interface (`StorageService`,
`AuthService`, `NotifyService`, `ClassifierService`) — never a concrete
implementation. `backend/app/services/factory.py` is the single place that
picks an implementation based on env vars:

```
STORAGE_PROVIDER=local|s3
AUTH_PROVIDER=local|cognito
NOTIFY_PROVIDER=console|sns
CLASSIFIER_PROVIDER=mock|rekognition
```

## Benchmarking

```bash
cd benchmark
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Runs the full 10 -> 50 -> 200 -> 500 user ramp against the local stack
locust -f locustfile.py --host http://localhost:8000 --headless --csv=results/run1 --run-time 10m

python analyze_results.py results/run1_stats.csv --out results/summary.csv
```

Point the same script at AWS later with `--host https://<your-api>`.
`analyze_results.py`'s `COST_PER_REQUEST` is a placeholder (0 for the local
stack) — replace it with real Lambda + API Gateway pricing when comparing
against the cloud deployment.

> Note: Locust depends on `gevent`, which builds from source on some Macs and
> requires Xcode Command Line Tools (`xcode-select --install`). If the wheel
> build fails, install Locust in a Linux container/CI runner instead.

## Cloud Migration Guide

Flip one provider switch in `.env` at a time; each corresponds to adding
exactly one new file. Nothing outside `services/factory.py` and the new file
itself needs to change.

| Switch | New file to add | Notes |
|---|---|---|
| `STORAGE_PROVIDER=s3` | `backend/app/services/storage/s3.py` — `S3StorageService(StorageService)` using boto3 (`upload_fileobj`, `generate_presigned_url`) | Update `/files/:key` route to become unused (S3 URLs are presigned directly) |
| `AUTH_PROVIDER=cognito` | `backend/app/services/auth/cognito.py` — `CognitoAuthService(AuthService)` using boto3's `cognito-idp` client (`SignUp`, `InitiateAuth`, `GetUser`) | `verify_token` should validate the Cognito JWT against the user pool's JWKS instead of the local HS256 secret |
| `NOTIFY_PROVIDER=sns` | `backend/app/services/notify/sns.py` — `SnsNotifyService(NotifyService)` using boto3's `sns.publish()` against `SNS_TOPIC_ARN` | Keep writing the `alerts` row too, for the admin audit trail |
| `CLASSIFIER_PROVIDER=rekognition` | `backend/app/services/classifier/rekognition.py` — `RekognitionClassifierService(ClassifierService)` using boto3's `rekognition.detect_labels()` against the uploaded S3 object | Map Rekognition's returned labels onto `CLASSIFIER_LABELS` in `app/core/constants.py` |
| Database -> DynamoDB | Replace `backend/app/db/session.py` + `backend/app/models/db.py` with a DynamoDB client/table definitions | Schema was kept deliberately simple/key-based (`incidents` by `incident_id`, `users` by `user_id`, `alerts` by `alert_id`) for exactly this migration |
| Compute -> Oracle Cloud VM | No code change | Deploy the same `docker-compose.yml` (or split services) onto the VM; point `VITE_API_URL` in the frontend's `.env` at the VM's public address |

After each swap, re-run `benchmark/locustfile.py` with `--host` pointed at
the new deployment and diff the `analyze_results.py` output against the
local baseline.
