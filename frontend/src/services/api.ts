/**
 * AgroShield Mesh - Frontend API Client
 */

const API_BASE = '/api/v1';

export async function fetchFields() {
  const res = await fetch(`${API_BASE}/fields`);
  if (!res.ok) throw new Error('Failed to fetch fields');
  return res.json();
}

export async function fetchFieldGeoJSON() {
  const res = await fetch(`${API_BASE}/fields-geojson`);
  if (!res.ok) throw new Error('Failed to fetch GeoJSON fields');
  return res.json();
}

export async function fetchFieldDetails(id: string) {
  const res = await fetch(`${API_BASE}/fields/${id}`);
  if (!res.ok) throw new Error('Failed to fetch field details');
  return res.json();
}

export async function fetchFieldSensors(fieldId: string) {
  const res = await fetch(`${API_BASE}/fields/${fieldId}/sensor-readings?limit=30`);
  if (!res.ok) throw new Error('Failed to fetch sensor readings');
  return res.json();
}

export async function fetchWeatherObservations() {
  const res = await fetch(`${API_BASE}/weather-observations?limit=10`);
  if (!res.ok) throw new Error('Failed to fetch weather');
  return res.json();
}

export async function fetchAdvisories() {
  const res = await fetch(`${API_BASE}/advisories?limit=50`);
  if (!res.ok) throw new Error('Failed to fetch advisories');
  return res.json();
}

export async function generateAdvisory(fieldId: string, language: string = 'ta') {
  const res = await fetch(`${API_BASE}/advisories?field_id=${fieldId}&language=${language}`, {
    method: 'POST'
  });
  if (!res.ok) throw new Error('Failed to generate advisory');
  return res.json();
}

export async function reviewAdvisory(
  advisoryId: string,
  reviewStatus: string,
  reviewerName: string,
  reviewNotes: string
) {
  const res = await fetch(`${API_BASE}/advisories/${advisoryId}/review`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      review_status: reviewStatus,
      reviewer_name: reviewerName,
      review_notes: reviewNotes
    })
  });
  if (!res.ok) throw new Error('Failed to submit expert review');
  return res.json();
}

export async function submitFeedback(payload: {
  advisory_id: string;
  farmer_id: string;
  rating: number;
  helpful_flag: boolean;
  actual_action_taken: string;
  unnecessary_irrigation_prevented_litres?: number;
  comments?: string;
}) {
  const res = await fetch(`${API_BASE}/advisories/${payload.advisory_id}/feedback`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  if (!res.ok) throw new Error('Failed to submit feedback');
  return res.json();
}

export async function fetchAuditLogs() {
  const res = await fetch(`${API_BASE}/audit?limit=30`);
  if (!res.ok) throw new Error('Failed to fetch audit log');
  return res.json();
}

export async function fetchSyntheticRaster(fieldId: string, stressPatch: boolean = false) {
  const res = await fetch(`${API_BASE}/fields/${fieldId}/synthetic-raster?stress_patch=${stressPatch}`);
  if (!res.ok) throw new Error('Failed to fetch raster analysis');
  return res.json();
}
