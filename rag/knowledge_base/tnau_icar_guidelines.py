"""
AgroShield Mesh - Curated Agricultural Knowledge Base
Authoritative recommendations compiled from:
- Tamil Nadu Agricultural University (TNAU) Agritech Portal
- Indian Council of Agricultural Research (ICAR) Water Management Manual
- India Meteorological Department (IMD) Agromet Advisory Services (Erode / Coimbatore Zone)
Preserving strict citations, page references, Tamil translations, and cryptographic SHA-256 hashes.
"""

import hashlib
from typing import List, Dict, Any


def compute_sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


RAW_KNOWLEDGE_DOCUMENTS: List[Dict[str, Any]] = [
    {
        "doc_id": "TNAU-CPG-PAD-01",
        "title": "TNAU Crop Production Guide: Wet Season Rice (Paddy) Water Management",
        "source": "Tamil Nadu Agricultural University (TNAU), Coimbatore",
        "publication_year": 2024,
        "section": "Irrigation Management - Alternate Wetting and Drying (AWD)",
        "page_or_bulletin": "Bulletin No. 14, pp. 48-52",
        "language": "en",
        "crop_targets": ["Paddy (Rice)", "Paddy", "Rice"],
        "stage_targets": ["vegetative", "flowering", "yield_formation"],
        "hazard_targets": ["irrigation_need", "drought_risk"],
        "content": (
            "Under Alternate Wetting and Drying (AWD), irrigate paddy to 5 cm depth only when the water level "
            "in the perforated field pipe drops to 15 cm below the soil surface during vegetative stage. "
            "CRITICAL EXCEPTION: Maintain continuous ponding of 3-5 cm water during panicle initiation to flowering stages "
            "(45-75 days after transplanting). Water stress at flowering causes severe spikelet sterility and yield loss up to 40%. "
            "If severe moisture depletion occurs below wilting point (soil moisture < 18%), irrigate immediately in the early morning "
            "to prevent thermal shock to roots."
        ),
        "tamil_translation": (
            "மாற்று ஈரமாக்கல் மற்றும் உலர்த்துதல் (AWD) முறையில், பயிர் வளர்ச்சிப் பருவத்தில் களக் குழாயில் நீர் மட்டம் "
            "மண் மட்டத்திலிருந்து 15 செ.மீ கீழே குறையும் போது மட்டும் 5 செ.மீ ஆழத்திற்கு நீர் பாய்ச்சவும். "
            "முக்கிய விதிவிலக்கு: கதிர் உருவாக்கம் மற்றும் பூக்கும் பருவத்தில் (நடவு செய்த 45 முதல் 75 நாட்கள் வரை) வயலில் எப்போதும் "
            "3 முதல் 5 செ.மீ தண்ணீர் தேங்கி இருக்க வேண்டும். பூக்கும் தருணத்தில் ஏற்படும் நீர் பற்றாக்குறை பதர் நெல் உருவாவதற்கு வழிவகுக்கும்."
        )
    },
    {
        "doc_id": "TNAU-CPG-PAD-02",
        "title": "TNAU Agromet Advisory: Heat Stress Mitigation in Rice at Flowering",
        "source": "TNAU Directorate of Extension Education & Agromet Advisory",
        "publication_year": 2024,
        "section": "Crop Weather Advisory - High Temperature Management",
        "page_or_bulletin": "AAS Bulletin No. 38/2024, p. 3",
        "language": "en",
        "crop_targets": ["Paddy (Rice)", "Paddy"],
        "stage_targets": ["flowering"],
        "hazard_targets": ["heat_stress"],
        "content": (
            "When ambient day temperature exceeds 35°C during paddy flowering, anther dehiscence and pollen viability are impaired. "
            "Actionable cultural mitigations: 1. Maintain 5 cm standing water in the field to buffer microclimate temperature by 2-3°C. "
            "2. Foliar spray of 1% potassium chloride (KCl) or 2% DAP at morning hours helps plants tolerate heat stress. "
            "PROHIBITED: Avoid chemical spraying during peak sunlight (11:00 AM to 3:00 PM) as it induces flower burn."
        ),
        "tamil_translation": (
            "பூக்கும் பருவத்தில் பகல் வெப்பநிலை 35°C-க்கு மேல் அதிகரிக்கும் போது, மகரந்தச் சேர்க்கை பாதிக்கப்பட்டு பதர் அதிகரிக்கும். "
            "பரிந்துரைகள்: 1. வயலில் 5 செ.மீ நீர் தேக்கி வைப்பதன் மூலம் நுண் தட்பவெப்பநிலையை 2 முதல் 3°C வரை குறைக்கலாம். "
            "2. காலை வேளையில் 1% பொட்டாசியம் குளோரைடு (KCl) இலைவழியாகத் தெளிப்பது வெப்ப அழுத்தத்தைத் தாங்க உதவும். "
            "தவிர்க்க வேண்டியவை: நண்பகல் 11 மணி முதல் 3 மணி வரை இலைவழி தெளிப்பைத் தவிர்க்கவும்."
        )
    },
    {
        "doc_id": "ICAR-WM-01",
        "title": "ICAR Handbook of Water Management: Drainage & Excess Rain Readiness",
        "source": "Indian Council of Agricultural Research (ICAR), New Delhi",
        "publication_year": 2023,
        "section": "Monsoon Surge & Field Inundation Prevention",
        "page_or_bulletin": "ICAR Monograph Series 8, pp. 112-116",
        "language": "en",
        "crop_targets": ["Paddy (Rice)", "Cotton", "Groundnut", "Millets"],
        "stage_targets": ["sowing", "vegetative", "flowering", "yield_formation", "ripening"],
        "hazard_targets": ["excess_rain_risk"],
        "content": (
            "When heavy rainfall exceeding 50 mm is forecast within 24 to 72 hours, all planned irrigation must be suspended immediately. "
            "Inspect and clear bund drainage outlets and trenches to remove silt and weeds. "
            "For upland and commercial crops like Groundnut and Cotton, prolonged water stagnation (>24 hours) induces root rot and asphyxiation. "
            "Ensure peripheral drainage furrows (30 cm depth) are functional to lead surplus runoff to farm ponds or recharge shafts."
        ),
        "tamil_translation": (
            "அடுத்த 24 முதல் 72 மணி நேரத்திற்குள் 50 மி.மீ-க்கு மேல் கனமழை பெய்ய வாய்ப்புள்ளதாக கணிக்கப்பட்டால், பாசனத்தை உடனடியாக நிறுத்த வேண்டும். "
            "வயல் வரப்பு வடிகால்கள் மற்றும் வாய்க்கால்களில் உள்ள அடைப்புகளை உடனே அகற்றவும். "
            "நிலக்கடலை மற்றும் பருத்தி பயிர்களில் 24 மணி நேரத்திற்கு மேல் நீர் தேங்குவது வேரழுகல் நோய்க்கு வழிவகுக்கும். "
            "வடிகால் வாய்க்கால்கள் வழியாக உபரி நீரை பண்ணைக் குட்டைக்குத் திருப்பி விடவும்."
        )
    },
    {
        "doc_id": "TNAU-CPG-COT-01",
        "title": "TNAU Crop Production Guide: Cotton Moisture & Square Drop Management",
        "source": "Tamil Nadu Agricultural University (TNAU), Coimbatore",
        "publication_year": 2024,
        "section": "Fibre Crops - Drip Fertigation & Abiotic Stress",
        "page_or_bulletin": "Vol. II (Commercial Crops), pp. 74-79",
        "language": "en",
        "crop_targets": ["Cotton"],
        "stage_targets": ["vegetative", "flowering", "yield_formation"],
        "hazard_targets": ["irrigation_need", "heat_stress", "drought_risk"],
        "content": (
            "Cotton is sensitive to both moisture stress and waterlogging during square and boll development. "
            "Adopt alternate furrow irrigation or drip irrigation at 0.8 IW/CPE ratio to save 35% water. "
            "During flowering, soil moisture must remain within 60-70% of field capacity. If high temperature exceeds 38°C, "
            "apply 0.5% zinc sulphate + 1% urea foliar spray to arrest square shedding. Do not over-irrigate as it leads to vegetative rank growth."
        ),
        "tamil_translation": (
            "பருத்தி பயிரில் பூ மொட்டு மற்றும் காய் பிடிக்கும் பருவத்தில் அதிக நீர் தேங்குதலும், நீர் பற்றாக்குறையும் காய்கள் உதிர்வதற்கு காரணமாகும். "
            "சொட்டு நீர்ப்பாசனம் மூலம் 0.8 விகிதத்தில் நீர் பாய்ச்சுவது 35% நீரைச் சேமிக்கும். "
            "பூக்கும் பருவத்தில் வெப்பநிலை 38°C-ஐத் தாண்டினால், 0.5% துத்தநாக சல்பேட் தெளிப்பது மொட்டுகள் உதிர்வதைத் தடுக்கும்."
        )
    },
    {
        "doc_id": "IMD-AAS-ERD-01",
        "title": "IMD District Agromet Advisory: Western Agro-Climatic Zone (Erode/Coimbatore)",
        "source": "India Meteorological Department (IMD) Agromet Advisory Unit",
        "publication_year": 2024,
        "section": "Seasonal Soil Moisture & Weather Warnings",
        "page_or_bulletin": "Weekly Bulletin No. 72, p. 2",
        "language": "en",
        "crop_targets": ["Paddy (Rice)", "Millets", "Groundnut", "Cotton"],
        "stage_targets": ["sowing", "vegetative", "flowering", "yield_formation"],
        "hazard_targets": ["sensor_anomaly", "drought_risk", "heat_stress"],
        "content": (
            "Dry weather prevailing with high solar radiation and gusty westerly winds (15-20 km/h) accelerates soil moisture depletion. "
            "Farmers are advised to practice mulching with coir pith or crop residues to conserve root-zone moisture. "
            "Check field moisture sensors regularly for root-soil contact. Clean sensor probes if sudden erratic shifts are recorded."
        ),
        "tamil_translation": (
            "வறண்ட வானிலையுடன் வீசும் மேற்கத்திய காற்று காரணமாக மண் ஈரப்பதம் வேகமாக குறையும் வாய்ப்புள்ளது. "
            "தென்னை நார்க்கழிவு அல்லது பயிர்க்கழிவுகளைக் கொண்டு மூடாக்கு அமைத்து வேர்ப்பகுதி ஈரப்பதத்தைப் பாதுகாக்கவும். "
            "மண் ஈரப்பத உணரி முனைகளில் தூசி படியாமல் சுத்தமாகப் பராமரிக்கவும்."
        )
    }
]


def get_all_knowledge_documents() -> List[Dict[str, Any]]:
    """Returns all knowledge base documents with calculated SHA-256 hashes."""
    docs = []
    for doc in RAW_KNOWLEDGE_DOCUMENTS:
        full_text = doc["title"] + " " + doc["content"]
        h = compute_sha256(full_text)
        docs.append({
            **doc,
            "document_hash_sha256": h
        })
    return docs
