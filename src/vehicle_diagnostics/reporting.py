"""Read actual pytest JUnit XML results; never invent PASS/FAIL metrics."""
from pathlib import Path
import xml.etree.ElementTree as ET


def read_junit(path: str | Path) -> dict:
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"No real pytest report at {path}. Run: python -m pytest --junitxml=reports/junit.xml")
    root = ET.parse(path).getroot()
    suites = [root] if root.tag == "testsuite" else root.findall(".//testsuite")
    # Avoid double-counting nested suite containers: pytest writes a single testsuite.
    tests = root.findall(".//testcase")
    failed = [f"{t.get('classname', '')}::{t.get('name', '')}" for t in tests if t.find('failure') is not None or t.find('error') is not None]
    skipped = sum(t.find('skipped') is not None for t in tests)
    elapsed = sum(float(t.get('time', '0')) for t in tests)
    return {"tests": len(tests), "passed": len(tests)-len(failed)-skipped, "failed": len(failed), "skipped": skipped, "duration_s": round(elapsed, 3), "failed_names": failed, "source": str(path)}
