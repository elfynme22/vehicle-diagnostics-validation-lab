import csv
from pathlib import Path
import pytest
from vehicle_diagnostics.diagnostics import diagnose

DATA = Path(__file__).resolve().parents[1] / "data" / "sample_scenarios.csv"
with DATA.open(newline="", encoding="utf-8") as f:
    CASES = list(csv.DictReader(f))

@pytest.mark.parametrize("case", CASES, ids=[c["sample_id"] for c in CASES])
def test_csv_cases(case):
    sample = {
        "sample_id": case["sample_id"], "scenario": case["scenario"],
        "battery_voltage": float(case["battery_voltage"]) if case["battery_voltage"] else None,
        "battery_temperature": float(case["battery_temperature"]) if case["battery_temperature"] else None,
        "sensor_available": case["sensor_available"].lower() == "true",
    }
    actual = diagnose(sample)
    assert actual["status"] == case["expected_status"]
    assert actual["alerts"] == case["expected_alerts"].split("|")
