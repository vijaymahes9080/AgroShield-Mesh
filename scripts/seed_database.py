"""
AgroShield Mesh - Database Seeder
Seeds realistic agricultural demo data:
- Farmers in Erode district, Tamil Nadu
- GeoJSON Fields (Paddy, Cotton, Ragi)
- Active Crop Cycles
- Time-series IoT mesh sensor readings
- IMD Agromet weather observations
- Sentinel-2 satellite NDVI observations
- Baseline risk assessments and advisories with citations
"""

import os
import sys
import json
from datetime import datetime, timezone, timedelta
from uuid import uuid4

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.db.session import SessionLocal
from backend.app.db import init_db
from backend.app.db.models import (
    UserModel, FarmerModel, FieldModel, CropCycleModel,
    SensorReadingModel, WeatherObservationModel, SatelliteObservationModel,
    RiskAssessmentModel, AdvisoryModel, AdvisoryFeedbackModel, AuditEventModel
)
from backend.app.core.security import get_password_hash, compute_sha256_hash


def seed_database():
    print("=" * 65)
    print("🌱 SEEDING AGROSHIELD MESH PRODUCTION DATABASE")
    print("=" * 65)

    init_db()
    db = SessionLocal()

    try:
        # Clear existing demo records
        db.query(AdvisoryFeedbackModel).delete()
        db.query(AdvisoryModel).delete()
        db.query(RiskAssessmentModel).delete()
        db.query(SatelliteObservationModel).delete()
        db.query(WeatherObservationModel).delete()
        db.query(SensorReadingModel).delete()
        db.query(CropCycleModel).delete()
        db.query(FieldModel).delete()
        db.query(FarmerModel).delete()
        db.query(UserModel).delete()
        db.commit()

        # 1. Users
        user_farmer = UserModel(
            id="user-farmer-01",
            username="vijay_farmer",
            email="Vijaypradhap2004@gmail.com",
            hashed_password=get_password_hash("Farmer@12345"),
            role="farmer"
        )
        user_expert = UserModel(
            id="user-expert-01",
            username="dr_raman_tnau",
            email="raman.agri@tnau.ac.in",
            hashed_password=get_password_hash("Expert@12345"),
            role="agronomist_expert"
        )
        db.add_all([user_farmer, user_expert])
        db.commit()

        # 2. Farmers
        farmer1 = FarmerModel(
            id="farmer-erode-01",
            user_id="user-farmer-01",
            name="Vijay Mahes",
            phone="+91 98765 43210",
            email="Vijaypradhap2004@gmail.com",
            village="Perundurai",
            taluk="Perundurai",
            district="Erode",
            state="Tamil Nadu",
            language_preference="ta",
            consent_data_sharing=True,
            consent_satellite_indexing=True
        )
        farmer2 = FarmerModel(
            id="farmer-erode-02",
            name="R. Murugesan",
            phone="+91 94432 11098",
            email="murugesan.farm@gmail.com",
            village="Bhavani",
            taluk="Bhavani",
            district="Erode",
            state="Tamil Nadu",
            language_preference="ta",
            consent_data_sharing=True,
            consent_satellite_indexing=True
        )
        db.add_all([farmer1, farmer2])
        db.commit()

        # 3. Fields
        geojson_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sample_data", "sample_fields.geojson")
        with open(geojson_path, "r", encoding="utf-8") as f:
            fields_geojson = json.load(f)

        f_models = []
        for feat in fields_geojson["features"]:
            p = feat["properties"]
            f_model = FieldModel(
                id=feat["id"],
                farmer_id="farmer-erode-01" if "Perundurai" in p["name"] else "farmer-erode-02",
                name=p["name"],
                boundary_geojson=feat["geometry"],
                area_hectares=p["area_hectares"],
                soil_type=p["soil_type"],
                irrigation_source=p["irrigation_source"],
                elevation_meters=245.0,
                srid=4326
            )
            f_models.append(f_model)
            db.add(f_model)
        db.commit()

        # 4. Crop Cycles
        now = datetime.now(timezone.utc)
        cycle1 = CropCycleModel(
            id="cycle-paddy-01",
            field_id="field-perundurai-01",
            crop_name="Paddy (Rice)",
            variety="CO 51",
            season="Samba",
            sowing_date=now - timedelta(days=55),
            expected_harvest_date=now + timedelta(days=65),
            current_stage="flowering",
            expected_yield_tonnes_per_ha=6.5,
            active_status=True
        )
        cycle2 = CropCycleModel(
            id="cycle-cotton-01",
            field_id="field-bhavani-02",
            crop_name="Cotton",
            variety="MCU 5",
            season="Kharif",
            sowing_date=now - timedelta(days=40),
            expected_harvest_date=now + timedelta(days=90),
            current_stage="vegetative",
            expected_yield_tonnes_per_ha=2.8,
            active_status=True
        )
        db.add_all([cycle1, cycle2])
        db.commit()

        # 5. Sensor Readings (Time-series for last 24h)
        for h in range(12, 0, -1):
            ts = now - timedelta(hours=h * 2)
            # Simulated realistic diurnal curve
            temp = 27.0 + (5.0 if 4 <= h <= 8 else 1.0)
            moist = 22.0 - (h * 0.4)
            db.add(SensorReadingModel(
                id=f"sensor-read-{h}",
                field_id="field-perundurai-01",
                device_id="AGRO-NODE-ERD-004",
                timestamp=ts,
                soil_moisture_pct=round(moist, 1),
                soil_temperature_c=round(temp - 2.0, 1),
                ambient_temperature_c=round(temp, 1),
                ambient_humidity_pct=round(68.0 - (temp - 27.0) * 2, 1),
                battery_pct=94.0,
                is_valid=True,
                anomaly_flag=False,
                data_source="observed"
            ))
        db.commit()

        # 6. Weather Observation
        db.add(WeatherObservationModel(
            id="weather-obs-01",
            field_id="field-perundurai-01",
            grid_location={"lat": 11.2735, "lon": 77.5828},
            timestamp=now,
            source="IMD_AWS_ERODE",
            temperature_c=36.5,
            relative_humidity_pct=64.0,
            rainfall_mm_last_24h=0.0,
            wind_speed_kmh=14.0,
            forecast_rain_next_24h_mm=0.0,
            forecast_rain_next_72h_mm=12.0,
            et0_evapotranspiration_mm=5.4,
            data_source="observed"
        ))
        db.commit()

        # 7. Satellite Observation
        db.add(SatelliteObservationModel(
            id="sat-obs-01",
            field_id="field-perundurai-01",
            observation_date=now - timedelta(days=2),
            satellite_mission="Sentinel-2B",
            cloud_cover_pct=8.5,
            ndvi_mean=0.68,
            ndvi_min=0.52,
            ndvi_max=0.81,
            ndwi_mean=0.34,
            resolution_meters=10.0,
            data_source="observed"
        ))
        db.commit()

        # 8. Sample Advisory & Feedback
        adv1 = AdvisoryModel(
            id="advisory-demo-01",
            field_id="field-perundurai-01",
            language="ta",
            title="அக்ரோஷீல்டு பயிர் ஆலோசனை - நெல் (பூக்கும் பருவம்)",
            summary="மண் ஈரப்பதம் 17.2% ஆகக் குறைந்துள்ளது. பூக்கும் பருவத்தில் நெற்பயிருக்கு நீர் பற்றாக்குறை ஏற்படாமல் காக்க காலை வேளையில் நீர் பாய்ச்சவும்.",
            action_items=[
                "பூக்கும் பருவத்தில் கதிர் நன்கு பால் பிடிக்க வயலில் 3-5 செ.மீ நீர் தேங்குமாறு பாசனம் செய்யவும்.",
                "நண்பகல் வேளையில் ஏற்படும் அதிக வெப்பத்தைத் தணிக்க மெல்லிய நீர் படலத்தைப் பராமரிக்கவும்.",
                "இலைவழி உர தெளிப்பை காலை 8 முதல் 10 மணிக்குள் முடிக்கவும்."
            ],
            prohibited_actions=[
                "நண்பகல் 11 மணி முதல் 3 மணி வரை தெளிப்பு மேற்கொள்வதைத் தவிர்க்கவும்.",
                "அனுமதிக்கப்படாத பூச்சிக்கொல்லிகளை முன்னெச்சரிக்கையின்றி தெளிக்க வேண்டாம்."
            ],
            source_citations=[
                {
                    "source_title": "TNAU Crop Production Guide: Wet Season Rice (Paddy) Water Management",
                    "author_organization": "Tamil Nadu Agricultural University (TNAU)",
                    "publication_year": 2024,
                    "document_section": "Irrigation Management - Alternate Wetting and Drying (AWD)",
                    "page_or_bulletin_no": "Bulletin No. 14, pp. 48-52",
                    "document_hash_sha256": compute_sha256_hash("TNAU Paddy AWD Guidance 2024")
                }
            ],
            confidence_level=0.92,
            requires_human_review=True,
            review_status="expert_approved",
            reviewed_by="Dr. M. Raman, Senior Agronomist (TNAU)",
            review_notes="Verified against localized IMD heat index bulletin and crop phenological stage. Approved for dispatch.",
            disclaimer="AGRONOMIC NOTICE: This guidance is evidence-grounded decision support based on university guidelines.",
            data_sources_used=["observed", "model_generated"],
            generated_at=now - timedelta(hours=3),
            reviewed_at=now - timedelta(hours=2)
        )
        db.add(adv1)
        db.commit()

        # Feedback
        fb1 = AdvisoryFeedbackModel(
            id="feedback-demo-01",
            advisory_id="advisory-demo-01",
            farmer_id="farmer-erode-01",
            rating=5,
            helpful_flag=True,
            actual_action_taken="அதிகாலை 6 மணிக்கு 3 செ.மீ நீர் பாய்ச்சினேன். கதிர் முதிர்தல் சீராக உள்ளது.",
            unnecessary_irrigation_prevented_litres=12000.0,
            comments="வெப்ப அழுத்தத்திலிருந்து பயிர் காப்பாற்றப்பட்டது. மிகுந்த பயனுள்ள வழிகாட்டல்.",
            recorded_at=now - timedelta(hours=1)
        )
        db.add(fb1)

        # Audit Event
        audit_event = AuditEventModel(
            id=str(uuid4()),
            event_type="DATABASE_SEEDED",
            entity_name="Database",
            entity_id="all",
            actor_id="system_seeder",
            actor_role="admin",
            action="SEED_DEMO_DATA",
            ip_address="127.0.0.1",
            request_id=str(uuid4()),
            payload_hash=compute_sha256_hash("seed_database_execution"),
            timestamp=now
        )
        db.add(audit_event)
        db.commit()

        print(f"✅ Successfully seeded {len(f_models)} fields, 2 farmers, sensors, weather, satellite, and advisories!")
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
