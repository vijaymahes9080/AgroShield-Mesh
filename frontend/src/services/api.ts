/**
 * AgroShield Mesh - Frontend API Client with Graceful Fallback
 * Works seamlessly both with live FastAPI backend and static GitHub Pages hosting.
 */

import {
  MOCK_FIELDS,
  MOCK_GEOJSON,
  MOCK_WEATHER,
  MOCK_ADVISORIES,
  MOCK_SENSORS,
  MOCK_AUDIT
} from './mockData';

const API_BASE = '/api/v1';

// Local in-memory store for mutations on static hosts (GitHub Pages)
let localAdvisories = [...MOCK_ADVISORIES];

export async function fetchFields() {
  try {
    const res = await fetch(`${API_BASE}/fields`);
    if (res.ok) return await res.json();
  } catch (_) {}
  return MOCK_FIELDS;
}

export async function fetchFieldGeoJSON() {
  try {
    const res = await fetch(`${API_BASE}/fields-geojson`);
    if (res.ok) return await res.json();
  } catch (_) {}
  return MOCK_GEOJSON;
}

export async function fetchFieldDetails(id: string) {
  try {
    const res = await fetch(`${API_BASE}/fields/${id}`);
    if (res.ok) return await res.json();
  } catch (_) {}
  return MOCK_FIELDS.find(f => f.id === id) || MOCK_FIELDS[0];
}

export async function fetchFieldSensors(fieldId: string) {
  try {
    const res = await fetch(`${API_BASE}/fields/${fieldId}/sensor-readings?limit=30`);
    if (res.ok) return await res.json();
  } catch (_) {}
  return MOCK_SENSORS.filter(s => s.field_id === fieldId || !s.field_id);
}

export async function fetchWeatherObservations() {
  try {
    const res = await fetch(`${API_BASE}/weather-observations?limit=10`);
    if (res.ok) return await res.json();
  } catch (_) {}
  return MOCK_WEATHER;
}

export async function fetchAdvisories() {
  try {
    const res = await fetch(`${API_BASE}/advisories?limit=50`);
    if (res.ok) return await res.json();
  } catch (_) {}
  return localAdvisories;
}

export async function fetchFieldRisk(fieldId: string) {
  try {
    const res = await fetch(`${API_BASE}/fields/${fieldId}/risk-assessments?limit=1`);
    if (res.ok) return await res.json();
  } catch (_) {}
  return [
    {
      id: `risk-${fieldId}`,
      field_id: fieldId,
      overall_risk_score: 58.0,
      risk_category: "MODERATE",
      urgency_level: "MEDIUM",
      moisture_depletion_pct: 42.5,
      flowering_heat_stress_index: 34.2,
      confidence_score: 0.94,
      assessed_at: new Date().toISOString()
    }
  ];
}

export async function generateAdvisory(fieldId: string, language: string = 'ta') {
  try {
    const res = await fetch(`${API_BASE}/advisories?field_id=${fieldId}&language=${language}`, {
      method: 'POST'
    });
    if (res.ok) return await res.json();
  } catch (_) {}

  // Fallback generation on static GitHub Pages
  const newAdv = {
    id: `adv-gh-${Date.now()}`,
    field_id: fieldId,
    farmer_id: "farmer-01",
    language,
    risk_level: "MODERATE",
    title: language === 'ta' 
      ? "AI வேளாண்மை பரிந்துரை: மாற்று ஈர மற்றும் உலர்த்துதல் (AWD)" 
      : "AI Agronomist Advisory: Alternate Wetting and Drying (AWD)",
    summary: language === 'ta'
      ? "மண்ணின் ஈரப்பதம் கண்காணிக்கப்பட்டு வருகிறது. அடுத்த 48 மணி நேரத்தில் மழை வர வாய்ப்புள்ளதால் குறைந்த அளவு நீர் மேலாண்மை போதுமானது."
      : "Soil moisture is being actively tracked. Light rain is forecasted in 48h; avoid continuous deep flooding.",
    action_items: language === 'ta'
      ? [
          "வயலில் 5 செ.மீ நீர் மட்டும் தேங்குமாறு பார்த்துக்கொள்ளவும்",
          "பூக்கும் தருணத்தில் பயிர் நீர் அழுத்தத்தைத் தவிர்க்கவும்"
        ]
      : [
          "Maintain thin water layer (5 cm) and monitor via field tube",
          "Avoid excessive waterlogging before forecast rainfall"
        ],
    prohibited_actions: language === 'ta'
      ? [
          "தேவையின்றி மின் மோட்டாரை தொடர்ந்து இயக்க வேண்டாம்",
          "அங்கீகரிக்கப்படாத ரசாயன மருந்துகளை பயன்படுத்த வேண்டாம்"
        ]
      : [
          "Do not run deep continuous pump flooding",
          "Never apply unverified synthetic chemical pesticides"
        ],
    citations: [
      {
        source_name: "TNAU Crop Production Guide",
        section: "AWD Water Management",
        page_number: 35,
        citation_hash: "a4f89b1c3e7208d1f7c00e129ba658b9",
        language
      }
    ],
    review_status: "approved",
    confidence_score: 0.93,
    created_at: new Date().toISOString()
  };
  localAdvisories = [newAdv, ...localAdvisories];
  return newAdv;
}

export async function reviewAdvisory(
  advisoryId: string,
  reviewStatus: string,
  reviewerName: string,
  reviewNotes: string
) {
  try {
    const res = await fetch(`${API_BASE}/advisories/${advisoryId}/review`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        review_status: reviewStatus,
        reviewer_name: reviewerName,
        review_notes: reviewNotes
      })
    });
    if (res.ok) return await res.json();
  } catch (_) {}

  // In-memory update
  localAdvisories = localAdvisories.map(a => 
    a.id === advisoryId ? { ...a, review_status: reviewStatus } : a
  );
  return { status: "success", review_status: reviewStatus };
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
  try {
    const res = await fetch(`${API_BASE}/advisories/${payload.advisory_id}/feedback`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (res.ok) return await res.json();
  } catch (_) {}
  return { status: "success", feedback_id: `fb-${Date.now()}` };
}

export async function fetchAuditLogs() {
  try {
    const res = await fetch(`${API_BASE}/audit?limit=30`);
    if (res.ok) return await res.json();
  } catch (_) {}
  return MOCK_AUDIT;
}

export async function fetchSyntheticRaster(fieldId: string, stressPatch: boolean = false) {
  try {
    const res = await fetch(`${API_BASE}/fields/${fieldId}/synthetic-raster?stress_patch=${stressPatch}`);
    if (res.ok) return await res.json();
  } catch (_) {}
  return {
    field_id: fieldId,
    mean_ndvi: stressPatch ? 0.42 : 0.74,
    mean_ndwi: stressPatch ? 0.18 : 0.38,
    canopy_status: stressPatch ? "Moderate Moisture Deficit" : "Optimal Vegetation Canopy",
    pixels_analyzed: 2500,
    timestamp: new Date().toISOString()
  };
}
