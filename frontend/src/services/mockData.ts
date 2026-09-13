/**
 * AgroShield Mesh - Static Mock Data for GitHub Pages & Offline Demos
 */

export const MOCK_FIELDS = [
  {
    id: "field-perundurai-01",
    farmer_id: "farmer-01",
    farmer_name: "Vijay Mahes",
    name: "Perundurai Delta Paddy Field A",
    boundary_geojson: {
      type: "Polygon",
      coordinates: [
        [
          [77.5810, 11.2720],
          [77.5845, 11.2720],
          [77.5845, 11.2755],
          [77.5810, 11.2755],
          [77.5810, 11.2720]
        ]
      ]
    },
    centroid_lat: 11.27375,
    centroid_lon: 77.58275,
    area_hectares: 2.45,
    soil_type: "Red Loam",
    soil_field_capacity: 32.0,
    soil_wilting_point: 14.0,
    irrigation_source: "Borewell / Drip",
    village: "Perundurai",
    district: "Erode",
    state: "Tamil Nadu",
    operational_status: "active"
  },
  {
    id: "field-bhavani-02",
    farmer_id: "farmer-02",
    farmer_name: "R. Murugesan",
    name: "Bhavani River Basin Cotton Field B",
    boundary_geojson: {
      type: "Polygon",
      coordinates: [
        [
          [77.6750, 11.4410],
          [77.6790, 11.4410],
          [77.6790, 11.4450],
          [77.6750, 11.4450],
          [77.6750, 11.4410]
        ]
      ]
    },
    centroid_lat: 11.4430,
    centroid_lon: 77.6770,
    area_hectares: 3.12,
    soil_type: "Black Clay",
    soil_field_capacity: 40.0,
    soil_wilting_point: 18.0,
    irrigation_source: "Canal / Furrow",
    village: "Bhavani",
    district: "Erode",
    state: "Tamil Nadu",
    operational_status: "active"
  },
  {
    id: "field-gobi-03",
    farmer_id: "farmer-03",
    farmer_name: "K. Selvi",
    name: "Gobichettipalayam Millet Terrace C",
    boundary_geojson: {
      type: "Polygon",
      coordinates: [
        [
          [77.4280, 11.4550],
          [77.4320, 11.4550],
          [77.4320, 11.4590],
          [77.4280, 11.4590],
          [77.4280, 11.4550]
        ]
      ]
    },
    centroid_lat: 11.4570,
    centroid_lon: 77.4300,
    area_hectares: 1.85,
    soil_type: "Sandy Loam",
    soil_field_capacity: 22.0,
    soil_wilting_point: 9.0,
    irrigation_source: "Rainfed / Sprinkler",
    village: "Gobichettipalayam",
    district: "Erode",
    state: "Tamil Nadu",
    operational_status: "active"
  }
];

export const MOCK_GEOJSON = {
  type: "FeatureCollection",
  crs: {
    type: "name",
    properties: { name: "urn:ogc:def:crs:OGC:1.3:CRS84" }
  },
  features: MOCK_FIELDS.map(f => ({
    type: "Feature",
    id: f.id,
    properties: {
      name: f.name,
      farmer_name: f.farmer_name,
      soil_type: f.soil_type,
      irrigation_source: f.irrigation_source,
      area_hectares: f.area_hectares,
      village: f.village,
      district: f.district
    },
    geometry: f.boundary_geojson
  }))
};

export const MOCK_WEATHER = [
  {
    id: "weather-01",
    station_id: "IMD-ERODE-04",
    station_name: "Erode Central Agromet Observatory",
    latitude: 11.3410,
    longitude: 77.7172,
    temperature_c: 32.5,
    relative_humidity_pct: 68.0,
    rainfall_1h_mm: 0.0,
    rainfall_24h_mm: 4.2,
    wind_speed_kmh: 11.4,
    forecast_rain_24h_mm: 12.0,
    forecast_rain_72h_mm: 28.5,
    observed_at: new Date().toISOString()
  }
];

export const MOCK_ADVISORIES = [
  {
    id: "adv-mock-01",
    field_id: "field-perundurai-01",
    farmer_id: "farmer-01",
    language: "ta",
    risk_level: "MODERATE",
    title: "AI வேளாண்மை பரிந்துரை: மாற்று ஈர மற்றும் உலர்த்துதல் (AWD) முறை",
    summary: "மண்ணின் ஈரப்பதம் 20% அளவை நெருங்குகிறது. அடுத்த 48 மணி நேரத்தில் 12 மி.மீ மழை எதிர்பார்க்கப்படுவதால் ஆழ்ந்த நீர்ப்பாசனத்தைத் தவிர்க்கவும்.",
    action_items: [
      "வயலில் 5 செ.மீ மட்டுமே நீர் தேங்குமாறு பார்த்துக்கொள்ளவும்",
      "மண்ணின் மேற்பரப்பு உலர்ந்த பிறகே அடுத்த பாசனம் செய்யவும்",
      "பயிரின் பூக்கும் பருவத்தில் 1% பொட்டாசியம் குளோரைடு தெளிக்கவும்"
    ],
    prohibited_actions: [
      "மின் மோட்டாரை தொடர்ந்து இயக்கி வயலில் அதிக நீர் தேக்க வேண்டாம்",
      "அங்கீகரிக்கப்படாத பூச்சிக்கொல்லிகளை கலக்க வேண்டாம்"
    ],
    citations: [
      {
        source_name: "TNAU Paddy Crop Management Guide 2020",
        section: "Water Management - AWD Technique",
        page_number: 42,
        citation_hash: "a4f89b1c3e7208d1f7c00e129ba658b9",
        language: "ta"
      }
    ],
    review_status: "approved",
    confidence_score: 0.94,
    created_at: new Date(Date.now() - 3600000).toISOString()
  },
  {
    id: "adv-mock-02",
    field_id: "field-bhavani-02",
    farmer_id: "farmer-02",
    language: "ta",
    risk_level: "LOW",
    title: "பருத்தி பாசன மற்றும் வடிகால் வழிகாட்டுதல்",
    summary: "கரிசல் மண்ணில் ஈரப்பதம் போதுமானதாக உள்ளது (34%). வடிகால் வசதியை உறுதிப்படுத்தவும்.",
    action_items: [
      "பாத்திகளில் தேங்கும் அதிகப்படியான மழைநீரை வடிகட்டவும்",
      "காய்ப்புழு தாக்குதலை கவனிக்கவும்"
    ],
    prohibited_actions: [
      "மண்ணில் ஈரம் இருக்கும்போது பாசனம் செய்ய வேண்டாம்"
    ],
    citations: [
      {
        source_name: "ICAR Cotton Production Bulletin",
        section: "Black Clay Soil Drainage Rules",
        page_number: 18,
        citation_hash: "7c3aed8f12b406e19d5c80ab91f24e3a",
        language: "ta"
      }
    ],
    review_status: "approved",
    confidence_score: 0.91,
    created_at: new Date(Date.now() - 7200000).toISOString()
  },
  {
    id: "adv-mock-03",
    field_id: "field-gobi-03",
    farmer_id: "farmer-03",
    language: "ta",
    risk_level: "HIGH",
    title: "கேழ்வரகு வெப்ப அழுத்த எச்சரிக்கை - வல்லுநர் மதிப்பீடு தேவை",
    summary: "அதிகபட்ச வெப்பநிலை 36°C தாண்டுகிறது. பூக்கும் பருவத்தில் தழைச்சத்து பற்றாக்குறை அபாயம்.",
    action_items: [
      "தெளிப்பு நீர் பாசனம் மூலம் பயிர் தட்பவெப்பத்தை குறைக்கவும்",
      "மாலையில் நுண்ணூட்டச்சத்து தெளிக்கவும்"
    ],
    prohibited_actions: [
      "நண்பகல் வேளையில் தெளிப்பு பாசனம் செய்ய வேண்டாம்"
    ],
    citations: [
      {
        source_name: "TNAU Millets Agronomy Protocol",
        section: "Heat Mitigation in Finger Millet",
        page_number: 29,
        citation_hash: "e5d8091cf76b2a0149e38d745acbb810",
        language: "ta"
      }
    ],
    review_status: "pending_review",
    confidence_score: 0.88,
    created_at: new Date(Date.now() - 1800000).toISOString()
  }
];

export const MOCK_SENSORS = [
  { id: "s-1", field_id: "field-perundurai-01", node_id: "node-mesh-01", soil_moisture_30cm_pct: 19.4, soil_moisture_60cm_pct: 26.8, soil_temp_c: 28.2, ambient_temp_c: 32.4, ambient_humidity_pct: 64.0, leaf_wetness_pct: 12.0, battery_volts: 3.92, recorded_at: new Date().toISOString() },
  { id: "s-2", field_id: "field-perundurai-01", node_id: "node-mesh-01", soil_moisture_30cm_pct: 21.0, soil_moisture_60cm_pct: 27.2, soil_temp_c: 27.9, ambient_temp_c: 31.8, ambient_humidity_pct: 66.0, leaf_wetness_pct: 15.0, battery_volts: 3.93, recorded_at: new Date(Date.now() - 3600000).toISOString() },
  { id: "s-3", field_id: "field-perundurai-01", node_id: "node-mesh-01", soil_moisture_30cm_pct: 23.5, soil_moisture_60cm_pct: 28.1, soil_temp_c: 26.5, ambient_temp_c: 29.5, ambient_humidity_pct: 71.0, leaf_wetness_pct: 22.0, battery_volts: 3.95, recorded_at: new Date(Date.now() - 7200000).toISOString() }
];

export const MOCK_AUDIT = [
  { id: "aud-01", event_type: "ADVISORY_GENERATION", actor_role: "SYSTEM", entity_id: "adv-mock-01", payload_summary: "Bounded agent generated AWD advisory for Perundurai Field A", chain_hash: "9af8c7b310...7d8e", created_at: new Date(Date.now() - 3600000).toISOString() },
  { id: "aud-02", event_type: "EXPERT_REVIEW", actor_role: "AGRONOMIST", entity_id: "adv-mock-01", payload_summary: "Senior Agronomist Dr. K. Ramanathan approved AWD advisory", chain_hash: "b21e87f4c0...5a19", created_at: new Date(Date.now() - 3200000).toISOString() },
  { id: "aud-03", event_type: "TELEMETRY_INGESTION", actor_role: "IOT_GATEWAY", entity_id: "node-mesh-01", payload_summary: "PII-masked telemetry ingested from Perundurai mesh probe", chain_hash: "e6f501ca92...3b77", created_at: new Date(Date.now() - 1200000).toISOString() }
];
