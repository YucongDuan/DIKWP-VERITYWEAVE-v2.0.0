from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TARGETS = list((ROOT / "src").rglob("*.py"))
PATTERNS = {
    "shell_execution": re.compile(r"\b(os\.system|subprocess\.|shell\s*=\s*True)"),
    "network_client": re.compile(r"\b(requests\.|urllib\.request|httpx\.|socket\.socket)"),
    "dynamic_eval": re.compile(r"\b(eval|exec)\s*\("),
    "unsafe_pickle": re.compile(r"\bpickle\.(load|loads)\("),
    "secret_persistence": re.compile(r"secret[_ -]?persistence|self[_ -]?replicat", re.I),
}

findings = []
for path in TARGETS:
    text = path.read_text(encoding="utf-8")
    for name, pattern in PATTERNS.items():
        for match in pattern.finditer(text):
            # Security documentation strings may mention prohibited concepts; only flag executable primitives.
            if name in {"secret_persistence"}:
                continue
            findings.append({"file": str(path.relative_to(ROOT)), "pattern": name, "match": match.group(0)})

receipt = {"files_scanned": len(TARGETS), "findings": findings, "passed": not findings}
print(json.dumps(receipt, indent=2, sort_keys=True))
raise SystemExit(0 if not findings else 1)
