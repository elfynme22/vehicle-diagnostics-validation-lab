from copy import deepcopy
import pytest
from vehicle_diagnostics.simulator import get_scenario
from vehicle_diagnostics.validation import validate_sample, InvalidSampleError

def test_good_data():
    assert validate_sample(get_scenario("normal")) is True

def test_unavailable_sensor():
    assert validate_sample(get_scenario("missing_sensor")) is False

@pytest.mark.parametrize("bad", ["abc", True, float("nan"), float("inf"), -1])
def test_bad_voltages(bad):
    sample = get_scenario("normal")
    sample["battery_voltage"] = bad
    with pytest.raises(InvalidSampleError):
        validate_sample(sample)

def test_missing_key():
    sample = get_scenario("normal")
    del sample["scenario"]
    with pytest.raises(InvalidSampleError, match="Missing fields"):
        validate_sample(sample)

def test_bool_field_invalid():
    sample = get_scenario("normal")
    sample["sensor_available"] = "yes"
    with pytest.raises(InvalidSampleError):
        validate_sample(sample)
