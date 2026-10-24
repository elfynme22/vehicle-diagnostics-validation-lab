# Intelligent Vehicle Diagnostics & Automated Regression Testing

**Status:** Implemented educational demo (not production automotive software)  
**Focus:** Python • synthetic diagnostics • automated pytest regression tests • Streamlit dashboard • GitHub Actions • optional anomaly detection  
**Disclaimer:** Independent educational project. Not affiliated with Tesla or any manufacturer. **No real vehicle data or connections.** All thresholds are invented.

## What you will see

- Choose one of four fixed scenarios: `normal`, `low_voltage`, `high_temperature`, `missing_sensor`.
- Get a deterministic diagnostic status and human-readable alerts.
- Run automated **unit, boundary, invalid-input, CSV-data and regression** tests.
- Review **actual** pytest results in Streamlit, plus example sensor charts.
- Verify tests automatically on GitHub push or pull request.
- Optionally execute a separate toy IsolationForest experiment on simulated data.

## 1. Quick start — Windows 11 + VS Code

Open this folder in VS Code and choose **Terminal → New Terminal** (PowerShell):

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[all]"
```

If PowerShell blocks activation, use `.\.venv\Scripts\python.exe` instead of `python` in each command. The package install may need an internet connection to download libraries. In VS Code, select the interpreter inside `.venv`.

**Try the CLI:**

```powershell
vehicle-diagnostics --scenario normal
vehicle-diagnostics --scenario low_voltage
vehicle-diagnostics --scenario high_temperature
vehicle-diagnostics --scenario missing_sensor
```

**Run tests and generate a REAL report:**

```powershell
New-Item -ItemType Directory -Force reports
python -m pytest -v --junitxml=reports/junit.xml
```

**Launch the dashboard:**

```powershell
python -m streamlit run dashboard/app.py
```

Then open the local URL printed by Streamlit (usually `http://localhost:8501`). Under **Real Test Results**, the dashboard reads `reports/junit.xml`; it never makes up a test run.

**Optional synthetic ML demo:**

```powershell
python ml/anomaly_detection.py
```

For a quick lightweight test-only install: `python -m pip install -e ".[test]"` (dashboard and ML libraries will not be installed).

## 2. Project flow

`Fixed synthetic sample → Input validation → Rule-based diagnostics → CLI/Streamlit`  
`pytest → JUnit XML → Streamlit test metrics`  
`GitHub push/PR → GitHub Actions → pytest`  
`Optional: Separate synthetic dataset → IsolationForest → precision/recall`.

## 3. Demo specification

| Sample | Battery voltage | Temperature | Expected |
|---|---:|---:|---|
| normal | 12.0 V | 30 °C | OK |
| low_voltage | 10.5 V | 30 °C | LOW_VOLTAGE |
| high_temperature | 12.0 V | 65 °C | HIGH_TEMPERATURE |
| missing_sensor | unavailable | 30 °C | INVALID_DATA |

Invented boundaries: voltage strictly **below** 11.0 V triggers low-voltage; temperature strictly **above** 60.0 °C triggers high-temperature. For simultaneous warnings, the function returns two alerts. Malformed data raises a documented exception. See [decisions](docs/decisions.md).

## 4. Structure

```text
src/vehicle_diagnostics/  simulator.py, validation.py, diagnostics.py, reporting.py, cli.py
tests/                    automated test suite
data/                     labeled simulated CSV examples
dashboard/app.py          Streamlit scenario + real test reports + charts
ml/anomaly_detection.py   OPTIONAL synthetic IsolationForest demonstration
docs/                     decisions, test plan, personal learning log
.github/workflows/        pytest on push and pull request
pyproject.toml            packaging, dependencies, CLI entry point
```

## 5. Regression testing demonstration (important)

1. First run all tests and see PASS.
2. In `src/vehicle_diagnostics/diagnostics.py`, intentionally change `voltage < LOW_VOLTAGE_LIMIT` into `voltage <= LOW_VOLTAGE_LIMIT`.
3. Rerun pytest. The boundary value **11.0** should now FAIL because it was specified as OK.
4. Restore `<` and rerun tests. They should pass again.

This is what **regression testing** means: repeat prior checks after changes to catch broken behavior. It is **not** machine-learning regression. Never leave the intentionally broken version committed.

## 6. What you learn

- Python packaging, CLI design, reusable modules, input validation
- Unit tests, test parametrization, boundary values, invalid inputs, expectations vs actuals
- Regression testing, root-cause analysis, test plans and traceability
- Presenting genuine test reports in a UI, and running tests on CI
- Optional: distinguishing a data-driven anomaly score from a deterministic diagnostic rule

## 7. Scope and limitations

- Fixed synthetic data; thresholds invented for demonstrating code paths.
- **No CAN, OBD, Tesla Service Mode integration, manufacturer rules, or real vehicle control.**
- Passing tests establish only the specified synthetic program behavior, not operational safety.
- ML evaluation on generated data is an educational illustration, not evidence of real diagnostic accuracy.
- No real sensor time-series history; dashboard displays scenario samples, not live trends.
- CI runs the core test suite; Streamlit and ML are optional local extras.

## 8. Interview/demo story

> “I built a reproducible synthetic vehicle diagnostics application and tested its rules with pytest. I covered threshold boundaries and invalid sensor data, then demonstrated regression detection by introducing and fixing a comparison-operator bug. The dashboard uses real JUnit test reports, and GitHub Actions reruns tests automatically.”

Understand and run the project yourself before claiming any implementation or testing experience.

## 9. Additional notes

- Detailed [test plan](docs/test-plan.md)
- [Engineering decisions](docs/decisions.md)
- [Learning log template](docs/learning-log.md)
- Official references: [pytest](https://docs.pytest.org/en/stable/), [Streamlit](https://docs.streamlit.io/), [GitHub Actions](https://docs.github.com/en/actions)
