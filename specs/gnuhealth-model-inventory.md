# GNU Health Model Inventory — AfyaConnect G0 Gate

**Status:** PENDING (awaiting team-lead sign-off)  
**Platform:** GNU Health 5.0.x / Tryton 7.0  
**Source:** `gnuhealth-all-modules` pip package (inspected offline)  
**Date:** June 2026  
**Task:** T002 (DevPlan v5)

## Purpose

Reconcile AfyaConnect module specifications against actual GNU Health 5.0.x model
names, field names, workflow states, and view IDs. **No Phase 1+ business logic
may be implemented until this document is approved (Gate G0).**

## Inspection method

Models inspected from installed package at:
`trytond/modules/{health,health_ems,health_icd10}/`

Live Docker verification pending (Docker daemon was unavailable during Phase 0 commit).
Re-run verification after `./scripts/start.sh`:

```bash
docker compose exec app python3 -c "
from trytond.pool import Pool
from trytond import backend
from trytond.config import config
config.update_etc('/opt/gnuhealth/etc/trytond.conf')
backend.Database().connect('health')
pool = Pool('health'); pool.init()
for m in ['gnuhealth.patient','gnuhealth.support_request','gnuhealth.institution']:
    print(m, pool.get(m).__name__)
"
```

---

## Core models

### `party.party` (health module PoolMeta)

| Field | Type | Notes |
|-------|------|-------|
| `name` | Char | Display name |
| `is_person` | Boolean | Required for patients/workers |
| `is_patient` | Boolean | Auto-creates `gnuhealth.patient` on save |
| `is_healthprof` | Boolean | Health professional flag |
| `is_institution` | Boolean | Required for facilities |
| `dob` | Date | Date of birth (on party, not patient) |
| `gender` | Selection | m, f, nb, other, nd, u, f-m, m-f |
| `ref` | Char | Person Unique Identifier (PUID) |

**AfyaConnect mapping:** AccessSession consent actor, seed script party creation.

### `gnuhealth.patient` (`PatientData`)

| Field | Type | Notes |
|-------|------|-------|
| `party` | M2O party.party | Required; domain requires is_patient=True |
| `gender` | Function | Derived from party |
| `dob` | Function | Derived from party.dob |
| `puid` | Function | From party.ref |

**Plan discrepancy:** DevPlan seed references `Patient.name`, `Patient.dob`, `Patient.gender` — these do not exist on the model. **Resolution:** Set demographics on `party.party`; patient is created via `is_patient=True` or explicit `Patient(party=...)`.

### `gnuhealth.institution` (`HealthInstitution`)

| Field | Type | Notes |
|-------|------|-------|
| `party` | M2O party.party | Required; domain is_institution=True |
| `code` | Char | Required, unique (use GOM-* codes) |
| `institution_type` | Selection | doctor_office, primary_care, clinic, hospital, specialized, nursing_home, hospice, rural |
| `public_level` | Selection | private, public, mixed — **required** |
| `operational_sectors` | O2M | Links to operational sectors |

**Plan discrepancy:** No `name` field — name comes from `party.name`. No lat/lon on institution — use `party.address` or operational sector. **Resolution:** Store coordinates in `extra_info` JSON or operational sector until AfyaConnect adds routing fields via PoolMeta.

### `gnuhealth.operational_sector`

| Field | Type | Notes |
|-------|------|-------|
| `name` | Char | Sector name |
| `operational_area` | M2O | Parent operational area (LGA-level) |

**AfyaConnect mapping:** Region coarsening (sector → LGA → state) per SPEC-PRIVACY-001.

### `gnuhealth.appointment`

| Field | Type | States |
|-------|------|--------|
| `name` | Char | APPT ID (readonly) |
| `patient` | M2O gnuhealth.patient | |
| `institution` | M2O gnuhealth.institution | |
| `state` | Selection | free, confirmed, checked_in, done, user_cancelled, center_cancelled, no_show |
| `urgency` | Selection | a (Normal), b (Urgent), c (Medical Emergency) |

### `gnuhealth.patient.evaluation` (`PatientEvaluation`)

| Field | Type | States |
|-------|------|--------|
| `code` | Char | Evaluation code |
| `patient` | M2O | Required |
| `evaluation_start` | DateTime | Required |
| `evaluation_endtime` | DateTime | |
| `state` | Selection | in_progress, done, signed (readonly) |
| `urgency` | Selection | a, b, c |
| `chief_complaint` | Char | Used by SupportRequest.complaint function |
| `healthprof` | M2O gnuhealth.healthprofessional | Initiator |
| `signed_by` | M2O gnuhealth.healthprofessional | |

**AfyaConnect mapping:** CreateEvaluationFromTriage wizard (T022) creates this model with ICD-10 conditions.

### `gnuhealth.support_request` (`SupportRequest`, health_ems)

| Field | Type | Notes |
|-------|------|-------|
| `code` | Char | Auto-generated, readonly |
| `patient` | M2O gnuhealth.patient | |
| `evaluation` | M2O gnuhealth.patient.evaluation | |
| `request_date` | DateTime | Required |
| `operational_sector` | M2O gnuhealth.operational_sector | |
| `latitude` / `longitude` | Numeric | Location |
| `healthcenter` | M2O gnuhealth.institution | Calling institution |
| `urgency` | Selection | low, urgent, emergency |
| `event_type` | Selection | event1–event30 (EMS incident types) |
| `state` | Selection | open, closed (readonly) |
| `ambulances` | O2M gnuhealth.ambulance.support | |

**Plan discrepancy:** DevPlan dispatch uses 10-state `dispatch_state` machine — **does not exist** on base model. **Resolution:** Add via PoolMeta in `z_health_afya_dispatch` (T033): dispatch_state, timing windows, approval fields, afya_triage_session M2O.

**Urgency mapping:**

| AfyaConnect triage_level | GH support_request.urgency |
|--------------------------|----------------------------|
| green | low |
| yellow | urgent |
| red / emergency | emergency |

### `gnuhealth.pathology` (ICD-10 via health_icd10 data)

`health_icd10` module loads ICD-10 pathology records into `gnuhealth.pathology`.
No separate ICD model — use pathology codes for evaluation conditions.

---

## AfyaConnect scaffold models (Phase 0)

| Model | Module | Status |
|-------|--------|--------|
| `gnuhealth.afya.config` | z_health_afya_core | Scaffold |
| `gnuhealth.afya.access_session` | z_health_afya_access | Scaffold |
| `gnuhealth.afya.triage_session` | z_health_afya_triage | Scaffold |
| `gnuhealth.afya.emergency_keyword` | z_health_afya_triage | Scaffold (term, language, active) |
| `gnuhealth.afya.dispatch_stub` | z_health_afya_dispatch | Scaffold (replaced by PoolMeta in Phase 4A) |
| `gnuhealth.afya.diaspora_specialist` | z_health_afya_diaspora | Scaffold |
| `gnuhealth.afya.analytics_outbox` | z_health_afya_analytics | Scaffold |

---

## Module activation status

| Module | Purpose | Activation |
|--------|---------|------------|
| health | Core HIS | init_and_run.sh |
| health_lab | Laboratory | init_and_run.sh |
| health_ems | Support requests / EMS | init_and_run.sh (new) |
| health_icd10 | ICD-10 pathology data | init_and_run.sh (new) |
| health_federation | Federation ID on party | init_and_run.sh (new) |
| health_crypto | Field encryption | init_and_run.sh (new) |
| health_reporting | Reporting / epidemics | init_and_run.sh (new) |
| z_health_afya_* (6) | AfyaConnect | init_and_run.sh (new) |

---

## Operational queues (Section 9 — planned menu parents)

| Queue | Model filter | Planned menu parent |
|-------|--------------|---------------------|
| Triage Review | TriageSession state=completed, human_review_required=True | z_health_afya_core.menu_afya_root |
| Dispatch Candidate | SupportRequest dispatch_state=candidate | z_health_afya_core.menu_afya_root |
| Post-Hoc Consent | PostHocConsentTask resolved=False | z_health_afya_core.menu_afya_root |
| Failed Export | AnalyticsOutbox export_error IS NOT NULL | z_health_afya_core.menu_afya_root |

Menu root XML ID: `z_health_afya_core.menu_afya_root` (created in Phase 0 scaffold).

---

## Discrepancy table

| Plan reference | Expected | Actual GH 5.0.x | Resolution |
|----------------|----------|-----------------|------------|
| `gnuhealth.evaluation` | Evaluation model | `gnuhealth.patient.evaluation` | Use correct model name |
| `Patient.name/dob/gender` | Direct fields | On `party.party` | Seed via party |
| `Institution.name` | Direct field | Via `party.name` | Create party with is_institution |
| `Institution.latitude/longitude` | Routing coords | Not on institution | Use party address or PoolMeta |
| `support_request.dispatch_state` | 10-state machine | Only open/closed | PoolMeta in z_health_afya_dispatch |
| `support_request.afya_triage_session` | M2O link | Does not exist | Add via PoolMeta |
| `triage_level` values | green/yellow/red/emergency | N/A (new model) | Implement on TriageSession |
| `icd10_codes` on triage | Field | Use gnuhealth.pathology M2M | Link via evaluation conditions |
| FHIR Encounter | FHIR resource | No native FHIR write | Read-only adapter via Tryton RPC |

---

## G0 sign-off

| Reviewer | Role | Date | Approved |
|----------|------|------|----------|
| | Team lead | | [ ] |
| | Clinical advisor | | [ ] |

**Next step after approval:** T017 Security PoC on `z_health_afya_triage`.
