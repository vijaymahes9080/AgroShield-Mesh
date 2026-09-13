# AgroShield Mesh - n8n Automation Engine

This directory contains the production-ready n8n automation workflow for AgroShield Mesh.

## Overview

The workflow coordinates autonomous agricultural event ingestion, risk scoring, advisory generation, and conditional notification dispatch:

```
[IoT Sensor / Webhook]
       │
       ▼
[Validate & Idempotency Check]
       │
       ▼
[Ingest to Backend API (/api/v1/sensor-readings)]
       │
       ▼
[Trigger Bounded Advisory Agent (/api/v1/advisories)]
       │
       ▼
[Check Human Review Gate (requires_human_review == true?)]
      ├── YES ──► [Queue for Expert Agronomist Review (Dashboard)]
      └── NO  ──► [Dispatch Mock Farmer Notification (SMS / WhatsApp)]
```

## Features

1. **Idempotency**: Prevents duplicate telemetry processing using compound keys (`field_id + timestamp`).
2. **Deterministic Risk Engine**: Bounded agronomic calculations with zero black-box hallucinations.
3. **Safety Review Gate**: Any advisory flagged with `HIGH` or `CRITICAL` risk is automatically held for accredited agronomist review before reaching the farmer.
4. **Mock Dispatch Mode**: Safe simulation of farmer SMS and WhatsApp notifications with PII masking.
5. **Retries & Timeouts**: Configured with 3 retries, exponential backoff, and 5-second request timeouts.

## Importing to n8n Community Edition

1. Open n8n UI (`http://localhost:5678`).
2. Click **Add Workflow** -> **Import from File**.
3. Select `n8n/agroshield_advisory_workflow.json`.
4. Configure backend endpoint URL (default: `http://backend:8000`).
5. Activate the workflow.

## Standalone Simulation

Run the Python simulator without needing a running n8n container:

```bash
python scripts/simulate_n8n_flow.py
```
