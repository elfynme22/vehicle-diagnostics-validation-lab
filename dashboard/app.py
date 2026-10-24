"""Streamlit app: run `streamlit run dashboard/app.py` after `pip install -e '.[all]'`."""
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

st.set_page_config(page_title="Vehicle Diagnostics Lab", page_icon="🚗", layout="wide")
st.title("🚗 Vehicle Diagnostics & Validation Lab")
st.warning("EDUCATIONAL SIMULATION ONLY — synthetic measurements and invented thresholds. No real vehicle or Tesla connectivity.")

tab1, tab2, tab3 = st.tabs(["Scenario Explorer", "Real Test Results", "Sensor Dataset"])
with tab1:
    scenario = st.selectbox("Choose a simulated case", scenario_names())
    sample = get_scenario(scenario)
    result = diagnose(sample)
    a, b, c = st.columns(3)
    a.metric("Battery voltage (synthetic)", f'{sample["battery_voltage"]} V' if sample["battery_voltage"] is not None else "Unavailable")
    b.metric("Battery temperature (synthetic)", f'{sample["battery_temperature"]} °C' if sample["battery_temperature"] is not None else "Unavailable")
    c.metric("Diagnostic status", result["status"])
    st.write("Alerts:", ", ".join(result["alerts"]))
    with st.expander("View exact input and output"):
        st.json({"input": sample, "output": result})
with tab2:
    path = ROOT / "reports" / "junit.xml"
    try:
        report = read_junit(path)
        a, b, c, d = st.columns(4)
        a.metric("Real executed tests", report["tests"])
        b.metric("PASS", report["passed"])
        c.metric("FAIL", report["failed"])
        d.metric("SKIPPED", report["skipped"])
        st.caption(f'Read from {report["source"]}; duration of test cases: {report["duration_s"]} s')
        if report["failed_names"]:
            st.error("Failed tests: " + ", ".join(report["failed_names"]))
        else:
            st.success("No failures recorded in the latest available local report.")
    except (FileNotFoundError, ValueError) as error:
        st.info(str(error))
        st.code("python -m pytest -v --junitxml=reports/junit.xml", language="bash")
with tab3:
    df = pd.read_csv(ROOT / "data" / "sample_scenarios.csv")
    st.dataframe(df, use_container_width=True)
    plot_df = df.melt(id_vars="scenario", value_vars=["battery_voltage", "battery_temperature"], var_name="sensor", value_name="value")
    fig = px.bar(plot_df, x="scenario", y="value", color="sensor", barmode="group", title="Synthetic sensor examples (different units; not directly comparable)")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("The voltage and temperature bars have different units; use their labeled values, not their relative heights, for interpretation.")
