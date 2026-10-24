"""Deterministic rules with SYNTHETIC thresholds (not manufacturer specifications)."""
from .validation import InvalidSampleError, validate_sample

LOW_VOLTAGE_LIMIT = 11.0  # synthetic, not real-world guidance
HIGH_TEMPERATURE_LIMIT = 60.0  # synthetic, not real-world guidance


def diagnose_voltage(voltage: float) -> str:
    if isinstance(voltage, bool) or not isinstance(voltage, (int, float)):
        raise InvalidSampleError("voltage must be numeric")
    import math
    if not math.isfinite(voltage) or voltage < 0:
        raise InvalidSampleError("voltage must be finite and nonnegative")
    return "LOW_VOLTAGE" if voltage < LOW_VOLTAGE_LIMIT else "OK"


def diagnose(sample: dict) -> dict:
    """Return ALL alerts in stable order; invalid/unavailable sensors are INVALID_DATA.

    Malformed input raises InvalidSampleError; unavailable or missing measurements
    return INVALID_DATA. This is a documented choice for v1.
    """
    if not isinstance(sample, dict):
        raise InvalidSampleError("Sample must be a dictionary")
    # A physically unavailable sensor is distinct from a malformed record.
    if sample.get("sensor_available") is False:
        # Still validate complete record keys/types to avoid silently accepting nonsense.
        validate_sample(sample)
        return {"sample_id": sample["sample_id"], "status": "INVALID_DATA", "alerts": ["INVALID_DATA"]}
    for field in ("battery_voltage", "battery_temperature"):
        if field in sample and sample[field] is None:
            # Missing reading is a diagnostic input problem, rather than OK.
            required_except = dict(sample)
            required_except["sensor_available"] = False
            validate_sample(required_except)
            return {"sample_id": sample["sample_id"], "status": "INVALID_DATA", "alerts": ["INVALID_DATA"]}
    if not validate_sample(sample):
        return {"sample_id": sample["sample_id"], "status": "INVALID_DATA", "alerts": ["INVALID_DATA"]}
    alerts = []
    if sample["battery_voltage"] < LOW_VOLTAGE_LIMIT:
        alerts.append("LOW_VOLTAGE")
    if sample["battery_temperature"] > HIGH_TEMPERATURE_LIMIT:
        alerts.append("HIGH_TEMPERATURE")
    return {"sample_id": sample["sample_id"], "status": "OK" if not alerts else "WARNING", "alerts": alerts or ["OK"]}
