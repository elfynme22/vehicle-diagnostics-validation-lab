"""Input validation is intentionally separate from the diagnostic rules."""
import math

REQUIRED = ("sample_id", "scenario", "battery_voltage", "battery_temperature", "sensor_available")

class InvalidSampleError(ValueError):
    """Unexpected or malformed input; not a real-vehicle diagnostic code."""


def validate_sample(sample: dict) -> bool:
    if not isinstance(sample, dict):
        raise InvalidSampleError("Sample must be a dictionary")
    missing = [field for field in REQUIRED if field not in sample]
    if missing:
        raise InvalidSampleError(f"Missing fields: {', '.join(missing)}")
    for field in ("sample_id", "scenario"):
        if not isinstance(sample[field], str) or not sample[field].strip():
            raise InvalidSampleError(f"{field} must be nonempty text")
    if type(sample["sensor_available"]) is not bool:
        raise InvalidSampleError("sensor_available must be a boolean")
    if not sample["sensor_available"]:
        return False
    for field in ("battery_voltage", "battery_temperature"):
        value = sample[field]
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            raise InvalidSampleError(f"{field} must be a finite number")
    if sample["battery_voltage"] < 0:
        raise InvalidSampleError("battery_voltage cannot be negative")
    # This demo imposes no physical upper/temperature limits beyond finite-number checking.
    return True
