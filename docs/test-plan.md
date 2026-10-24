# Validation plan

| Requirement | Expected behavior | Corresponding tests |
|---|---|---|
| R-01 | Valid normal case -> OK | `test_four_scenarios`, `test_csv_cases` |
| R-02 | Voltage < 11.0 -> LOW_VOLTAGE | `test_voltage_boundary`, `test_csv_cases` |
| R-03 | Temperature > 60.0 -> HIGH_TEMPERATURE | `test_temperature_boundary`, `test_csv_cases` |
| R-04 | Sensor unavailable / missing reading -> INVALID_DATA | `test_missing_reading`, `test_unavailable_sensor_stays_invalid` |
| R-05 | Exactly 11.0 -> OK | `test_voltage_boundary` |
| R-06 | Exactly 60.0 -> OK | `test_temperature_boundary` |
| R-07 | Malformed numeric input rejected | `test_bad_type_rejected`, `test_bad_voltages` |
| R-08 | Simultaneous faults -> both alerts | `test_two_alerts` |
| R-09 | Real JUnit report parsed; missing report is not PASS | `test_real_xml_format`, `test_missing_report` |

## Regression demonstration

1. Run `python -m pytest -v` and confirm tests pass.
2. Temporarily change `< LOW_VOLTAGE_LIMIT` to `<= LOW_VOLTAGE_LIMIT` in `diagnostics.py`.
3. Run `python -m pytest -v`; the 11.0 boundary tests **should fail**.
4. Revert the change and rerun; all tests should pass.
5. Document the failing test, expected/actual value, underlying cause, fix and retest.

A passing test suite is not certification of automotive safety. No hardware integration or real-vehicle coverage is provided.
