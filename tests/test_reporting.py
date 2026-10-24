from pathlib import Path
import pytest
from vehicle_diagnostics.reporting import read_junit

def test_missing_report(tmp_path):
    with pytest.raises(FileNotFoundError):
        read_junit(tmp_path / "missing.xml")

def test_real_xml_format(tmp_path):
    path = tmp_path / "report.xml"
    path.write_text('''<testsuites><testsuite tests="3"><testcase name="pass" time="0.2"/><testcase name="fail" time="0.1"><failure>bad</failure></testcase><testcase name="skip"><skipped/></testcase></testsuite></testsuites>''')
    result = read_junit(path)
    assert (result["tests"], result["passed"], result["failed"], result["skipped"]) == (3,1,1,1)
    assert result["failed_names"] == ["::fail"]
