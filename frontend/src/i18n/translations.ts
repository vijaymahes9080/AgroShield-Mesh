export type Language = 'en' | 'ta';

export const translations = {
  en: {
    appTitle: 'AGROSHIELD MESH',
    appSubtitle: 'Agricultural Intelligence & Bounded Risk Engine',
    nav: {
      overview: 'Overview',
      fieldMap: 'Field Map',
      sensors: 'Sensors & Mesh',
      cropRisk: 'Crop Risk',
      advisories: 'Advisories & Gate',
      evidence: 'Evidence & RAG',
      feedback: 'Farmer Feedback',
      audit: 'Audit Log',
      benchmarks: 'Benchmarks'
    },
    header: {
      location: 'Erode District, Tamil Nadu',
      mode: 'Decision Support Active',
      expertRole: 'Agronomist Reviewer',
      lowBandwidth: 'Low Bandwidth',
      refresh: 'Refresh Live Data'
    },
    overview: {
      totalFields: 'Registered Fields',
      avgMoisture: 'Average Root Moisture',
      activeAlerts: 'Active Risk Alerts',
      pendingReview: 'Expert Review Queue',
      quickActionTitle: 'Trigger Autonomous Field Advisory',
      selectField: 'Select Target Field',
      evaluateBtn: 'Run Bounded Agent Pipeline',
      statusSummary: 'Real-time Agricultural Telemetry',
      recentAdvisories: 'Recent Advisories',
      weatherOverview: 'District Weather Observation'
    },
    map: {
      title: 'Geospatial Field Telemetry & Satellite Indices',
      legend: 'Risk Severity Index',
      low: 'Optimal (Low)',
      moderate: 'Caution (Moderate)',
      high: 'High Deficit / Heat',
      critical: 'Emergency / Waterlogging',
      ndviLayer: 'Sentinel-2 NDVI Overlay',
      sensorsLayer: 'IoT Mesh Nodes'
    },
    risk: {
      title: 'Deterministic Risk Factor Breakdown',
      score: 'Composite Risk Score',
      irrigationNeed: 'Irrigation Deficit Urgency',
      heatStress: 'Thermal Heat Stress',
      droughtRisk: 'Drought & Deficit Index',
      excessRain: 'Excess Rain / Flood Threat',
      sensorAnomaly: 'Telemetry Anomaly Score',
      confidence: 'System Confidence Score',
      missingData: 'Data Freshness Caveats',
      verificationStep: 'Mandatory Verification Step'
    },
    advisory: {
      title: 'Bilingual Crop Advisories & Human Review Gate',
      aiSuggested: 'AI Draft (Pending Expert Review)',
      expertApproved: 'Expert Approved & Certified',
      autoDispatched: 'Auto-Dispatched (Low Risk)',
      actionItems: 'Actionable Agronomic Guidance',
      prohibited: 'Strictly Prohibited Actions',
      citations: 'Authoritative University Citations',
      reviewAction: 'Review Decision',
      approveBtn: 'Approve for Farmer Dispatch',
      rejectBtn: 'Reject / Flag for Revision',
      notesPlaceholder: 'Enter verification notes and rationale...'
    },
    feedback: {
      title: 'Farmer Adoption & Verification Feedback',
      rating: 'Advisory Helpfulness Rating',
      actionTaken: 'Actual Action Executed on Field',
      waterSaved: 'Estimated Water Conserved (Litres)',
      submit: 'Submit Field Feedback',
      success: 'Feedback recorded successfully!'
    },
    benchmarks: {
      title: '100 Synthetic Scenarios Performance Benchmark',
      subtitle: 'Rigorous empirical evaluation against expert agronomist ground-truth labels',
      irrigationAgreement: 'Irrigation Urgency Agreement',
      riskAccuracy: 'Risk Classification Accuracy',
      citationCoverage: 'Citation Provenance Coverage',
      falseAlertRate: 'False High-Alert Rate',
      maxLatency: 'Max Advisory Latency'
    }
  },
  ta: {
    appTitle: 'அக்ரோஷீல்டு மெஷ்',
    appSubtitle: 'விவசாய நுண்ணறிவு மற்றும் இடர் மேலாண்மை தளம்',
    nav: {
      overview: 'கண்ணோட்டம்',
      fieldMap: 'வயல் வரைபடம்',
      sensors: 'சென்சார் நெட்வொர்க்',
      cropRisk: 'பயிர் இடர் ஆய்வு',
      advisories: 'ஆலோசனைகள் & ஒப்புதல்',
      evidence: 'பல்கலைக்கழக சான்றுகள்',
      feedback: 'விவசாயி கருத்து',
      audit: 'தணிக்கை பதிவு',
      benchmarks: 'செயல்திறன் மதிப்பீடு'
    },
    header: {
      location: 'ஈரோடு மாவட்டம், தமிழ்நாடு',
      mode: 'முடிவெடுக்கும் ஆதரவு இயங்குகிறது',
      expertRole: 'வேளாண் வல்லுநர்',
      lowBandwidth: 'குறைந்த அலைவரிசை',
      refresh: 'புதுப்பி'
    },
    overview: {
      totalFields: 'பதிவுசெய்த வயல்கள்',
      avgMoisture: 'சராசரி மண் ஈரப்பதம்',
      activeAlerts: 'செயலில் உள்ள எச்சரிக்கைகள்',
      pendingReview: 'வல்லுநர் ஒப்புதல் வரிசை',
      quickActionTitle: 'பயிர் ஆலோசனையை உருவாக்கு',
      selectField: 'வயலைத் தேர்ந்தெடுக்கவும்',
      evaluateBtn: 'ஆய்வை இயக்கவும்',
      statusSummary: 'நிகழ்நேர விவசாயத் தகவல்கள்',
      recentAdvisories: 'சமீபத்திய ஆலோசனைகள்',
      weatherOverview: 'மாவட்ட வானிலை அறிக்கை'
    },
    map: {
      title: 'புவிசார் வயல் தகவல் மற்றும் செயற்கைக்கோள் குறியீடு',
      legend: 'அபாய அளவு',
      low: 'சரியானது (குறைவு)',
      moderate: 'கவனம் (நடுத்தரம்)',
      high: 'அதிக பற்றாக்குறை / வெப்பம்',
      critical: 'அவசரம் / நீர் தேக்கம்',
      ndviLayer: 'சென்டினல்-2 NDVI அடுக்கு',
      sensorsLayer: 'IoT சென்சார் முனைகள்'
    },
    risk: {
      title: 'விவசாய இடர் காரணிகளின் பகுப்பாய்வு',
      score: 'ஒட்டுமொத்த இடர் குறியீடு',
      irrigationNeed: 'பாசனத் தேவை அவசரம்',
      heatStress: 'வெப்ப அழுத்த இடர்',
      droughtRisk: 'வறட்சி அபாயக் குறியீடு',
      excessRain: 'கனமழை / வெள்ள அபாயம்',
      sensorAnomaly: 'சென்சார் பிழைக் குறியீடு',
      confidence: 'அமைப்பின் நம்பகத்தன்மை',
      missingData: 'கிடைக்காத தரவு எச்சரிக்கைகள்',
      verificationStep: 'நேரடி கள ஆய்வு வழிகாட்டல்'
    },
    advisory: {
      title: 'இருமொழி விவசாய ஆலோசனைகள் & வல்லுநர் ஒப்புதல்',
      aiSuggested: 'AI பரிந்துரை (வல்லுநர் பார்வைக்கு)',
      expertApproved: 'வல்லுநர் சரிபார்த்து அங்கீகரித்தது',
      autoDispatched: 'தானியங்கி அனுப்பப்பட்டது',
      actionItems: 'மேற்கொள்ள வேண்டிய நடவடிக்கைகள்',
      prohibited: 'தவிர்க்க வேண்டிய தவறான நடவடிக்கைகள்',
      citations: 'அதிகாரப்பூர்வ பல்கலைக்கழக சான்றுகள்',
      reviewAction: 'வல்லுநர் முடிவு',
      approveBtn: 'விவசாயிக்கு அனுப்ப ஒப்புதல் அளி',
      rejectBtn: 'மறுபரிசீலனை செய்',
      notesPlaceholder: 'சரிபார்ப்பு குறிப்புகளை எழுதவும்...'
    },
    feedback: {
      title: 'விவசாயி பயன்பாடு மற்றும் முடிவுகள் பின்னூட்டம்',
      rating: 'ஆலோசனையின் பயனுள்ள மதிப்பீடு',
      actionTaken: 'வயலில் உண்மையில் செய்த நடவடிக்கை',
      waterSaved: 'சேமிக்கப்பட்ட நீர் அளவு (லிட்டர்கள்)',
      submit: 'பின்னூட்டத்தை பதிவு செய்',
      success: 'பின்னூட்டம் வெற்றிகரமாகப் பதிவு செய்யப்பட்டது!'
    },
    benchmarks: {
      title: '100 மாதிரி சூழல்களின் செயல்திறன் மதிப்பீடு',
      subtitle: 'வேளாண் வல்லுநர்களின் உண்மைத் தீர்ப்புகளுடன் ஒப்பீடு',
      irrigationAgreement: 'பாசனத் தேவை ஒப்பீட்டுப் பொருத்தம்',
      riskAccuracy: 'இடர் கணிப்புத் துல்லியம்',
      citationCoverage: 'பல்கலைக்கழக சான்றுகள் பாதுகாப்பு',
      falseAlertRate: 'தவறான உயர் எச்சரிக்கை விகிதம்',
      maxLatency: 'அதிகபட்ச ஆலோசனை உருவாக்க நேரம்'
    }
  }
};
