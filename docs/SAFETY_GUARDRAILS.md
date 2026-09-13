# AgroShield Mesh — Safety Guardrails & Operating Constraints

## Core Safety Rules & Invariants

AgroShield Mesh is designed as a **Decision Support System (DSS)**. It does not replace physical on-field agronomic inspection and enforces strict safety invariants:

### 1. No Agronomic Certainty Claims
- Biological systems exhibit stochastic variance across microclimates and root depths.
- All models, calculations, and RAG retrievals must report confidence scores (0.0 to 1.0) and missing data penalties.
- Outputs are labeled as **Evidence-Grounded Recommendations**, never infallible certainty.

### 2. Zero Autonomous Machine Actuation
- The platform **strictly disallows** direct control or autonomous triggering of high-power irrigation pumps, motors, or chemical fertigation valves.
- The advisory delivers human-actionable guidance (e.g. "Apply 3–5 cm light irrigation"). The farmer or operator remains the sole controller of field valves.

### 3. Prohibited Chemical Prescriptions
- The platform **never invents or prescribes hazardous synthetic insecticides or unverified pesticide dosages**.
- Advisories focus exclusively on:
  - Cultural water management (e.g. Alternate Wetting & Drying - AWD).
  - Agronomic microclimate management (e.g. standing water cooling during heatwaves).
  - Mulching and drainage channel clearance.
  - Approved university foliar nutrient sprays (e.g. 1% KCl or 2% DAP as per TNAU package of practices).

### 4. Mandatory Source Citations
- Every recommendation based on guidance must cite:
  - Authoritative source organization (e.g. TNAU, ICAR, IMD).
  - Title and publication year.
  - Document section and page/bulletin number.
  - Cryptographic SHA-256 document hash for immutable provenance.

### 5. Mandatory Human / Expert Review Gate
- When composite risk or single-hazard severity is classified as **HIGH** or **CRITICAL**:
  - The advisory is locked into `pending_review` status.
  - External notifications (SMS/WhatsApp) are withheld.
  - The advisory is queued in the Agronomist Dashboard for accredited expert review.
  - Once reviewed and approved by an accredited agronomist, the status transitions to `expert_approved` for distribution.

### 6. PII Masking & Data Privacy
- Farmer phone numbers, email addresses, and exact cadastral identifiers are masked before internal logging or transmission across telemetry pipelines.
- Only authorized farmers and accredited agronomists have access to field-level details.
