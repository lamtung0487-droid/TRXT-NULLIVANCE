"""
Central Gate Runner - the only component allowed to issue ladder verdicts.

Design rules (lab gate-integrity, 2026-07-09):
  1. Criteria live in scripts/gates_criteria.json and are pre-declared.
  2. A gate's status is computed from its process exit code AND output
     markers; scripts cannot self-declare ladder-level success.
  3. Every invocation appends a dated block to results/logs/gate_ledger.md
     and writes per-gate logs to results/logs/.
  4. Statuses: PASS / FAIL / NOT_RUN / ERROR / TIMEOUT. The ladder verdict
     is LADDER CLEAR only if every gate is PASS; any FAIL blocks; NOT_RUN
     gates leave the ladder INCOMPLETE (never silently skipped).

Run from repo root:  python scripts/run_gates.py [gate_id ...]
"""
import json
import os
import subprocess
import sys
import datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CRITERIA = os.path.join(ROOT, "scripts", "gates_criteria.json")
LOG_DIR = os.path.join(ROOT, "results", "logs")


def run_gate(gate):
    script = os.path.join(ROOT, gate["script"])
    stamp = datetime.date.today().strftime("%Y%m%d")
    log_path = os.path.join(LOG_DIR, f"{gate['id']}_{stamp}.log")
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    try:
        proc = subprocess.run(
            [sys.executable, script], cwd=ROOT, env=env,
            capture_output=True, text=True, encoding="utf-8",
            errors="replace", timeout=gate.get("timeout_s", 600),
        )
        out = (proc.stdout or "") + "\n" + (proc.stderr or "")
        code = proc.returncode
    except subprocess.TimeoutExpired as e:
        out = (e.stdout or "") + "\nTIMEOUT"
        code = None

    with open(log_path, "w", encoding="utf-8") as f:
        f.write(out)

    if code is None:
        return "TIMEOUT", log_path
    if gate.get("not_run_marker") and gate["not_run_marker"] in out:
        return "NOT_RUN", log_path
    if code == 2:
        return "NOT_RUN", log_path
    has_pass = gate["pass_marker"] in out
    has_fail = gate.get("fail_marker") and gate["fail_marker"] in out
    if has_fail:
        return "FAIL", log_path
    if has_pass and code == 0:
        return "PASS", log_path
    if has_pass and code != 0:
        return "ERROR", log_path  # inconsistent script: pass marker but bad exit
    return "ERROR" if code != 0 else "FAIL", log_path


def main():
    with open(CRITERIA, encoding="utf-8") as f:
        config = json.load(f)
    gates = config["gates"]
    wanted = set(sys.argv[1:])
    if wanted:
        gates = [g for g in gates if g["id"] in wanted]

    os.makedirs(LOG_DIR, exist_ok=True)
    git = subprocess.run(["git", "log", "-1", "--oneline"], cwd=ROOT,
                         capture_output=True, text=True).stdout.strip()
    dirty = subprocess.run(["git", "status", "--short"], cwd=ROOT,
                           capture_output=True, text=True).stdout.strip()

    results = []
    for gate in gates:
        print(f"[{gate['id']}] {gate['name']} ...", flush=True)
        status, log_path = run_gate(gate)
        print(f"    -> {status}   ({os.path.relpath(log_path, ROOT)})")
        results.append((gate, status, log_path))

    statuses = [s for _, s, _ in results]
    if all(s == "PASS" for s in statuses):
        verdict = "LADDER CLEAR"
    elif any(s in ("FAIL", "ERROR", "TIMEOUT") for s in statuses):
        first_bad = next(g["id"] for g, s, _ in results
                         if s in ("FAIL", "ERROR", "TIMEOUT"))
        verdict = f"BLOCKED (first failure: {first_bad})"
    else:
        verdict = "INCOMPLETE (NOT_RUN gates present)"

    stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        "",
        f"## GATE REPORT {stamp} (scripts/run_gates.py)",
        "",
        f"Code state: {git}" + ("  [dirty tree]" if dirty else ""),
        "",
        "| Gate | Status | Criterion | Log |",
        "|---|---|---|---|",
    ]
    for gate, status, log_path in results:
        lines.append(f"| {gate['id']} {gate['name']} | **{status}** | "
                     f"{gate['criterion']} | {os.path.relpath(log_path, ROOT)} |")
    lines += ["", f"### Verdict: **{verdict}**", ""]

    ledger = os.path.join(LOG_DIR, "gate_ledger.md")
    with open(ledger, "a", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print("\n" + "\n".join(lines))
    return 0 if verdict == "LADDER CLEAR" else 1


if __name__ == "__main__":
    sys.exit(main())
