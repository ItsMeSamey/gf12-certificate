"""Execute the frozen CLI checks in fresh isolated, no-site Python processes."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path, help="new result directory")
    args = parser.parse_args()
    output = args.output.absolute()
    output.mkdir(parents=True, exist_ok=False)
    manifest = json.loads((ROOT / "PACKAGE_MANIFEST.json").read_text())
    for relative, digest in manifest.items():
        if sha(ROOT / relative) != digest:
            raise ValueError("Package source differs from its manifest: " + relative)
    freeze = json.loads((ROOT / "fixtures/FROZEN_CASES.json").read_text())
    if sha(ROOT / "certificate.json") != freeze["certificate_sha256"]:
        raise ValueError("Retained certificate differs from its freeze")
    records = []
    for case in freeze["cases"]:
        fixture = ROOT / case["path"]
        if sha(fixture) != case["sha256"]:
            raise ValueError("Frozen case changed: " + case["name"])
        command = [sys.executable, "-I", "-S", "-B", str(ROOT / "gf12_checker.py"), str(fixture)]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (output / (case["name"] + ".stdout.json")).write_bytes(result.stdout)
        (output / (case["name"] + ".stderr.txt")).write_bytes(result.stderr)
        issues = []
        try:
            report = json.loads(result.stdout)
            expected = case["expected_status"]
            if report.get("status") != expected:
                issues.append("Unexpected status")
            expected_exit = {"verified": 0, "semantic_failure": 1, "invalid_certificate": 2}[expected]
            if result.returncode != expected_exit:
                issues.append("Unexpected exit code")
            if result.stderr:
                issues.append("Unexpected stderr or traceback")
            runtime = report.get("runtime", {})
            if not runtime.get("isolated") or not runtime.get("no_site") or runtime.get("site_loaded"):
                issues.append("Isolated no-site execution was not established")
            if runtime.get("non_stdlib_modules") != []:
                issues.append("Non-stdlib modules loaded")
            if expected != "invalid_certificate":
                if report.get("basis_pairs_checked") != 144 or report.get("terms") != 42:
                    issues.append("Not all basis pairs checked")
                if report.get("input_sha256") != case["sha256"]:
                    issues.append("Input identity metadata differs")
                if expected == "verified":
                    if report.get("mismatching_basis_pairs") != 0 or report.get("first_witness") is not None:
                        issues.append("Positive certificate reports a mismatch")
                else:
                    witness = report.get("first_witness") or {}
                    if any(witness.get(key) != value for key, value in case["expected_witness"].items()):
                        issues.append("Semantic witness differs from frozen coefficient-delta proof")
                    if report.get("mismatching_basis_pairs", 0) <= 0:
                        issues.append("Corrupted tensor did not report mismatches")
            else:
                error = report.get("error", {})
                if not all(type(error.get(key)) is str and error[key] for key in ["code", "location", "message"]):
                    issues.append("Invalid input lacks an intelligible diagnostic")
        except (ValueError, KeyError, TypeError) as error:
            report = {}
            issues.append("Malformed checker output: " + type(error).__name__)
        records.append({"case": case["name"], "command": command, "exit_code": result.returncode,
                        "passed": not issues, "issues": issues, "report": report})
        print(case["name"] + ": " + ("PASS" if not issues else "FAIL"), flush=True)
    by_name = {row["case"]: row for row in records}
    different_positive_hashes = (by_name["retained"]["report"].get("canonical_sha256") !=
                                 by_name["reversed"]["report"].get("canonical_sha256"))
    unchanged = all(sha(ROOT / relative) == digest for relative, digest in manifest.items())
    summary = {"passed": all(row["passed"] for row in records) and different_positive_hashes and unchanged,
               "cases": len(records), "failed_cases": [row["case"] for row in records if not row["passed"]],
               "distinct_positive_certificate_hashes": different_positive_hashes,
               "package_unchanged": unchanged,
               "fixture_freeze_sha256": sha(ROOT / "fixtures/FROZEN_CASES.json"),
               "package_manifest_sha256": sha(ROOT / "PACKAGE_MANIFEST.json")}
    (output / "records.json").write_text(json.dumps(records, indent=2) + "\n")
    (output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, sort_keys=True), flush=True)
    return 0 if summary["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
