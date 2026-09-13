# AgroShield Mesh — Architectural Design & Ingestion Gateway

## Executive Summary

**AgroShield Mesh** is an evidence-grounded agricultural intelligence platform developed to address agricultural volatility, water scarcity, and heat stress across Tamil Nadu and arid agro-ecological zones.

## System Topology & Data Pipeline

```
Farmer / Sensor / Satellite / Weather
              │
              ▼
        Ingestion Gateway
              │
              ▼
       Validation + PII Masking
              │
       ┌──────┴──────┐
       │             │
       ▼             ▼
   PostGIS       Time-Series Store
       │             │
       └──────┬──────┘
              ▼
       Field Intelligence Layer
       - NDVI / stress
       - water need
       - risk rules
              │
              ▼
       Agricultural RAG Layer (TNAU / ICAR / IMD)
              │
              ▼
       Bounded Agent Workflow
       (COLLECT → VALIDATE → ANALYZE → RETRIEVE → COMPOSE → VERIFY → DELIVER)
              │
       Expert / Human Review Gate
              │
       ┌──────┴──────┐
       │             │
       ▼             ▼
      n8n       Farmer Dashboard
       │         (Tamil & English)
       ▼
  Bilingual Advisory + Feedback Loop
```

## Architectural Layers

### 1. Ingestion Gateway
- Ingests multi-modal agricultural telemetry:
  - **Soil Moisture Mesh Nodes**: Volumetric water content (VWC %), soil temperature.
  - **Weather Stations**: Ambient dry-bulb temperature, relative humidity, wind speed, 24h & 72h precipitation forecast, reference evapotranspiration ($ET_0$).
  - **Sentinel-2 Satellite**: Multispectral surface reflectance (Red Band 4, NIR Band 8, SWIR Band 11).

### 2. Validation & PII Masking
- Validates physical biological boundaries (moisture 0–100%, temperatures -5°C to 65°C).
- Sanitizes personally identifiable information: phone numbers and email addresses are masked prior to internal storage and logging.

### 3. Field Intelligence & Deterministic Risk Engine
- Zero black-box hallucinations.
- Calculates transparent indices:
  - **Irrigation Urgency Score** (0–100): Depletion ratio against Field Capacity (FC) and Permanent Wilting Point (PWP) with phenological sensitivity and rain credits.
  - **Heat Stress Index** (0–100): Evaluates wet-bulb/heat index during sensitive crop stages (e.g. flowering spikelet sterility).
  - **Drought Risk Index** (0–100): Cumulative 14-day precipitation deficit + vegetative vigour depression.
  - **Excess Rain / Flood Threat** (0–100): 24h/72h forecast precipitation combined with soil saturation in heavy clay soils.
  - **Sensor Anomaly Score** (0–100): Flags stuck sensors, impossible jumps, and critical battery depletion.

### 4. Agricultural RAG Layer
- Curated repository of university research packages:
  - Tamil Nadu Agricultural University (TNAU) Agritech Portal crop production guides.
  - Indian Council of Agricultural Research (ICAR) water management handbook.
  - India Meteorological Department (IMD) Agromet Advisory bulletins.
- Embeddings with cosine similarity and metadata filtering (crop, stage, hazard type).
- Insufficient-evidence fallback when confidence falls below threshold.

### 5. Bounded Agent Workflow
- 7-Stage Finite State Machine:
  1. `COLLECT`: Assembles field context and observations.
  2. `VALIDATE`: Enforces integrity and masks PII.
  3. `ANALYZE`: Computes deterministic agronomic risk factors.
  4. `RETRIEVE`: Queries university guidance and extracts verified citations.
  5. `COMPOSE`: Generates bilingual Tamil and English structured advisories.
  6. `VERIFY`: Validates against safety invariants (no autonomous pump trigger, no chemical pesticide dosages).
  7. `DELIVER`: Routes High/Critical risk to Expert Review Gate, and Moderate/Low risk to auto-dispatch.

### 6. Human / Expert Review Gate
- High-risk advisories (e.g. acute drought, flood evacuation, severe heat stress at flowering) must receive human sign-off from an accredited agronomist before dispatch to farmers.

### 7. Farmer Dashboard & Feedback Loop
- React + Leaflet + Tailwind CSS dashboard.
- Bilingual (English & தமிழ்).
- Transparent confidence badges, provenance inspector, and farmer feedback logging.
