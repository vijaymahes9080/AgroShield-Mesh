"""
AgroShield Mesh - 100 Scenario Benchmark Evaluation Runner
Measures:
- Agreement with expert labels (Target: >= 80% irrigation agreement, >= 75% risk classification)
- False-alert rate on high severity (Target: < 15%)
- Citation coverage (Target: >= 90%)
- Advisory latency (Target: < 30s)
- Missing data detection rate
Outputs results to benchmarks/benchmark_results.json.
"""

import os
import sys
import json
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from benchmarks.scenarios import generate_100_benchmark_scenarios
from agents.risk_engine import AgronomicRiskEngine
from agents.workflow import BoundedAgentWorkflow
from backend.app.schemas.domain import LanguagePreference, RiskLevel


def run_benchmarks() -> dict:
    scenarios = generate_100_benchmark_scenarios()
    workflow = BoundedAgentWorkflow(use_sentence_transformers=False)

    print("=" * 70)
    print(f"🚀 RUNNING AGROSHIELD MESH BENCHMARK SUITE ({len(scenarios)} SCENARIOS)")
    print("=" * 70)

    total_scenarios = len(scenarios)
    irrigation_matches = 0
    risk_matches = 0
    false_high_alerts = 0
    total_normal_scenarios = 0
    citation_present_count = 0
    latencies = []
    category_metrics = {}

    start_suite_time = time.time()

    for idx, sc in enumerate(scenarios, 1):
        sc_id = sc["id"]
        cat = sc["category"]
        if cat not in category_metrics:
            category_metrics[cat] = {"total": 0, "risk_correct": 0, "irrigation_correct": 0}

        category_metrics[cat]["total"] += 1

        # Prepare telemetry
        sensor_list = sc.get("sensor_history", [sc.get("sensor", {})])
        weather = sc.get("weather")
        sat = sc.get("satellite")
        crop = {"crop_name": sc.get("crop_name"), "current_stage": sc.get("crop_stage")}
        lang = LanguagePreference.TA if sc.get("language") == "ta" else LanguagePreference.EN

        t0 = time.time()
        state = workflow.run(
            field_id=sc["field_id"],
            crop_cycle=crop,
            sensor_readings=sensor_list,
            weather_observation=weather,
            satellite_observation=sat,
            language=lang
        )
        elapsed_sec = time.time() - t0
        latencies.append(elapsed_sec)

        risk = state.risk_assessment
        advisory = state.final_advisory

        # 1. Irrigation urgency comparison
        irr_score = risk.factor_breakdown.irrigation_need_score
        pred_irr = "HIGH" if irr_score > 60 else "MODERATE" if irr_score > 30 else "LOW"
        if "expected_irrigation_urgency" in sc:
            exp_irr = sc["expected_irrigation_urgency"]
            if exp_irr == "UNCERTAIN_ANOMALY":
                # For anomalous sensors, detecting the anomaly counts as agreement
                if risk.factor_breakdown.sensor_anomaly_score >= 35.0:
                    irrigation_matches += 1
                    category_metrics[cat]["irrigation_correct"] += 1
            elif pred_irr == exp_irr:
                irrigation_matches += 1
                category_metrics[cat]["irrigation_correct"] += 1

        # 2. Risk level classification
        pred_risk = risk.overall_risk_level.value
        exp_risk = sc.get("expected_risk_level", "low")
        if pred_risk == exp_risk:
            risk_matches += 1
            category_metrics[cat]["risk_correct"] += 1

        # 3. False alert calculation (when ground truth is low risk, did we trigger high/critical?)
        if exp_risk == "low":
            total_normal_scenarios += 1
            if pred_risk in ["high", "critical"]:
                false_high_alerts += 1

        # 4. Citation coverage
        if advisory and len(advisory.source_citations) > 0:
            citation_present_count += 1

    total_time = time.time() - start_suite_time

    # Calculate percentages
    irrigation_agreement_pct = round((irrigation_matches / total_scenarios) * 100.0, 2)
    risk_classification_accuracy_pct = round((risk_matches / total_scenarios) * 100.0, 2)
    citation_coverage_pct = round((citation_present_count / total_scenarios) * 100.0, 2)
    false_alert_rate_pct = round((false_high_alerts / max(1, total_normal_scenarios)) * 100.0, 2)
    avg_latency_sec = round(sum(latencies) / len(latencies), 3)
    max_latency_sec = round(max(latencies), 3)

    results = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "total_scenarios_evaluated": total_scenarios,
        "execution_duration_seconds": round(total_time, 2),
        "metrics": {
            "irrigation_agreement_pct": irrigation_agreement_pct,
            "irrigation_target_pct": 80.0,
            "irrigation_target_met": irrigation_agreement_pct >= 80.0,
            "risk_classification_accuracy_pct": risk_classification_accuracy_pct,
            "risk_target_pct": 75.0,
            "risk_target_met": risk_classification_accuracy_pct >= 75.0,
            "citation_coverage_pct": citation_coverage_pct,
            "citation_target_pct": 90.0,
            "citation_target_met": citation_coverage_pct >= 90.0,
            "false_alert_rate_pct": false_alert_rate_pct,
            "false_alert_target_max_pct": 15.0,
            "false_alert_target_met": false_alert_rate_pct < 15.0,
            "avg_advisory_latency_seconds": avg_latency_sec,
            "max_advisory_latency_seconds": max_latency_sec,
            "latency_target_max_seconds": 30.0,
            "latency_target_met": max_latency_sec < 30.0
        },
        "category_breakdown": category_metrics
    }

    print("\n" + "=" * 70)
    print("📊 BENCHMARK EVALUATION RESULTS SUMMARY")
    print("=" * 70)
    print(f"✅ Irrigation Urgency Agreement: {irrigation_agreement_pct}% (Target: >=80%) -> {'PASS' if results['metrics']['irrigation_target_met'] else 'FAIL'}")
    print(f"✅ Risk Classification Accuracy: {risk_classification_accuracy_pct}% (Target: >=75%) -> {'PASS' if results['metrics']['risk_target_met'] else 'FAIL'}")
    print(f"✅ Citation Coverage Rate:     {citation_coverage_pct}% (Target: >=90%) -> {'PASS' if results['metrics']['citation_target_met'] else 'FAIL'}")
    print(f"✅ False High-Alert Rate:      {false_alert_rate_pct}% (Target: <15%) -> {'PASS' if results['metrics']['false_alert_target_met'] else 'FAIL'}")
    print(f"✅ Max Advisory Latency:       {max_latency_sec}s (Target: <30s) -> {'PASS' if results['metrics']['latency_target_met'] else 'FAIL'}")
    print(f"⚡ Total Benchmark Run Time:   {round(total_time, 2)} seconds")
    print("=" * 70)

    out_path = os.path.join(os.path.dirname(__file__), "benchmark_results.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"Saved benchmark results artifact to: {out_path}")

    return results


if __name__ == "__main__":
    run_benchmarks()
