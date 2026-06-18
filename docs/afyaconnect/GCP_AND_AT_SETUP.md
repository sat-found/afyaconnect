# GCP and Africa's Talking Setup Guide

Deferred setup for AfyaConnect cloud services. Run after the local Docker demo path (G1) is working.

## Prerequisites

- Google Cloud account with billing enabled
- `gcloud` CLI installed and authenticated
- Africa's Talking developer account (sandbox)

## 1. GCP Project Checklist

Create a new project or use an existing one:

```bash
export PROJECT_ID=afyaconnect-prototype
gcloud projects create "${PROJECT_ID}" --name="AfyaConnect Prototype"
gcloud config set project "${PROJECT_ID}"
gcloud billing projects link "${PROJECT_ID}" --billing-account=BILLING_ACCOUNT_ID
```

Enable required APIs:

```bash
gcloud services enable \
  run.googleapis.com \
  sqladmin.googleapis.com \
  secretmanager.googleapis.com \
  pubsub.googleapis.com \
  bigquery.googleapis.com \
  cloudscheduler.googleapis.com \
  aiplatform.googleapis.com \
  artifactregistry.googleapis.com
```

## 2. Service Account Matrix

| Service account | Purpose | Roles |
|-----------------|---------|-------|
| `sa-gnuhealth` | GNU Health on Cloud SQL | Cloud SQL Client |
| `sa-access-gateway` | Access Gateway Cloud Run | Secret Manager Secret Accessor |
| `sa-triage-agent` | AI Triage Agent | Vertex AI User, Secret Manager Secret Accessor |
| `sa-fhir-adapter` | FHIR read-only adapter | Secret Manager Secret Accessor |
| `sa-analytics-exporter` | Outbox poller | BigQuery Data Editor, Pub/Sub Publisher |
| `sa-scheduler` | Cloud Scheduler invoker | Cloud Run Invoker |

Create service accounts via `setup/02-service-accounts.sh` (not yet implemented).

## 3. Secrets (Secret Manager)

| Secret | Contents |
|--------|----------|
| `tryton-rpc-url` | GNU Health Tryton RPC endpoint (internal) |
| `tryton-rpc-user` | RPC service user |
| `tryton-rpc-password` | RPC service password |
| `africas-talking-api-key` | Africa's Talking sandbox/production API key |
| `africas-talking-username` | Africa's Talking username |
| `google-maps-api-key` | Maps routing for facility recommendations |
| `vertex-ai-project` | GCP project ID for Vertex AI |

```bash
echo -n "YOUR_AT_API_KEY" | gcloud secrets create africas-talking-api-key --data-file=-
```

## 4. Africa's Talking Sandbox

1. Register at [https://africastalking.com](https://africastalking.com)
2. Create an application in the sandbox environment
3. Note the **API Key** and **Username**
4. Store credentials in Secret Manager (see above)
5. Configure sandbox callback URLs once Access Gateway is deployed:
   - SMS: `https://access-gateway-XXXX.run.app/webhooks/sms`
   - USSD: `https://access-gateway-XXXX.run.app/webhooks/ussd`
   - Voice: `https://access-gateway-XXXX.run.app/webhooks/voice`

Test SMS from sandbox:

```bash
curl -X POST "https://api.sandbox.africastalking.com/version1/messaging" \
  -H "apiKey: YOUR_SANDBOX_API_KEY" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=YOUR_USERNAME&to=+254711082XXX&message=AfyaConnect test"
```

## 5. Vertex AI (Gemini Pro + Vector Search)

Enable Vertex AI and create a Vector Search index for WHO RAG (Phase 1, T016):

```bash
gcloud ai indexes create \
  --display-name="who-protocols-rag" \
  --metadata-file=who-index-metadata.json \
  --region=us-central1
```

Deploy Gemini Pro endpoint for triage agent inference. The AI Triage Agent service
(Phase 3) calls this endpoint with retrieved protocol chunks.

## 6. Bootstrap Script Order

Run scripts in `setup/` sequentially on a clean GCP project:

| Order | Script | Outcome |
|-------|--------|---------|
| 1 | `01-gcp-project.sh` | APIs enabled |
| 2 | `02-service-accounts.sh` | SAs created |
| 3 | `03-secrets.sh` | Secrets populated |
| 4 | `04-cloud-sql.sh` | PostgreSQL instance |
| 5 | `05-gnu-health.sh` | GNU Health deployed |
| 6 | `06-bigquery.sh` | Analytics dataset |
| 7 | `07-pubsub.sh` | Event topic |
| 8 | `08-cloud-scheduler.sh` | Exporter schedule (every 2 min) |
| 9 | `09-deploy-services.sh` | All Cloud Run services |
| 10 | `10-seed-data.sh` | Gombe seed data |

**Acceptance (T060):** After completion, GNU Health is accessible, modules activated,
seed data loaded, Cloud Run services reachable, Looker dashboard shows at least one test event.

## 7. When to Run

| Milestone | Action |
|-----------|--------|
| Phase 0 (now) | Local Docker only. This guide is reference. |
| After G1 | Create GCP project, run `01`–`05`, deploy Access Gateway and Triage Agent |
| After G2 | Full bootstrap including analytics pipeline and Looker |

## 8. Cost Controls

- Use Cloud SQL db-f1-micro for prototype
- Set Cloud Run min instances to 0
- Use BigQuery sandbox free tier where possible
- Delete resources after demo if not needed
