"""Repeatable synthetic vehicle data. All thresholds are invented for education."""
from copy import deepcopy

SCENARIOS = {
    "normal": {"sample_id": "S-001", "scenario": "normal", "battery_voltage": 12.0, "battery_temperature": 30.0, "sensor_available": True},
    "low_voltage": {"sample_id": "S-002", "scenario": "low_voltage", "battery_voltage": 10.5, "battery_temperature": 30.0, "sensor_available": True},
    "high_temperature": {"sample_id": "S-003", "scenario": "high_temperature", "battery_voltage": 12.0, "battery_temperature": 65.0, "sensor_available": True},
    "missing_sensor": {"sample_id": "S-004", "scenario": "missing_sensor", "battery_voltage": None, "battery_temperature": 30.0, "sensor_available": False},
}

def get_scenario(name: str) -> dict:
    if name not in SCENARIOS:
        raise ValueError(f"Unknown scenario: {name!r}. Options: {', '.join(SCENARIOS)}")
    return deepcopy(SCENARIOS[name])

def scenario_names() -> list[str]:
    return list(SCENARIOS)
