# Chicken Freshness Checker — Project Documentation

Overview
- Purpose: Backend API for an IoT-based chicken spoilage detection device. Accepts sensor data, runs a spoilage calculation, stores readings, and returns live results.
- Tech: FastAPI, Uvicorn, SQLModel (SQLite by default), scikit-learn/pandas for model logic; containerized with Docker and deployable to Google Cloud Run.

Architecture
- Entrypoint: `app.main:app` — creates DB tables on startup and registers API routes.
- Routes: See `app/api/routes.py` — main endpoints:
  - `GET /` health-check
  - `POST /api/ingest` accept IoT packet (JSON) and return `LiveDataOut` with spoilage calculation.
- Services: `app/services/analyzer.py` contains `calculate_spoilage()` used by the ingest flow.
- Persistence: `app/database.py` provides the SQLModel engine and `get_session()` dependency. Default is SQLite `database.db`. For production use `DATABASE_URL` (Cloud SQL recommended).

Schemas and expected payloads
- Input schema: `IoTPacketIn` in `app/schemas.py`.
- Example JSON (aliases supported):

```json
{
  "device_id": "DEVICE-001",
  "gas-sensor": 12.5,
  "temp": 6.2,
  "humidity": 55.1,
  "time+date": "2026-05-13T00:00:00Z"
}
```

- Response: On success `POST /api/ingest` returns HTTP 201 with processed reading JSON containing `spoilage_percent` and `category`.

Running locally
- Install dependencies: `pip install -r requirements.txt`.
- Run locally: `uvicorn app.main:app --reload --port 8000`.
- Test ingest quickly with the provided script: `python scripts/test_post.py`.

Deployment
- Dockerfile and `.dockerignore` are provided. Cloud Run listens on port 8080 by default.
- CI/CD: GitHub Actions workflow (if configured) builds and deploys to Cloud Run using a GCP service account with appropriate permissions. Alternatively use `gcloud builds submit` + `gcloud run deploy`.

Configuration & env
- `DATABASE_URL` optional: set to a production DB (e.g., Cloud SQL) to avoid local SQLite.
- Add any model artifacts or secrets via environment variables or mounted volumes as needed.

Maintenance notes
- Tighten CORS origins in `app/main.py` before production.
- Replace `calculate_spoilage()` in `app/services/analyzer.py` with a real model and add versioning.

Production checklist
- Create a managed database (Cloud SQL Postgres recommended) and note the connection string.
- Set repository secrets:
  - `GCP_SA_KEY` — service account key JSON for GitHub Actions
  - `GCP_PROJECT` — GCP project ID
  - `GCP_REGION` — Cloud Run region (e.g., `us-central1`)
  - `DATABASE_URL` — Postgres connection string (e.g., `postgresql://user:pass@host:5432/db`)
  - `CORS_ORIGINS` — comma-separated list of allowed origins (e.g., `https://app.example.com`)

Deploying to production
- The repo includes a GitHub Actions workflow `.github/workflows/deploy-cloud-run.yml` that builds, pushes, and deploys the container. It reads `DATABASE_URL` and `CORS_ORIGINS` from repository secrets and sets Cloud Run resource settings (memory, concurrency, min instances).

Cloud SQL notes
- For Cloud Run + Cloud SQL, either use the Cloud SQL Auth proxy or the Cloud SQL Python connector. Update `DATABASE_URL` accordingly and grant the service account the `Cloud SQL Client` role.

Logging & monitoring
- Cloud Run automatically writes logs to Cloud Logging. For production, add structured logs (JSON) or integrate with an APM. Consider adding alerting policies for error rates and CPU/memory usage.
