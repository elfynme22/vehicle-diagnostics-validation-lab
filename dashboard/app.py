
"""Vehicle Diagnostics & Validation Lab — Streamlit dashboard."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import pandas as pd
import plotly.express as px
import streamlit as st

from vehicle_diagnostics.simulator import get_scenario, scenario_names
from vehicle_diagnostics.diagnostics import diagnose
from vehicle_diagnostics.reporting import read_junit


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Vehicle Diagnostics & Validation Lab",
    page_icon="🚗",
    layout="wide",
)

st.title("🚗 Vehicle Diagnostics & Validation Lab")

st.markdown(
    "### Automated Diagnostic Validation & Regression Testing"
)

st.write(
    "An educational Python project exploring software validation, "
    "automated testing, boundary conditions, and regression detection "
    "through simulated vehicle diagnostics."
)


# --------------------------------------------------
# VALIDATION OVERVIEW
# --------------------------------------------------

report_path = ROOT / "reports" / "junit.xml"

try:
    summary = read_junit(report_path)

    a, b, c = st.columns(3)

    a.metric(
        "Automated Tests Passed",
        f'{summary["passed"]}/{summary["tests"]}',
    )

    b.metric(
        "Regression Demonstration",
        "Detected & Fixed",
    )

    c.metric(
        "GitHub Actions",
        "CI Configured",
    )

    st.caption(
        "Test counts are read from a saved pytest JUnit report. "
        "They do not represent a live test execution. "
        "The regression demonstration was performed separately."
    )

except (FileNotFoundError, ValueError):
    st.info(
        "A saved pytest report is not available in this environment. "
        "See the GitHub Actions workflow for automated test results."
    )


st.warning(
    "EDUCATIONAL SIMULATION ONLY — synthetic measurements "
    "and invented thresholds. No real vehicle or Tesla connectivity."
)


# --------------------------------------------------
# REGRESSION TESTING HIGHLIGHT
# --------------------------------------------------

st.subheader("Regression Testing in Practice")

st.write(
    "A small comparison-operator change was deliberately introduced "
    "to demonstrate how automated tests can detect unexpected behavior."
)

left, right = st.columns(2)

with left:
    st.markdown("**Expected behavior**")
    st.code(
        "voltage < LOW_VOLTAGE_LIMIT",
        language="python",
    )
    st.success("11.0 V → OK")

with right:
    st.markdown("**Introduced regression**")
    st.code(
        "voltage <= LOW_VOLTAGE_LIMIT",
        language="python",
    )
    st.error("11.0 V → LOW_VOLTAGE (incorrect)")

st.write(
    "The boundary test detected the incorrect result. "
    "After restoring the original comparison, all 39 tests "
    "passed again."
)

st.link_button(
    "View Source Code & GitHub Actions",
    "https://github.com/elfynme22/vehicle-diagnostics-validation-lab",
)

st.divider()


# --------------------------------------------------
# APPLICATION TABS
# --------------------------------------------------

tab1, tab2, tab3 = st.tabs(
    [
        "Scenario Explorer",
        "Real Test Results",
        "Sensor Dataset",
    ]
)


# --------------------------------------------------
# TAB 1 — DIAGNOSTIC SCENARIOS
# --------------------------------------------------

with tab1:

    st.subheader("Explore Diagnostic Scenarios")

    st.write(
        "Select a simulated vehicle condition and observe how "
        "the diagnostic rules classify the measurements."
    )

    scenario = st.selectbox(
        "Choose a simulated case",
        scenario_names(),
    )

    sample = get_scenario(scenario)
    result = diagnose(sample)

    a, b, c = st.columns(3)

    a.metric(
        "Battery Voltage",
        (
            f'{sample["battery_voltage"]} V'
            if sample["battery_voltage"] is not None
            else "Unavailable"
        ),
    )

    b.metric(
        "Battery Temperature",
        (
            f'{sample["battery_temperature"]} °C'
            if sample["battery_temperature"] is not None
            else "Unavailable"
        ),
    )

    c.metric(
        "Diagnostic Status",
        result["status"],
    )

    alerts = result["alerts"]

    if result["status"] == "OK":
        st.success("Diagnostic result: OK — No alerts detected.")

    elif result["status"] == "WARNING":
        st.warning(
            "Diagnostic warning: " + ", ".join(alerts)
        )

    else:
        st.error(
            "Diagnostic result: " + result["status"]
        )
        st.write("Alerts:", ", ".join(alerts))

    with st.expander("View Exact Input & Output"):
        st.json(
            {
                "input": sample,
                "output": result,
            }
        )


# --------------------------------------------------
# TAB 2 — AUTOMATED TEST RESULTS
# --------------------------------------------------

with tab2:

    st.subheader("Automated Software Test Results")

    st.write(
        "This section displays results from a saved pytest "
        "JUnit XML report. It does not execute tests in the browser."
    )

    try:
        report = read_junit(report_path)

        a, b, c, d = st.columns(4)

        a.metric("Total Tests", report["tests"])
        b.metric("Passed", report["passed"])
        c.metric("Failed", report["failed"])
        d.metric("Skipped", report["skipped"])

        st.caption(
            f'Report source: {report["source"]} | '
            f'Test-case duration: {report["duration_s"]} seconds'
        )

        if report["failed_names"]:
            st.error(
                "Failed tests: "
                + ", ".join(report["failed_names"])
            )

        else:
            st.success(
                "No failures recorded in the saved test report."
            )

    except (FileNotFoundError, ValueError) as error:

        st.info(str(error))

        st.code(
            "python -m pytest -v "
            "--junitxml=reports/junit.xml",
            language="bash",
        )

    st.markdown(
        "[View GitHub Actions test runs]"
        "(https://github.com/elfynme22/"
        "vehicle-diagnostics-validation-lab/actions)"
    )


# --------------------------------------------------
# TAB 3 — SENSOR DATASET
# --------------------------------------------------

with tab3:

    st.subheader("Synthetic Sensor Dataset")

    st.write(
        "The dataset contains simulated voltage and temperature "
        "measurements used to demonstrate diagnostic scenarios."
    )

    df = pd.read_csv(
        ROOT / "data" / "sample_scenarios.csv"
    )

    st.dataframe(
        df,
        use_container_width=True,
    )

    plot_df = df.melt(
        id_vars="scenario",
        value_vars=[
            "battery_voltage",
            "battery_temperature",
        ],
        var_name="sensor",
        value_name="value",
    )

    fig = px.bar(
        plot_df,
        x="scenario",
        y="value",
        color="sensor",
        barmode="group",
        title="Synthetic Sensor Examples",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    st.caption(
        "Voltage and temperature use different measurement units. "
        "Compare their labeled values rather than bar heights."
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Vehicle Diagnostics & Validation Lab | "
    "Independent educational software testing project | "
    "Python · pytest · Streamlit · GitHub Actions"
)
