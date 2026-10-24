from copy import deepcopy
import pytest
from vehicle_diagnostics.simulator import get_scenario
from vehicle_diagnostics.diagnostics import diagnose, diagnose_voltage
from vehicle_diagnostics.validation import InvalidSampleError

@pytest.mark.parametrize("scenario,expected", [
    ("normal", ["OK"]), ("low_voltage", ["LOW_VOLTAGE"]),
    ("high_temperature", ["HIGH_TEMPERATURE"]), ("missing_sensor", ["INVALID_DATA"]),
])
def test_four_scenarios(scenario, expected):
    assert diagnose(get_scenario(scenario))["alerts"] == expected

@pytest.mark.parametrize("voltage,expected", [(10.99,"LOW_VOLTAGE"),(11.0,"OK"),(11.01,"OK")])
def test_voltage_boundary(voltage,expected):
    assert diagnose_voltage(voltage) == expected

@pytest.mark.parametrize("temperature,expected", [(59.99,["OK"]),(60.0,["OK"]),(60.01,["HIGH_TEMPERATURE"])])
def test_temperature_boundary(temperature,expected):
    sample = get_scenario("normal")
    sample["battery_temperature"] = temperature
    assert diagnose(sample)["alerts"] == expected

def test_two_alerts():
    sample = get_scenario("normal")
    sample.update(battery_voltage=10.5, battery_temperature=65)
    assert diagnose(sample)["alerts"] == ["LOW_VOLTAGE", "HIGH_TEMPERATURE"]

def test_missing_reading():
    sample = get_scenario("normal")
    sample["battery_voltage"] = None
    assert diagnose(sample)["alerts"] == ["INVALID_DATA"]

def test_bad_type_rejected():
    sample = get_scenario("normal")
    sample["battery_voltage"] = "abc"
    with pytest.raises(InvalidSampleError):
        diagnose(sample)

def test_unavailable_sensor_stays_invalid():
    assert diagnose(get_scenario("missing_sensor"))["status"] == "INVALID_DATA"
