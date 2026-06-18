# AfyaConnect Constitution

**Version:** 1.0 (Phase 0)  
**Base platform:** GNU Health HIS 5.0.x (Tryton 7.0)  
**Methodology:** Spec-Driven Development (SDD)

## Licensing

| Component | License |
|-----------|---------|
| `z_health_afya_*` Tryton modules | GPL-3.0-or-later |
| Cloud Run services (`services/`) | Apache 2.0 |
| Bootstrap scripts (`setup/`) | Apache 2.0 |
| Looker dashboards | Apache 2.0 |

Legal review of dual licensing is scheduled for Phase 1.

## Execution Gates

No phase proceeds without explicit team-lead sign-off.

| Gate | Condition | Blocks |
|------|-----------|--------|
| **G0** | `gnuhealth-model-inventory.md` approved. Module specs reconciled against actual GH 5.0.x model names, fields, workflow states, and view IDs. | All module implementation (Phases 2–5). No business logic before G0. |
| **G1** | Core demo path end-to-end: USSD or SMS → AI triage → GH triage record → human review → dispatch candidate → human approval → analytics outbox → BigQuery → Looker tile. Core acceptance tests pass. | Voice integration and diaspora work (Phase 5). |
| **G2** | All acceptance tests pass (40 scenarios, all dispatch windows, privacy, safety, dashboard, language, FHIR). Bootstrap scripts validated on clean GCP project. | Demo prep (Phase 6). |

## Architecture Principles

1. **GNU Health is system of record** — all clinical workflow state lives in Tryton.
2. **AI services are stateless** — GH is never in the user-facing latency path.
3. **Internal writes via Tryton RPC; external reads via FHIR** — MVP is FHIR-readable, not FHIR-writable.
4. **Human-in-the-loop** — dispatch and triage escalation require wizard-enforced human approval.
5. **Analytics via outbox pattern** — no GCP SDK inside GNU Health; exporter polls outbox table.
6. **No raw model reasoning stored** — clinical rationale is validated structured JSON only.

## PRD Deviations (MVP)

| PRD Feature | MVP Treatment | Post-MVP Path |
|-------------|---------------|---------------|
| Multi-turn voice | Single-turn STT → triage → TTS | Conversational flow via Gemini function-calling |
| FHIR for all writes | Read-only FHIR; internal writes via Tryton RPC | FHIR write for Encounter, ServiceRequest, Appointment |
| Resource allocation dashboard | Deferred | Integrate post-pilot |
| Policy insights dashboard | Deferred | Enable after 6+ months of data |
| WebRTC video consults | Audio-only (demotable) | Add with recording post-MVP |
| Consultation recording | Deferred | Implement with consent flow + encrypted Cloud Storage |
| Real NAERS integration | Stub API | Replace stub with live endpoint |
| Full Fulfulde Tryton UI | Fulfulde in voice/SMS/USSD only | Add .po files if demanded |
| Web portal for health workers | Deferred | Build FastAPI web portal post-MVP |
| CMEK encryption | Cloud SQL default | Upgrade for production |
| 9 security roles | 5 prototype roles | Expand for production |

## Demo Truthfulness

Components marked **Live** in demos must use real integrations (sandbox where applicable).
Components marked **Stubbed** or **Simulated** must be disclosed to the audience.

| Component | Status |
|-----------|--------|
| USSD / SMS / voice triage | Live (Africa's Talking sandbox) |
| AI triage (Gemini + WHO RAG) | Live |
| GH triage / dispatch wizards | Live |
| FHIR patient history | Live (read-only adapter) |
| NAERS submission | Stubbed |
| Analytics → BigQuery → Looker | Live |
| Patient records / Gombe facilities | Synthetic |
| Diaspora matching | Live or simulated (demotable) |

## Safety & Privacy

- **symptoms_raw:** 30-day TTL, phone-number regex redaction, never exported to analytics.
- **Analytics identity:** Event-level random UUIDs only. No patient or session hashes.
- **k-anonymity:** k≥10 on rolling 24-hour window; cascade coarsening (sector → LGA → state).
- **Consent:** Six statuses, categorical notes only (no free text).
- **Clinical validation:** 40-scenario prototype-grade validation; not clinical deployment validation.

## Module Dependency Order

```
z_health_afya_core
├── z_health_afya_access
├── z_health_afya_triage → z_health_afya_dispatch
├── z_health_afya_diaspora
└── z_health_afya_analytics
```
