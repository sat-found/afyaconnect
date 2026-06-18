# AfyaConnect Cloud Run Services

Apache 2.0 licensed services planned for GCP Cloud Run deployment.

| Service | Purpose | Phase |
|---------|---------|-------|
| `access-gateway` | Voice (single-turn), SMS, USSD webhooks; writes AccessSession via Tryton RPC | Phase 2 (T023) |
| `ai-triage-agent` | Vertex AI Gemini + WHO RAG; clinical rationale JSON; phone redaction | Phase 3 (T027) |
| `fhir-adapter` | Read-only FHIR R4 (Patient, Encounter, Condition, ServiceRequest, Location, Practitioner) | Phase 1 (T012) |
| `analytics-exporter` | Polls AnalyticsOutbox, validates schema, publishes to Pub/Sub | Phase 4B (T043) |
| `diaspora-matching` | Specialist matching via Vertex AI (demotable to seed script) | Phase 5 (T052) |

Each service will live in its own subdirectory with FastAPI, Dockerfile, and OpenAPI contract
under `specs/interface-contracts/`.

**Status:** Not implemented. Local Docker + Tryton modules are built first (Phase 0).
