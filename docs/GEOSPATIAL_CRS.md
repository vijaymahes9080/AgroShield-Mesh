# AgroShield Mesh — Geospatial Coordinate Systems & Spectral Indices

## Coordinate Reference Systems (CRS)

All spatial geometries in AgroShield Mesh are explicitly defined with defined SRIDs:

| CRS Code | Authority | Type | Unit | Usage in AgroShield Mesh |
| :--- | :--- | :--- | :--- | :--- |
| **EPSG:4326** | OGC WGS 84 | Geographic 2D | Decimal Degrees (lat/lon) | Storage in SQLite/PostGIS, GeoJSON API contracts, GPS sensors, Leaflet map overlays |
| **EPSG:3857** | WGS 84 / Pseudo-Mercator | Projected 2D | Meters | Planar distance buffers, raster tile grid alignment |

### Field Boundary Validation & Geodesic Calculation
Field polygons undergo topological validation using Shapely:
- Rings must be closed ($P_0 = P_n$).
- Self-intersections and sliver polygons are rejected.
- Geodesic area is calculated on the WGS 84 ellipsoid:
  $$A = \frac{R^2}{4} \sum_{i=1}^{n-1} (\lambda_{i+1} - \lambda_i) (2 + \sin \phi_i + \sin \phi_{i+1})$$
  Expressed in **hectares** ($1\text{ ha} = 10,000\text{ m}^2$).

---

## Synthetic Multispectral Raster Analysis

AgroShield Mesh generates synthetic Sentinel-2 MSI (MultiSpectral Instrument) multi-band reflectance:

1. **Band 4 — Red ($\lambda = 665\text{ nm}$)**: Chlorophyll absorption band.
2. **Band 8 — NIR ($\lambda = 842\text{ nm}$)**: High reflectance by mesophyll leaf structure in healthy crops.
3. **Band 11 — SWIR ($\lambda = 1610\text{ nm}$)**: Water absorption band indicating canopy moisture.

### Normalized Difference Vegetation Index (NDVI)
$$\text{NDVI} = \frac{\text{NIR} - \text{Red}}{\text{NIR} + \text{Red}}$$

- **Healthy Dense Canopy**: $\text{NDVI} \in [0.65, 0.85]$
- **Moderate Growth / Mild Stress**: $\text{NDVI} \in [0.40, 0.64]$
- **Severe Moisture Deficit / Sparse Vegetation**: $\text{NDVI} < 0.35$

### Normalized Difference Water Index (NDWI)
$$\text{NDWI} = \frac{\text{NIR} - \text{SWIR}}{\text{NIR} + \text{SWIR}}$$
Measures liquid water content in crop canopy.
