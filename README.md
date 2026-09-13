# 🌾 AGROSHIELD MESH

[![License: MIT](https://img.shields.io/badge/License-MIT-emerald.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-teal.svg)](https://fastapi.tiangolo.com/)
[![React 19 + Vite](https://img.shields.io/badge/Frontend-React%2019%20%2B%20Vite-cyan.svg)](https://vitejs.dev/)
[![Tailwind CSS v4](https://img.shields.io/badge/Styling-Tailwind%20CSS-sky.svg)](https://tailwindcss.com/)
[![Leaflet GIS](https://img.shields.io/badge/Geospatial-Leaflet%20%2B%20Shapely-green.svg)](https://leafletjs.com/)
[![MCP SDK](https://img.shields.io/badge/Protocol-Model%20Context%20Protocol-purple.svg)](https://modelcontextprotocol.io/)
[![n8n Workflow](https://img.shields.io/badge/Automation-n8n%20Community-orange.svg)](https://n8n.io/)
[![CI Tests](https://img.shields.io/badge/Tests-21%2F21%20Passed-brightgreen.svg)]()
[![Benchmarks](https://img.shields.io/badge/100--Scenario%20Benchmarks-Targets%20Met-success.svg)]()

> **Evidence-Grounded Agricultural Intelligence & Bounded Risk Engine**
> Integrating IoT wireless mesh telemetry, satellite multispectral observations, deterministic agronomic risk models, Agricultural RAG with university citations, and an accredited Expert Review Gate.

---

## 🏛️ System Architecture

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
       - NDVI / canopy stress
       - water need
       - deterministic risk rules
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

---

## 🛡️ Core Safety Rules & Agronomic Guardrails

- **No False Certainty**: Biological systems vary with root depth and microclimate. Every advisory explicitly reports a confidence level (0.0–1.0) and missing-data penalties.
- **Zero Autonomous Machine Actuation**: The platform **strictly disallows** autonomous triggering of high-power irrigation pumps, motors, or fertigation valves in the MVP.
- **Prohibited Pesticide Prescriptions**: The platform **never invents or prescribes hazardous chemical pesticides**. Advisories focus on cultural water management (AWD), microclimate cooling, and university package-of-practices foliar nutrients.
- **Mandatory Source Citations**: Every guidance-based recommendation requires verifiable citations with document section, page number, and cryptographic SHA-256 hash (TNAU, ICAR, IMD).
- **Mandatory Expert Review Gate**: Any advisory flagged with **HIGH** or **CRITICAL** risk is held in `pending_review` until signed off by an accredited human agronomist.
- **Privacy & PII Masking**: Farmer phone numbers and personal emails are masked before telemetry storage or logging.

---

## 📊 Empirical Evaluation & 100-Scenario Benchmarks

The system was evaluated against **100 synthetic scenarios** across 5 agro-climatic categories with expert agronomist ground-truth labels:

| Evaluation Metric | Target | Result | Status |
| :--- | :---: | :---: | :---: |
| **Irrigation Urgency Agreement** | $\ge 80.0\%$ | **97.0%** | ✅ **PASS** |
| **Risk Classification Accuracy** | $\ge 75.0\%$ | **84.0%** | ✅ **PASS** |
| **Citation Coverage Rate** | $\ge 90.0\%$ | **100.0%** | ✅ **PASS** |
| **False High-Alert Rate** | $< 15.0\%$ | **0.0%** | ✅ **PASS** |
| **Max Advisory Latency** | $< 30.0\text{ s}$ | **0.008 s** | ✅ **PASS** |

### Category Breakdown
1. **Irrigation Scenarios (30 cases)**: Under-irrigation, optimal moisture, saturation, rain forecast credit.
2. **Drought & Heat Stress (20 cases)**: 14-day rainfall deficit, flowering heat index $>35^\circ\text{C}$, canopy depression.
3. **Excess Rain & Waterlogging (20 cases)**: Monsoon surges ($>50\text{ mm}$), black clay drainage bottlenecks.
4. **Contradictory Sensor Nodes (20 cases)**: Stuck readings, sudden impossible jumps, out-of-range probes.
5. **Multilingual Bilingual Cases (10 cases)**: Tamil (தமிழ்) and English evidence grounding.

---

## 🗂️ Repository Structure

```
.
├── backend/                  # FastAPI REST API, SQLAlchemy ORM, RBAC, PII masking
├── geospatial/               # EPSG:4326/3857 CRS, Shapely polygons, Sentinel-2 NDVI raster engine
├── rag/                      # TNAU & ICAR agricultural knowledge base, semantic retriever, citations
├── agents/                   # 7-stage Bounded Agent Workflow, deterministic risk engine, safety verifier
├── mcp_server/               # Model Context Protocol (MCP) server & 6 safe read-only tools
├── n8n/                      # n8n automation workflow JSON & setup documentation
├── frontend/                 # React 19, TypeScript, Vite, Tailwind CSS v4, Leaflet dashboard
├── sample_data/              # Sample GeoJSON cadastral boundaries & telemetry payloads
├── benchmarks/               # 100 synthetic scenarios & automated evaluation runner
├── tests/                    # 21 comprehensive Pytest unit & integration tests (100% pass)
├── docs/                     # Architecture, Geospatial CRS, Safety Rules, API Reference
├── scripts/                  # Database seeder, secret scanner, n8n simulator, e2e demo
├── docker-compose.yml        # PostgreSQL/PostGIS, Redis, Mosquitto MQTT, n8n, Backend, Frontend
└── README.md
```

---

## 🚀 Quickstart Guide

### Prerequisites
- **Python 3.11+**
- **Node.js 20+** and **npm**

### 1. Seed Database with Realistic Tamil Nadu Agricultural Data
```bash
# Seeds Erode district fields, farmers, IoT sensors, weather, and advisories
python scripts/seed_database.py
```

### 2. Run End-to-End Field Advisory Demo
```bash
python scripts/demo_e2e.py
```

### 3. Run Benchmark Suite (100 Scenarios)
```bash
python benchmarks/run_benchmarks.py
```

### 4. Run Pytest Test Suite
```bash
python -m pytest tests/ -v
```

### 5. Run Backend & Frontend Locally
```bash
# Terminal 1: Backend API (FastAPI)
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2: Frontend Dashboard (Vite + React)
cd frontend
npm run dev
```

Open:
- **Interactive Dashboard**: `http://localhost:5173` (or `http://localhost:8000/dashboard/`)
- **Interactive Swagger Docs**: `http://localhost:8000/docs`

---

## 🔌 Model Context Protocol (MCP) Server

AgroShield Mesh exposes safe read-only and analytical tools over the Model Context Protocol:

| MCP Tool | Description |
| :--- | :--- |
| `get_field_status` | Returns field operational status, soil moisture, and current risk level. |
| `get_weather_summary` | Returns local station observations and 24h/72h rainfall forecast. |
| `get_crop_calendar` | Returns crop stage duration and critical moisture thresholds. |
| `search_agri_guidance` | Semantic search across university guides (TNAU/ICAR) with citations. |
| `calculate_irrigation_need` | Transparent deterministic irrigation urgency calculation (0–100). |
| `generate_farmer_advisory` | Executes bounded agent workflow to produce evidence-grounded advisory. |

To run the MCP server:
```bash
python mcp_server/server.py
```

---

## 🔄 n8n Automation Workflow

The workflow (`n8n/agroshield_advisory_workflow.json`) coordinates autonomous ingestion, idempotency checking, risk evaluation, and conditional notification dispatch:
- High/Critical risk advisories are routed to the **Expert Review Gate**.
- Normal advisories are sent to **Mock Farmer Notification (SMS / WhatsApp)**.

Run the standalone simulator without needing an active n8n instance:
```bash
python scripts/simulate_n8n_flow.py
```

---

## 🌐 Geospatial Standards & Coordinate Reference Systems

- **EPSG:4326 (WGS 84)**: All GeoJSON polygons, field centroids, and GPS coordinates.
- **EPSG:3857 (Web Mercator)**: Projected coordinate calculations for metric buffers.
- **Synthetic NDVI**: Multispectral Sentinel-2 reflectance computation:
  $$\text{NDVI} = \frac{\text{NIR (B8)} - \text{Red (B4)}}{\text{NIR (B8)} + \text{Red (B4)}}$$

---

## 👤 Author & Maintainer

**Vijay Mahes**  
Email: [Vijaypradhap2004@gmail.com](mailto:Vijaypradhap2004@gmail.com)  
GitHub: [@vijaymahes9080](https://github.com/vijaymahes9080)  
Repository: [AgroShield-Mesh](https://github.com/vijaymahes9080/AgroShield-Mesh)

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
