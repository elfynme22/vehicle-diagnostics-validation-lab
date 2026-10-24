"""Console entry point; use `vehicle-diagnostics --help`."""
import argparse
import json
from .simulator import get_scenario, scenario_names
from .diagnostics import diagnose
from .validation import InvalidSampleError


def main(argv=None):
    parser = argparse.ArgumentParser(description="Synthetic vehicle diagnostics educational demo")
    parser.add_argument("--scenario", choices=scenario_names(), default="normal")
    args = parser.parse_args(argv)
    try:
        sample = get_scenario(args.scenario)
        print(json.dumps({"simulated": True, "input": sample, "diagnostics": diagnose(sample)}, indent=2))
        return 0
    except (ValueError, InvalidSampleError) as exc:
        parser.exit(2, f"Error: {exc}\n")

if __name__ == "__main__":
    raise SystemExit(main())
