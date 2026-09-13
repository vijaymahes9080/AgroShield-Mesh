# AgroShield Mesh — REST API Reference (v1.0.0)

Base URL: `/api/v1`

## Authentication & Authorization
Uses JWT Bearer Tokens (`Authorization: Bearer <token>`).
Roles: `farmer`, `agronomist_expert`, `admin`.

| Method | Path | Description | Roles |
| :--- | :--- | :--- | :--- |
| `POST` | `/auth/register` | Register new user | Public |
| `POST` | `/auth/token` | Obtain JWT Bearer Token | Public |

## Farm & Field Management

| Method | Path | Description |
| :--- | :--- | :--- |
| `POST` | `/farmers` | Register farmer with consent flags |
| `GET` | `/farmers` | List registered farmers |
| `GET` | `/farmers/{id}` | Get farmer profile (PII masked) |
| `POST` | `/fields` | Create cadastral field boundary (GeoJSON in EPSG:4326) |
| `GET` | `/fields` | List fields with soil and irrigation metadata |
| `GET` | `/fields/{id}` | Get field details |
| `GET` | `/fields-geojson` | Export styled Leaflet/MapLibre GeoJSON FeatureCollection |
| `GET` | `/fields/{id}/synthetic-raster` | Generate Sentinel-2 multispectral NDVI & NDWI spectral analysis |

## Crop Cycles & Ingestion Gateway

| Method | Path | Description |
| :--- | :--- | :--- |
| `POST` | `/fields/{id}/crop-cycles` | Register active crop cycle (crop name, variety, stage, dates) |
| `GET` | `/fields/{id}/crop-cycles` | List crop cycles for field |
| `POST` | `/sensor-readings` | Ingest IoT mesh soil moisture and temperature telemetry |
| `GET` | `/fields/{id}/sensor-readings` | Fetch historical sensor observations |
| `POST` | `/weather-observations` | Ingest IMD / AWS weather observation and forecasts |
| `GET` | `/weather-observations` | List latest weather observations |
| `POST` | `/satellite-observations` | Ingest Sentinel-2 / Landsat surface reflectance records |
| `GET` | `/fields/{id}/satellite-observations` | Fetch satellite NDVI time-series observations |

## Risk Engine, Advisories & Expert Review Gate

| Method | Path | Description |
| :--- | :--- | :--- |
| `POST` | `/risk-assessments` | Trigger deterministic agronomic multi-factor risk assessment |
| `GET` | `/fields/{id}/risk-assessments` | Fetch risk assessment history |
| `POST` | `/advisories` | Run bounded agent workflow (Tamil/English with RAG citations) |
| `GET` | `/advisories` | List advisories (filter by `review_status`) |
| `POST` | `/advisories/{id}/review` | Expert Review Gate: Approve or reject advisory with notes |
| `POST` | `/advisories/{id}/feedback` | Record farmer adoption rating (1–5 stars) and water saved |

## Audit & System

| Method | Path | Description |
| :--- | :--- | :--- |
| `GET` | `/audit` | Retrieve cryptographically chained SHA-256 audit log |
| `GET` | `/health` | Service health status check |
| `GET` | `/version` | System version, CRS, and safety configuration |
