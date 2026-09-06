from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .utils import digest_json, utc_now

REQUIRED_CORRECTION_RECEIPTS = {
    "RESTORE_ACCESS_OR_OPPORTUNITY",
    "CORRECT_ORIGINAL_RECORD",
    "NOTIFY_DOWNSTREAM_RECIPIENTS",
    "COMPENSATE_VERIFIED_LOSS",
    "REVISE_OR_RETIRE_RULE_OR_MODEL",
}


def open_appeal(store: str | Path, decision_id: str, appellant_scope: str, grounds: str) -> dict[str, Any]:
    path = Path(store)
    path.parent.mkdir(parents=True, exist_ok=True)
    data = _load(path)
    appeal = {
        "appeal_id": digest_json({"decision_id": decision_id, "grounds": grounds, "opened_at": utc_now()})[:20],
        "decision_id": decision_id,
        "appellant_scope": appellant_scope,
        "grounds": grounds,
        "opened_at": utc_now(),
        "status": "OPEN",
        "correction_receipts": [],
        "consequential_use_blocked": True,
    }
    data[appeal["appeal_id"]] = appeal
    _save(path, data)
    return appeal


def add_correction_receipt(store: str | Path, appeal_id: str, receipt_type: str, evidence: str) -> dict[str, Any]:
    if receipt_type not in REQUIRED_CORRECTION_RECEIPTS:
        raise ValueError(f"Unsupported correction receipt: {receipt_type}")
    path = Path(store)
    data = _load(path)
    if appeal_id not in data:
        raise KeyError(f"Unknown appeal: {appeal_id}")
    appeal = data[appeal_id]
    appeal["correction_receipts"].append(
        {"type": receipt_type, "evidence": evidence, "recorded_at": utc_now()}
    )
    completed = {item["type"] for item in appeal["correction_receipts"]}
    if REQUIRED_CORRECTION_RECEIPTS.issubset(completed):
        appeal["status"] = "CORRECTION_CLOSED"
        appeal["consequential_use_blocked"] = False
        appeal["closed_at"] = utc_now()
    else:
        appeal["status"] = "CORRECTION_IN_PROGRESS"
        appeal["consequential_use_blocked"] = True
    _save(path, data)
    return appeal


def get_appeal(store: str | Path, appeal_id: str) -> dict[str, Any]:
    data = _load(Path(store))
    if appeal_id not in data:
        raise KeyError(f"Unknown appeal: {appeal_id}")
    appeal = dict(data[appeal_id])
    completed = {item["type"] for item in appeal.get("correction_receipts", [])}
    appeal["missing_receipts"] = sorted(REQUIRED_CORRECTION_RECEIPTS - completed)
    return appeal


def _load(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _save(path: Path, value: dict[str, Any]) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
