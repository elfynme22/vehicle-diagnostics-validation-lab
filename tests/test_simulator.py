import pytest
from vehicle_diagnostics.simulator import get_scenario, scenario_names

def test_four_scenarios():
    assert set(scenario_names()) == {"normal", "low_voltage", "high_temperature", "missing_sensor"}

@pytest.mark.parametrize("name", scenario_names())
def test_repeatable_data(name):
    assert get_scenario(name) == get_scenario(name)

def test_result_is_independent_copy():
    first = get_scenario("normal")
    first["battery_voltage"] = -99
    assert get_scenario("normal")["battery_voltage"] == 12

def test_unknown_scenario():
    with pytest.raises(ValueError, match="Unknown scenario"):
        get_scenario("broken")
