# AfyaConnect GCP Bootstrap Scripts

Planned bootstrap scripts for a clean GCP project (DevPlan v5, Section 11.2).

| Script | Purpose | Status |
|--------|---------|--------|
| `01-gcp-project.sh` | Enable APIs, set project defaults | Not implemented |
| `02-service-accounts.sh` | Create SAs for Cloud Run, Scheduler, BigQuery | Not implemented |
| `03-secrets.sh` | Secret Manager: Tryton RPC creds, Africa's Talking, Vertex AI | Not implemented |
| `04-cloud-sql.sh` | Cloud SQL PostgreSQL for GNU Health | Not implemented |
| `05-gnu-health.sh` | Deploy GNU Health on Cloud SQL | Not implemented |
| `06-bigquery.sh` | Analytics dataset and tables | Not implemented |
| `07-pubsub.sh` | Pub/Sub topic for analytics events | Not implemented |
| `08-cloud-scheduler.sh` | Scheduler for Analytics Exporter (every 2 min) | Not implemented |
| `09-deploy-services.sh` | Deploy all Cloud Run services | Not implemented |
| `10-seed-data.sh` | Load Gombe seed data into production GH | Not implemented |

**Acceptance (T060):** Run on clean GCP project with billing only. After completion: GH
accessible, modules activated, seed data loaded, Cloud Run services reachable, Looker dashboard
populated with at least one test event.

**When to run:** After G1 local demo path works. See `docs/afyaconnect/GCP_AND_AT_SETUP.md`.
