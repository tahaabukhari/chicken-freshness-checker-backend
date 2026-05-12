# Chicken Freshness Checker — Backend

This repository contains a FastAPI backend for an IoT-based chicken spoilage detector. The project is Cloud Run–ready; this README explains how to create a GitHub repo, add the necessary secrets, and deploy to Google Cloud Run via GitHub Actions.

## What I added

- GitHub Actions workflow: `.github/workflows/deploy-cloud-run.yml` — builds the container, pushes to GCR, and deploys to Cloud Run on `main` branch pushes.
- `.dockerignore` and `.gcloudignore` — reduce build/upload context.

## Prerequisites

- A Google Cloud project with billing enabled.
- `gcloud` CLI installed locally (optional for manual deploys).
- `git` and optional `gh` (GitHub CLI) for repo creation.

## GCP setup (one-time)

1. Enable required APIs:

```bash
gcloud services enable run.googleapis.com containerregistry.googleapis.com iam.googleapis.com
```

2. Create a service account for GitHub Actions and download its JSON key:

```bash
gcloud iam service-accounts create gha-deployer --display-name="GitHub Actions Deployer"
gcloud projects add-iam-policy-binding $GCP_PROJECT --member="serviceAccount:gha-deployer@${GCP_PROJECT}.iam.gserviceaccount.com" --role="roles/run.admin"
gcloud projects add-iam-policy-binding $GCP_PROJECT --member="serviceAccount:gha-deployer@${GCP_PROJECT}.iam.gserviceaccount.com" --role="roles/storage.admin"
gcloud iam service-accounts keys create key.json --iam-account=gha-deployer@${GCP_PROJECT}.iam.gserviceaccount.com
```

Adjust roles as needed (for Artifact Registry, add artifactregistry.writer). Keep `key.json` secure.

## Create GitHub repository and push

Using the GitHub CLI (`gh`):

```bash
cd path/to/chicken-freshness-checker-backend
git init
git add .
git commit -m "Initial commit"
gh repo create <your-username>/chicken-freshness-checker-backend --public --source=. --remote=origin --push
```

Or using plain `git` and GitHub web UI: create a new repo on GitHub, then:

```bash
git remote add origin https://github.com/<your-username>/chicken-freshness-checker-backend.git
git branch -M main
git push -u origin main
```

## Add GitHub Secrets

- `GCP_SA_KEY` : the contents of `key.json` (the service account key) — add as a repository secret.
- `GCP_PROJECT` : your Google Cloud project ID.
- `GCP_REGION` : Cloud Run region (e.g., `us-central1`).

To set `GCP_SA_KEY` via `gh` CLI:

```bash
gh secret set GCP_SA_KEY --body "$(jq -c . key.json)"
gh secret set GCP_PROJECT --body "$GCP_PROJECT"
gh secret set GCP_REGION --body "us-central1"
```

## First deployment (manual, optional)

You can deploy directly from your machine using `gcloud` to verify everything works:

```bash
gcloud run deploy chicken-freshness-checker \
  --source . \
  --region us-central1 \
  --project $GCP_PROJECT \
  --allow-unauthenticated
```

Or build and push an image then deploy:

```bash
IMAGE=gcr.io/${GCP_PROJECT}/chicken-freshness-checker:latest
docker build -t $IMAGE .
docker push $IMAGE
gcloud run deploy chicken-freshness-checker --image $IMAGE --region us-central1 --project $GCP_PROJECT --allow-unauthenticated
```

## Notes and production recommendations

- The app currently uses SQLite (`database.db`) by default. For production, use Cloud SQL (Postgres) and configure `DATABASE_URL` via Secrets or Cloud Run environment variables. See Cloud SQL connector docs for Cloud Run.
- Tighten CORS origins before public deployment.
- Pin package versions in `requirements.txt` for reproducible builds.

If you want, I can: create the remote GitHub repo for you (requires a GitHub token), or, with your permission, run the `gh` and `gcloud` commands from your environment to finish the deployment.

Docs
- Project documentation: [docs/PROJECT_DOCUMENTATION.md](docs/PROJECT_DOCUMENTATION.md)
- Feature test report: [docs/FEATURE_TEST_REPORT.md](docs/FEATURE_TEST_REPORT.md)
