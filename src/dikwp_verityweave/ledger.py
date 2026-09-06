from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .utils import canonical_json, digest_json, utc_now

GENESIS = "0" * 64


def append_event(path: str | Path, event_type: str, payload: dict[str, Any]) -> dict[str, Any]:
    ledger_path = Path(path)
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    previous = GENESIS
    sequence = 1
    if ledger_path.exists():
        lines = [line for line in ledger_path.read_text(encoding="utf-8").splitlines() if line.strip()]
        if lines:
            last = json.loads(lines[-1])
            previous = str(last["event_digest"])
            sequence = int(last["sequence"]) + 1
    body = {
        "sequence": sequence,
        "timestamp": utc_now(),
        "event_type": event_type,
        "payload": payload,
        "previous_digest": previous,
    }
    body["event_digest"] = digest_json(body)
    with ledger_path.open("a", encoding="utf-8") as handle:
        handle.write(canonical_json(body) + "\n")
    return body


def verify_ledger(path: str | Path) -> dict[str, Any]:
    ledger_path = Path(path)
    if not ledger_path.exists():
        return {"valid": True, "events": 0, "last_digest": GENESIS}
    previous = GENESIS
    count = 0
    errors: list[str] = []
    for line_number, line in enumerate(ledger_path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        count += 1
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"Line {line_number}: invalid JSON: {exc}")
            continue
        supplied = record.pop("event_digest", None)
        calculated = digest_json(record)
        if supplied != calculated:
            errors.append(f"Line {line_number}: digest mismatch")
        if record.get("previous_digest") != previous:
            errors.append(f"Line {line_number}: previous digest mismatch")
        previous = supplied or calculated
    return {"valid": not errors, "events": count, "last_digest": previous, "errors": errors}
